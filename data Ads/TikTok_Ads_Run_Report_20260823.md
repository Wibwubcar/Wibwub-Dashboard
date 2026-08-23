# TikTok Ads — scheduled run report, 23 ส.ค. 2569 (Sun)

## ⚠️ ต้องทำด้วยมือ 2 อย่าง

1. **ลบไฟล์ค้าง `.git/index.lock`** ในโฟลเดอร์ `All/` — คำสั่ง git ทุกคำสั่งที่เขียน index จะพังจนกว่าจะลบ
   (sandbox ลบเองไม่ได้ — "Operation not permitted")
   ```
   rm "…/Digital Marketing/claude/All/.git/index.lock"
   ```
2. **ดับเบิลคลิก `push_now.command`** เพื่อ push commit `a2ccad1` ขึ้น remote

เล็กน้อย: ลบไฟล์ทดสอบ `~/Downloads/__dltest_20260823.txt` (6 bytes) ได้เลย

## สิ่งที่ทำไม่สำเร็จ — ดาวน์โหลด xlsx

Session TikTok Ads **ยังไม่หมดอายุ** (dashboard โหลดข้อมูลได้ปกติ) และตั้งช่วงวันที่
1–23 ส.ค. 2569 ได้ถูกต้องทั้งหน้า GMV Max และหน้า Campaigns

แต่ **ไฟล์ export ไม่เคยลงมาที่ ~/Downloads เลย** ลองแล้ว 6 วิธี บนปุ่ม export 3 จุด
(ไอคอนดาวน์โหลดหน้า GMV Max Overview, ไอคอน export หน้า Trends ของ Business Ads,
เมนู More → Export data):

- คลิกด้วยพิกัดพิกเซล
- `find` + คลิกผ่าน ref
- `element.click()`
- ยิง pointer/mouse event ตามลำดับจริง
- เรียก `onClick()` ของ React fiber โดยตรง

ทุกวิธีรายงานว่าสำเร็จ, tracking beacon ยิงออกจริง, ไม่มี error ใน console,
แต่ไม่มีไฟล์เกิดขึ้น **ทดสอบดาวน์โหลด blob ธรรมดาแล้วสำเร็จ** (`__dltest_20260823.txt`)
แปลว่า Chrome ดาวน์โหลดได้ปกติ — ปัญหาคือ export ที่เว็บ TikTok เป็นคนเริ่มถูกบล็อก/หายไป
น่าจะต้องให้คนกดเอง (browser ต้องเห็น real user gesture หรือมี prompt ที่ค้างอยู่)

**ไม่ได้สร้างไฟล์ xlsx ปลอมไว้ในโฟลเดอร์ archive** เพราะจะทำให้ source of truth เพี้ยน
และหลอกรอบถัดไป

## สิ่งที่ทำแทน — อัปเดต dashboard จากตัวเลขบนหน้าจอ

Task file สั่งชัดว่า "ห้ามจบงานแค่ download" และเหตุผลที่มี schedule นี้คือกัน dashboard ค้าง
จึงอ่านยอดรวมจากหน้า TikTok Ads Manager โดยตรง (ตัวเลขชุดเดียวกับแถว Total ในไฟล์ xlsx)
แล้วอัปเดต `WIBWUB_Ads_Dashboard.html` พร้อมหมายเหตุ provenance กำกับไว้ในโค้ด

### ตัวเลข ส.ค. 1–23 (23 ส.ค. ยังไม่เต็มวัน)

| | เดิม (1–22) | ใหม่ (1–23) |
|---|---|---|
| GMV Max spend | 439,240.37 | **447,471.99** |
| GMV Max orders | 7,988 | **8,130** |
| GMV Max revenue | 1,628,287.79 | **1,654,025.47** |
| GMV Max ROI / CPA | 3.71 / 54.99 | **3.70 / 55.04** |
| Business Ads spend | 11,209.23 | **11,502.82** |
| Business Ads imp | 159,526 | **163,944** |
| Business Ads clicks | 4,568 | **4,620** |
| TikTok รวม spend | 450,449.60 | **458,974.81** |
| TikTok ROAS / CPA | 3.61 / 56.39 | **3.60 / 56.45** |

- `TK_BREAKDOWN.all` gmvMax/bizAds เลื่อนตาม delta ของเดือน ส.ค. แล้ว
- `gmvLive` **ไม่แตะ** — LIVE campaign ล่าสุดยังเป็น "live 19.08.26" เหมือนเดิม
  (และ Overview เป็น shop-level รวม LIVE อยู่แล้ว ห้ามบวกซ้ำ)
- label / badge / `#ads-updated` แก้เป็น TikTok 1-23 ส.ค. แล้ว
  Shopee ยังเป็น 1-22 ส.ค. เต็มวัน (refresh ไปแล้วเมื่อ 08:12-08:15 ICT วันนี้โดย schedule อื่น)

### ตรวจแล้ว

- `node --check` ผ่าน
- ผลรวม 2 campaigns ของ Business Ads = แถว Total เป๊ะ (11,480.52 + 22.30 = 11,502.82 / 162,833 + 1,111 = 163,944 / 4,612 + 8 = 4,620)
- ROI, CPA, CPM, CTR, ROAS คำนวณใหม่ตรงกับค่าที่เก็บทุกตัว
- TikTok revenue รวมทุกเดือน = 10,730,231.10 → label ฿10.73M ตรง
- backup ไว้ที่ `WIBWUB_Ads_Dashboard.html.bak_20260823`
- `sw.js` v781 → **v782**
- commit `a2ccad1` (ยังไม่ push)

**รอบหน้าเมื่อโหลด xlsx สำเร็จ ให้ตรวจตัวเลขชุดนี้ซ้ำอีกที**
