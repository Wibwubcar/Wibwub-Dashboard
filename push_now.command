#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git add WIBWUB_Affiliate_Dashboard.html WIBWUB_Mobile.html sw.js
git commit -m "auto-update: Affiliate $(date +%Y-%m-%d)"
git push && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
