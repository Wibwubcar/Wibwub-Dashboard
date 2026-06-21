#!/bin/bash
cd "$(dirname "$0")"
rm -f .git/index.lock .git/HEAD.lock
echo "กำลัง push ขึ้น GitHub..."
git push origin main && echo "✅ Push สำเร็จ!" || echo "❌ Push ล้มเหลว ตรวจสอบ token"
