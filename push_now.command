#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git add WIBWUB_Mobile.html WIBWUB_Affiliate_Dashboard.html sw.js push_now.command
git diff --cached --quiet || git commit -m "monday-update 2026-08-19: Shipnity Top Products ถึง 19 ส.ค. (ALL_PRODUCTS + PROD_MO), affiliate 1-16 ส.ค. (Transaction Analysis ล่าสุด), sw v724"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
