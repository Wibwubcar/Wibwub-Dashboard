#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
# Monday update 31/08/2026 — commit 82d0635 (sw v908)
# คำขอสินค้า sync 31/08/2026 — commit be8020b (WIBWUB_Affiliate_Dashboard.html + sw.js v909)
# คำขอสินค้า sync 31/08/2026 (รอบ 2) — commit 2c0124d (WIBWUB_Affiliate_Dashboard.html + sw.js v911)
rm -f .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock
git add WIBWUB_Affiliate_Dashboard.html sw.js 2>/dev/null; git diff --cached --quiet || git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" commit -m "auto-update: คำขอสินค้า $(date +%Y-%m-%d)"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
