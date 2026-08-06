#!/usr/bin/env python3
"""
update_followers_api.py — อัปเดต TikTok Followers ใน Dashboard + Mobile
โดยใช้ข้อมูลจาก TikTok Studio insight API (fetched via browser) แทนการดาวน์โหลด zip,
เนื่องจากปุ่มดาวน์โหลดในหน้า TikTok Studio ไม่ trigger การดาวน์โหลดไฟล์จริงในรอบนี้
(บันทึกไว้เพื่อ debug ในอนาคต — ดูหมายเหตุท้าย task)

ใช้ logic เดียวกับ update_followers.py (by_month / FOL_DATA regeneration)
"""
import re
from datetime import datetime, timedelta
from pathlib import Path

MAC_BASE = Path("/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All")
if MAC_BASE.exists():
    BASE = MAC_BASE
else:
    BASE = Path(__file__).resolve().parent

DASH = BASE / "WIBWUB_Dashboard.html"
MOBILE = BASE / "WIBWUB_Mobile.html"

MONTH_MAP = {
    'มกราคม':1,'กุมภาพันธ์':2,'มีนาคม':3,'เมษายน':4,
    'พฤษภาคม':5,'มิถุนายน':6,'กรกฎาคม':7,'สิงหาคม':8,
    'กันยายน':9,'ตุลาคม':10,'พฤศจิกายน':11,'ธันวาคม':12
}
MONTH_REV = {v: k for k, v in MONTH_MAP.items()}

def parse_thai_date(s):
    for th, n in MONTH_MAP.items():
        if th in s:
            day = int(s.split()[0])
            return datetime(datetime.now().year, n, day)
    return None

# ── raw history fetched from TikTok Studio insight API (follower_num_history, 122d ending today) ──
HIST = [25078,25093,25113,25117,25127,25142,25157,25170,25186,25196,25206,25229,25239,25257,25277,25298,25310,25377,25424,25437,25508,25527,25543,25557,25575,25590,25597,25619,25641,25659,25763,25785,25850,25908,25924,25944,25964,25977,26004,26016,26037,26047,26057,26084,26099,26112,26124,26133,26152,26172,26218,26229,26247,26277,26304,26320,26339,26390,26403,26424,26445,26448,26519,26533,26550,26560,26570,26592,26601,26615,26645,26687,26697,26716,26741,26746,26755,26780,26808,26821,26834,26917,26937,26948,26976,26989,27083,27086,27106,27127,27145,27164,27191,27232,27253,27272,27296,27323,27346,27386,27404,27438,27454,27484,27506,27539,27559,27583,27625,27646,27663,27690,27707,27733,27749,27780,27811,27834,27843,27885,27912]
TODAY_LIVE = 27946  # follower_num (real-time total ตอนดึงข้อมูล)
ANCHOR = datetime(2026, 8, 4)  # index 120 (last of HIST) = Aug 4, 2026

rows = []
for i, v in enumerate(HIST):
    d = ANCHOR - timedelta(days=(len(HIST) - 1 - i))
    thai_month = MONTH_REV[d.month]
    rows.append((f"{d.day} {thai_month}", v))
today = datetime.now()
rows.append((f"{today.day} {MONTH_REV[today.month]}", TODAY_LIVE))

# ── main (เหมือน update_followers.py) ───────────────────────────────────
by_month = {}
jan_count = None
for date_str, count in rows:
    d = parse_thai_date(date_str)
    if d:
        if d.month == 1 and jan_count is None:
            jan_count = count
        by_month[d.month] = count

latest_date, latest_count = rows[-1]
latest_k = round(latest_count / 1000, 3)
print(f"📊 Followers ล่าสุด: {latest_count:,} ({latest_k}K) — {latest_date}")

if jan_count:
    delta = latest_count - jan_count
    delta_k = round(delta / 1000, 1)
    delta_str = f"+{delta_k}K จาก ม.ค."
    print(f"   Delta ม.ค.: {delta_str}")
else:
    delta_str = None
    print("   ⚠️ ไม่มีข้อมูลย้อนหลังถึง ม.ค. ใน 122 วันนี้ — ข้าม delta")

cur_month = datetime.now().month
cur_idx = cur_month - 1

# ── WIBWUB_Dashboard.html : soc_follow TikTok array ─────────────────────
dash = DASH.read_text(encoding='utf-8')

def update_tiktok_array(html, new_val, idx):
    def replacer(m):
        vals = [v.strip() for v in m.group(1).split(',')]
        while len(vals) <= idx:
            vals.append('null')
        vals[idx] = str(new_val)
        while vals and vals[-1] == 'null':
            vals.pop()
        return "{label:'TikTok',data:[" + ','.join(vals) + "]"
    return re.sub(r"\{label:'TikTok',data:\[([^\]]+)\]", replacer, html)

dash = update_tiktok_array(dash, latest_k, cur_idx)

# ── WIBWUB_Mobile.html ───────────────────────────────────────────────────
mobile = MOBILE.read_text(encoding='utf-8')
disp_k = f"{latest_k:.1f}K" if latest_k < 100 else f"{int(latest_k)}K"
mobile = re.sub(
    r'(<div class="mks">[^<]*<div class="mks-ic">📺</div>[^<]*<div class="mks-lbl">TK Followers</div>[^<]*<div class="mks-val">)[^<]*(</div>)',
    rf'\g<1>{disp_k}\g<2>', mobile
)
if delta_str:
    mobile = re.sub(
        r'(TK Followers.*?<div class="mks-sub">)[^<]*(</div>)',
        rf'\g<1>{delta_str}\g<2>', mobile, flags=re.DOTALL
    )
MOBILE.write_text(mobile, encoding='utf-8')
print("✅ WIBWUB_Mobile.html อัปเดตแล้ว")

# ── FOL_DATA (Follower รายวัน เดือนปัจจุบัน) ─────────────────────────────
TH_MONTHS_ABBR = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']

def build_fol_month_entry(cur_month, rows):
    abbr = TH_MONTHS_ABBR[cur_month - 1]
    full_name = MONTH_REV[cur_month]
    year_be = datetime.now().year + 543

    month_rows = []
    prev_month_last = None
    for date_str, count in rows:
        d = parse_thai_date(date_str)
        if not d:
            continue
        if d.month == cur_month:
            month_rows.append((d.day, count))
        elif d.month == cur_month - 1 or (cur_month == 1 and d.month == 12):
            prev_month_last = count

    if not month_rows:
        return None

    month_rows.sort(key=lambda x: x[0])
    start = prev_month_last if prev_month_last is not None else month_rows[0][1]
    end = month_rows[-1][1]
    net = end - start
    pct = round(net / start * 100, 2) if start else 0
    last_day = month_rows[-1][0]

    days_list = []
    vals_list = []
    for day, count in month_rows:
        if day == 1:
            days_list.append(f"1 {abbr}")
        elif day == last_day:
            days_list.append(f"{day} {abbr}")
        else:
            days_list.append(str(day))
        vals_list.append(count)

    label = f"{full_name} {year_be}"
    sub = (f"{label} · เริ่ม {start:,} → ล่าสุด {end:,} · +{net:,} คน (+{pct}%) "
           f"(ข้อมูลรายวัน 1–{last_day} {abbr})")
    days_js = ",".join(f'"{d}"' for d in days_list)
    vals_js = ",".join(str(v) for v in vals_list)

    return (f"{{label:'{label}',start:{start},end:{end},net:{net},pct:{pct},sub:'{sub}',\n"
            f"         col:'#1A5CDB',\n"
            f"         days:[{days_js}],\n"
            f"         vals:[{vals_js}]}}")

def update_fol_data(html, cur_month, rows):
    full_name = MONTH_REV[cur_month]
    year_be = datetime.now().year + 543
    new_entry = build_fol_month_entry(cur_month, rows)
    if not new_entry:
        print(f"⚠️  FOL_DATA: ไม่พบข้อมูล {full_name} {year_be} — ข้าม")
        return html, False
    pattern = re.compile(
        r"\{label:'" + re.escape(f"{full_name} {year_be}") + r"',.*?vals:\[[^\]]*\]\}",
        re.DOTALL
    )
    if not pattern.search(html):
        print(f"⚠️  FOL_DATA: ไม่พบ entry เดือน {full_name} {year_be} ในไฟล์ — ข้าม")
        return html, False
    html2 = pattern.sub(lambda m: new_entry, html, count=1)
    return html2, True

dash, fol_updated = update_fol_data(dash, cur_month, rows)
if fol_updated:
    print("✅ FOL_DATA (Follower รายวัน) อัปเดตแล้ว")

DASH.write_text(dash, encoding='utf-8')
print("✅ WIBWUB_Dashboard.html อัปเดตแล้ว")
print(f"\n✅ Done — {latest_count:,} followers ({latest_date})")
