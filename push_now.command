#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock .git/refs/heads/main.lock 2>/dev/null
git add "data Ads/WIBWUB_Ads_Dashboard.html" "data Ads/TikTok/GMV Max/Campaign overview data 20260601 - 20260630.xlsx" sw.js push_now.command
git commit -m "update 01/07/2026: Ads Dashboard มิ.ย. ครบ — Shopee 1-30 + TikTok GMV Max 1-30" 2>/dev/null || echo "(nothing new to commit)"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
