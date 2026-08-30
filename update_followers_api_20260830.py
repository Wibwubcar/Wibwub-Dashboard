#!/usr/bin/env python3
"""
update_followers_api_20260830.py — อัปเดต TikTok Followers ใน Dashboard + Mobile

ที่มาของข้อมูล: TikTok Studio insight API (follower_num_history, days=122, end_days=1)
ดึงผ่าน browser fetch เพราะปุ่ม "ดาวน์โหลดข้อมูล" ในหน้า TikTok Studio
ไม่ trigger การดาวน์โหลดไฟล์จริง (ปัญหาเดิม — ดู update_followers_api.py)

ANCHOR ตรวจสอบแล้ว (สำคัญ):
  index 120 (ค่าสุดท้ายที่ไม่ null) = 28 ส.ค. 2026
  index 121 = 29 ส.ค. (status 2 = ยังไม่ final)
  ยืนยันด้วย 3 จุด: index 0 = 30 เม.ย. = 25590 (= dashboard เม.ย. 25.590),
  index 31 = 31 พ.ค. = 26339, index 61 = 30 มิ.ย. = 27083 — ตรงทั้งหมด
  (ค่า ก.ค. เดิมใน dashboard = 27.834 คลาดเคลื่อน 1 วัน ค่าที่ถูกคือ 27.843 = 31 ก.ค.)
"""
import re
from datetime import datetime, timedelta
from pathlib import Path

MAC_BASE = Path("/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All")
BASE = MAC_BASE if MAC_BASE.exists() else Path(__file__).resolve().parent
DASH = BASE / "WIBWUB_Dashboard.html"
MOBILE = BASE / "WIBWUB_Mobile.html"

MONTH_MAP = {'มกราคม':1,'กุมภาพันธ์':2,'มีนาคม':3,'เมษายน':4,'พฤษภาคม':5,'มิถุนายน':6,
             'กรกฎาคม':7,'สิงหาคม':8,'กันยายน':9,'ตุลาคม':10,'พฤศจิกายน':11,'ธันวาคม':12}
MONTH_REV = {v: k for k, v in MONTH_MAP.items()}
TH_ABBR = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']

# ── raw history จาก insight API (122 วัน, ค่าสุดท้าย null = 29 ส.ค. ยังไม่ final) ──
HIST = [25590,25597,25619,25641,25659,25763,25785,25850,25908,25924,25944,25964,25977,26004,
        26016,26037,26047,26057,26084,26099,26112,26124,26133,26152,26172,26218,26229,26247,
        26277,26304,26320,26339,26390,26403,26424,26445,26448,26519,26533,26550,26560,26570,
        26592,26601,26615,26645,26687,26697,26716,26741,26746,26755,26780,26808,26821,26834,
        26917,26937,26948,26976,26989,27083,27086,27106,27127,27145,27164,27191,27232,27253,
        27272,27296,27323,27346,27386,27404,27438,27454,27484,27506,27539,27559,27583,27625,
        27646,27663,27690,27707,27733,27749,27780,27811,27834,27843,27885,27912,27942,27962,
        27977,27996,28032,28062,28078,28097,28113,28146,28172,28208,28235,28254,28275,28303,
        28317,28329,28346,28375,28412,28443,28479,28500,28539]
LAST_HIST_DATE = datetime(2026, 8, 28)   # = HIST[-1]
TODAY_LIVE = 28594                        # follower_num (real-time) ณ 30 ส.ค. 2026
TODAY = datetime(2026, 8, 30)

rows = []
for i, v in enumerate(HIST):
    d = LAST_HIST_DATE - timedelta(days=(len(HIST) - 1 - i))
    rows.append((d, v))
rows.append((TODAY, TODAY_LIVE))

latest_date, latest_count = rows[-1]
latest_k = round(latest_count / 1000, 3)
print(f"📊 Followers ล่าสุด: {latest_count:,} ({latest_k}K) — {latest_date:%d %b %Y}")

cur_month = TODAY.month
cur_idx = cur_month - 1

# ── 1) WIBWUB_Dashboard.html : soc_follow TikTok array (ค่าปลายเดือน) ──────────
dash = DASH.read_text(encoding='utf-8')

# ค่าปลายเดือนที่ถูกต้องจาก history (แก้ ก.ค. ที่คลาดเคลื่อน 1 วันด้วย)
month_end = {}
for d, v in rows:
    if d.date() != TODAY.date():
        nxt = d + timedelta(days=1)
        if nxt.month != d.month:
            month_end[d.month] = v
month_end[cur_month] = latest_count   # เดือนปัจจุบันใช้ค่า live

def update_tiktok_array(html):
    def replacer(m):
        vals = [v.strip() for v in m.group(1).split(',')]
        while len(vals) <= cur_idx:
            vals.append('null')
        for mth, val in month_end.items():
            idx = mth - 1
            if idx < len(vals):
                vals[idx] = f"{round(val/1000, 3):g}"
        while vals and vals[-1] == 'null':
            vals.pop()
        return "{label:'TikTok',data:[" + ','.join(vals) + "]"
    return re.sub(r"\{label:'TikTok',data:\[([^\]]+)\]", replacer, html)

dash = update_tiktok_array(dash)

# ── 2) FOL_DATA (Follower รายวันเดือนปัจจุบัน) ─────────────────────────────────
abbr = TH_ABBR[cur_idx]
full_name = MONTH_REV[cur_month]
year_be = TODAY.year + 543
label = f"{full_name} {year_be}"

month_rows = [(d, v) for d, v in rows if d.month == cur_month and d.year == TODAY.year]
prev_last = None
for d, v in rows:
    if d.month == cur_month - 1:
        prev_last = v

start = prev_last if prev_last is not None else month_rows[0][1]
end = month_rows[-1][1]
net = end - start
pct = round(net / start * 100, 2) if start else 0
last_day = month_rows[-1][0].day
hist_last_day = LAST_HIST_DATE.day

days_list, vals_list = [], []
for d, v in month_rows:
    if d.day == 1 or d.day == last_day:
        days_list.append(f"{d.day} {abbr}")
    else:
        days_list.append(str(d.day))
    vals_list.append(v)

sub = (f"{label} · เริ่ม {start:,} → ล่าสุด {end:,} · +{net:,} คน (+{pct}%) "
       f"(ข้อมูลรายวัน 1–{hist_last_day} {abbr} + ล่าสุด {last_day} {abbr})")
new_entry = ("{label:'" + label + f"',start:{start},end:{end},net:{net},pct:{pct},sub:'{sub}',\n"
             "         col:'#1A5CDB',\n"
             "         days:[" + ",".join(f'"{d}"' for d in days_list) + "],\n"
             "         vals:[" + ",".join(str(v) for v in vals_list) + "]}")

pattern = re.compile(r"\{label:'" + re.escape(label) + r"',.*?vals:\[[^\]]*\]\}", re.DOTALL)
if pattern.search(dash):
    dash = pattern.sub(lambda m: new_entry, dash, count=1)
    print("✅ FOL_DATA (Follower รายวัน) อัปเดตแล้ว")
else:
    print(f"⚠️  ไม่พบ FOL_DATA entry '{label}' — ข้าม")

DASH.write_text(dash, encoding='utf-8')
print("✅ WIBWUB_Dashboard.html อัปเดตแล้ว")

# ── 3) WIBWUB_Mobile.html : TK Followers KPI ──────────────────────────────────
mobile = MOBILE.read_text(encoding='utf-8')
disp_k = f"{latest_k:.1f}K" if latest_k < 100 else f"{int(latest_k)}K"
mobile, n = re.subn(r'(TK Followers</div><div class="mks-val">)[^<]*(</div>)',
                    rf'\g<1>{disp_k}\g<2>', mobile)
MOBILE.write_text(mobile, encoding='utf-8')
print(f"✅ WIBWUB_Mobile.html อัปเดตแล้ว (TK Followers = {disp_k}, {n} จุด)")
print(f"\n✅ Done — {latest_count:,} followers")
