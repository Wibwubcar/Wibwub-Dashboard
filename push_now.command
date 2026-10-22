#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock

# commit สิ่งที่ sandbox commit ไม่ได้ (sw.js bump + stock_snapshot.json)
git add sw.js "Data Shipnity/stock/stock_snapshot.json" Procurement_Dashboard.html WIBWUB_Affiliate_Dashboard.html
git diff --cached --quiet || git commit -m "auto-update: Stock forecast + คำขอสินค้า $(date +%Y-%m-%d) — Shipnity live + sw bump"

git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
