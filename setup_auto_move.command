#!/bin/bash
echo "🔧 ติดตั้ง WIBWUB Auto-Move Downloads..."

PLIST_SRC="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/com.wibwub.download-mover.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.wibwub.download-mover.plist"

# Unload ถ้ามีอยู่แล้ว
launchctl unload "$PLIST_DST" 2>/dev/null || true

# Copy plist ไปที่ LaunchAgents
cp "$PLIST_SRC" "$PLIST_DST"
echo "✅ Copied plist to LaunchAgents"

# Load
launchctl load "$PLIST_DST"
echo "✅ LaunchAgent loaded!"

echo ""
echo "🎉 เสร็จแล้ว! ตั้งแต่นี้ไปเมื่อ schedule ดาวน์โหลดไฟล์มาใน Downloads"
echo "   ระบบจะย้ายไปโฟลเดอร์งานอัตโนมัติภายใน 5 วินาที"
echo ""
echo "กด Enter เพื่อปิด"
read
