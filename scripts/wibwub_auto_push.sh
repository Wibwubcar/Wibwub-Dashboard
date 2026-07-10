#!/bin/bash
# WIBWUB Auto Push — รันโดย LaunchAgent ทุก 5 นาที (macOS จริง ไม่ติด proxy)
REPO="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

cd "$REPO" || exit 0

# ลบ stale locks ถ้ามี
find .git -name "*.lock" -mmin +10 -delete 2>/dev/null || true

# เช็คว่ามี commit ที่ยังไม่ push หรือไม่
UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
if [ "$UNPUSHED" -gt "0" ]; then
  git push origin main >> "$REPO/scripts/auto_push.log" 2>&1
  echo "$(date '+%Y-%m-%d %H:%M') pushed $UNPUSHED commits" >> "$REPO/scripts/auto_push.log"
fi
