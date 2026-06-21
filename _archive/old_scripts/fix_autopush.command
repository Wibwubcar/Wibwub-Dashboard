#!/bin/bash
# fix_autopush.command — ดับเบิลคลิกครั้งเดียว แก้ auto-push ทำงานได้เลย

REPO="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
SCRIPT="$HOME/.wibwub_autopush.sh"
PLIST="$HOME/Library/LaunchAgents/com.wibwub.autopush.plist"
LOG="$HOME/Library/Logs/wibwub_autopush.log"

echo "🔧 แก้ WIBWUB Auto-Push..."

# ── 1. สร้าง script ที่ LOCAL path (ไม่ใช่ Google Drive) ──────
cat > "$SCRIPT" << 'PUSH_SCRIPT'
#!/bin/bash
REPO="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
LOG="$HOME/Library/Logs/wibwub_autopush.log"

cd "$REPO" || { echo "[$(date)] ERROR: cd failed" >> "$LOG"; exit 1; }
rm -f .git/index.lock .git/HEAD.lock 2>/dev/null

git add \
  WIBWUB_Mobile.html \
  WIBWUB_Dashboard.html \
  WIBWUB_Affiliate_Dashboard.html \
  WIBWUB_TikTok_Dashboard_v7.html \
  "data Ads/WIBWUB_Ads_Dashboard.html" \
  "Data Shipnity/Sales_Dashboard.html" \
  sw.js 2>/dev/null

if git diff --cached --quiet; then
  exit 0
fi

TS=$(date '+%Y-%m-%d %H:%M')
git commit -m "auto: $TS" >> "$LOG" 2>&1
git push origin main >> "$LOG" 2>&1 && \
  echo "[$TS] ✅ pushed OK" >> "$LOG" || \
  echo "[$TS] ❌ push failed" >> "$LOG"
PUSH_SCRIPT

chmod +x "$SCRIPT"
echo "✓ Script ย้ายไปที่ ~/.wibwub_autopush.sh แล้ว"

# ── 2. อัปเดต LaunchAgent plist ชี้ไปที่ local script ────────
launchctl unload "$PLIST" 2>/dev/null

cat > "$PLIST" << PLIST_END
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.wibwub.autopush</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$SCRIPT</string>
  </array>
  <key>StartInterval</key>
  <integer>180</integer>
  <key>RunAtLoad</key>
  <false/>
  <key>StandardOutPath</key>
  <string>$LOG</string>
  <key>StandardErrorPath</key>
  <string>$LOG</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
    <key>HOME</key>
    <string>$HOME</string>
  </dict>
</dict>
</plist>
PLIST_END

launchctl load "$PLIST"
echo "✓ LaunchAgent โหลดใหม่แล้ว (รันทุก 3 นาที)"

# ── 3. Push งานที่ค้างทันที ────────────────────────────────────
echo ""
echo "📤 Push งานที่ค้างทันที..."
cd "$REPO"
rm -f .git/index.lock .git/HEAD.lock 2>/dev/null

git add \
  WIBWUB_Mobile.html \
  WIBWUB_Dashboard.html \
  "data Ads/WIBWUB_Ads_Dashboard.html" \
  "Data Shipnity/Sales_Dashboard.html" \
  sw.js

if git diff --cached --quiet; then
  echo "✓ ไม่มีอะไรค้าง (pushed แล้ว)"
else
  git commit -m "fix: Sales_Dashboard full rebuild Jan–May 2026 + sw.js v94

- rebuilt all_lines: 103,339 lines (was 32,097)
- Jan/Mar/Apr revenue: price*qty, ฿9M not ฿31M
- added order_id 'o' field; fixed total_orders count
- added Feb 2026 data (12,322 lines, ฿7.5M)
- May: full Data_01-06-2026.xlsx (17,733 lines, 1-31 May)
- pickerLeftMonth: opens May not June
- sw.js v94"
  git push origin main && echo "✅ Push สำเร็จ!" || echo "❌ Push ล้มเหลว — เช็ค GitHub credentials"
fi

echo ""
echo "✅ เสร็จ! Auto-push จะทำงานทุก 3 นาทีโดยอัตโนมัติ"
echo "ดู log: tail -f ~/Library/Logs/wibwub_autopush.log"
echo ""
read -p "กด Enter เพื่อปิด..."
