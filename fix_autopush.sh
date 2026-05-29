#!/bin/bash
# WIBWUB Auto-Push + Self-Healing Watchdog Setup
# รัน 1 ครั้ง: bash fix_autopush.sh
# หลังจากนั้น watchdog จะดูแลตัวเองอัตโนมัติ

set -e

FOLDER="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
AUTOPUSH_SCRIPT="$HOME/.wibwub_autopush.sh"
WATCHDOG_SCRIPT="$HOME/.wibwub_watchdog.sh"
AUTOPUSH_PLIST="$HOME/Library/LaunchAgents/com.wibwub.autopush.plist"
WATCHDOG_PLIST="$HOME/Library/LaunchAgents/com.wibwub.watchdog.plist"
AUTOPUSH_LABEL="com.wibwub.autopush"
WATCHDOG_LABEL="com.wibwub.watchdog"

echo "╔══════════════════════════════════════════╗"
echo "║   WIBWUB Auto-Push Self-Healing Setup    ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── 1. สร้าง autopush script ─────────────────────────────────────
python3 - "$FOLDER" "$AUTOPUSH_SCRIPT" << 'PYEOF'
import sys
folder, path = sys.argv[1], sys.argv[2]
content = f"""#!/bin/bash
FOLDER="{folder}"
cd "$FOLDER"
rm -f .git/index.lock .git/HEAD.lock
git add *.html "Data Shipnity/Sales_Dashboard.html" "data Ads/WIBWUB_Ads_Dashboard.html" sw.js
if ! git diff --cached --quiet; then
    git commit -m "auto: $(date '+%Y-%m-%d %H:%M')"
    git push origin main
    echo "$(date '+%Y-%m-%d %H:%M:%S'): ✅ pushed" >> /tmp/wibwub_autopush.log
else
    echo "$(date '+%Y-%m-%d %H:%M:%S'): — no changes" >> /tmp/wibwub_autopush.log
fi
"""
open(path, 'w').write(content)
print(f"  ✓ autopush script: {path}")
PYEOF
chmod +x "$AUTOPUSH_SCRIPT"

# ── 2. สร้าง watchdog script ─────────────────────────────────────
# watchdog ทำ 3 อย่าง:
#   A. ตรวจว่า autopush plist มีอยู่ ถ้าไม่มีให้ re-run fix_autopush.sh
#   B. ตรวจว่า launchd job loaded อยู่ ถ้าไม่ให้ reload
#   C. log สถานะไว้
python3 - "$FOLDER" "$WATCHDOG_SCRIPT" "$AUTOPUSH_PLIST" "$AUTOPUSH_LABEL" "$AUTOPUSH_SCRIPT" << 'PYEOF'
import sys
folder, wdog_path, autopush_plist, autopush_label, autopush_script = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
fix_script = f"{folder}/fix_autopush.sh"
content = f"""#!/bin/bash
# WIBWUB Watchdog — self-healing for autopush
AUTOPUSH_PLIST="{autopush_plist}"
AUTOPUSH_LABEL="{autopush_label}"
AUTOPUSH_SCRIPT="{autopush_script}"
FIX_SCRIPT="{fix_script}"
LOG="/tmp/wibwub_watchdog.log"

needs_fix=0

# ── A. ตรวจว่า plist ไฟล์มีอยู่ไหม
if [ ! -f "$AUTOPUSH_PLIST" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S'): ⚠️  plist หาย — กำลัง reinstall..." >> "$LOG"
    needs_fix=1
fi

# ── B. ตรวจว่า launchd job loaded อยู่ไหม
if ! launchctl list 2>/dev/null | grep -q "$AUTOPUSH_LABEL"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S'): ⚠️  job หลุดจาก launchd — กำลัง reload..." >> "$LOG"
    needs_fix=1
fi

# ── C. ถ้าต้องแก้ไข
if [ "$needs_fix" -eq 1 ]; then
    if [ -f "$FIX_SCRIPT" ]; then
        bash "$FIX_SCRIPT" >> "$LOG" 2>&1
        echo "$(date '+%Y-%m-%d %H:%M:%S'): ✅ fix_autopush.sh รันสำเร็จ — autopush กลับมาแล้ว" >> "$LOG"
    else
        # plist หาย ไม่มี fix script ให้ rebuild plist โดยตรง
        launchctl unload "$AUTOPUSH_PLIST" 2>/dev/null || true
        launchctl load "$AUTOPUSH_PLIST" 2>/dev/null || true
        echo "$(date '+%Y-%m-%d %H:%M:%S'): ✅ reload plist โดยตรง" >> "$LOG"
    fi
else
    echo "$(date '+%Y-%m-%d %H:%M:%S'): ✓ autopush ปกติ" >> "$LOG"
fi

# ── D. จำกัดขนาด log ไม่เกิน 500 บรรทัด
if [ -f "$LOG" ]; then
    tail -500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi
"""
open(wdog_path, 'w').write(content)
print(f"  ✓ watchdog script: {wdog_path}")
PYEOF
chmod +x "$WATCHDOG_SCRIPT"

# ── 3. สร้าง autopush plist ──────────────────────────────────────
python3 - "$AUTOPUSH_SCRIPT" "$AUTOPUSH_PLIST" "$AUTOPUSH_LABEL" << 'PYEOF'
import sys
script, plist, label = sys.argv[1], sys.argv[2], sys.argv[3]
content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{label}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>{script}</string>
  </array>
  <key>StartInterval</key>
  <integer>180</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <false/>
  <key>StandardOutPath</key>
  <string>/tmp/wibwub_autopush.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/wibwub_autopush.log</string>
</dict>
</plist>
"""
open(plist, 'w').write(content)
print(f"  ✓ autopush plist: {plist}")
PYEOF

# ── 4. สร้าง watchdog plist ──────────────────────────────────────
python3 - "$WATCHDOG_SCRIPT" "$WATCHDOG_PLIST" "$WATCHDOG_LABEL" << 'PYEOF'
import sys
script, plist, label = sys.argv[1], sys.argv[2], sys.argv[3]
content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{label}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>{script}</string>
  </array>
  <key>StartInterval</key>
  <integer>300</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <false/>
  <key>StandardOutPath</key>
  <string>/tmp/wibwub_watchdog.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/wibwub_watchdog.log</string>
</dict>
</plist>
"""
open(plist, 'w').write(content)
print(f"  ✓ watchdog plist: {plist}")
PYEOF

# ── 5. Fix permissions ───────────────────────────────────────────
chmod 644 "$AUTOPUSH_PLIST"
chmod 644 "$WATCHDOG_PLIST"

# ── 6. Unload & reload launchd jobs ─────────────────────────────
echo ""
echo "กำลัง load launchd jobs..."
launchctl unload "$AUTOPUSH_PLIST" 2>/dev/null || true
launchctl unload "$WATCHDOG_PLIST" 2>/dev/null || true
sleep 1
launchctl load "$AUTOPUSH_PLIST"
echo "  ✓ autopush loaded (ทุก 3 นาที)"
launchctl load "$WATCHDOG_PLIST"
echo "  ✓ watchdog loaded (ทุก 5 นาที)"

# ── 7. Push ครั้งแรกทันที ────────────────────────────────────────
echo ""
echo "── กำลัง push ครั้งแรก ──"
bash "$AUTOPUSH_SCRIPT"
echo "── เสร็จแล้ว ──"

# ── 8. แสดงสถานะ ─────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   ✅ Setup เสร็จสมบูรณ์                  ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "สถานะ launchd:"
launchctl list | grep wibwub || echo "  (ยังไม่เห็น — ลอง run อีกครั้ง)"
echo ""
echo "Logs:"
echo "  Auto-push : cat /tmp/wibwub_autopush.log"
echo "  Watchdog  : cat /tmp/wibwub_watchdog.log"
echo ""
echo "ระบบจะทำงานอัตโนมัติ:"
echo "  • autopush ทุก 3 นาที (push ถ้ามีการเปลี่ยนแปลง)"
echo "  • watchdog ทุก 5 นาที (ตรวจ + restart ถ้า autopush หลุด)"
echo "  • ทั้งสองอย่าง auto-start ทุกครั้งที่ login เข้า Mac"
