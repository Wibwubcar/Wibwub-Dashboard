#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock .git/*.lock .git/refs/heads/main.lock 2>/dev/null
git add WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js push_now.command
git commit -m "auto-update: TikTok followers 2026-07-01 — 27075 followers" || echo "(nothing new to commit)"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
