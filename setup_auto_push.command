#!/bin/bash
echo "🚀 ติดตั้ง WIBWUB Auto-Push to GitHub..."

PLIST_SRC="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/com.wibwub.auto-push.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.wibwub.auto-push.plist"

# Unload ถ้ามีอยู่แล้ว
launchctl unload "$PLIST_DST" 2>/dev/null || true

cp "$PLIST_SRC" "$PLIST_DST"
launchctl load "$PLIST_DST"

echo "✅ LaunchAgent loaded — จะ push อัตโนมัติทุก 5 นาที"
echo ""

# ทดสอบ push ทันที
echo "🔄 ทดสอบ push ตอนนี้เลย..."
/bin/bash "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/wibwub_auto_push.sh"
echo "✅ เสร็จแล้ว — ตั้งแต่นี้ push อัตโนมัติ 100% ทุก 5 นาที!"
echo ""
echo "กด Enter เพื่อปิด"; read
