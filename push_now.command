#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

# ลบ lock ค้างจาก sandbox (sandbox ลบเองไม่ได้ — Operation not permitted บน Google Drive mount)
rm -f .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock
rm -f .git/objects/*/tmp_obj_* 2>/dev/null

git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
echo ""
echo "กด Enter เพื่อปิดหน้าต่าง..."
read
