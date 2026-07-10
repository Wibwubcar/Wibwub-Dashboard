#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git add -A
git commit -m "WIBWUB affiliate auto-update $(date +%Y-%m-%d_%H%M)" || echo "ℹ️ ไม่มีอะไรให้ commit"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
