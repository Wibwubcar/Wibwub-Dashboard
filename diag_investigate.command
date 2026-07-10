#!/bin/bash
cd "$(dirname "$0")"
python3 diag_investigate.py
echo ""
echo "===== เสร็จสิ้น กด Enter เพื่อปิดหน้าต่างนี้ ====="
read
