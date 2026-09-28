import re

FILE = '/sessions/vigilant-epic-cannon/mnt/All/data Ads/WIBWUB_Ads_Dashboard.html'

with open('/sessions/vigilant-epic-cannon/mnt/All/.tmp_sync/shopee_obj.txt', encoding='utf-8') as f:
    new_shopee_obj = f.read()

with open(FILE, encoding='utf-8') as f:
    content = f.read()

# --- 1. Replace shopee:{...} object for sep period ---
sep_idx = content.find('sep:')
shopee_key_idx = content.find('shopee:{', sep_idx)
assert shopee_key_idx > 0
start = shopee_key_idx  # include the 'shopee:' prefix, replace whole thing
brace_start = shopee_key_idx + len('shopee:')
assert content[brace_start] == '{'
depth = 0
i = brace_start
in_str = False
str_char = ''
while i < len(content):
    c = content[i]
    if in_str:
        if c == '\\':
            i += 2
            continue
        if c == str_char:
            in_str = False
    else:
        if c == '"' or c == "'":
            in_str = True
            str_char = c
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                i += 1
                break
    i += 1
end = i

old_shopee_obj = content[start:end]
assert old_shopee_obj.startswith('shopee:{')
assert old_shopee_obj.endswith('}')
print('OLD shopee obj length:', len(old_shopee_obj))
print('Occurrences of old_shopee_obj in file:', content.count(old_shopee_obj))
assert content.count(old_shopee_obj) == 1, "old_shopee_obj substring is not unique!"

content2 = content.replace(old_shopee_obj, new_shopee_obj, 1)
assert content2 != content
print('shopee object replaced OK')

# --- 2. Replace cover:{...} object ---
old_cover = "cover:{ shopeeDay:19, tiktokDay:20, shopeePull:'20 ก.ย. 23:22 น. (รายงาน 01-19 ก.ย., 39 แคมเปญ product/CPC ads เท่านั้น — ยังไม่รวม search/shop ads 4 แคมเปญ; รวม 01-17 cumulative + 18 ก.ย. single-day + 19 ก.ย. single-day)', tiktokPull:'20 ก.ย. 23:55 น. (scheduled wibwub-download-tiktok-ads: GMV Max Total row Sep 1-20 spend 561,712.59 / 9,887 ออเดอร์ / revenue 2,158,341.70 / ROI 3.84 / CPA 56.81; Business Ads รวม 97 แคมเปญ spend 16,563.89 / imp 240,378 / clicks 2,904 / CPM 68.91 / CTR 1.21% — ผลรวม 6 แคมเปญ spend>0 ตรงกับแถว Total of 97 results ทุกตัว. 15 ก.ย. restate เล็กน้อย revenue 111,886.20→111,780.87; 16 ก.ย. ปิดวันแล้วเต็มที่ 32,338.31/637/112,514.65 (จากบางส่วน 4,473.01/98/18,317.96). 20 ก.ย. ยังเป็นวันเปิดอยู่ ตัวเลขจะถูก restate รอบถัดไป)' },"

assert content2.count(old_cover) == 1, "old_cover substring not found uniquely: %d" % content2.count(old_cover)

new_cover = "cover:{ shopeeDay:20, tiktokDay:20, shopeePull:'21 ก.ย. 19:12 น. (รายงาน 01-20 ก.ย., official Shopee Ads export ข้อมูล-Shopee-Ads-01_09_2026-20_09_2026.csv, 39 แคมเปญ product/CPC ads เท่านั้น — ยังไม่รวม search/shop ads 4 แคมเปญ)', tiktokPull:'20 ก.ย. 23:55 น. (scheduled wibwub-download-tiktok-ads: GMV Max Total row Sep 1-20 spend 561,712.59 / 9,887 ออเดอร์ / revenue 2,158,341.70 / ROI 3.84 / CPA 56.81; Business Ads รวม 97 แคมเปญ spend 16,563.89 / imp 240,378 / clicks 2,904 / CPM 68.91 / CTR 1.21% — ผลรวม 6 แคมเปญ spend>0 ตรงกับแถว Total of 97 results ทุกตัว. 15 ก.ย. restate เล็กน้อย revenue 111,886.20→111,780.87; 16 ก.ย. ปิดวันแล้วเต็มที่ 32,338.31/637/112,514.65 (จากบางส่วน 4,473.01/98/18,317.96). 20 ก.ย. ยังเป็นวันเปิดอยู่ ตัวเลขจะถูก restate รอบถัดไป)' },"

content3 = content2.replace(old_cover, new_cover, 1)
assert content3 != content2
print('cover object replaced OK')

# --- 3. Insert a new AUDIT NOTE comment right before the sep: shopee assignment's existing comment block,
#     following the file's established style. Insert right after "sep: {" opening.
anchor = "sep: {\n    /* Sep 1-10"
assert content3.count(anchor) == 1
new_note = (
    "sep: {\n"
    "    /* AUDIT NOTE 2026-09-21 (19:12 ICT, scheduled wibwub-download-shopee-ads): shopee totals below "
    "re-synced from official Shopee Ads export ข้อมูล-Shopee-Ads-01_09_2026-20_09_2026.csv (39 product/CPC "
    "campaigns, report generated 21/09/2026 19:12, covers 01-20 ก.ย. — first file to include 20 ก.ย. data). "
    "Recomputed totals directly from the CSV (index 11=imp, 12=clicks, 16=orders, 24=revenue, 26=spend, "
    "27=roas verified against header row): spend 714,615.75 / revenue 4,508,945.00 / orders 10,773 / "
    "imp 5,907,530 / clicks 144,968 / ROAS 6.31 (up from 01-19 ก.ย. cumulative 681,897.88 spend / "
    "4,282,422.00 revenue / 10,227 orders — day 20 ก.ย. alone contributed 32,717.87 spend / 226,523.00 "
    "revenue / 546 orders / 280,153 imp / 8,296 clicks). Per-campaign top5/worst5/all recomputed directly "
    "from this file's 39 rows (same 39 campaign names as prior rounds, no new campaigns). cover.shopeeDay "
    "bumped 19 → 20. Still product/CPC ads only (39 campaigns) — search/shop ads (4 campaigns) NOT included "
    "this round, same known caveat as prior rounds. SH_ADS in WIBWUB_Dashboard.html / WIBWUB_Mobile.html "
    "updated this round to match the new spend total per user instruction (normally sourced from the "
    "Google Sheet sales sync, not the Ads-report spend figure — flagged as a deviation from the usual rule). */\n"
    "    /* Sep 1-10"
)
content4 = content3.replace(anchor, new_note, 1)
assert content4 != content3
print('audit note inserted OK')

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content4)

print('DONE. New file length:', len(content4), 'old:', len(content))
