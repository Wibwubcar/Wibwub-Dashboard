#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git add WIBWUB_Affiliate_Dashboard.html sw.js
git commit -m "update: sync affiliate สินค้า data (cr/vid) 2026-07-31 — creator data blocked by TikTok 503 outage"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
