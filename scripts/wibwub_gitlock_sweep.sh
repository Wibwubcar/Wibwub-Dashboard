#!/bin/bash
# WIBWUB — กวาด .git lock ค้าง (LaunchAgent com.wibwub.gitlock · ทุก 60 วินาที)
#
# ทำไมต้องมี (28 ต.ค. 69):
#   งานตั้งเวลาฝั่ง local รันในแซนด์บ็อกซ์ที่ **สร้างไฟล์ในรีโปได้ แต่ลบไม่ได้**
#   git จึงสร้าง HEAD.lock / index.lock แล้วลบคืนไม่ได้ตอนจบ — หลักฐานจาก audit.jsonl:
#     warning: unable to unlink '.git/objects/d2/tmp_obj_h41dHa': Operation not permitted
#   lock ที่ค้างบล็อก commit ของ **ทุกงาน** ที่มาทีหลัง
#   ตัวกวาดใน wibwub_auto_push.sh ใช้ -mmin +10 และรันทุก 5 นาที = ค้างได้ถึง ~15 นาที
#   ตัวนี้จึงแยกออกมาเป็น job เล็กของตัวเอง ทุก 1 นาที ลด window เหลือ ~3 นาที
#
# ความปลอดภัย: ลบต่อเมื่อ **ไม่มี process ชื่อ git ทำงานอยู่** และ lock เก่าเกิน 2 นาที
#   (git ในรีโปนี้ทำงานเสร็จใน < 5 วินาที) · ไม่แตะ working tree ไม่ fetch ไม่ push
REPO="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
LOG="$REPO/scripts/auto_push.log"

[ -d "$REPO/.git" ] || exit 0
pgrep -x git >/dev/null 2>&1 && exit 0        # มี git ทำงานอยู่ — ไม่แตะอะไรเลย

N=$(/usr/bin/find "$REPO/.git" -name '*.lock' -mmin +2 2>/dev/null | wc -l | tr -d ' ')
if [ "$N" -gt 0 ]; then
  /usr/bin/find "$REPO/.git" -name '*.lock' -mmin +2 -delete 2>/dev/null
  echo "$(date '+%Y-%m-%d %H:%M') 🔓 gitlock: ลบ lock ค้าง $N ไฟล์" >> "$LOG"
fi

# เศษ tmp_obj_* จากสาเหตุเดียวกัน — ไม่บล็อกงาน แต่โตวันละ ~105 ไฟล์
T=$(/usr/bin/find "$REPO/.git/objects" -name 'tmp_obj_*' -mmin +60 2>/dev/null | wc -l | tr -d ' ')
if [ "$T" -gt 0 ]; then
  /usr/bin/find "$REPO/.git/objects" -name 'tmp_obj_*' -mmin +60 -delete 2>/dev/null
  echo "$(date '+%Y-%m-%d %H:%M') 🧹 gitlock: กวาดเศษ tmp_obj_* $T ไฟล์" >> "$LOG"
fi
exit 0
