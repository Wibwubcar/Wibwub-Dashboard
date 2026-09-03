#!/usr/bin/env python3
"""
update_followers.py — อัปเดต TikTok Followers ใน Dashboard + Mobile
อ่านจาก FollowerHistory.csv ล่าสุดใน Downloads หรือ data content/
"""
import os, re, csv, zipfile, glob
from datetime import datetime
from pathlib import Path

MAC_BASE = Path("/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All")
MAC_DL   = Path("/Users/thanasablilutanon/Downloads")

# Portable path resolution: when run inside the sandbox (bash tool), the mac
# paths above don't exist — the same folders are mounted under
# /sessions/<session-name>/mnt/All and /sessions/<session-name>/mnt/Downloads,
# where <session-name> changes every run. Resolve relative to this script's
# own location instead of hardcoding a session name.
if MAC_BASE.exists():
    BASE = MAC_BASE
    DL = MAC_DL
else:
    BASE = Path(__file__).resolve().parent  # .../mnt/All
    DL = BASE.parent / "Downloads"          # .../mnt/Downloads

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

# เดือนของ "ข้อมูลแถวล่าสุด" (ไม่ใช่ datetime.now()) — TikTok export มัก lag
# 1–2 วัน ดังนั้นวันที่ 1 ของเดือนใหม่ ข้อมูลล่าสุดยังเป็นของเดือนก่อน ถ้าใช้
# datetime.now().month จะไปเขียนค่าเดือนก่อนลงช่องเดือนใหม่ที่ยังไม่มีข้อมูลจริง
_latest_d = parse_thai_date(latest_date)
cur_month = _latest_d.month if _latest_d else datetime.now().month
# soc_follow data: [ม.ค., ก.พ., มี.ค., เม.ย., พ.ค., มิ.ย.]
# index = cur_month - 1 (0-indexed)
cur_idx = cur_month - 1

# ── อัปเดต WIBWUB_Dashboard.html ─────────────────────────────────────────
dash = DASH.read_text(encoding='utf-8')

# fallback: CSV ครอบคลุมแค่ 60 วัน จึงไม่มี ม.ค. — ดึงค่า ม.ค. จาก soc_follow
# array ใน Dashboard แทน (index 0) เพื่อไม่ให้ label "จาก ม.ค." ค้างเป็นค่าเก่า
if not delta_str:
    _m = re.search(r"\{label:'TikTok',data:\[\s*([0-9.]+)", dash)
    if _m:
        _jan_k = float(_m.group(1))
        _delta_k = round(latest_k - _jan_k, 1)
        delta_str = f"+{_delta_k}K จาก ม.ค."
        print(f"   Delta ม.ค. (จาก dashboard array): {delta_str}")

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

# อัปเดต TK_FOL (array ยอด follower ปลายเดือน ที่ Mobile ใช้วาดกราฟ + คำนวณ
# folCur/folMoM/folTotal) — เดิม script ไม่เคยแตะ array นี้ ทำให้ Mobile ค้างที่
# ค่าที่กรอกมือครั้งสุดท้าย และไม่ตรงกับ soc_follow ใน Dashboard
TH_ABBR_ALL = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']
_m_fol = re.search(r'const TK_FOL=\[([^\]]*)\];', mobile)
if _m_fol:
    _vals = [v.strip() for v in _m_fol.group(1).split(',') if v.strip()]
    while len(_vals) <= cur_idx:
        _vals.append('0')
    # เดือนที่มีข้อมูลครบใน CSV → เขียนทับด้วยค่าปลายเดือนจริง
    for _mo, _cnt in by_month.items():
        _i = _mo - 1
        if _i < len(_vals):
            _vals[_i] = str(_cnt)
    _vals[cur_idx] = str(latest_count)
    mobile = re.sub(r'const TK_FOL=\[[^\]]*\];',
                    'const TK_FOL=[' + ','.join(_vals) + '];', mobile)
    mobile = re.sub(r"const FOL_M=\[[^\]]*\];",
                    "const FOL_M=[" + ",".join(f"'{m}'" for m in TH_ABBR_ALL[:len(_vals)]) + "];",
                    mobile)
    print(f"✅ TK_FOL อัปเดตแล้ว ({len(_vals)} เดือน, ล่าสุด {latest_count:,})")

MOBILE.write_text(mobile, encoding='utf-8')
print("✅ WIBWUB_Mobile.html อัปเดตแล้ว")

# ── อัปเดต FOL_DATA (Follower รายวัน drill-down ในเดือนปัจจุบัน) ──────────
# ก่อนหน้านี้ script นี้อัปเดตแค่ soc_follow (ยอดรวมรายเดือน) แต่ไม่เคยแตะ
# FOL_DATA (array ที่ใช้วาดกราฟ "Follower รายวัน" แยกตามเดือน) ทำให้เดือน
# ปัจจุบันค้างที่วันสุดท้ายที่เคยกรอกด้วยมือ — แก้โดย regenerate เฉพาะ
# "เดือนปัจจุบัน" จากข้อมูลจริงใน FollowerHistory ทุกครั้งที่รัน
TH_MONTHS_ABBR = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']
TH_MONTHS_FULL_REV = {v: k for k, v in MONTH_MAP.items()}  # 7 -> 'กรกฎาคม'

def build_fol_month_entry(cur_month, rows):
    abbr = TH_MONTHS_ABBR[cur_month - 1]
    full_name = TH_MONTHS_FULL_REV[cur_month]
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
            prev_month_last = count  # เก็บค่าล่าสุดของเดือนก่อนหน้าไว้เป็น start

    if not month_rows:
        return None  # ไม่มีข้อมูลเดือนนี้ใน CSV — ข้าม ไม่แตะไฟล์เดิม

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
    full_name = TH_MONTHS_FULL_REV[cur_month]
    year_be = datetime.now().year + 543
    new_entry = build_fol_month_entry(cur_month, rows)
    if not new_entry:
        print(f"⚠️  FOL_DATA: ไม่พบข้อมูล {full_name} {year_be} ใน FollowerHistory.csv — ข้าม")
        return html, False
    pattern = re.compile(
        r"\{label:'" + re.escape(f"{full_name} {year_be}") + r"',.*?vals:\[[^\]]*\]\}",
        re.DOTALL
    )
    if not pattern.search(html):
        print(f"⚠️  FOL_DATA: ไม่พบ entry เดือน {full_name} {year_be} ในไฟล์ (เดือนใหม่? ต้องเพิ่ม entry เองในโค้ด) — ข้าม")
        return html, False
    html2 = pattern.sub(lambda m: new_entry, html, count=1)
    return html2, True

dash, fol_updated = update_fol_data(dash, cur_month, rows)
if fol_updated:
    print("✅ FOL_DATA (Follower รายวัน) อัปเดตแล้ว")

# เขียนไฟล์ครั้งเดียว หลังจากแก้ทั้ง soc_follow และ FOL_DATA แล้ว
DASH.write_text(dash, encoding='utf-8')
print("✅ WIBWUB_Dashboard.html อัปเดตแล้ว")

# ── ย้ายไฟล์ไป data content/ ─────────────────────────────────────────────
today = datetime.now().strftime('%d.%m.%y')
dest_dir = BASE / "data content" / f"Followers_wibwubcar ({today})"
dest_dir.mkdir(parents=True, exist_ok=True)
# extract zip
with zipfile.ZipFile(zip_path) as z:
    z.extractall(dest_dir)
print(f"📁 Extract ไปยัง: data content/Followers_wibwubcar ({today})/")
print(f"\n✅ Done — {latest_count:,} followers ({latest_date})")
