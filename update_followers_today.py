#!/usr/bin/env python3
"""
update_followers_today.py — อัปเดต TikTok Followers ใน Dashboard + Mobile
ใช้ข้อมูลจาก TikTok API (fallback แทนการ download zip) เนื่องจากไฟล์ที่ดาวน์โหลด
ผ่าน Chrome extension ไม่ถูก sync เข้ามาใน sandbox mount แบบ realtime
"""
import re
from pathlib import Path
from datetime import datetime

BASE = Path("/sessions/loving-great-turing/mnt/All")
DASH = BASE / "WIBWUB_Dashboard.html"
MOBILE = BASE / "WIBWUB_Mobile.html"

# ── ข้อมูลจริงจาก TikTok Studio API (follower_num_history, 122 days, end_days=1) ──
latest_date = "2026-07-30"
latest_count = 27780
cur_month = 7  # กรกฎาคม
cur_idx = cur_month - 1  # 0-indexed => 6

latest_k = round(latest_count / 1000, 3)
print(f"📊 Followers ล่าสุด: {latest_count:,} ({latest_k}K) — {latest_date}")

# ── อัปเดต WIBWUB_Dashboard.html — TikTok dataset ในกราฟ soc_follow ──
dash = DASH.read_text(encoding='utf-8')

def update_tiktok_array(html, new_val, idx):
    def replacer(m):
        arr_str = m.group(1)
        vals = [v.strip() for v in arr_str.split(',')]
        while len(vals) <= idx:
            vals.append('null')
        vals[idx] = str(new_val)
        while vals and vals[-1] == 'null':
            vals.pop()
        return "{label:'TikTok',data:[" + ','.join(vals) + "]"
    return re.sub(r"\{label:'TikTok',data:\[([^\]]+)\]", replacer, html)

before = re.search(r"\{label:'TikTok',data:\[([^\]]+)\]", dash).group(1)
dash = update_tiktok_array(dash, latest_k, cur_idx)
after = re.search(r"\{label:'TikTok',data:\[([^\]]+)\]", dash).group(1)
print(f"   Dashboard TikTok array: [{before}] -> [{after}]")

DASH.write_text(dash, encoding='utf-8')
print("✅ WIBWUB_Dashboard.html อัปเดตแล้ว")

# ── อัปเดต WIBWUB_Mobile.html ──
mobile = MOBILE.read_text(encoding='utf-8')

# TK_FOL array (monthly snapshot array used by follower detail widget)
m = re.search(r"const TK_FOL=\[([^\]]+)\];", mobile)
if m:
    vals = [v.strip() for v in m.group(1).split(',')]
    while len(vals) <= cur_idx:
        vals.append('0')
    old_val = vals[cur_idx]
    vals[cur_idx] = str(latest_count)
    new_arr = ','.join(vals)
    mobile = mobile.replace(f"const TK_FOL=[{m.group(1)}];", f"const TK_FOL=[{new_arr}];")
    print(f"   Mobile TK_FOL[{cur_idx}]: {old_val} -> {latest_count}")

# mks-val (การ์ด TK Followers) — แสดงเป็น K ทศนิยม 1 ตำแหน่ง
disp_k = f"{latest_k:.1f}K"
mobile = re.sub(
    r'(<div class="mks-lbl">TK Followers</div><div class="mks-val">)[^<]*(</div>)',
    rf'\g<1>{disp_k}\g<2>', mobile
)
print(f"   Mobile mks-val (TK Followers): -> {disp_k}")

MOBILE.write_text(mobile, encoding='utf-8')
print("✅ WIBWUB_Mobile.html อัปเดตแล้ว")

print(f"\n✅ Done — {latest_count:,} followers ({latest_date})")
