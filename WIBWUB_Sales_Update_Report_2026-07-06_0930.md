# WIBWUB Sales Sheet Update — จันทร์ 6 ก.ค. 2026 09:30 (automated run)

## สรุป: ไม่มีข้อมูลใหม่ให้ sync — ไม่มี commit ใหม่

---

## STEP 1: อ่าน Google Sheets ทั้ง 3 (fileId ที่ถูกต้องจาก SKILL_update-wibwub_v2.md, ไม่ใช่จาก task file เดิมที่ fileId ผิด/ชี้ไปไฟล์ "ส่งเสริมการขาย Shopee" อื่น)

- Shopee: `10LrzWB8bbCO9FigCQFz5gZ3iSXMVhK0S` (gid=1820466351)
- Lazada: `1FxLAUiwabmNcBc3TA-bpHqg2MSK7uJ4U` (gid=1032656124)
- TikTok: `1k22c3PGY6aQjygAX6df_rQLR8aTzL-iz` (gid=150856480)

**ผลตรวจ:** ตาราง "ยอดรายเดือน" ของทั้ง 3 sheet มีข้อมูลล่าสุดถึงแค่ **พ.ค. 2569** เท่านั้น
- Shopee 01-31/05/26: ยอดขาย 5,581,064 / ads 826,300 / fee 1,433,217.24 / cancel% 5.38
- Lazada 01-31/05/26: ยอดขาย 129,523.54 / ads 6,590 / fee 22,874.79 / coupon 2,910 / cost% 24.995
- TikTok: ตรวจแล้วไม่พบ row เดือน มิ.ย./ก.ค. เช่นกัน (ค้นด้วย grep ทั้งไฟล์ CSV ขนาด ~13MB)

ค้นหา pattern `/06/26` และ `/07/26` ในทั้ง 3 ไฟล์ CSV เต็ม — **ไม่พบแม้แถวเดียว** แปลว่าพนักงานยังไม่ได้กรอกยอดเดือน มิ.ย./ก.ค. ลงชีตนี้

## STEP 2: เทียบกับค่าปัจจุบันใน Dashboard/Mobile

`SH_REV`, `TK_REV`, `LZ_REV`, `M5` ปัจจุบันมี 5 elements ตรงกับ ม.ค.–พ.ค. อยู่แล้ว และค่า พ.ค. ตรงกับ sheet เป๊ะ
(`SH_REV[4]=5581064` ตรงกับ 01-31/05/26 ใน sheet) → **ไม่มี delta ให้อัปเดต**

## STEP 3–6: ข้าม (ไม่มีข้อมูลใหม่)
M5/arrays/KPI text/date picker ไม่ต้องแก้ — MP_DATE_MAX คำนวณ dynamic จาก `_now` อยู่แล้วไม่ hardcode
ไม่ bump sw.js, ไม่ commit (ไม่มีการเปลี่ยนแปลงในขอบเขต task นี้)

---

## ⚠️ พบความไม่ตรงกันที่มีอยู่ก่อน (นอกขอบเขต task นี้ — ฝากตรวจสอบ)

ใน `WIBWUB_Mobile.html`: `TOTAL_REV`/`TOTAL_ORD` มี **6 elements** (ถึง มิ.ย., ตัวสุดท้าย TOTAL_REV=3986941)
แต่ `SH_REV`/`TK_REV`/`LZ_REV`/`M5` มีแค่ **5 elements** (ถึง พ.ค.)
→ ตัวเลข TOTAL น่าจะมาจาก pipeline อื่น (Shipnity/all-channel) ที่มีข้อมูล มิ.ย. แล้ว แต่ breakdown รายแพลตฟอร์มจาก sheet นี้ยังไม่มี มิ.ย.
ไม่ได้แก้ในรอบนี้เพราะอยู่นอกขอบเขต (task นี้ดึงแค่ 3 sheet Shopee/TikTok/Lazada) และไม่มีข้อมูลรายแพลตฟอร์มเดือน มิ.ย. จริงจาก sheet ให้ใส่แทน

ยังมีประเด็นค้างจากรายงาน 29 มิ.ย. (มิ.ย. หายจาก SH_REV/TK_REV/LZ_REV จาก daemon regression) ที่ยังไม่ถูกแก้ — เพราะ sheet ต้นทางยังไม่มีข้อมูล มิ.ย. ให้ดึงกลับมาอย่างถูกต้อง (ค่าที่เคยอยู่ก่อน regression ไม่สามารถ verify กับ sheet ปัจจุบันได้)
