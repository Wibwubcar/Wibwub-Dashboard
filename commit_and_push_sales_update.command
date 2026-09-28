#!/bin/bash
# Fix stuck git locks (sandbox can't unlink() under .git/), commit the sales-sheet sync
# (WIBWUB_Dashboard.html, WIBWUB_Mobile.html, sw.js), then push.
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

echo "Repo: $(pwd)"
for f in .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock .git/refs/heads/main.lock; do
  if [ -e "$f" ]; then rm -f "$f" && echo "removed $f"; fi
done
find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null

git add WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js

if git diff --cached --quiet; then
  echo "ℹ️  ไม่มีอะไรต้อง commit ใหม่ (อาจ commit ไปแล้ว)"
else
  git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
      commit -m "auto-update: sales from Sheets 2026-09-21 09:30 run2 — Shopee/Lazada extend 01-13→01-20/09 (SH_REV/ORD/FEE/CANCEL_PCT, LZ_REV/ADS/FEE/COUPON/COST_PCT), TikTok TK_AFI/TK_NET/TK_AFIPCT refined to 01-20/09 (TK_REV/ORD already synced); sw.js bump v1195→v1196" \
    && echo "✅ Commit สำเร็จ"
fi

git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
echo ""
read -p "กด Enter เพื่อปิดหน้าต่าง..."
