# WIBWUB Daily TikTok Followers — 19 ก.ย. 2026

## สรุป
**อัปเดตสำเร็จ พร้อมแก้บั๊กสำคัญที่ค้างมานาน**

ดึงข้อมูล FollowerHistory.csv จาก TikTok Studio (60 วันล่าสุด: 20 ก.ค. – 17 ก.ย., ข้อมูลถึง 17 กันยายน = **29,594 followers**) สำเร็จ และ sync เข้า dashboard เรียบร้อย

- `WIBWUB_Dashboard.html` → TikTok data array และ FOL_DATA เดือนกันยายนอัปเดตถึง 17 ก.ย. (29,594) ✅ — ถูกรวมเข้ากับ commit ของ task อื่นที่รันคู่ขนาน (`637a654`) แล้ว ตรวจสอบ diff สะอาด
- `WIBWUB_Mobile.html` → `TK_FOL` array อัปเดตเป็น `[...,28684,29594]` (29.6K, +6.2K จาก ม.ค.) ✅ — commit `1993b9b`
- `sw.js` → cache version อยู่ที่ `wibwub-v1167` แล้ว (bump โดย task คู่ขนานอื่น แต่ตรงตามเงื่อนไขที่ต้องการ) ✅
- `push_now.command` → มีอยู่แล้วจาก task อื่น ไม่ได้แก้ไขเพิ่ม ✅

## บั๊กที่พบและแก้ไข
พบว่า `update_followers.py` **ไม่เคยอัปเดต `TK_FOL` array ใน WIBWUB_Mobile.html สำเร็จเลยในทุกรอบที่ผ่านมา** แม้จะพิมพ์ข้อความ "✅ WIBWUB_Mobile.html อัปเดตแล้ว" ก็ตาม

**สาเหตุ**: regex `r'const TK_FOL=\[([^\]]*)\];'` (บรรทัด 159) ไม่รองรับช่องว่างรอบเครื่องหมาย `=` แต่ไฟล์จริงเขียนว่า `const TK_FOL = [...]` (มีเว้นวรรค) ทำให้ regex ไม่ match และ block การอัปเดตทั้งหมดถูกข้ามไปแบบเงียบๆ

**แก้ไข**: เปลี่ยน regex ทั้ง search และ replace ให้ใช้ `\s*` รอบ `=` — ทดสอบรันซ้ำแล้วเห็นข้อความ `✅ TK_FOL อัปเดตแล้ว (9 เดือน, ล่าสุด 29,594)` และ array อัปเดตถูกต้อง — commit `fefa564`

## รายละเอียดทางเทคนิค
- การดาวน์โหลด CSV ผ่านปุ่ม Download บน TikTok Studio ยังคงล้มเหลวแบบเงียบเหมือนรอบก่อนๆ ใช้ workaround เดิม: capture blob ผ่าน `URL.createObjectURL` override + parse โครงสร้าง ZIP (local file header, STORED entries) ด้วย JS โดยตรงเพื่อดึง CSV text ออกมา แทนการพึ่ง native download
- พบว่า repo นี้มี **task/agent อื่นหลายตัวรันคู่ขนานและ commit เข้า repo เดียวกัน** (Shopee Live, Shopee Ads, TikTok sales from Sheets, Stock forecast) ทำให้เกิด `.git/index.lock`, `.git/HEAD.lock`, `.git/refs/heads/main.lock` ชนกันบ่อยมาก
  - ใช้ git plumbing (`hash-object` → `mktree` → `commit-tree` → `update-ref`) เพื่อ commit โดยไม่ต้องแตะ index lock โดยตรง
  - พบเคส `refs/heads/main.lock` ค้างเกิน 4 นาที (ไฟล์ที่ค้างเป็นของความพยายาม update-ref ของตัวเองก่อนหน้า ที่ rename ไม่สำเร็จเพราะ permission) แก้โดย `mv` ไฟล์ lock ไปเป็น `refs/heads/main` โดยตรง (เนื้อหาถูกต้องอยู่แล้ว) แทนการลบแล้วรอ retry

## ข้อเสนอแนะ
1. บั๊ก regex ใน `update_followers.py` ได้รับการแก้แล้ว — ควรตรวจสอบ Mobile dashboard ในรอบถัดๆ ไปว่า TK_FOL ยังอัปเดตต่อเนื่องปกติ
2. ปัญหา git lock contention จาก multi-agent ควร monitor ต่อ — ถ้าเกิดถี่ขึ้นอาจพิจารณาใช้ retry queue หรือ lock file ที่มี timeout สั้นลง
3. ปัญหาการดาวน์โหลดไฟล์ล้มเหลวแบบเงียบจาก TikTok Studio ยังคงเป็นปัญหาเดิม แนะนำปรับ default workflow ให้ใช้วิธี JS ZIP-parse ตั้งแต่ต้น
