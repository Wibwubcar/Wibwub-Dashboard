#!/bin/bash
OUT="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/diag_output.txt"
{
echo "===== launchctl list (wibwub/shipnity) ====="
launchctl list | grep -i "wibwub\|shipnity"
echo ""
echo "===== ~/Library/LaunchAgents ====="
ls -la ~/Library/LaunchAgents/ 2>&1
echo ""
echo "===== LaunchAgents plist contents (wibwub/shipnity related) ====="
for f in ~/Library/LaunchAgents/*.plist; do
  if grep -qi "wibwub\|shipnity\|stock" "$f" 2>/dev/null; then
    echo "--- $f ---"
    cat "$f"
    echo ""
  fi
done
echo "===== crontab -l ====="
crontab -l 2>&1
echo ""
echo "===== find home for shipnity/stock fetch scripts ====="
find ~ -maxdepth 4 -iname "*shipnity*" 2>/dev/null | grep -v "Library/CloudStorage"
find ~ -maxdepth 4 -iname "*stock*fetch*" -o -iname "*fetch*stock*" 2>/dev/null | grep -v "Library/CloudStorage"
echo ""
echo "===== Automator / Shortcuts related ====="
find ~ -maxdepth 5 -iname "*.workflow" 2>/dev/null
echo ""
echo "DONE"
} > "$OUT" 2>&1
echo "เขียนผลลัพธ์ไว้ที่ diag_output.txt แล้ว กด Enter เพื่อปิด"
read
