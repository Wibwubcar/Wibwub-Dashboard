#!/bin/bash
# WIBWUB — push Monday update (9 ก.ย. 2569 · sw v1053)
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock .git/refs/heads/main.lock
find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null
git add WIBWUB_Dashboard.html WIBWUB_Mobile.html WIBWUB_Affiliate_Dashboard.html sw.js
git diff --cached --quiet || git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" commit -m "auto-update: Monday $(date +%Y-%m-%d) — Shipnity + Affiliate + ภาพรวมธุรกิจ (sw v1053)"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
