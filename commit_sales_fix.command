#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git add "Data Shipnity/Sales_Dashboard.html"
git commit -m "fix: Sales Dashboard — deduplicate Shipnity files, fix June inflation

- Use correct 1-file-per-month mapping (Jan-Jun, 6 files)
- Exclude redundant June files (Data_มิถุนายน_17, Data_04-06-2026)
- Dedup by (order_id, SKU), 727 duplicates removed
- June: 8,439 unique orders, 4,709,831 baht (was 10,208,818 — fixed 53.6% inflation)"
git push origin main && echo "✅ Commit + Push สำเร็จ!" || echo "❌ Push ล้มเหลว"
read -p "Press Enter to close..."
