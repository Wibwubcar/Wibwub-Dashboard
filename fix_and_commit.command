#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git add WIBWUB_Dashboard.html WIBWUB_Mobile.html WIBWUB_Affiliate_Dashboard.html Procurement_Dashboard.html sw.js
git commit -m "fix 03/07: M5→7เดือน + Affiliate มิ.ย.ครบ+ก.ค.1 + Stock 193SKUs + DatePicker"
git push origin main && echo "✅ Push สำเร็จ!" || echo "❌ Push ล้มเหลว"
echo "Done! กด Enter เพื่อปิด"; read
