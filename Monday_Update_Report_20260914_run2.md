# ✅ WIBWUB Weekly Update (wibwub-monday-update) — 14 ก.ย. 2569 (จันทร์) — รอบที่ 2 (สำเร็จบางส่วน)

## สถานะ: STEP 1–3 และ 5 สำเร็จ / STEP 2 (Affiliate) และ STEP 4 หยุด — session TikTok หมดอายุ

รอบแรกของวันนี้ (02:14 น.) ถูก BLOCK เพราะ Chrome extension ไม่ connected (ดู `Monday_Update_Report_20260914_BLOCKED.md`)
รอบนี้ Chrome connected แล้ว จึงดำเนินการต่อได้ถึง STEP 5 ยกเว้นส่วน TikTok Affiliate

## สิ่งที่ทำสำเร็จ

- ✅ **Protection check**: `M5` array ใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` มี 9 เดือน (ม.ค.–ก.ย.)
  ตรงกับเดือนปัจจุบันอยู่แล้ว — ไม่ต้องแก้ไข
- ✅ **STEP 1 — Shipnity**: เปิด Shipnity ผ่าน Chrome, ตั้งช่วงวันที่ถึงวันปัจจุบัน, export product-level xlsx สำเร็จ
  → บันทึกเป็น `Data Shipnity/Data_14-09-2026.xlsx` (17.3MB, auto-moved จาก Downloads โดย LaunchAgent)
- ✅ **STEP 3 — Top Products**: ประมวลผลไฟล์ Shipnity ทั้งหมด (~108 ไฟล์ ม.ค.–14 ก.ย.) พร้อม dedup logic
  (composite key order/product/qty) แล้วอัปเดต:
  - `WIBWUB_Mobile.html` → `ALL_PRODUCTS` (Top 15 สินค้า, cumulative ม.ค.–14 ก.ย.)
  - `WIBWUB_Dashboard.html` → ตาราง Top Products + KPI (ยอดขายรวม ฿71.28M, สินค้าขายดีสุด Sugar 500ml ฿6.30M/20,369 ชิ้น, จำนวนชิ้นรวม 283K)
  - หมายเหตุ: กราฟ per-channel breakdown (`pr_channel`) ไม่ได้แตะ เพราะไม่มีข้อมูลแยกแพลตฟอร์มใหม่ในรอบนี้ (out of scope)
- ✅ **STEP 5 — Version bump & commit**: bump `sw.js` เป็น `wibwub-v1108`, commit ไฟล์ที่แก้ 4 ไฟล์
  (`WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, `WIBWUB_Affiliate_Dashboard.html`, `sw.js`)
  → commit `629df1f`: "auto-update: Monday 2026-09-14 — Shipnity Top Products refresh (Affiliate TikTok session expired, not updated)"
  → สร้าง/overwrite `push_now.command` ให้กดรัน push เอง (sandbox push ติด proxy HTTP 403)

  > หมายเหตุ: `WIBWUB_Affiliate_Dashboard.html` มีการแก้ไข `VIDEOS` array (246 บรรทัด) ที่ค้างอยู่จาก
  > automation รอบอื่นก่อนหน้านี้ในวันนี้ — รวมเข้า commit นี้ด้วยตามงานเดิม ไม่ได้ทิ้งงาน

## สิ่งที่ถูกบล็อก

- ❌ **STEP 2 — TikTok Affiliate Transaction Analysis**: เปิด
  `https://affiliate.tiktok.com/insights/transaction-analysis?shop_region=TH&shop_id=7494549095358892612`
  แล้วถูก redirect ไปหน้า marketing สาธารณะของ seller.tiktok.com (ปุ่ม Log in/Join now) แทนที่จะเป็นหน้า dashboard
  → **session expired** ลองใหม่อีกครั้งผลเหมือนเดิม → ตามกฎ error handling ("session หมดอายุ → log และหยุด")
  จึงไม่ export/ดาวน์โหลดไฟล์ Affiliate ในรอบนี้
- ❌ **STEP 4 — Affiliate arrays**: `AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR` (Affiliate Dashboard) และ
  `AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM` (Mobile) **ไม่ได้อัปเดต** เพราะไม่มีไฟล์ Transaction Analysis ใหม่จาก STEP 2

## ที่ต้องทำ (ต้องมีคนที่เครื่อง Mac)

1. **Re-login TikTok Affiliate Center** บน Chrome เครื่อง Mac (deviceId `b75a6bb0-5b78-4e44-92a8-75224f1ce4ee`)
   — session หมดอายุ ทำให้ดึงข้อมูล GMV/commission ล่าสุดไม่ได้ (ปัญหาเกิดซ้ำจากวันที่ 11, 13 ก.ย. ด้วย)
2. **รัน `push_now.command`** (ดับเบิลคลิกในโฟลเดอร์ `claude/All`) เพื่อ push commit `629df1f` ขึ้น `origin/main`
   (sandbox push ไม่ได้เพราะ proxy คืน HTTP 403)
3. หลัง re-login แล้ว รัน schedule นี้ใหม่อีกครั้งเพื่อดึงข้อมูล TikTok Affiliate ที่ยังค้าง (9–14 ก.ย.)
