#!/bin/bash
# WIBWUB Auto Push — รันโดย LaunchAgent ทุก 5 นาที (macOS จริง ไม่ติด proxy)
REPO="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

cd "$REPO" || exit 0

# ลบ stale locks ถ้ามี
find .git -name "*.lock" -mmin +10 -delete 2>/dev/null || true

# sync กับ remote ก่อนเช็ค unpushed (เผื่อ remote มี commit ใหม่ที่ local ไม่มี เช่น push จากเครื่องอื่น/แก้ผ่าน GitHub web)
git fetch origin main >> "$REPO/scripts/auto_push.log" 2>&1

# เช็คว่ามี commit ที่ยังไม่ push หรือไม่
UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
if [ "$UNPUSHED" -gt "0" ]; then
  # ถ้า local ตามหลัง remote ด้วย (diverged) ต้อง pull/merge ก่อน ไม่งั้น push จะถูก reject วนไปเรื่อยๆ
  BEHIND=$(git log HEAD..origin/main --oneline 2>/dev/null | wc -l | tr -d ' ')
  if [ "$BEHIND" -gt "0" ]; then
    git pull --no-edit origin main >> "$REPO/scripts/auto_push.log" 2>&1
    if [ $? -ne 0 ]; then
      echo "$(date '+%Y-%m-%d %H:%M') ⚠️ pull failed (conflict?) — skipping push, needs manual fix" >> "$REPO/scripts/auto_push.log"
      exit 0
    fi
  fi
  git push origin main >> "$REPO/scripts/auto_push.log" 2>&1
  echo "$(date '+%Y-%m-%d %H:%M') pushed $UNPUSHED commits" >> "$REPO/scripts/auto_push.log"
fi
