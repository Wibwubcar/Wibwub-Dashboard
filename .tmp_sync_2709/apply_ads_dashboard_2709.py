import re

FILE = 'WIBWUB_Ads_Dashboard.html'

with open('shopee_obj.txt', encoding='utf-8') as f:
    new_shopee_obj = f.read()

with open(FILE, encoding='utf-8') as f:
    content = f.read()

# --- 1. Replace shopee:{...} object for sep period ---
sep_idx = content.find('sep: {\n')
assert sep_idx > 0
shopee_key_idx = content.find('shopee:{', sep_idx)
assert shopee_key_idx > 0
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

old_shopee_obj = content[shopee_key_idx:end]
assert old_shopee_obj.startswith('shopee:{')
assert old_shopee_obj.endswith('}')
print('OLD shopee obj length:', len(old_shopee_obj))
print('Occurrences of old_shopee_obj in file:', content.count(old_shopee_obj))
assert content.count(old_shopee_obj) == 1, "old_shopee_obj substring is not unique!"

content2 = content.replace(old_shopee_obj, new_shopee_obj, 1)
assert content2 != content
print('shopee object replaced OK')

# --- 2. Replace cover:{...} object (shopeeDay + shopeePull only, keep tiktok fields) ---
old_cover = "cover:{ shopeeDay:26, tiktokDay:26, shopeePull:'26 ก.ย. 19:36 น. (scheduled wibwub-download-shopee-ads): re-synced via direct POST to /api/pas/v1/report/export_job/trigger/ with report_type=new_cpc_homepage__overall (43 campaigns in one export, bypassing the UI \"ภาพรวมข้อมูลโฆษณา\" button which only returns 39 campaigns via report_type=product_homepage_v2__overall) covering 01/09-26/09/2026, 26 ก.ย. เป็นข้อมูลบางส่วน (ระหว่างวัน); totals spend 996,918.27 / revenue 6,096,567.00 / orders 14,690 / ROAS 6.12', tiktokPull:'26 ก.ย. 19:39 น. (scheduled wibwub-download-tiktok-ads, รอบเย็น): GMV Max Overview xlsx \"Campaign overview data 20260901 - 20260926.xlsx\" แถว Total (spend 708,032.39 / 12,466 ออเดอร์ / revenue 2,662,006.04 / ROI 3.76 / CPA 56.80); Business Ads \"WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-26.xlsx\" Total of 97 results (spend 22,452.71 / imp 304,529 / clicks 3,759) — ผลรวม 6 แคมเปญที่มี spend > 0 ตรงกับแถว Total ทุกตัว; gmvLive ยังไม่ได้ดึง (0 = ยังไม่เก็บ) ไม่ถูกบวกซ้ำ; รวม TikTok spend 730,485.10 · ROAS 3.64 · CPA 58.60; 26 ก.ย. ยังไม่จบวัน (ข้อมูลบางส่วน ผ่านมา ~19:39 น.)' }"

assert content2.count(old_cover) == 1, "old_cover substring not found uniquely: %d" % content2.count(old_cover)

new_cover = "cover:{ shopeeDay:27, tiktokDay:26, shopeePull:'27 ก.ย. 08:30 น. (scheduled wibwub-download-shopee-ads): re-synced via direct POST to /api/pas/v1/report/export_job/trigger/ with report_type=new_cpc_homepage__overall (43 campaigns in one export, bypassing the UI \"ภาพรวมข้อมูลโฆษณา\" button which only returns 39 campaigns via report_type=product_homepage_v2__overall) covering 01/09-27/09/2026, 27 ก.ย. เป็นข้อมูลบางส่วน (ระหว่างวัน); totals spend 1,010,364.82 / revenue 6,165,647.00 / orders 14,868 / ROAS 6.10', tiktokPull:'26 ก.ย. 19:39 น. (scheduled wibwub-download-tiktok-ads, รอบเย็น): GMV Max Overview xlsx \"Campaign overview data 20260901 - 20260926.xlsx\" แถว Total (spend 708,032.39 / 12,466 ออเดอร์ / revenue 2,662,006.04 / ROI 3.76 / CPA 56.80); Business Ads \"WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-26.xlsx\" Total of 97 results (spend 22,452.71 / imp 304,529 / clicks 3,759) — ผลรวม 6 แคมเปญที่มี spend > 0 ตรงกับแถว Total ทุกตัว; gmvLive ยังไม่ได้ดึง (0 = ยังไม่เก็บ) ไม่ถูกบวกซ้ำ; รวม TikTok spend 730,485.10 · ROAS 3.64 · CPA 58.60; 26 ก.ย. ยังไม่จบวัน (ข้อมูลบางส่วน ผ่านมา ~19:39 น.) — หมายเหตุ: ตัวเลข TikTok ยังเป็นของ 26 ก.ย. (ยังไม่ pull รอบใหม่ใน run นี้)' }"

content3 = content2.replace(old_cover, new_cover, 1)
assert content3 != content2
print('cover object replaced OK')

# --- 3. Insert audit note comment right after "sep: {\n" ---
anchor = "sep: {\n"
assert content3.count(anchor) == 2  # one for the main sep object, one unrelated (gmvLive nested key)
# Only replace the FIRST occurrence (the top-level sep object opening)
first_idx = content3.find(anchor)
new_note = (
    "sep: {\n"
    "    /* AUDIT NOTE 2026-09-27 (08:30 ICT, scheduled wibwub-download-shopee-ads): shopee totals below "
    "re-synced from official Shopee Ads export ข้อมูล-Shopee-Ads-01_09_2026-27_09_2026-full43.csv (report "
    "generated 27/09/2026 08:30, covers 01-27 ก.ย., 27 ก.ย. ข้อมูลบางส่วน). UI \"ดาวน์ขลดข้อมูลบ > "
    "ภาพรวมข้อมูลโฆษณา\" again produced report_type=product_homepage_v2__overall (39 campaigns only, spend "
    "920,398.05), so re-triggered via POST /api/pas/v1/report/export_job/trigger/ with "
    "report_type=new_cpc_homepage__overall to get ALL 43 campaigns, same workaround as prior rounds. "
    "Recomputed totals directly from the CSV (index 11=imp, 12=clicks, 16=orders, 24=revenue, 26=spend, "
    "27=roas verified against header row): spend 1,010,364.82 / revenue 6,165,647.00 / orders 14,868 / "
    "imp 8,164,256 / clicks 330,948 / ROAS 6.10 (up from 26 ก.ย. cumulative 996,918.27 spend / "
    "6,096,567.00 revenue / 14,690 orders — day 27 ก.ย. so far contributed 13,446.55 spend / 69,080.00 "
    "revenue / 178 orders / 136,518 imp / 4,152 clicks; 27 ก.ย. still an open/partial day at pull time). "
    "Per-campaign top5/worst5/all recomputed directly from this file's 43 rows (same campaign set as prior "
    "rounds, no new campaigns). cover.shopeeDay bumped 26 → 27. */\n"
) + content3[first_idx + len(anchor):]

content4 = content3[:first_idx] + new_note
assert content4 != content3
print('audit note inserted OK')

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content4)

print('DONE. New file length:', len(content4), 'old:', len(content))
