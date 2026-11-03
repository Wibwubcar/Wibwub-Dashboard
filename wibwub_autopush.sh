#!/bin/bash
# WIBWUB Auto-Push Script v2
# Push commits ที่ Claude ทำไว้ใน sandbox ขึ้น GitHub อัตโนมัติ
# รันทุก 2 นาทีผ่าน LaunchAgent

REPO="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
LOG="$HOME/Library/Logs/wibwub_autopush.log"

cd "$REPO" || { echo "[$(date)] ERROR: Cannot cd to repo" >> "$LOG"; exit 1; }

# ลบ lock ที่ค้างจริงเท่านั้น — ยกด่าน 2 ชั้นจาก scripts/wibwub_gitlock_sweep.sh (3 พ.ย. 69)
#
# ของเดิมเป็น `rm -f .git/index.lock .git/HEAD.lock` ทุก 120 วินาทีโดยไม่เช็คอะไรเลย
# ถ้างานตั้งเวลาตัวไหนกำลัง git commit อยู่พอดี มันจะลบ lock ของโปรเซสที่ยังมีชีวิต
# → index เสียหาย / commit ของ 2 งานทับกันแบบหาสาเหตุไม่เจอ
#
# ด่าน 1: มีโปรเซส git ทำงานอยู่ = ไม่แตะอะไรเลย ข้ามทั้งรอบ (push รอบถัดไป ช้าสุด +2 นาที)
# ด่าน 2: ลบเฉพาะ lock ที่เก่ากว่า 2 นาที (git ในรีโปนี้ทำงานเสร็จใน < 5 วินาที)
# lock ที่ค้างจริงยังมี gitlock (ทุก 60 วินาที) กวาดให้อีกทางอยู่แล้ว
if pgrep -x git >/dev/null 2>&1; then
  exit 0
fi
/usr/bin/find .git -maxdepth 1 \( -name index.lock -o -name HEAD.lock \) -mmin +2 -delete 2>/dev/null

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
