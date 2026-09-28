#!/bin/bash
# Fix stuck git locks, commit anything pending, then push.
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

rm -f .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock

git add fastmoss_history.json WIBWUB_FastMoss_Competitor_Dashboard.html

if git diff --cached --quiet; then
  echo "ℹ️  ไม่มีอะไรต้อง commit ใหม่"
else
  git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
      commit -m "auto: update FastMoss competitor snapshot $(date +%F)" \
    && echo "✅ Commit สำเร็จ"
fi

git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
echo ""
read -p "กด Enter เพื่อปิดหน้าต่าง..."
