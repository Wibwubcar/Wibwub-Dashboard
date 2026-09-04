#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
# Affiliate auto-update 04/09/2026 — commit f4acd81 (sw v978)
# AF_*/AFI_* + PRODUCTS cr/vid + VIDEOS (ก.ย. 1-1)
rm -f .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
read -p "กด Enter เพื่อปิด"
