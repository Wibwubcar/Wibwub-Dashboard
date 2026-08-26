#!/bin/bash
# WIBWUB — push Thursday Affiliate auto-update (2026-08-26)
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" || exit 1
echo "=== WIBWUB push — $(date) ==="
git status --short
# stage the auto-update files in case the sandbox commit didn't land
git add WIBWUB_Affiliate_Dashboard.html WIBWUB_Mobile.html sw.js
if ! git diff --cached --quiet; then
  git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
      commit -m "auto-update: Affiliate $(date +%Y-%m-%d)"
fi
git push origin HEAD
echo "=== done ==="
read -n 1 -s -r -p "Press any key to close..."
