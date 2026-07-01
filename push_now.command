#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock .git/refs/heads/main.lock 2>/dev/null
git add WIBWUB_Dashboard.html WIBWUB_Mobile.html "data Ads/WIBWUB_Ads_Dashboard.html" sw.js push_now.command
git commit -m "fix 02/07: (1) June arrays ครบ 6 เดือน (2) Live Ads มิ.ย. 8 campaigns (3) GMV Max มิ.ย. Top5/Worst5 11 campaigns" 2>/dev/null || echo "(nothing to commit)"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
