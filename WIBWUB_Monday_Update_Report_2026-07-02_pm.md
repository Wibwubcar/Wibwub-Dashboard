# WIBWUB Weekly Update — พฤ. 2 ก.ค. 2026 (automated run, รอบเสริม)

## สรุป: ไม่มี commit ใหม่ — ซ่อม working-tree ที่ถูก corrupt (June หายจาก sales arrays) กลับให้ตรง HEAD

รอบนี้ตรวจพบว่า working copy ของ WIBWUB_Dashboard.html และ WIBWUB_Mobile.html
ถูกเขียนทับให้ตัด element เดือน มิ.ย. (ตัวที่ 6) ออกจากทุก sales array และย้อน M5 กลับเหลือ 5 เดือน
ทั้งที่ HEAD (commit 3e85350) ถูกต้องเป็น 6 เดือนอยู่แล้ว -> regression ต้องแก้

## การตรวจสอบ (verify)
Affiliate มิ.ย. ตรงกับไฟล์ต้นทางเป๊ะ (Transaction_Analysis_Creator_List_20260601-20260630.xlsx):
- GMV 642,490 = AFI_GMV[7] OK
- NET 632,313 = AFI_NET[7] OK
- COMM 79,284 = AFI_COMM[7] OK
- Creators (GMV>=1K) 87 = header OK
- Orders 3,103 = header OK
-> Affiliate June sync + commit เสร็จตั้งแต่ commit 3e85350 วันนี้ ไม่ต้องทำซ้ำ

Top Products: ครอบคลุม ม.ค.-มิ.ย. (current) ก.ค. เพิ่งผ่าน 2 วัน ยังไม่ต้องเพิ่ม
Data downloads: ไฟล์สดอยู่แล้ว (Shipnity ก.ค. 01:07, Affiliate June creator file) -> ข้าม Chrome re-download

## การแก้ไข
- git checkout ล้มเหลว (unable to unlink, Operation not permitted - ข้อจำกัด Google Drive mount)
- ใช้ in-place overwrite: git show HEAD:<file> > <file>
- ผล: ทั้งสองไฟล์ byte-identical กับ HEAD อีกครั้ง
  - const M5 = 6 เดือน (ม.ค.-มิ.ย.) OK
  - SH_REV มี 5225845 (มิ.ย.) OK
  - Affiliate June arrays ครบ OK

## ไม่ได้ทำ (โดยตั้งใจ)
- ไม่รัน guardrail M5 script (จะตั้ง M5=7 ทั้งที่ arrays มี 6 -> index 7 = NaN -> แดชบอร์ดเพี้ยน)
- ไม่ commit / ไม่ push / ไม่ bump sw.js (HEAD ถูกต้องแล้ว ไม่มี legitimate change ค้าง)

## หมายเหตุ / ตามต่อ
- stale .git/index.lock (0 byte) ค้างจาก git checkout ที่ fail — sandbox ลบไม่ได้; push_now.command มี rm -f .git/index.lock เคลียร์เองบนเครื่องจริง
- ต้นตอ regression: มี process/daemon เขียนทับไฟล์ตัด มิ.ย. ออกซ้ำ ๆ — แนะนำตรวจ automation ตัวอื่นที่แก้ไฟล์เดียวกัน
- HEAD 3e85350 จะขึ้น live เมื่อ user รัน push_now.command (sandbox push ติด proxy 403)
