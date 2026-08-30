#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
# commit b64afa3 พร้อม push แล้ว (Shipnity ส.ค. 1-29 Top Products + Affiliate ส.ค. 1-27, sw v889)
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
