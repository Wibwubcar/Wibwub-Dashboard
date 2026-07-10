#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
echo "===== รัน wibwub_update.py ====="
python3 wibwub_update.py
echo ""
echo "===== รัน update_stock.py (Procurement/Forecast) ====="
python3 update_stock.py
echo ""
echo "===== เสร็จสิ้น กด Enter เพื่อปิดหน้าต่างนี้ ====="
read
