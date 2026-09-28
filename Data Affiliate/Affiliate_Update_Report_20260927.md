# WIBWUB Affiliate Update — 2026-09-27

## สถานะ: ⚠️ สำเร็จบางส่วน (Partial) — ครีเอเตอร์/สินค้า/วีดีโอ อัปเดตแล้ว, ไลฟ์สตรีมติด 503 ซ้ำ

## ช่วงข้อมูล
- ครีเอเตอร์: 1–25 ก.ย. 2569 (ใช้ไฟล์ export จาก 26 ก.ย. เนื่องจากรอบนี้ retry export ใหม่โดน 503)
- สินค้า: 1–25 ก.ย. 2569 (export ใหม่สำเร็จ)
- วีดีโอ: 1–24 ก.ย. 2569 (export ใหม่สำเร็จ)
- ไลฟ์สตรีม: ยังค้างที่ 1–23 ก.ย. 2569 (export ใหม่โดน 503 ซ้ำ — ไม่มีข้อมูลใหม่)

## สิ่งที่ทำสำเร็จ
1. เชื่อมต่อ Chrome บน Mac สำเร็จ (deviceId b75a6bb0-5b78-4e44-92a8-75224f1ce4ee)
2. หน้าเว็บ TikTok Affiliate เปลี่ยน UI ใหม่ต่อจากเดิม — เมนู "ครีเอเตอร์"/"สินค้า" ย้ายไปอยู่ใต้ "การวิเคราะห์" (creator-analysis, product-performance) และ "วีดีโอ" อยู่ที่เมนู "วิดีโอทั้งหมด" (video-analysis) แยกต่างหาก ส่วน "ไลฟ์สตรีม" ย้ายไปอยู่เป็น tab ในหน้า "ผลการดำเนินงาน" (transaction-analysis/Performance)
3. Export สำเร็จและดาวน์โหลดได้:
   - สินค้า: `ListProducts_2026-09-01-2026-09-26_ALLPlan_20260927015624.xlsx` → ย้ายเข้า `Data Affiliate/สินค้า/`
   - วีดีโอ: `Video_Analysis_Video_List_20260901-20260924.xlsx` → ย้ายเข้า `Data Affiliate/วีดีโอ/`
4. ประมวลผลและอัปเดต Dashboard:
   - **WIBWUB_Affiliate_Dashboard.html**: AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR เดือน ก.ย. อัปเดตจาก (1-23) → (1-25): GMV ฿1,777,507 / Net ฿1,652,658 / Comm ฿196,450 / Creators 955
   - PRODUCTS[].cr/vid ทั้ง 7 รายการ refresh ใหม่จากไฟล์สินค้าล่าสุด (Leather Wipes cr:540/vid:500, Interior wipes cr:242/vid:241, Sugar cr:206/vid:217, CLEANER cr:34/vid:35, Interior cr:59/vid:106, Refresh cr:0/vid:0, Visible cr:16/vid:22)
   - VIDEOS array: อัปเดต 96 รายการเดิม (เดือน ก.ย.), เพิ่มใหม่ 121 รายการ → รวม 9,778 รายการ (parse ผ่าน entry_re ปกติ, verify ด้วย node eval ผ่าน, git diff --stat เปลี่ยน ~3.3% ของไฟล์ — อยู่ในเกณฑ์ปลอดภัย)
   - **WIBWUB_Mobile.html**: AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM sync ค่าเดียวกับ Affiliate Dashboard (KPI tile บนมือถือคำนวณแบบ dynamic จาก array อยู่แล้ว ไม่ต้องแก้ hardcode)
   - sw.js bump cache version (ผ่านหลายรอบจาก automation อื่นที่รันขนานกัน ปัจจุบันอยู่ที่ v1273)
5. Commit เข้า local git สำเร็จ (ไฟล์ถูกรวมเข้ากับ commit ของ automation อื่นที่รันขนานกันในช่วงเวลาเดียวกัน เช่น FastMoss/TikTok followers sync) — **ยังไม่ได้ push ขึ้น GitHub** เนื่องจาก sandbox นี้ไม่มีสิทธิ์เข้าถึง github.com โดยตรง (403 จาก proxy) ต้องรอผู้ใช้ดับเบิ้ลคลิก `push_now.command`

## จุดที่ติดปัญหา (ต่อเนื่องจากรอบก่อนหน้า)
**TikTok export/file endpoint ยังคง 503 เป็นระยะ ๆ** — ยืนยันด้วย network log:
- Retry export ตาราง "ครีเอเตอร์" (task_id ใหม่ `01M3G95RN39TCHD03MVMZBHE2Hv2`) → 503 ซ้ำ 2 ครั้ง (endpoint `/api/v1/insights/export/file/*`)
- Export ตาราง "ไลฟ์สตรีม" (task_id `01M3G9K6JVBNP6WPJRHTHJ53KPv2`) → 503 ซ้ำ 2 ครั้ง (endpoint `/api/v1/oec/affiliate/compass/export_task/export` — คนละ endpoint กับครีเอเตอร์ แต่ปัญหาเดียวกัน)
- ตรงกันข้าม: Export "สินค้า" และ "วีดีโอ" สำเร็จได้ปกติในรอบนี้ — แสดงว่าปัญหาไม่ได้บล็อกทั้งระบบ แต่เป็น intermittent ต่อ task_id/endpoint

**นี่คือครั้งที่ 4+ ที่พบปัญหานี้ต่อเนื่องมาตั้งแต่ 20 ก.ย. 2569** (ครั้งก่อน: 20 ก.ย., 26 ก.ย. เช้า, 26 ก.ย. เย็น, และวันนี้) รวมระยะเวลากว่า 1 สัปดาห์ — ควรพิจารณาแจ้ง TikTok Shop support อย่างจริงจัง

## Git/Infrastructure
- พบ `.git/index.lock` ค้าง (จาก process อื่นที่ crash) บล็อกไม่ให้ commit ได้ชั่วคราว — แก้ไขโดยขอสิทธิ์ลบไฟล์ผ่าน device_request_delete_permission แล้ว `rm -f .git/index.lock` สำเร็จ
- Repo นี้มี automation หลายตัวรันขนานกันในช่วงเวลาเดียวกัน (Shopee Ads, TikTok followers, FastMoss, stock ฯลฯ) ทำให้ commit ของแต่ละ task ปะปนกันบ้าง (ไฟล์ของ Affiliate ถูกรวมเข้า commit ของ FastMoss/TikTok followers) — ข้อมูลถูกต้องครบถ้วน แต่ commit message ไม่ตรงกับ task ที่แก้จริง

## ยังไม่ได้ทำ (ต้องรอรอบถัดไปหรือ manual)
- ไลฟ์สตรีม (Live List) ยังไม่มีข้อมูลใหม่กว่า 1-23 ก.ย. — ไม่ได้แตะ VIDEOS/PRODUCTS ในส่วนที่ต้องพึ่งไฟล์นี้ (ไม่มี field ใน dashboard ที่ผูกกับไฟล์ live โดยตรงนอกจากรายงานหน้า analysis เอง)
- Push ขึ้น GitHub — รอผู้ใช้ดับเบิ้ลคลิก `push_now.command`
