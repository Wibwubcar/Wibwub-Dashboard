#!/bin/bash
# =========================================================
# WIBWUB Auto-Push Installer
# รันครั้งเดียวจาก Terminal เพื่อติดตั้ง launchd agent
# หลังจากนั้น Mac จะ auto-push ทุกครั้งที่ Claude แก้ไขไฟล์
# =========================================================

REPO_PATH="$HOME/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
SCRIPT_PATH="$HOME/.wibwub_autopush.sh"
PLIST_PATH="$HOME/Library/LaunchAgents/com.wibwub.autopush.plist"
LOG_PATH="$HOME/Library/Logs/wibwub_autopush.log"

echo "📦 ติดตั้ง WIBWUB Auto-Push..."

# ── 1. สร้าง push script ──────────────────────────────────
cat > "$SCRIPT_PATH" << 'PUSH_SCRIPT'
#!/bin/bash
REPO="$HOME/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
LOG="$HOME/Library/Logs/wibwub_autopush.log"

cd "$REPO" || exit 1

# ลบ lock files ถ้ามี (เหลือค้างจาก sandbox)
rm -f .git/index.lock .git/HEAD.lock 2>/dev/null

# เช็คว่ามีไฟล์ที่เปลี่ยนแปลงไหม
git add WIBWUB_Mobile.html \
        WIBWUB_Dashboard.html \
        WIBWUB_Affiliate_Dashboard.html \
        WIBWUB_TikTok_Dashboard_v7.html \
        "data Ads/WIBWUB_Ads_Dashboard.html" \
        "Data Shipnity/Sales_Dashboard.html" \
        sw.js 2>/dev/null

if git diff --cached --quiet; then
    exit 0  # ไม่มีอะไรเปลี่ยน ไม่ต้อง push
fi

# Commit และ push
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git commit -m "auto-push: $TIMESTAMP" >> "$LOG" 2>&1
git push origin main >> "$LOG" 2>&1

if [ $? -eq 0 ]; then
    echo "[$TIMESTAMP] ✓ pushed successfully" >> "$LOG"
else
    echo "[$TIMESTAMP] ✗ push failed" >> "$LOG"
fi
PUSH_SCRIPT

chmod +x "$SCRIPT_PATH"
echo "✓ สร้าง push script แล้ว: $SCRIPT_PATH"

# ── 2. สร้าง launchd plist (รันทุก 3 นาที) ───────────────
cat > "$PLIST_PATH" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.wibwub.autopush</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$SCRIPT_PATH</string>
    </array>

    <key>StartInterval</key>
    <integer>180</integer>

    <key>RunAtLoad</key>
    <false/>

    <key>StandardOutPath</key>
    <string>$LOG_PATH</string>

    <key>StandardErrorPath</key>
    <string>$LOG_PATH</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
        <key>HOME</key>
        <string>$HOME</string>
    </dict>
</dict>
</plist>
PLIST

echo "✓ สร้าง launchd plist แล้ว: $PLIST_PATH"

# ── 3. โหลด launchd agent ─────────────────────────────────
# Unload ก่อนถ้ามีอยู่แล้ว
launchctl unload "$PLIST_PATH" 2>/dev/null

launchctl load "$PLIST_PATH"
if [ $? -eq 0 ]; then
    echo "✓ launchd agent โหลดสำเร็จ"
else
    echo "⚠️  launchctl load ล้มเหลว ลองรัน:"
    echo "    launchctl load $PLIST_PATH"
fi

# ── 4. ทดสอบ push ครั้งแรก ───────────────────────────────
echo ""
echo "🧪 ทดสอบ push ครั้งแรก..."
bash "$SCRIPT_PATH"
if [ $? -eq 0 ]; then
    echo "✅ Auto-push ทำงานได้แล้ว!"
    echo ""
    echo "ตอนนี้ทุกครั้งที่ Claude อัปเดตไฟล์ Mac จะ push GitHub ภายใน 3 นาทีโดยอัตโนมัติ"
    echo "ดู log ได้ที่: $LOG_PATH"
else
    echo "⚠️  ไม่มีไฟล์ที่ต้องการ push ในตอนนี้ (ปกติถ้าไม่มีการเปลี่ยนแปลง)"
fi

echo ""
echo "📋 คำสั่งที่มีประโยชน์:"
echo "  ดู status:  launchctl list | grep wibwub"
echo "  ดู log:     tail -f ~/Library/Logs/wibwub_autopush.log"
echo "  หยุดชั่วคราว: launchctl unload $PLIST_PATH"
echo "  เปิดใหม่:   launchctl load $PLIST_PATH"
