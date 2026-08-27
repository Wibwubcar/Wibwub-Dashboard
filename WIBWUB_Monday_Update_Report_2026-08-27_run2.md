# WIBWUB Weekly Update — 27 ส.ค. 2569 (รอบที่ 2, 20:4x ICT)

Commit `7534250` — auto-update: Monday 2026-08-27 — Shipnity + Affiliate + ภาพรวมธุรกิจ
**ยังไม่ push** → รัน `push_now.command`

## STEP 0 — M5 protection
`const M5` = 8 labels (ม.ค.–ส.ค.) ทั้งใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` ตรงกับเดือนปัจจุบัน (8) → ไม่แก้ไข ไม่สร้าง array ใหม่

## STEP 1 — Shipnity
`Data Shipnity/Data_27-08-2026.xlsx` (28.1 MB, ช่วง 1–27 ส.ค. 2569) และคัดลอกเป็น `Data_สิงหาคม.xlsx` เรียบร้อยตั้งแต่รอบเช้า

## STEP 2 — TikTok Affiliate (สิ่งที่รอบก่อนยังค้าง)
Export ช่วง **1–25 ส.ค.** ผ่าน Transaction Analysis เสร็จแล้ว (queue ใช้เวลานานกว่าปกติ) — ดาวน์โหลดและคัดลอกเป็น
`Data Affiliate/Transaction_Analysis_Creator_List_20260801-20260825.xlsx` (607 KB)

**หมายเหตุ/ข้อจำกัด:** ปฏิทิน TikTok เลือกได้สูงสุดถึง **25/08** (26–27 ยัง greyed out) จึงเป็นข้อมูล partial month 1–25 ไม่ใช่ 1–27 ตาม Shipnity

## STEP 3 — ภาพรวมธุรกิจ (Top Products)
ทำเสร็จและ commit ไปแล้วในรอบเช้า (commit `1a44173`) — `ALL_PRODUCTS` + `PROD_MO` ใน Mobile และ Top Products chart/table ใน Dashboard เป็นข้อมูลสะสม ม.ค.–27 ส.ค. รอบนี้ไม่มีไฟล์ Shipnity ใหม่จึงไม่แก้ซ้ำ

## STEP 4 — Affiliate arrays (ตรวจสอบซ้ำแบบอิสระ)
คำนวณใหม่จากไฟล์ export โดย match ชื่อคอลัมน์ (ไม่ใช้ index ตายตัว — ไฟล์จริงมี 22 คอลัมน์ ไม่ใช่ 12 ตามที่ task file ระบุ) และข้ามแถวคำอธิบาย (row 2):

| Metric | ส.ค. 1-24 (เดิม) | ส.ค. 1-25 (ใหม่) |
|---|---|---|
| GMV | ฿1,313,998 | **฿1,375,920** |
| Refund | ฿22,159 | ฿22,949 |
| Net GMV | ฿1,291,840 | **฿1,352,971** |
| Commission | ฿151,291 | **฿158,103** |
| Creators (GMV>0) | 670 | **704** |

ค่าที่คำนวณได้ตรงกับค่าที่อยู่ในไฟล์ dashboard แล้วทุกตัว (ยืนยันข้าม)

- `WIBWUB_Affiliate_Dashboard.html`: `AF_MO[7]` = "ส.ค. (1-25)", `AF_GMV/AF_NET/AF_COM/AF_CR` index 7 → **overwrite เดือนเดิม ไม่ append**
- `WIBWUB_Mobile.html`: `AFI_MONTHS[9]` = "สค.69 (1-25)", `AFI_GMV/AFI_NET/AFI_COMM` index 9 → overwrite
- ยืนยัน index สุดท้ายเป็นเดือน ส.ค. จริงโดย match label ไม่ได้คำนวณจาก month-1 → **ไม่มีเดือนก่อนหน้าถูกทับ**

## STEP 5 — sw.js + commit
`wibwub-v854` → `wibwub-v855`
commit 3 ไฟล์: `WIBWUB_Mobile.html`, `WIBWUB_Affiliate_Dashboard.html`, `sw.js`
`push_now.command` เขียนใหม่ (ตัด `git add`/`git commit` ซ้ำซ้อนออก เหลือ push อย่างเดียว) และ `chmod +x` แล้ว

## Verification
- `node --check` บน JS ที่ extract จากทั้ง 3 dashboard → ผ่านทั้งหมด
- ความยาว array: `AF_*` = 8 ทุกตัว, `AFI_*` = 10 ทุกตัว (สอดคล้องกัน)
- `M5` = 8 ทั้งสองไฟล์
- `git status` สะอาดสำหรับไฟล์ที่แก้ทั้ง 3

## Deviation ที่ต้องรับทราบ
1. ข้อมูล affiliate เป็น **1–25 ส.ค.** (TikTok ปล่อยข้อมูลถึงแค่นั้น) ขณะที่ยอดขาย Shipnity เป็น 1–27 ส.ค. — ตัวเลขสองชุดนี้ครอบคลุมช่วงไม่เท่ากันโดยตั้งใจ และ label บนกราฟระบุช่วงไว้ชัดเจนแล้ว
2. Task file ระบุ Transaction Analysis เป็นไฟล์ 12 คอลัมน์ (col[1]=GMV, col[2]=returns, col[10]=commission) แต่ไฟล์จริงมี 22 คอลัมน์ — parse ด้วยชื่อหัวคอลัมน์แทน ควรอัปเดต task file
3. push ทำจาก sandbox ไม่ได้ (proxy HTTP 403) — ต้องรัน `push_now.command` บนเครื่อง
