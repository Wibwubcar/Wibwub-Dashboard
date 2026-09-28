# TikTok Ads Download — จันทร์ 21 ก.ย. 2569

📅 ช่วงข้อมูล: 01–21 ก.ย. 2569

## ผลการดาวน์โหลด

✅ **GMV Max**: `Campaign overview data 20260901 - 20260921.xlsx` — บันทึกที่ `data Ads/TikTok/GMV Max/`

✅ **Business Ads**: `WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-21.xlsx` — บันทึกที่ `data Ads/TikTok/Business Ads/`

## หมายเหตุปัญหาที่พบระหว่างทำงาน

1. **Date-range formula bug**: การคำนวณ start_ms/end_ms ของ GMV Max ตามสูตรใน skill ให้ผลลัพธ์ช่วง 31 ส.ค.–22 ก.ย. (เกินมา 1 วันหัวและท้าย) เพราะ timezone offset ในสูตรผิด ไฟล์ export จึงมีแถว 31 ส.ค. และ 22 ก.ย. ปนอยู่ ผมตัดสองแถวนี้ออกและ sum เฉพาะแถว 1–21 ก.ย. เอง แทนการใช้แถว "Total" ตรง ๆ ตามปกติ (ถ้าใช้ตรง ๆ จะบวกยอด 31 ส.ค. ซ้ำเข้าไป 20,631.06 บาท / 398 ออเดอร์)
2. **ปุ่ม Download/Export ไม่ตอบสนองต่อ pixel-click ปกติ**: ทั้งปุ่ม GMV Max download และเมนู "More > Export data" ของ Business Ads ต้องคลิกผ่าน DOM element (dispatchEvent) แทน เนื่องจาก CSS px กับ screenshot px มีอัตราส่วนไม่ตรงกัน (~0.846) ทำให้ pixel-coordinate click พลาดเป้า
3. **Git commit/push ทำจาก sandbox ไม่ได้**: โฟลเดอร์นี้ sync ผ่าน Google Drive ทำให้ sandbox unlink ไฟล์ใน `.git/` ไม่ได้ (`.git/index.lock` ค้างอยู่) ผมแก้ไขเนื้อหาไฟล์ dashboard และ sw.js เสร็จเรียบร้อยแล้ว แต่ **ยังไม่ได้ commit/push** — สร้างสคริปต์ `push_tiktok_ads_20260921.command` ไว้ให้แล้ว กรุณา double-click ไฟล์นี้บนเครื่อง Mac เพื่อ commit + push

## อัปเดต WIBWUB_Ads_Dashboard.html

- **GMV Max** (1–21 ก.ย., sum เอง ไม่ใช้แถว Total): spend 583,464.27 / ออเดอร์ 10,290 / revenue 2,232,646.39 / ROI 3.83 / CPA 56.70
- **Business Ads** (97 แคมเปญ, ตรงกับแถว Total of 97 results ทุกตัว): spend 17,141.51 / imp 248,538 / clicks 3,034 / CPM 68.97 / CTR 1.22%
- **TikTok รวม** (DATA_PERIODS.sep.tiktok): spend 600,605.78 / revenue 2,232,646.39 / ออเดอร์ 10,290 / ROAS 3.72 / CPA 58.37
- `cover.tiktokDay` 20 → 21, `tiktokPull` และ `#ads-updated` title อัปเดตแล้ว
- Validate JS ผ่าน (`node --check`), bump `sw.js` cache v1194 → v1195
- **ยังไม่ commit/push** — ต้อง double-click `push_tiktok_ads_20260921.command`
