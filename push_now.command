#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
echo "🔄 กำลัง pull ข้อมูลล่าสุดจาก GitHub ก่อน push..."
git pull --no-edit origin main
if [ $? -ne 0 ]; then
  echo "⚠️ Pull ไม่สำเร็จ (อาจมี conflict) — กรุณาแจ้ง Claude เพื่อช่วยแก้ conflict ก่อน push"
  exit 1
fi
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
