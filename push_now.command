#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
# ย้าย lock ค้างแทนการลบ (กฎเดิมของรีโปนี้) — เช็คก่อนว่าไม่มี git ทำงานอยู่จริง
if pgrep -f "[g]it " >/dev/null; then echo "มี git ทำงานอยู่ — ห้ามแตะ lock รอให้จบก่อน"; else
  for f in index.lock HEAD.lock objects/maintenance.lock; do
    [ -e ".git/$f" ] && mv ".git/$f" ".git/stale-$(date +%s)-$(basename "$f")"
  done
fi
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
