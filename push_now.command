#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

# ลบ lock files ที่ค้างอยู่
rm -f .git/HEAD.lock .git/index.lock .git/MERGE_HEAD.lock 2>/dev/null

# commit ไฟล์ที่แก้ไขค้าง
git add WIBWUB_Dashboard.html WIBWUB_Mobile.html WIBWUB_Affiliate_Dashboard.html sw.js
git diff --cached --quiet || git commit -m "fix: ภาพรวมธุรกิจ ใช้ข้อมูล Shipnity — เพิ่ม FB/Line ทุก channel ใน Dashboard+Mobile, bump sw.js v146"

# push
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
