# WIBWUB Sales Sheet Update — พุธ 22 ก.ค. 2026 (automated run)

## สรุป: ข้อมูลตรงกันหมดแล้ว — ไม่มี commit ใหม่ (ของเดิมถูกอัปเดตไปก่อนหน้านี้ในวันเดียวกัน)

---

## STEP 1 — อ่าน Google Sheets

- Shopee: `19P7945wP4mQI0zzWA3qgFsEFOd1VQOLctLfSM0TJMos` — แถวล่าสุด `01-19/07/26`: ยอดขาย 3,789,950 / ads 606,406.44 / fee 1,135,469.02 / order 6,883 / cancel 321 (4.66%)
- TikTok: `1k22c3PGY6aQjygAX6df_rQLR8aTzL-iz` — แถวล่าสุด `01-19/07/26`: ยอดขาย 1,358,229.08 / ads(GMV) 1,337,558.33 / ads+GMV spend 332,929.94 / fee+comm 354,806.12 / order 7,336
- Lazada: `1x8bbjZxgoQe6bT4s1_S8W2A9EONsI4bl4d4znwq9t7E` — แถวล่าสุด `01-19/07/26`: ยอดขาย 58,344.78 / ads 4,350 / fee 10,304.62 / coupon 2,160 / cost% 28.82

## STEP 2 — เทียบกับ arrays ใน Dashboard/Mobile (index 6 = ก.ค.)

ทุกค่าตรงกับ sheet เป๊ะแล้ว — ไม่มี delta:

- `SH_REV[6]=3789950`, `SH_ORD[6]=6883`, `SH_ADS[6]=606406`, `SH_FEE[6]=1135469`, `SH_CANCEL_PCT[6]=4.66`
- `TK_REV[6]=1358229.08`, `TK_ORD[6]=7336`, `TK_ADS[6]=1337558`, `TK_ADSSPEND[6]=332929`, `TK_FEECOMM[6]=354806`
- `LZ_REV[6]=58345`, `LZ_ADS[6]=4350`, `LZ_FEE[6]=10305`, `LZ_COUPON[6]=2160`, `LZ_COST_PCT[6]=28.82`

ตรวจ git log พบว่าค่าชุดนี้ถูก commit ไปแล้วในวันนี้ (`3988f00 auto: update 2026-07-22 18:24`) และ HEAD ตรงกับ `origin/main` — แปลว่ามีการรันซิงก์ข้อมูลชุดนี้และ push สำเร็จไปแล้วก่อนหน้ารอบนี้

## STEP 3–6: ข้าม (ไม่มีข้อมูลใหม่ให้อัปเดต)

- ไม่แก้ arrays / hardcoded KPI text (ไม่มี delta)
- M5 มี 7 label (ม.ค.–ก.ค.) ตรงกับเดือนปัจจุบันแล้ว, date picker ปัจจุบันแล้ว
- sw.js อยู่ที่ `wibwub-v442` แล้ว, ไม่ต้อง bump / commit / push ซ้ำ
