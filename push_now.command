#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
echo "Pushing latest WIBWUB dashboard commit to GitHub..."
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
read -n 1 -s -r -p "Press any key to close this window..."
echo ""
