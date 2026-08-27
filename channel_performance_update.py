#!/usr/bin/env python3
"""
channel_performance_update.py — WIBWUB monthly sales-channel performance
updater (Video / Affiliate / Live / Ads).

WHY THIS SCRIPT EXISTS
-----------------------
The user asked for a monthly, filterable comparison of which sales channel
performs best — shoppable video content, affiliate creators, TikTok Live,
and paid Ads — plus Top 10 rankings (by GMV/revenue) for video, affiliate
creators, and live sessions to use in presentations.

None of this needs NEW data collection: every number already lives inside
three existing WIBWUB dashboards that are kept up to date by other
skills/scripts (update-wibwub, ads dashboard updates). This script just
EXTRACTS the relevant JS consts from those dashboards' <script> blocks,
reshapes them into one monthly channel-performance JSON, and regenerates
WIBWUB_Channel_Performance_Dashboard.html from it — same
extract-and-regenerate pattern as fastmoss_update.py / update_stock.py.

SOURCES (read-only — this script never edits these files)
------------------------------------------------------------
  WIBWUB_Affiliate_Dashboard.html
    - CREATORS         : [{name, gmv, returns, net, comm, orders, comm_rate}]
                          (lifetime/period totals per creator)
    - CREATOR_MONTHS    : {creatorName: [mar,apr,may,jun,jul,aug]}  (GMV per month)
    - VIDEOS            : [{creator, product, vid_id, caption, gmv, units,
                             date, monthly:{mar..aug}}]
                          (shoppable-video GMV attribution — this IS the
                          "video" sales channel, distinct from TikTok
                          organic engagement stats in the TikTok Dashboard,
                          which have no dollar figures at all)

  data Ads/WIBWUB_Ads_Dashboard.html
    - TK_BREAKDOWN      : {jan..aug, all: {
                             gmvLive: {total:{spend,orders,revenue,views,roi,cpa},
                                       sessions:[{name,spend,orders,revenue,roi,views}]},
                             gmvMax:  {total:{...}, campaigns:[...]},
                             bizAds:  {total:{...}, campaigns:[...]}
                           }}
                          gmvLive.sessions[] is the "live" sales channel
                          (per-session revenue). gmvMax + bizAds together
                          are the "ads" channel (paid spend/revenue).

  fastmoss_history.json (plain JSON — no extraction needed, just json.load)
    - {"shops": {wibwub:{...}, munwow:{...}}, "history": [{"date":...,
       "shops": {wibwub:{cumulative:{...}, trend28d:{...},
       top_products:[...]}, munwow:{...}}}]}
      This is the SAME file WIBWUB_FastMoss_Competitor_Dashboard.html and
      fastmoss_update.py already maintain. This script only reads the
      latest snapshot and embeds it as CHANNEL_DATA.fastmoss so the
      Channel Performance Dashboard can show a "vs munwow" section next to
      the internal channel breakdown. It's shop-level only (see caveat
      below) — never merge these numbers with the channel totals above.

EXTRACTION METHOD
-------------------
JS object/array literals in these files use unquoted keys, trailing
comments, and Thai text with punctuation — not valid JSON. Rather than
regex-parse them (fragile against nested braces/semicolons inside strings
or comments), this script:
  1. Locates each `const NAME = <literal>;` by scanning character-by-character
     with a bracket-depth counter that correctly skips over string literals
     ('...' "..." `...`) and comments (// and /* */), so semicolons or
     braces inside those never miscount.
  2. Writes the raw literal to a temp .js file as `module.exports = <literal>;`
  3. Shells out to `node -e "console.log(JSON.stringify(require(...)))"` to
     let a real JS engine parse it (handles unquoted keys, comments, etc.
     for free) and dump valid JSON.
This is the same trick used any time we need to read one of these
dashboards' embedded data programmatically instead of by hand.

OUTPUT
--------
  channel_performance_data.json  — source-of-truth, keyed by month (mar..aug):
    {
      "months": ["mar","apr","may","jun","jul","aug"],
      "month_labels_th": {"mar":"มี.ค.", ...},
      "generated": "YYYY-MM-DD HH:MM",
      "channels": {
        "video":     {"mar": {"gmv":.., "top10":[{creator,product,caption,gmv,units,vid_id}]}, ...},
        "affiliate": {"mar": {"gmv":.., "top10":[{name,gmv,orders,comm}]}, ...},
        "live":      {"mar": {"revenue":.., "spend":.., "orders":.., "roi":.., "top10":[{name,revenue,orders,roi,views}]}, ...},
        "ads":       {"mar": {"spend":.., "revenue":.., "roi":..}, ...}   // gmvMax+bizAds combined
      },
      "fastmoss": { ... latest snapshot of fastmoss_history.json, or null if that file doesn't exist yet ... }
    }

  WIBWUB_Channel_Performance_Dashboard.html — regenerated from the JSON via
  the same marker-delimited embed pattern as the other WIBWUB dashboards
  (const CHANNEL_DATA = {...}; /*CHANNEL_DATA_END*/).

USAGE
-------
  python3 channel_performance_update.py            # re-extract + regenerate + commit
  python3 channel_performance_update.py --no-commit # skip git commit/push
  python3 channel_performance_update.py --regen-only # rebuild HTML from existing JSON only

Re-run any time the Affiliate or Ads dashboards get new monthly data — this
script has no manual snapshot step (unlike fastmoss_update.py), because all
its inputs are already-maintained dashboard files, not a manual scrape.

CAVEAT — "affiliate" vs "video" overlap
------------------------------------------
`video.top10` and `affiliate.top10` are NOT mutually exclusive: every
shoppable video in VIDEOS is posted by a creator who also appears in
CREATORS. "Affiliate" here means the creator's TOTAL GMV across all their
content, while "Video" means GMV attributed to one specific piece of
content. Do not sum video + affiliate GMV together as if they were
independent channels — that would double count. Treat them as two
different lenses (by creator vs. by content) on the same affiliate
program, and Live/Ads as the genuinely separate paid channels.

CAVEAT — FastMoss comparison is shop-level, not channel-level
------------------------------------------------------------
The `fastmoss` section compares WIBWUB's WHOLE SHOP against munwow's whole
shop (orders/sales/creators/lives/videos counts, rankings, top products).
It is NOT a per-channel comparison, because FastMoss does not expose a $
breakdown by video/affiliate/live/ads for any shop — not even ours. Do not
try to reconcile or sum fastmoss numbers against the channels{} totals
above; they answer different questions ("how do we compare to a
competitor overall" vs. "which of our own channels performs best").
"""
import json
import re
import subprocess
import argparse
import tempfile
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent
AFFILIATE_PATH = BASE / "WIBWUB_Affiliate_Dashboard.html"
ADS_PATH = BASE / "data Ads" / "WIBWUB_Ads_Dashboard.html"
FASTMOSS_PATH = BASE / "fastmoss_history.json"
DATA_PATH = BASE / "channel_performance_data.json"
DASHBOARD_PATH = BASE / "WIBWUB_Channel_Performance_Dashboard.html"

DATA_MARKER_START = "const CHANNEL_DATA = "
DATA_MARKER_END = ";\n/*CHANNEL_DATA_END*/"

MONTHS = ["mar", "apr", "may", "jun", "jul", "aug"]
MONTH_LABELS_TH = {
    "jan": "ม.ค.", "feb": "ก.พ.", "mar": "มี.ค.", "apr": "เม.ย.",
    "may": "พ.ค.", "jun": "มิ.ย.", "jul": "ก.ค.", "aug": "ส.ค.",
}


def extract_js_literal(text, const_name):
    """Return the raw JS literal text assigned to `const <const_name> = ...;`
    Scans char-by-char with bracket-depth tracking that skips over string
    literals and comments, so semicolons/braces inside those never confuse
    the scan.
    """
    marker = f"const {const_name} ="
    start_idx = text.index(marker) + len(marker)
    i = start_idx
    n = len(text)
    depth = 0
    started = False
    in_str = None  # one of '"', "'", '`', or None
    in_line_comment = False
    in_block_comment = False
    escape = False

    while i < n:
        c = text[i]
        c2 = text[i:i + 2]

        if in_line_comment:
            if c == "\n":
                in_line_comment = False
        elif in_block_comment:
            if c2 == "*/":
                in_block_comment = False
                i += 1
        elif in_str:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == in_str:
                in_str = None
        else:
            if c2 == "//":
                in_line_comment = True
                i += 1
            elif c2 == "/*":
                in_block_comment = True
                i += 1
            elif c in ("'", '"', "`"):
                in_str = c
            elif c in "{[(":
                depth += 1
                started = True
            elif c in "}])":
                depth -= 1
            elif c == ";" and depth == 0 and started:
                break
        i += 1

    return text[start_idx:i].strip()


def js_literal_to_python(js_literal):
    """Use Node to parse a JS object/array literal (unquoted keys, comments,
    trailing text allowed) and dump it as JSON, then load with Python's
    json module. Raises if node isn't available or the literal is invalid.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".js", delete=False, encoding="utf-8"
    ) as f:
        f.write("module.exports = " + js_literal + ";\n")
        tmp_path = f.name
    try:
        result = subprocess.run(
            ["node", "-e", f"console.log(JSON.stringify(require('{tmp_path}')))"],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def extract_consts(filepath, names):
    text = filepath.read_text(encoding="utf-8")
    out = {}
    for name in names:
        literal = extract_js_literal(text, name)
        out[name] = js_literal_to_python(literal)
    return out


def build_video_channel(videos):
    """VIDEOS is a flat list of {creator,product,vid_id,caption,gmv,units,
    date,monthly:{mar..aug}}. Build per-month gmv total + top10 by that
    month's monthly[] value (falls back to lifetime gmv for months where a
    video has no monthly breakdown at all, which shouldn't normally happen
    since 'monthly' always has all 6 keys, just possibly zero).
    """
    out = {}
    for m in MONTHS:
        rows = []
        total = 0
        for v in videos:
            val = (v.get("monthly") or {}).get(m, 0) or 0
            total += val
            if val > 0:
                rows.append({
                    "creator": v.get("creator"),
                    "product": v.get("product"),
                    "caption": (v.get("caption") or "")[:120],
                    "vid_id": v.get("vid_id"),
                    "gmv": val,
                    "units": v.get("units"),
                })
        rows.sort(key=lambda r: r["gmv"], reverse=True)
        out[m] = {"gmv": round(total), "top10": rows[:10]}
    return out


def build_affiliate_channel(creator_months, creators):
    """CREATOR_MONTHS is {name: [mar,apr,may,jun,jul,aug]}. Build per-month
    total + top10 creators for that month. Pull comm_rate/orders context
    from CREATORS (lifetime) where available, just for display.
    """
    creator_meta = {c["name"]: c for c in creators}
    out = {}
    for idx, m in enumerate(MONTHS):
        rows = []
        total = 0
        for name, monthly in creator_months.items():
            if idx >= len(monthly):
                continue
            val = monthly[idx] or 0
            total += val
            if val > 0:
                meta = creator_meta.get(name, {})
                rows.append({
                    "name": name,
                    "gmv": val,
                    "comm_rate": meta.get("comm_rate"),
                })
        rows.sort(key=lambda r: r["gmv"], reverse=True)
        out[m] = {"gmv": round(total), "top10": rows[:10]}
    return out


def build_live_channel(tk_breakdown):
    out = {}
    for m in MONTHS:
        period = tk_breakdown.get(m, {})
        live = period.get("gmvLive", {})
        total = live.get("total", {}) or {}
        sessions = live.get("sessions", []) or []
        rows = sorted(sessions, key=lambda s: s.get("revenue", 0), reverse=True)[:10]
        out[m] = {
            "revenue": total.get("revenue", 0),
            "spend": total.get("spend", 0),
            "orders": total.get("orders", 0),
            "roi": total.get("roi", 0),
            "views": total.get("views", 0),
            "top10": rows,
        }
    return out


def build_ads_channel(tk_breakdown):
    """Combine gmvMax + bizAds as the paid 'ads' channel per month."""
    out = {}
    for m in MONTHS:
        period = tk_breakdown.get(m, {})
        mx = (period.get("gmvMax", {}) or {}).get("total", {}) or {}
        biz = (period.get("bizAds", {}) or {}).get("total", {}) or {}
        spend = (mx.get("spend", 0) or 0) + (biz.get("spend", 0) or 0)
        revenue = mx.get("revenue", 0) or 0  # bizAds has no revenue/orders (impression-based)
        orders = mx.get("orders", 0) or 0
        roi = round(revenue / spend, 2) if spend else 0
        out[m] = {
            "spend": round(spend, 2),
            "revenue": round(revenue, 2),
            "orders": orders,
            "roi": roi,
            "gmv_max_spend": mx.get("spend", 0),
            "gmv_max_revenue": mx.get("revenue", 0),
            "biz_ads_spend": biz.get("spend", 0),
        }
    return out


def load_fastmoss():
    """Load the FastMoss competitor snapshot (WIBWUB vs munwow). This is
    plain JSON (unlike the dashboards above) since it's written directly by
    fastmoss_update.py — no JS-literal extraction needed, just json.load().

    This is SHOP-LEVEL data only: FastMoss never exposes a $ breakdown by
    sales channel (video/affiliate/live/ads) for any shop, including our
    own. So this section can only compare "whole shop vs whole shop" — it
    complements, but can never replace or be merged numerically with, the
    channel breakdown above (which IS ours, broken down by channel/clip/
    creator). Returns None if the file doesn't exist yet so the dashboard
    can render an empty-state instead of crashing.
    """
    if not FASTMOSS_PATH.exists():
        return None
    with open(FASTMOSS_PATH, encoding="utf-8") as f:
        return json.load(f)


def build_channel_data():
    affiliate_consts = extract_consts(AFFILIATE_PATH, ["CREATORS", "CREATOR_MONTHS", "VIDEOS"])
    ads_consts = extract_consts(ADS_PATH, ["TK_BREAKDOWN"])

    data = {
        "months": MONTHS,
        "month_labels_th": MONTH_LABELS_TH,
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "channels": {
            "video": build_video_channel(affiliate_consts["VIDEOS"]),
            "affiliate": build_affiliate_channel(
                affiliate_consts["CREATOR_MONTHS"], affiliate_consts["CREATORS"]
            ),
            "live": build_live_channel(ads_consts["TK_BREAKDOWN"]),
            "ads": build_ads_channel(ads_consts["TK_BREAKDOWN"]),
        },
        "fastmoss": load_fastmoss(),
    }
    return data


def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def load_data():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def regen_html(data):
    html = DASHBOARD_PATH.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    pattern = re.compile(
        re.escape(DATA_MARKER_START) + r".*?" + re.escape(DATA_MARKER_END),
        re.DOTALL,
    )
    new_block = DATA_MARKER_START + payload + DATA_MARKER_END
    if not pattern.search(html):
        raise RuntimeError(
            "Could not find CHANNEL_DATA marker block in dashboard HTML — "
            "has the template changed? Look for 'const CHANNEL_DATA = ' and "
            "'/*CHANNEL_DATA_END*/' in the <script> section."
        )
    html = pattern.sub(new_block, html, count=1)
    now_label = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = re.sub(
        r'(<span id="gen-ts">).*?(</span>)',
        lambda m: m.group(1) + now_label + m.group(2),
        html,
        count=1,
    )
    DASHBOARD_PATH.write_text(html, encoding="utf-8")


def git_commit():
    subprocess.run(
        ["git", "add", str(DASHBOARD_PATH), str(DATA_PATH)], cwd=BASE, check=False
    )
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    subprocess.run(
        [
            "git", "-c", "user.name=WIBWUB Bot",
            "-c", "user.email=marketingwibwub@gmail.com",
            "commit", "-m", f"auto: update channel performance dashboard {ts}",
        ],
        cwd=BASE,
        check=False,
    )
    subprocess.run(["git", "push", "origin", "main"], cwd=BASE, check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--regen-only", action="store_true",
        help="Skip re-extracting from source dashboards, just rebuild the "
        "HTML from the existing channel_performance_data.json",
    )
    ap.add_argument("--no-commit", action="store_true")
    args = ap.parse_args()

    if args.regen_only:
        data = load_data()
    else:
        data = build_channel_data()
        save_data(data)

    regen_html(data)
    print(f"Regenerated {DASHBOARD_PATH.name} from {'existing JSON' if args.regen_only else 'source dashboards'}")

    if not args.no_commit:
        git_commit()
        print("Committed. Remember: double-click push_now.command on your Mac to actually push.")


if __name__ == "__main__":
    main()
