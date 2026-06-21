#!/bin/bash
# WIBWUB Auto-Push Script v2
# Push commits ที่ Claude ทำไว้ใน sandbox ขึ้น GitHub อัตโนมัติ
# รันทุก 2 นาทีผ่าน LaunchAgent

REPO="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
LOG="$HOME/Library/Logs/wibwub_autopush.log"

cd "$REPO" || { echo "[$(date)] ERROR: Cannot cd to repo" >> "$LOG"; exit 1; }

# ลบ lock files ถ้ามี
rm -f .git/index.lock .git/HEAD.lock 2>/dev/null

# เช็คว่ามี commits ที่ยังไม่ได้ push ไหม
UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')

if [ "$UNPUSHED" = "0" ]; then
  exit 0  # ไม่มี commit ค้าง ไม่ต้องทำอะไร
fi

echo "[$(date)] พบ ${UNPUSHED} commit(s) ที่ยังไม่ได้ push" >> "$LOG"

# Push
git push origin main 2>> "$LOG" && \
  echo "[$(date)] ✅ Push สำเร็จ (${UNPUSHED} commits)" >> "$LOG" || \
  echo "[$(date)] ❌ Push ล้มเหลว" >> "$LOG"
