#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

# Remove all lock files
rm -f .git/HEAD.lock .git/index.lock .git/refs/heads/main.lock 2>/dev/null

# Commit pending changes
git add WIBWUB_Dashboard.html WIBWUB_Mobile.html WIBWUB_HR_Dashboard.html \
        Procurement_Dashboard.html "Data Shipnity/stock_snapshot.json" \
        "data Ads/WIBWUB_Ads_Dashboard.html" sw.js push_now.command 2>/dev/null

git commit -m "update 01/07/2026: fix Ads JS syntax + June arrays + Procurement stock refresh" 2>/dev/null || echo "(nothing new to commit)"

# Push
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
