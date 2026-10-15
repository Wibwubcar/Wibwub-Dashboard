#!/usr/bin/env python3
"""WIBWUB Affiliate Dashboard — คำขอสินค้า tab updater (SAMP_V2).
Reads the Google Sheet "Top 30 Affiliate" > tab "ขอสินค้า" exported as CSV and rewrites, in WIBWUB_Affiliate_Dashboard.html:
  SAMPLE_MONTHS[*].funnel  (req, appr, shipped=appr, posted, clips, waiting)  — every month, from the sheet (perf.* = TikTok Insights, untouched)
  SAMPLE_LAST7D            (rolling 7 days ending today, Bangkok)
  SAMPLE_PRODUCTS / SAMPLE_PRODUCTS_LAST7D  (per product from col "สินค้าที่ Creator ขอ" — never "สินค้าที่ให้")
  SAMPLE_POSTWAIT          (approved requests still waiting for a post, from col "การลงโพสต์")
usage: python3 samp_update.py <csv> [--dry] [--no-commit]     exit 10 = no change
"""
import csv, json, re, sys, subprocess, datetime as dt
from pathlib import Path
from collections import OrderedDict
ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "WIBWUB_Affiliate_Dashboard.html"
BKK = dt.timezone(dt.timedelta(hours=7))
TH = ["ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.","ก.ค.","ส.ค.","ก.ย.","ต.ค.","พ.ย.","ธ.ค."]
POST_FROM = "2026-06"   # คอลัมน์ "การลงโพสต์" เริ่มกรอกจริง มิ.ย. 69

def die(m, code=1): print(json.dumps({"status": "ERROR", "error": m}, ensure_ascii=False)); sys.exit(code)
def pdate(v):
    m = re.match(r"\s*(\d{1,2})/(\d{1,2})/(\d{4})", v or "")
    if not m: return None
    y = int(m[3]); y -= 543 if y > 2400 else 0
    try: return dt.date(y, int(m[2]), int(m[1]))
    except ValueError: return None

def load(path):
    rows = list(csv.reader(open(path, encoding="utf-8-sig")))
    hdr = [h.strip() for h in rows[0]]
    need = {"Date": 0, "Creator": 1, "url": 2, "สินค้าที่ Creator ขอ": 3, "สินค้าที่ให้": 4, "Status": 5, "การลงโพสต์": 7}
    for k, i in need.items():
        if i >= len(hdr) or hdr[i] != k: die(f"sheet columns changed: expected '{k}' in column {i+1}, got {hdr[i] if i < len(hdr) else None}")
    out = []
    for r in rows[1:]:
        r = r + [""] * (12 - len(r)); d = pdate(r[0])
        if not d: continue
        out.append({"d": d, "c": r[1].strip(), "u": r[2].strip(), "ask": r[3].strip(), "give": r[4].strip(), "st": r[5].strip(),
                    "post": r[7].strip(), "ship": pdate(r[8])})
    if len(out) < 500: die(f"only {len(out)} dated rows — export looks incomplete")
    return out

def post_kind(p):
    if re.search(r"โพสต์แล้ว\s*\d*", p) or "ไลฟ์" in p: return "posted"
    if "ยังไม่" in p or "ไม่โพสต์" in p: return "waiting"
    return ""

def clips(p): return sum(int(x) for x in re.findall(r"โพสต์แล้ว\s*(\d+)", p))

def funnel(rs, mkey=None):
    req = len(rs); appr = sum(r["st"] == "Approve" for r in rs)
    has = any(r["post"] for r in rs) or (mkey is not None and mkey >= POST_FROM)
    if not has: return OrderedDict(req=req, appr=appr, shipped=appr, posted=None, clips=None, waiting=None, sale=0)
    return OrderedDict(req=req, appr=appr, shipped=appr, posted=sum(post_kind(r["post"]) == "posted" for r in rs),
                       clips=sum(clips(r["post"]) for r in rs), waiting=sum(post_kind(r["post"]) == "waiting" for r in rs), sale=0)

def products(rs):
    items = OrderedDict(); un = dict(c=0, appr=0, rej=0, other=0)
    def bump(o, st):
        o["c"] += 1; o["appr" if st == "Approve" else "rej" if st == "Reject" else "other"] += 1
    for r in rs:
        names = [x.strip() for x in re.split(r"[,\n]", r["ask"]) if x.strip() and x.strip() != "-"]
        if not names: bump(un, r["st"]); continue
        for n in dict.fromkeys(names): bump(items.setdefault(n, dict(c=0, appr=0, rej=0, other=0)), r["st"])
    lst = sorted(items.items(), key=lambda kv: -kv[1]["c"])
    return {"total": len(rs), "unspecified": un, "items": [dict(n=n, **v) for n, v in lst]}

def js(o): return json.dumps(o, ensure_ascii=False, separators=(",", ":"))
def jsobj(o):   # {total:..} style keys like the hand-written file
    return re.sub(r'"([A-Za-z_][A-Za-z0-9_]*)":', r"\1:", js(o))

def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a: die("usage: samp_update.py <csv>")
    src = a[0]
    if src == "auto":   # newest wibwub_samp_req_*.csv downloaded by Chrome in the last 30 min
        import time, os
        cands = [p for d in (Path.home() / "mnt/Downloads", Path.home() / "Downloads", ROOT / "Data Affiliate/ขอสินค้า") if d.exists()
                 for p in d.glob("wibwub_samp_req_*.csv")]
        cands = [p for p in cands if time.time() - p.stat().st_mtime < 1800]
        if not cands: die("no fresh wibwub_samp_req_*.csv in Downloads (download step failed?)")
        src = str(max(cands, key=lambda p: p.stat().st_mtime))
    R = load(src); today = dt.datetime.now(BKK).date()
    t = PAGE.read_text(encoding="utf-8"); t0 = t
    months = OrderedDict()
    for r in sorted(R, key=lambda r: r["d"]): months.setdefault(r["d"].strftime("%Y-%m"), []).append(r)
    # ---- SAMPLE_MONTHS funnel per month
    m = re.search(r"const SAMPLE_MONTHS = \[\n(.*?)\n\];", t, re.S)
    if not m: die("SAMPLE_MONTHS not found")
    lines = m.group(1).split("\n"); have = {}
    for i, l in enumerate(lines):
        k = re.search(r"\{key:'(\d{4}-\d{2})'", l)
        if k: have[k.group(1)] = i
    changed_past = []
    for mk, rs in months.items():
        f = funnel(rs, mk); fj = "funnel:" + jsobj(f)
        last = (dt.date(int(mk[:4]) + (mk[5:] == "12"), int(mk[5:]) % 12 + 1, 1) - dt.timedelta(days=1))
        cur = mk == today.strftime("%Y-%m")
        if mk in have:
            i = have[mk]; old = re.search(r"funnel:\{[^}]*\}", lines[i]).group(0)
            if old != fj:
                o = re.search(r"req:(\d+)", old); 
                if not cur and o and int(o.group(1)) != f["req"]: changed_past.append(f"{mk}: คำขอ {o.group(1)} → {f['req']}")
                lines[i] = lines[i].replace(old, fj)
            if cur:
                d2 = min(today, last).day
                lines[i] = re.sub(r"label:'[^']*'", f"label:'{TH[int(mk[5:])-1]} {int(mk[:4])+543} (1-{d2})'", lines[i])
                lines[i] = re.sub(r"range:'[^']*'", f"range:'01/{mk[5:]}/{mk[:4]} - {d2:02d}/{mk[5:]}/{mk[:4]}'", lines[i])
                lines[i] = re.sub(r"partial:(true|false)", "partial:true", lines[i])
            elif "partial:true" in lines[i] and today > last:   # month just closed
                lines[i] = re.sub(r"label:'[^']*'", f"label:'{TH[int(mk[5:])-1]} {int(mk[:4])+543}'", lines[i]).replace("partial:true", "partial:false")
                lines[i] = re.sub(r"range:'[^']*'", f"range:'01/{mk[5:]}/{mk[:4]} - {last.day:02d}/{mk[5:]}/{mk[:4]}'", lines[i])
        else:
            d2 = min(today, last).day
            lines.append(f"  {{key:'{mk}', label:'{TH[int(mk[5:])-1]} {int(mk[:4])+543} (1-{d2})', short:'{TH[int(mk[5:])-1]}', partial:true, "
                         f"range:'01/{mk[5:]}/{mk[:4]} - {d2:02d}/{mk[5:]}/{mk[:4]}', {fj}, perf:{{shipped:0,gmv:0,cogs:0,content:0,roi:0}}, noPerfData:true}},")
    t = t[:m.start(1)] + "\n".join(lines) + t[m.end(1):]
    # ---- rolling 7 days (today - 6 .. today)
    w0 = today - dt.timedelta(days=6); r7 = [r for r in R if w0 <= r["d"] <= today]
    win = f"{w0:%d/%m/%Y} - {today:%d/%m/%Y}"
    l7 = ("const SAMPLE_LAST7D = {\n  key:'last7d', label:'7 วันล่าสุด', short:'7 วันล่าสุด', partial:true, rolling:true,\n"
          f"  range:'{win}',\n  funnel:{jsobj(funnel(r7, today.strftime('%Y-%m')))},\n  perf:{{shipped:0, gmv:0, cogs:0, content:0, roi:0}}, noPerfData:true\n}};")
    t, n = re.subn(r"const SAMPLE_LAST7D = \{.*?\n\};", lambda _: l7, t, count=1, flags=re.S)
    if not n: die("SAMPLE_LAST7D not found")
    # ---- products
    keys = sorted(set(months) | set(have))
    sp = "const SAMPLE_PRODUCTS = {\n" + ",\n".join(f"  '{mk}': {jsobj(products(months.get(mk, [])))}" for mk in keys) + "\n};"
    t, n = re.subn(r"const SAMPLE_PRODUCTS = \{\n.*?\n\};", lambda _: sp, t, count=1, flags=re.S)
    if not n: die("SAMPLE_PRODUCTS not found")
    p7 = products(r7); p7["window"] = win
    t, n = re.subn(r"const SAMPLE_PRODUCTS_LAST7D = \{.*?\};\n", lambda _: "const SAMPLE_PRODUCTS_LAST7D = " + jsobj(p7) + ";\n", t, count=1, flags=re.S)
    if not n: die("SAMPLE_PRODUCTS_LAST7D not found")
    # ---- approved requests waiting for a post (since posting was tracked)
    W = [dict(d=r["d"].isoformat(), c=r["c"], u=r["u"], p=r["give"] or r["ask"], s=r["ship"].isoformat() if r["ship"] else "",
              h=r["post"] or "ยังไม่กรอก") for r in R
         if r["st"] == "Approve" and r["d"].strftime("%Y-%m") >= POST_FROM and post_kind(r["post"]) != "posted"]
    W.sort(key=lambda w: (w["s"] or w["d"]))
    pw = "const SAMPLE_POSTWAIT = [\n" + ",\n".join(jsobj(w) for w in W) + "\n];"
    if "const SAMPLE_POSTWAIT = [" in t: t = re.sub(r"const SAMPLE_POSTWAIT = \[\n.*?\n?\];", lambda _: pw, t, count=1, flags=re.S)
    else: die("SAMPLE_POSTWAIT not found (run the UI patch first)")
    t = re.sub(r"const SAMPLE_DATA_ASOF = '[^']*';", f"const SAMPLE_DATA_ASOF = '{max(r['d'] for r in R):%d/%m/%Y}';", t)
    if t == t0: print(json.dumps({"status": "NO_CHANGE"})); sys.exit(10)
    cur = funnel(months.get(today.strftime("%Y-%m"), []), today.strftime("%Y-%m"))
    summary = {"status": "UPDATED", "source": Path(src).name, "rows": len(R), "latest_row": max(r["d"] for r in R).isoformat(), "this_month": cur,
               "last7d": funnel(r7, "9999"), "waiting_post": len(W), "past_month_req_changed": changed_past,
               "top_products_this_month": [(i["n"], i["c"]) for i in products(months.get(today.strftime("%Y-%m"), []))["items"][:5]]}
    if "--dry" in sys.argv: print(json.dumps(summary, ensure_ascii=False, default=str)); return
    # syntax check before writing
    import tempfile; tmpjs = Path(tempfile.gettempdir()) / "wibwub_aff_check.js"
    tmpjs.write_text("\n;\n".join(x for x in re.findall(r"<script>(.*?)</script>", t, re.S)), encoding="utf-8")
    r = subprocess.run(["node", "--check", str(tmpjs)], capture_output=True, text=True)
    if r.returncode: die("node --check failed: " + r.stderr[:400])
    PAGE.with_suffix(".tmp.html").write_text(t, encoding="utf-8"); PAGE.with_suffix(".tmp.html").replace(PAGE)
    if "--no-commit" not in sys.argv:
        sw = ROOT / "sw.js"; s = sw.read_text(); v = int(re.search(r"wibwub-v(\d+)", s).group(1))
        sw.write_text(s.replace(f"wibwub-v{v}", f"wibwub-v{v+1}", 1))
        for lk in ("index.lock", "HEAD.lock"):
            p = ROOT / ".git" / lk
            if p.exists(): p.rename(ROOT / ".git" / f"stale-{lk}-{int(dt.datetime.now().timestamp())}")
        g = lambda *x: subprocess.run(["git", "-C", str(ROOT), *x], capture_output=True, text=True)
        g("add", "WIBWUB_Affiliate_Dashboard.html", "sw.js")
        c = g("-c", "user.name=WIBWUB Bot", "-c", "user.email=marketingwibwub@gmail.com", "commit", "-m",
              f"auto-update: คำขอสินค้า {today} — {cur['req']} คำขอ / {cur['appr']} อนุมัติ / {cur['posted']} โพสต์แล้ว")
        summary["commit"] = g("log", "-1", "--format=%h").stdout.strip() if c.returncode == 0 else ("FAILED: " + c.stderr[-300:])
    print(json.dumps(summary, ensure_ascii=False, default=str))

if __name__ == "__main__": main()
