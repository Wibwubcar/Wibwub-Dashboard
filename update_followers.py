#!/usr/bin/env python3
"""
update_followers.py — อัปเดต TikTok Followers ใน Dashboard + Mobile
อ่านจาก FollowerHistory.csv ล่าสุดใน Downloads หรือ data content/
"""
import os, re, csv, zipfile, glob
from datetime import datetime
from pathlib import Path

BASE    = Path("/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All")
DL      = Path("/Users/thanasablilutanon/Downloads")
DASH    = BASE / "WIBWUB_Dashboard.html"
MOBILE  = BASE / "WIBWUB_Mobile.html"

# ── หา zip ล่าสุด ──────────────────────────────────────────────────────────
def find_latest_zip():
    patterns = [
        DL / "Followers_wibwubcar*.zip",
        BASE / "data content" / "Followers_wibwubcar*.zip",
    ]
    all_zips = []
    for p in patterns:
        all_zips += glob.glob(str(p))
    if not all_zips:
        raise FileNotFoundError("ไม่พบไฟล์ Followers zip")
    return max(all_zips, key=os.path.getmtime)

# ── อ่าน FollowerHistory ──────────────────────────────────────────────────
def read_followers(zip_path):
    rows = []
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if 'History' in name or 'history' in name:
                data = z.read(name).decode('utf-8-sig')
                reader = csv.reader(data.splitlines())
                next(reader)  # skip header
                for row in reader:
                    if len(row) >= 2 and row[1].strip().lstrip('"').rstrip('"').isdigit():
                        date_str = row[0].strip().strip('"')
                        count = int(row[1].strip().strip('"'))
                        rows.append((date_str, count))
    return rows  # [(date_str, count), ...]

# ── month name → month number ─────────────────────────────────────────────
MONTH_MAP = {
    'มกราคม':1,'กุมภาพันธ์':2,'มีนาคม':3,'เมษายน':4,
    'พฤษภาคม':5,'มิถุนายน':6,'กรกฎาคม':7,'สิงหาคม':8,
    'กันยายน':9,'ตุลาคม':10,'พฤศจิกายน':11,'ธันวาคม':12
}
def parse_thai_date(s):
    for th, n in MONTH_MAP.items():
        if th in s:
            day = int(s.split()[0])
            return datetime(datetime.now().year, n, day)
    return None

# ── main ──────────────────────────────────────────────────────────────────
zip_path = find_latest_zip()
print(f"📂 อ่านจาก: {Path(zip_path).name}")

rows = read_followers(zip_path)
if not rows:
    raise ValueError("ไม่พบข้อมูลใน FollowerHistory")

# จัด group by month → ค่าสุดท้ายของแต่ละเดือน
by_month = {}
jan_count = None
for date_str, count in rows:
    d = parse_thai_date(date_str)
    if d:
        if d.month == 1 and jan_count is None:
            jan_count = count
        by_month[d.month] = count  # เก็บค่าล่าสุดของเดือนนั้น

latest_date, latest_count = rows[-1]
latest_k = round(latest_count / 1000, 3)
print(f"📊 Followers ล่าสุด: {latest_count:,} ({latest_k}K) — {latest_date}")

# คำนวณ delta จาก ม.ค.
if jan_count:
    delta = latest_count - jan_count
    delta_k = round(delta / 1000, 1)
    delta_str = f"+{delta_k}K จาก ม.ค."
    print(f"   Delta ม.ค.: {delta_str}")
else:
    delta_str = None

# เดือนปัจจุบัน (index ใน array)
cur_month = datetime.now().month  # 6 = มิ.ย.
# soc_follow data: [ม.ค., ก.พ., มี.ค., เม.ย., พ.ค., มิ.ย.]
# index = cur_month - 1 (0-indexed)
cur_idx = cur_month - 1

# ── อัปเดต WIBWUB_Dashboard.html ─────────────────────────────────────────
dash = DASH.read_text(encoding='utf-8')

# อัปเดต TikTok dataset ใน soc_follow chart (แทนค่าในเดือนปัจจุบัน)
def update_tiktok_array(html, new_val, idx):
    def replacer(m):
        arr_str = m.group(1)
        vals = [v.strip() for v in arr_str.split(',')]
        while len(vals) <= idx:
            vals.append('null')
        vals[idx] = str(new_val)
        # trim trailing nulls
        while vals and vals[-1] == 'null':
            vals.pop()
        return "{label:'TikTok',data:[" + ','.join(vals) + "]"
    return re.sub(r"\{label:'TikTok',data:\[([^\]]+)\]", replacer, html)

dash = update_tiktok_array(dash, latest_k, cur_idx)

DASH.write_text(dash, encoding='utf-8')
print("✅ WIBWUB_Dashboard.html อัปเดตแล้ว")

# ── อัปเดต WIBWUB_Mobile.html ────────────────────────────────────────────
mobile = MOBILE.read_text(encoding='utf-8')

# อัปเดต mks-val (TK Followers)
disp_k = f"{latest_k:.1f}K" if latest_k < 100 else f"{int(latest_k)}K"
mobile = re.sub(
    r'(<div class="mks">[^<]*<div class="mks-ic">📺</div>[^<]*<div class="mks-lbl">TK Followers</div>[^<]*<div class="mks-val">)[^<]*(</div>)',
    rf'\g<1>{disp_k}\g<2>', mobile
)
# อัปเดต mks-sub (delta)
if delta_str:
    mobile = re.sub(
        r'(TK Followers.*?<div class="mks-sub">)[^<]*(</div>)',
        rf'\g<1>{delta_str}\g<2>', mobile, flags=re.DOTALL
    )

MOBILE.write_text(mobile, encoding='utf-8')
print("✅ WIBWUB_Mobile.html อัปเดตแล้ว")

# ── ย้ายไฟล์ไป data content/ ─────────────────────────────────────────────
today = datetime.now().strftime('%d.%m.%y')
dest_dir = BASE / "data content" / f"Followers_wibwubcar ({today})"
dest_dir.mkdir(parents=True, exist_ok=True)
# extract zip
with zipfile.ZipFile(zip_path) as z:
    z.extractall(dest_dir)
print(f"📁 Extract ไปยัง: data content/Followers_wibwubcar ({today})/")
print(f"\n✅ Done — {latest_count:,} followers ({latest_date})")
