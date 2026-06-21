#!/bin/bash
# WIBWUB Downloads Cleaner
# ลบไฟล์ Shipnity + Affiliate เก่าที่ค้างใน Downloads
# (ไฟล์เหล่านี้ถูก copy ไปโฟลเดอร์งานแล้ว)

DOWNLOADS=~/Downloads

echo "🧹 WIBWUB Downloads Cleaner"
echo "================================"
echo ""

# นับก่อน
SH_COUNT=$(ls "$DOWNLOADS"/Data_*-*-2026*.xlsx 2>/dev/null | wc -l | tr -d ' ')
AF_COUNT=$(ls "$DOWNLOADS"/Transaction_Analysis_Creator_List_*.xlsx 2>/dev/null | wc -l | tr -d ' ')

echo "พบไฟล์ที่จะลบ:"
echo "  📊 Shipnity export:  $SH_COUNT ไฟล์"
echo "  🛒 Affiliate report: $AF_COUNT ไฟล์"
echo ""

if [ "$SH_COUNT" -eq 0 ] && [ "$AF_COUNT" -eq 0 ]; then
  echo "✅ Downloads สะอาดดีแล้ว!"
  read -p "กด Enter เพื่อปิด..."
  exit 0
fi

echo "⚠️  จะลบไฟล์เหล่านี้ออกจาก Downloads (ไม่ใช่โฟลเดอร์งาน)"
read -p "ยืนยันลบ? (y/n): " confirm

if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
  # ลบ Shipnity exports (Data_DD-MM-YYYY.xlsx)
  rm -f "$DOWNLOADS"/Data_*-*-2026*.xlsx 2>/dev/null
  echo "✅ ลบ Shipnity exports $SH_COUNT ไฟล์"

  # ลบ Affiliate reports
  rm -f "$DOWNLOADS"/Transaction_Analysis_Creator_List_*.xlsx 2>/dev/null
  echo "✅ ลบ Affiliate reports $AF_COUNT ไฟล์"

  echo ""
  REMAINING=$(ls "$DOWNLOADS" | wc -l | tr -d ' ')
  echo "🎉 เสร็จ! เหลือไฟล์ใน Downloads: $REMAINING ไฟล์"
else
  echo "ยกเลิก — ไม่ได้ลบอะไร"
fi

echo ""
read -p "กด Enter เพื่อปิด..."
