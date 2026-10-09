#!/usr/bin/env python3
"""WIBWUB HR attendance — deterministic part of the pipeline.

Claude only scrapes Discord (hr_scrape.js) and talks to Google Sheets.
Everything else happens here, using the SAME JavaScript rules that the
dashboard page runs (extracted from WIBWUB_HR_Attendance.html and executed
with node), so the dashboard and the HR sheet can never disagree.

Commands (run from anywhere; paths are resolved from this file):
  state                         -> JSON: month, last day, `since` day for the next scrape
  merge --in F --out F [--since N] [--full] [--month YYYY-MM]
                                -> verifies overlap, writes RAW_IN/RAW_OUT, node-checks,
                                   exits 10 when nothing changed
  commit                        -> bump sw.js, git commit (auto-push script pushes it)
  sheet --grid-current F --confirm-sheet-id N [--grid-sheet-id N]
                                -> writes work/grid_update.json and work/confirm_*.json
  newmonth --src-id N --new-id N --title "NOV 26" --index N
                                -> work/newmonth_requests.json (duplicate last month's grid)
"""
import argparse, datetime as dt, hashlib, json, os, re, subprocess, sys
from pathlib import Path

from zoneinfo import ZoneInfo
BKK = ZoneInfo("Asia/Bangkok")  # the Mac bridge VM runs in UTC
HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
PAGE = REPO / "WIBWUB_HR_Attendance.html"
SW = REPO / "sw.js"
WORK = HERE / "work"
STATE = HERE / "hr_state.json"
TH_MONTH = ["มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน","กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"]
EN_MON = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
DOWF = ["จันทร์","อังคาร","พุธ","พฤหัส","ศุกร์","เสาร์","อาทิตย์"]  # python weekday()
DAYCOL = {"จันทร์":(1,0.851,0.4),"อังคาร":(0.918,0.82,0.863),"พุธ":(0.714,0.843,0.659),"พฤหัส":(1,0.427,0.004),
          "ศุกร์":(0.29,0.525,0.91),"เสาร์":(0.827,0.443,0.839),"อาทิตย์":(1,0,0)}
LINE_RE = re.compile(r"^\d{1,2}\|\d{1,2}:\d{2}\|[^|]+\|[^|]*\|[\d.,]*$")

def die(msg, code=2):
    print("ERROR:", msg); sys.exit(code)

def read_page():
    t = PAGE.read_text(encoding="utf-8")
    month = re.search(r'const MONTH="(\d{4}-\d{2})";', t).group(1)
    rin = re.search(r"const RAW_IN=`([^`]*)`;", t).group(1).strip()
    rout = re.search(r"const RAW_OUT=`([^`]*)`;", t).group(1).strip()
    split = lambda s: [l for l in s.split("\n") if l.strip()]
    return t, month, split(rin), split(rout)

def read_archive(t):
    m = re.search(r"const ARCHIVE=(\{.*?\});\n", t, re.S)
    return json.loads(m.group(1)) if m else {}

def write_archive(t, arc):
    s = "const ARCHIVE=" + json.dumps(dict(sorted(arc.items())), ensure_ascii=False) + ";\n"
    if re.search(r"const ARCHIVE=\{.*?\};\n", t, re.S):
        return re.sub(r"const ARCHIVE=\{.*?\};\n", lambda _: s, t, count=1, flags=re.S)
    return t.replace("const LOC=", s + "const LOC=", 1)

def day(l): return int(l.split("|", 1)[0])

def load_lines(path):
    lines = [l.strip() for l in Path(path).read_text(encoding="utf-8").split("\n") if l.strip()]
    bad = [l for l in lines if not LINE_RE.match(l)]
    if bad: die(f"{path}: {len(bad)} malformed lines, e.g. {bad[:3]}")
    return lines

def js_source(t):
    js = [s for s in re.findall(r"<script>(.*?)</script>", t, re.S) if "const RAW_IN" in s]
    if not js: die("inline script not found")
    return js[0]

def node_check(t):
    WORK.mkdir(exist_ok=True)
    f = WORK / "_check.js"; f.write_text(js_source(t), encoding="utf-8")
    r = subprocess.run(["node", "--check", str(f)], capture_output=True, text=True)
    if r.returncode: die("node syntax check failed: " + r.stderr[:500])

def compute(t):
    """Run the page's own rules with node; returns dict with DAY rows etc."""
    WORK.mkdir(exist_ok=True)
    logic = js_source(t).split("// ---------- UI ----------")[0]
    logic += """
require('fs').writeFileSync(process.argv[2], JSON.stringify({LAST, LAST_DATE, MONTH,
 EMP: EMP.map(e=>({real:e.real, dept:e.dept, ot:DEPTS[e.dept].ot})),
 UNKNOWN: [...new Set([...INR,...OUTR].filter(r=>!r.emp).map(r=>r.nick))],
 LEAVE_WARN: [...new Set(typeof LEAVE_WARN==="undefined"?[]:LEAVE_WARN)],
 LEAVES: typeof LEAVES==="undefined"?[]:LEAVES.map(r=>({id:r.id,status:r.status,real:r.real,kind:r.kind,dates:r.dates,min:r.span?r.span.min:null})),
 FUZZY: [...new Set([...INR,...OUTR].filter(r=>r.fuzzy).map(r=>r.nick+' -> '+r.fuzzy))],
 GRID: (()=>{const bk={};DAY.forEach(r=>{if(r.emp)bk[r.real+"|"+r.date]=r});const td=process.env.HR_TODAY;
   return Object.fromEntries(MONTHS.map(m=>[m,Object.fromEntries(EMP.map(e=>[e.real,gridRow(e,monthDates(m),td,bk)]))]))})(),
 DAY: DAY.filter(r=>r.emp).map(r=>({date:r.date, real:r.real, dept:r.dept, inTime:r.inTime, outTime:r.outTime,
   lateMin:r.lateMin, otMin:r.otMin, flags:r.flags.map(f=>f[1])}))}));"""
    f = WORK / "_compute.js"; f.write_text(logic, encoding="utf-8")
    out = WORK / "day.json"
    env = dict(os.environ, HR_TODAY=dt.datetime.now(BKK).date().isoformat())
    r = subprocess.run(["node", str(f), str(out)], capture_output=True, text=True, env=env)
    if r.returncode: die("node compute failed: " + r.stderr[:500])
    return json.loads(out.read_text(encoding="utf-8"))

# ---------------------------------------------------------------- state
def cmd_state(a):
    t, month, rin, rout = read_page()
    last = max([day(l) for l in rin + rout] or [0])
    today = dt.datetime.now(BKK).date()
    cur = today.strftime("%Y-%m")
    new_month = cur != month
    since = 1 if new_month else max(1, last - 1)
    y, m = map(int, (cur if not a.month else a.month).split("-"))
    pm = 12 if m == 1 else m - 1
    print(json.dumps({"page_month": month, "current_month": cur, "new_month": new_month,
        "last_day": last, "since": since, "in_lines": len(rin), "out_lines": len(rout),
        "scrape_params": {"cur": TH_MONTH[m-1], "prev": TH_MONTH[pm-1], "since": since},
        "leave_params": {"sinceTs": (today.replace(day=1) - dt.timedelta(days=1)).replace(day=1).isoformat()}}, ensure_ascii=False))

# ---------------------------------------------------------------- merge
def merge_one(old, new, since, full, label):
    if full:
        result = new
        changed_old = [l for l in old if l not in set(new)]
        return result, {"removed_or_changed": changed_old[:10], "removed_count": len(changed_old)}
    new = [l for l in new if day(l) >= since]
    # overlap check: the `since` day must be identical in old and new (proves the scrape lines up)
    o = [l for l in old if day(l) == since]; n = [l for l in new if day(l) == since]
    if o and o != n[:len(o)]:
        die(f"{label}: overlap day {since} differs from saved data (saved {len(o)} lines, scraped {len(n)}). "
            f"Run again with --full.", 3)
    return [l for l in old if day(l) < since] + new, {}

def cmd_merge(a):
    t, month, rin, rout = read_page()
    target = a.month or month
    nin, nout = load_lines(a.in_file), load_lines(a.out_file)
    full = a.full or target != month
    since = 1 if full else a.since
    if not full and not since: die("--since required unless --full")
    if full and target == month and (len(nin) < 0.9 * len(rin) or len(nout) < 0.9 * len(rout)):
        die(f"full scrape looks incomplete (in {len(nin)} vs saved {len(rin)}, out {len(nout)} vs {len(rout)})", 4)
    old_in, old_out = (rin, rout) if target == month else ([], [])
    m_in, info_in = merge_one(old_in, nin, since, full, "check-in")
    m_out, info_out = merge_one(old_out, nout, since, full, "check-out")
    if target == month and m_in == rin and m_out == rout:
        print(json.dumps({"status": "NO_CHANGE", "in": len(rin), "out": len(rout)})); sys.exit(10)
    t2 = t
    if target != month and target > month:   # new month: keep the old month for the dashboard's month selector
        arc = read_archive(t); arc[month] = {"in": "\n".join(rin), "out": "\n".join(rout)}; t2 = write_archive(t, arc)
    elif target != month:
        die(f"--month {target} is older than the page month {month}; use the `archive` command for past months")
    t2 = re.sub(r'const MONTH="\d{4}-\d{2}";', f'const MONTH="{target}";', t2, count=1)
    t2 = re.sub(r"const RAW_IN=`[^`]*`;", lambda _: "const RAW_IN=`" + "\n".join(m_in) + "`;", t2, count=1)
    t2 = re.sub(r"const RAW_OUT=`[^`]*`;", lambda _: "const RAW_OUT=`" + "\n".join(m_out) + "`;", t2, count=1)
    node_check(t2)
    d = compute(t2)
    tmp = PAGE.with_suffix(".tmp.html"); tmp.write_text(t2, encoding="utf-8"); os.replace(tmp, PAGE)
    if hashlib.md5(PAGE.read_bytes()).hexdigest() != hashlib.md5(t2.encode()).hexdigest(): die("page write did not stick")
    print(json.dumps({"status": "UPDATED", "month": target, "full": full,
        "in": [len(rin), len(m_in)], "out": [len(rout), len(m_out)],
        "added_in": len(m_in) - len(old_in), "added_out": len(m_out) - len(old_out),
        "diff_full": {"in": info_in, "out": info_out} if full else None,
        "last": d["LAST"], "unknown_names": d["UNKNOWN"], "typo_matches": d["FUZZY"],
        "forgot_checkout": sum(1 for r in d["DAY"] if r["date"].startswith(target) and "ลืมเช็คเอาท์" in r["flags"]),
        "late_today": [r["real"] for r in d["DAY"] if r["date"] == d["LAST_DATE"] and r["lateMin"] > 0],
        "ot_month_min": sum(r["otMin"] for r in d["DAY"] if r["date"].startswith(target))}, ensure_ascii=False))

# ---------------------------------------------------------------- commit
def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    if check and r.returncode: die("git " + " ".join(args) + ": " + (r.stderr or r.stdout)[:400])
    return r.stdout.strip()

def clear_locks():
    """git leaves *.lock files behind when the bridge does not allow deletes; move them aside so the next git command works."""
    stamp = dt.datetime.now(BKK).strftime("%Y%m%d%H%M%S")
    for lk in (".git/index.lock", ".git/HEAD.lock", ".git/objects/maintenance.lock") + tuple(
            str(p.relative_to(REPO)) for p in (REPO / ".git").glob("next-index-*.lock")):
        f = REPO / lk
        if not f.exists(): continue
        try: f.unlink()
        except PermissionError: f.rename(REPO / ".git" / f"stale-{f.name}-{stamp}")

def cmd_commit(a):
    clear_locks()
    s = SW.read_text(encoding="utf-8")
    m = re.search(r"const CACHE = 'wibwub-v(\d+)';", s)
    if not m: die("sw.js CACHE line not found — do not commit, check sw.js line 2")
    s2 = s.replace(m.group(0), f"const CACHE = 'wibwub-v{int(m.group(1))+1}';", 1)
    SW.write_text(s2, encoding="utf-8")
    if "const CACHE = 'wibwub-v" not in SW.read_text(encoding="utf-8").split("\n")[1]: die("sw.js line 2 broken after bump")
    git("add", "WIBWUB_HR_Attendance.html", "sw.js")
    name = git("log", "-1", "--format=%an"); mail = git("log", "-1", "--format=%ae")
    now = dt.datetime.now(BKK).strftime("%Y-%m-%d %H:%M")
    # commit ONLY our two files (other tasks may have staged their own files)
    git("-c", f"user.name={name}", "-c", f"user.email={mail}", "commit", "-q", "-m", f"auto-update: HR attendance {now} — Discord",
        "--", "WIBWUB_HR_Attendance.html", "sw.js")
    clear_locks()
    head = git("show", "HEAD:WIBWUB_HR_Attendance.html")
    ok = head.strip() == PAGE.read_text(encoding="utf-8").strip()
    print(json.dumps({"commit": git("log", "-1", "--oneline"), "cache": int(m.group(1))+1, "verified": ok,
                      "note": "scripts/wibwub_auto_push.sh pushes within 5 minutes"}, ensure_ascii=False))
    if not ok: die("committed file differs from working file")

# ---------------------------------------------------------------- sheet
def hm(s):
    if not s: return ""
    s = s.replace(" (+1)", ""); h, m = s.split(":"); return f"{int(h)}:{m}"

SYSTEM_VAL = re.compile(r"^(\d{1,2}:\d{2}|หยุด|ลืมสแกน)?$")

def grid_values(d):
    """Grid cells come from the page's own gridRow() (same as the Excel export)."""
    mon = d["MONTH"]; g = d["GRID"].get(mon)
    if g is None: die(f"month {mon} not in the page (MONTH or ARCHIVE)")
    ndays = len(next(iter(g.values()))) // 2
    return g, ndays

def col(n):  # 0-based -> A1 letters
    s = ""; n += 1
    while n: n, r = divmod(n - 1, 26); s = chr(65 + r) + s
    return s

def confirm_payload(d, sid):
    by = {}
    for r in d["DAY"]: by.setdefault(r["real"], []).append(r)
    mon_th = TH_MONTH[int(d["MONTH"][5:7]) - 1]
    L, LF, R, RF = [], [], [], []
    for e in d["EMP"]:
        if not e["ot"]: continue
        rows = sorted([r for r in by.get(e["real"], []) if r["otMin"] > 0], key=lambda r: r["date"])
        if not rows: continue
        L += [[e["real"]], ["ลำดับ","วันที่","เดือน","เวลาเลิกงาน","หน่วย (นาที)"]]; LF += ["name","hdr"]
        s0 = len(L) + 1
        for i, r in enumerate(rows): L.append([i+1, int(r["date"][8:]), mon_th, hm(r["outTime"]), r["otMin"]]); LF.append("data")
        L.append(["รวม","","","",f"=SUM(E{s0}:E{len(L)})"]); LF.append("total"); L.append([]); LF.append("blank")
    for e in d["EMP"]:
        rows = sorted([r for r in by.get(e["real"], []) if r["lateMin"] > 0], key=lambda r: r["date"])
        if not rows: continue
        R += [[e["real"]], ["สายวันที่","วัน","เวลาเข้างาน","เกินเวลา (นาที)"]]; RF += ["name","hdr"]
        s0 = len(R) + 1
        for r in rows:
            x = dt.date.fromisoformat(r["date"]); R.append([x.day, DOWF[x.weekday()], hm(r["inTime"]), r["lateMin"]]); RF.append("data")
        R.append([f'="รวม "&SUM(J{s0}:J{len(R)})&" นาที"']); RF.append("total"); R.append([]); RF.append("blank")
    n = max(len(L), len(R), 1)
    vals = []
    for i in range(n):
        a = (L[i] if i < len(L) else []); a = a + [""] * (5 - len(a))
        b = (R[i] if i < len(R) else []); b = b + [""] * (4 - len(b))
        vals.append(a + [""] + b)
    G = lambda r0, r1, c0, c1: {"sheetId": sid, "startRowIndex": r0, "endRowIndex": r1, "startColumnIndex": c0, "endColumnIndex": c1}
    SOL = {"style": "SOLID"}
    req = [{"unmergeCells": {"range": G(0, 300, 0, 10)}},
           {"updateCells": {"range": G(0, 300, 0, 10), "fields": "userEnteredValue,userEnteredFormat"}},
           {"repeatCell": {"range": G(0, n, 0, 10), "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"}},
                           "fields": "userEnteredFormat.horizontalAlignment,userEnteredFormat.verticalAlignment"}}]
    def blocks(kinds, c0, c1, bg, total_merge_end):
        i = 0
        while i < len(kinds):
            if kinds[i] == "name":
                j = i
                while kinds[j] != "blank": j += 1
                req.append({"mergeCells": {"range": G(i, i+1, c0, c1), "mergeType": "MERGE_ALL"}})
                req.append({"repeatCell": {"range": G(i, i+1, c0, c1), "cell": {"userEnteredFormat": {"backgroundColor": bg, "textFormat": {"bold": True}}},
                                           "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat.bold"}})
                req.append({"repeatCell": {"range": G(i+1, i+2, c0, c1), "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}}, "fields": "userEnteredFormat.textFormat.bold"}})
                req.append({"updateBorders": {"range": G(i, j, c0, c1), "top": SOL, "bottom": SOL, "left": SOL, "right": SOL, "innerHorizontal": SOL, "innerVertical": SOL}})
                req.append({"mergeCells": {"range": G(j-1, j, c0, total_merge_end), "mergeType": "MERGE_ALL"}})
                i = j
            i += 1
    blocks(LF, 0, 5, {"red": 0.2745, "green": 0.7412, "blue": 0.7765}, 4)
    blocks(RF, 6, 10, {"red": 1, "green": 0.949, "blue": 0.8}, 10)
    for c, fmt in ((3, {"type": "TIME", "pattern": "h:mm"}), (8, {"type": "TIME", "pattern": "h:mm"}), (4, {"type": "NUMBER", "pattern": "#,##0"})):
        req.append({"repeatCell": {"range": G(0, n, c, c+1), "cell": {"userEnteredFormat": {"numberFormat": fmt}}, "fields": "userEnteredFormat.numberFormat"}})
    return vals, req

def split_requests(req, limit=12000):
    out, cur, size = [], [], 0
    for r in req:
        s = len(json.dumps(r, ensure_ascii=False, separators=(",", ":")))
        if cur and size + s > limit: out.append(cur); cur, size = [], 0
        cur.append(r); size += s
    if cur: out.append(cur)
    return out

def cmd_sheet(a):
    t, *_ = read_page(); d = compute(t)
    mon = a.month or d["MONTH"]
    d["MONTH"] = mon
    if mon != d["LAST_DATE"][:7]:            # a closed month: everything up to its last day is final
        y, m = map(int, mon.split("-")); d["LAST_DATE"] = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).isoformat()
    d["DAY"] = [r for r in d["DAY"] if r["date"].startswith(mon)]
    WORK.mkdir(exist_ok=True)
    y, m = map(int, d["MONTH"].split("-")); tag = f"{EN_MON[m-1]} {str(y)[2:]}"
    want, ndays = grid_values(d)
    cur = json.loads(Path(a.grid_current).read_text(encoding="utf-8")).get("values", [])
    names = {(r[0].strip() if r else ""): i for i, r in enumerate(cur) if i >= 3}
    missing = [n for n in want if n not in names]
    if missing: die(f"names missing from sheet '{tag}' column A: {missing} — add the rows by hand first", 5)
    first = min(names[n] for n in want); last_row = max(names[n] for n in want)
    st = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    wkey = tag + "_written"
    if wkey not in st:   # first run on this tab: every non-empty cell counts as already written (by HR or us)
        st[wkey] = sorted(f"{col(ci+1)}{ri+1}" for ri in range(first, last_row + 1) if ri < len(cur)
                          for ci in range(2 * ndays) if ci + 1 < len(cur[ri]) and cur[ri][ci + 1].strip())
        STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
    written = set(st[wkey]); new_cells = []
    block, kept, changes = [], [], 0
    for ri in range(first, last_row + 1):
        row = cur[ri] if ri < len(cur) else []
        nm = row[0].strip() if row else ""
        out = []
        for ci in range(2 * ndays):
            have = row[ci + 1].strip() if ci + 1 < len(row) else ""
            new = want.get(nm, [None] * (2 * ndays))[ci] if nm in want else None
            if new is None or new == "" or have == new: out.append(None); continue
            a1 = f"{col(ci+1)}{ri+1}"
            # APPEND-ONLY: never change a cell that has a value, and never refill a cell we (or HR) already filled once
            if have or a1 in written:
                kept.append(f"{nm} {a1} sheet='{have}' system='{new}'"); out.append(None); continue
            out.append(new); changes += 1; new_cells.append(a1)
        block.append(out)
    # trim columns that never change
    used = [ci for ci in range(2 * ndays) if any(r[ci] is not None for r in block)]
    grid = None
    if used:
        c0, c1 = min(used), max(used)
        grid = {"range": f"'{tag}'!{col(c0+1)}{first+1}:{col(c1+1)}{last_row+1}",
                "values": [[(v if v is not None else None) for v in r[c0:c1+1]] for r in block]}
    (WORK / "grid_update.json").write_text(json.dumps(grid, ensure_ascii=False), encoding="utf-8")
    vals, req = confirm_payload(d, a.confirm_sheet_id)
    digest = hashlib.md5(json.dumps(vals, ensure_ascii=False).encode()).hexdigest()
    st = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    confirm_changed = st.get(tag + "_confirm") != digest or a.force_confirm
    confirm_blocked = []
    last_vals = st.get(tag + "_confirm_vals")
    if confirm_changed and last_vals is not None:
        if not a.confirm_current: die("--confirm-current is required (get_values of the confirm tab) to check HR has not edited it", 2)
        cc = json.loads(Path(a.confirm_current).read_text(encoding="utf-8")).get("values", [])
        nz = lambda v: str(v).strip().replace(",", "")
        for ri in range(max(len(cc), len(last_vals))):
            for ci in range(10):
                old = last_vals[ri][ci] if ri < len(last_vals) and ci < len(last_vals[ri]) else ""
                now = cc[ri][ci] if ri < len(cc) and ci < len(cc[ri]) else ""
                if isinstance(old, str) and old.startswith("="): continue
                if nz(old) != nz(now): confirm_blocked.append(f"{col(ci)}{ri+1}: was '{old}' now '{now}'")
    if confirm_blocked: confirm_changed = False   # HR edited our tab: leave it alone and report
    batches = split_requests(req) if confirm_changed else []
    for i, b in enumerate(batches):
        (WORK / f"confirm_req_{i+1}.json").write_text(json.dumps(b, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (WORK / "confirm_values.json").write_text(json.dumps({"range": f"'{tag} confirm ot'!A1:J{len(vals)}", "values": vals}, ensure_ascii=False), encoding="utf-8")
    pend = {wkey: sorted(written | set(new_cells))}
    if confirm_changed: pend.update({tag + "_confirm": digest, tag + "_confirm_vals": vals})
    (WORK / "pending_digest.json").write_text(json.dumps(pend, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"grid_tab": tag, "grid_cells_to_write": changes, "grid_file": "work/grid_update.json" if grid else None,
        "skipped_cells_not_empty": kept[:30], "confirm_changed": confirm_changed, "confirm_blocked_hr_edits": confirm_blocked[:20], "confirm_request_files": [f"work/confirm_req_{i+1}.json" for i in range(len(batches))],
        "confirm_values_file": "work/confirm_values.json" if confirm_changed else None,
        "after_success_run": "python3 hr_update.py sheet-done"}, ensure_ascii=False))

def cmd_sheet_done(a):
    p = WORK / "pending_digest.json"
    if not p.exists(): die("nothing pending")
    st = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    pend = json.loads(p.read_text(encoding="utf-8"))
    if not pend: die("nothing pending")
    st.update(pend); STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
    p.write_text("{}", encoding="utf-8")   # the bridge may not allow deleting files
    print("saved")

def cmd_archive(a):
    """Store a past month (full scrape) for the dashboard's month selector."""
    t, month, *_ = read_page()
    if a.month >= month: die("archive is only for months before the page month " + month)
    nin, nout = load_lines(a.in_file), load_lines(a.out_file)
    if len(nin) < 20 or len(nout) < 20: die(f"too few lines ({len(nin)}/{len(nout)}) — scrape incomplete?", 4)
    arc = read_archive(t); old = arc.get(a.month)
    arc[a.month] = {"in": "\n".join(nin), "out": "\n".join(nout)}
    t2 = write_archive(t, arc)
    if t2 == t: print(json.dumps({"status": "NO_CHANGE"})); sys.exit(10)
    node_check(t2); d = compute(t2)
    tmp = PAGE.with_suffix(".tmp.html"); tmp.write_text(t2, encoding="utf-8"); os.replace(tmp, PAGE)
    rows = [r for r in d["DAY"] if r["date"].startswith(a.month)]
    print(json.dumps({"status": "UPDATED" if old else "ADDED", "month": a.month, "in": len(nin), "out": len(nout),
        "unknown_names": d["UNKNOWN"], "days": len({r["date"] for r in rows}),
        "late_count": sum(1 for r in rows if r["lateMin"] > 0), "ot_min": sum(r["otMin"] for r in rows)}, ensure_ascii=False))

LEAVE_RE = re.compile(r"^\d+-\d+\|\d{4}-\d{2}-\d{2}T\d{2}:\d{2}\|[^|\n]*(\|[^|\n]*){5}$")

def cmd_leave(a):
    """Merge scraped #การลาที่รออนุมัติ lines (msgId|ts|status|name|type|date|reason|considered) into RAW_LEAVE.
    Lines with the same message id are replaced (status edits); older messages outside the scan window are kept."""
    t, month, *_ = read_page()
    m = re.search(r"const RAW_LEAVE=`([^`]*)`;", t)
    if not m: die("RAW_LEAVE not found in the page (run patch_leave first)")
    old = [l for l in m.group(1).split("\n") if l.strip()]
    new = [l.strip() for l in Path(a.in_file).read_text(encoding="utf-8").split("\n") if l.strip()]
    bad = [l for l in new if not LEAVE_RE.match(l)]
    if bad: die(f"{len(bad)} malformed leave lines, e.g. {bad[:2]}")
    by = {l.split("|", 1)[0]: l for l in old}
    changed = [l for l in new if by.get(l.split("|", 1)[0]) != l]
    for l in new: by[l.split("|", 1)[0]] = l
    lines = sorted(by.values(), key=lambda l: l.split("|")[1])
    if not changed: print(json.dumps({"status": "NO_CHANGE", "leave_lines": len(lines)})); sys.exit(10)
    t2 = t[:m.start()] + "const RAW_LEAVE=`" + "\n".join(lines) + "`;" + t[m.end():]
    node_check(t2); d = compute(t2)
    tmp = PAGE.with_suffix(".tmp.html"); tmp.write_text(t2, encoding="utf-8"); os.replace(tmp, PAGE)
    print(json.dumps({"status": "UPDATED", "leave_lines": len(lines), "new_or_changed": len(changed),
        "changed": [{"status": l.split("|")[2], "name": l.split("|")[3], "type": l.split("|")[4], "date": l.split("|")[5]} for l in changed[:30]],
        "warnings": d.get("LEAVE_WARN", [])}, ensure_ascii=False))

def cmd_newmonth(a):
    sid = a.new_id; y, m = map(int, a.month.split("-"))
    ndays = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days
    G = lambda r0, r1, c0, c1: {"sheetId": sid, "startRowIndex": r0, "endRowIndex": r1, "startColumnIndex": c0, "endColumnIndex": c1}
    req = [{"duplicateSheet": {"sourceSheetId": a.src_id, "insertSheetIndex": a.index, "newSheetId": sid, "newSheetName": a.title}},
           {"updateCells": {"range": G(1, 29, 1, 73), "fields": "userEnteredValue,note"}},
           {"updateCells": {"range": G(0, 1, 0, 73), "fields": "userEnteredValue,note"}},
           {"unmergeCells": {"range": G(0, 1, 1, 73)}},
           {"repeatCell": {"range": G(0, 3, 1, 1 + 2 * ndays), "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER", "numberFormat": {"type": "TEXT"}, "textFormat": {"fontFamily": "Arial", "fontSize": 8}}},
                           "fields": "userEnteredFormat.horizontalAlignment,userEnteredFormat.numberFormat,userEnteredFormat.textFormat"}},
           {"repeatCell": {"range": G(0, 1, 1 + 2 * ndays, 73), "cell": {"userEnteredFormat": {}}, "fields": "userEnteredFormat.backgroundColor"}},
           {"repeatCell": {"range": G(3, 29, 1, 73), "cell": {"userEnteredFormat": {"backgroundColor": {"red": 1, "green": 1, "blue": 1}, "horizontalAlignment": "CENTER", "numberFormat": {"type": "TIME", "pattern": "h:mm"}, "textFormat": {"fontFamily": "Arial", "fontSize": 8}}},
                           "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.horizontalAlignment,userEnteredFormat.numberFormat,userEnteredFormat.textFormat"}}]
    hdr = [[""], ["ชื่อ"], [""]]
    for i in range(ndays):
        x = dt.date(y, m, i + 1); c = 1 + 2 * i; r, g, b = DAYCOL[DOWF[x.weekday()]]
        req.append({"mergeCells": {"range": G(0, 1, c, c + 2), "mergeType": "MERGE_ALL"}})
        req.append({"repeatCell": {"range": G(0, 1, c, c + 2), "cell": {"userEnteredFormat": {"backgroundColor": {"red": r, "green": g, "blue": b}}}, "fields": "userEnteredFormat.backgroundColor"}})
        hdr[0] += [DOWF[x.weekday()], ""]; hdr[1] += [f"'{i+1}", f"'{i+1}"]; hdr[2] += ["เข้า", "ออก"]
    WORK.mkdir(exist_ok=True)
    files = []
    for i, b in enumerate(split_requests(req)):
        f = WORK / f"newmonth_req_{i+1}.json"; f.write_text(json.dumps(b, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"); files.append("work/" + f.name)
    (WORK / "newmonth_header.json").write_text(json.dumps({"range": f"'{a.title}'!A1:{col(2*ndays)}3", "values": hdr}, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"request_files_in_order": files, "header_values": "work/newmonth_header.json",
                      "note": "rows 4-29 keep the names from last month (column A is not cleared)"}))

def main():
    p = argparse.ArgumentParser(); s = p.add_subparsers(dest="cmd", required=True)
    s.add_parser("state").add_argument("--month")
    m = s.add_parser("merge"); m.add_argument("--in", dest="in_file", required=True); m.add_argument("--out", dest="out_file", required=True)
    m.add_argument("--since", type=int); m.add_argument("--full", action="store_true"); m.add_argument("--month")
    s.add_parser("commit")
    sh = s.add_parser("sheet"); sh.add_argument("--grid-current", required=True); sh.add_argument("--confirm-sheet-id", type=int, required=True)
    sh.add_argument("--force-confirm", action="store_true"); sh.add_argument("--month"); sh.add_argument("--confirm-current")
    s.add_parser("sheet-done")
    lv = s.add_parser("leave"); lv.add_argument("--in", dest="in_file", required=True)
    ar = s.add_parser("archive"); ar.add_argument("--month", required=True); ar.add_argument("--in", dest="in_file", required=True); ar.add_argument("--out", dest="out_file", required=True)
    n = s.add_parser("newmonth"); n.add_argument("--src-id", type=int, required=True); n.add_argument("--new-id", type=int, required=True)
    n.add_argument("--title", required=True); n.add_argument("--index", type=int, required=True); n.add_argument("--month", required=True)
    a = p.parse_args()
    {"state": cmd_state, "merge": cmd_merge, "commit": cmd_commit, "sheet": cmd_sheet, "sheet-done": cmd_sheet_done, "newmonth": cmd_newmonth, "archive": cmd_archive, "leave": cmd_leave}[a.cmd](a)

if __name__ == "__main__":
    main()
