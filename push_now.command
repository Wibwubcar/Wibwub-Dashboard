#!/bin/bash
# WIBWUB — push commits made by the Cowork sandbox (regenerated 30.08.69 รอบเย็น — commit 44ffce0)
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

# สร้าง commit ในแซนด์บ็อกซ์ทิ้ง lock/tmp ไว้ — ลบก่อน
rm -f .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock
find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null

# index ของเครื่องอาจค้าง (sandbox ใช้ GIT_INDEX_FILE แยก) — รีเฟรชให้ตรงกับ HEAD
git reset --mixed >/dev/null 2>&1

# ไฟล์แดชบอร์ดหลักที่ยังค้างใน working tree (แซนด์บ็อกซ์คอมมิตไม่ได้เพราะ index.lock)
DASH_FILES="WIBWUB_Dashboard.html WIBWUB_Mobile.html WIBWUB_Affiliate_Dashboard.html WIBWUB_TikTok_Dashboard_v7.html Procurement_Dashboard.html WIBWUB_Platform_Analytics.html WIBWUB_FastMoss_Competitor_Dashboard.html sw.js"
# ไฟล์ที่มีช่องว่างในพาธ — เก็บใน array แยก (word-split ไม่ได้)
EXTRA_FILES=("Data Shipnity/stock/stock_snapshot.json")
PENDING=()
for f in $DASH_FILES; do
  [ -f "$f" ] && ! git diff --quiet -- "$f" && PENDING+=("$f")
done
for f in "${EXTRA_FILES[@]}"; do
  [ -f "$f" ] && ! git diff --quiet -- "$f" && PENDING+=("$f")
done
if [ ${#PENDING[@]} -gt 0 ]; then
  echo "▶ พบไฟล์ที่ยังไม่ commit: ${PENDING[*]}"
  git add "${PENDING[@]}"
  git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
      commit -m "auto: commit pending dashboard changes $(date +%Y-%m-%d)" >/dev/null 2>&1 \
      && echo "✅ commit เพิ่มแล้ว"
fi

echo "▶ commit ล่าสุด: $(git log -1 --oneline)"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
echo ""
read -n 1 -s -r -p "กด Enter เพื่อปิดหน้าต่าง..."
