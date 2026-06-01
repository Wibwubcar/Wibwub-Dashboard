#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

# Remove stale git locks
rm -f .git/index.lock .git/HEAD.lock 2>/dev/null

# Stage updated files
git add WIBWUB_Mobile.html WIBWUB_Dashboard.html "data Ads/WIBWUB_Ads_Dashboard.html" sw.js

# Commit (skip if nothing to commit)
git diff --cached --quiet || git commit -m "fix: update Ads Dashboard all-period DATA + sw.js v93

- DATA.shopee: spend 3.03M->3.35M, revenue 18.2M->20.3M, orders 43716->47958
- DATA.tiktok: spend 1.05M->1.12M, revenue 5.44M->5.81M, orders 20779->22700
- ADS_PERIOD_SUMMARY: Shopee 19.34M->20.30M, TikTok 5.65M->5.81M
- sw.js bumped to v93"

# Push
echo "Pushing..."
git push origin main && echo "✅ Push สำเร็จ!" || echo "❌ FAIL"
read -p "กด Enter เพื่อปิด..."
