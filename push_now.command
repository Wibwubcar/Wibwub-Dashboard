#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock .git/refs/heads/main.lock 2>/dev/null
git add Procurement_Dashboard.html "Data Shipnity/stock_snapshot.json" sw.js push_now.command
git commit -m "update 01/07/2026: Procurement stock live from Shipnity (192 SKUs + subproducts)" 2>/dev/null || echo "(nothing new to commit)"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
