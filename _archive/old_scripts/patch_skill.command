#!/bin/bash
# patch_skill.command — เพิ่ม ผิดพลาด #7-#11 ใน update-wibwub SKILL.md
# double-click เพื่อรัน

SKILL="/var/folders/rp/gcgj8vnn68n9v7flmfth963c0000gn/T/claude-hostloop-plugins/967f28441b6e2074/skills/update-wibwub/SKILL.md"

# ตรวจว่าไฟล์มีอยู่
if [ ! -f "$SKILL" ]; then
  echo "❌ ไม่พบไฟล์: $SKILL"
  read -p "กด Enter เพื่อปิด..."
  exit 1
fi

# ตรวจว่าเคย patch แล้วหรือยัง
if grep -q "ผิดพลาด #7" "$SKILL"; then
  echo "✅ ไฟล์ patch แล้ว (ผิดพลาด #7 มีอยู่แล้ว) ไม่ต้องทำซ้ำ"
  read -p "กด Enter เพื่อปิด..."
  exit 0
fi

# เนื้อหาที่จะแทรก (หลัง ผิดพลาด #6 ก่อน "## Official Data Sources")
NEW_CONTENT='
### ผิดพลาด #7: Sales arrays มี 9 elements แต่ M5 มีแค่ 5 labels — root cause ของ data มั่ว
**อาการ:** Dashboard แสดงยอดเดือนกันยา-มกรา แทนที่จะเป็น ม.ค.-พ.ค. เพราะ labels มีแค่ 5 แต่ arrays มี 9
**สาเหตุ:** wibwub_update.py ไม่ได้ filter เฉพาะปีปัจจุบัน ทำให้ `available` รวมทุกเดือนตั้งแต่ Sep 2025
**แก้ใน wibwub_update.py:** เพิ่ม `current_yr = datetime.now().year % 100` แล้ว filter:
```python
available = [m for m in ALL_MONTHS if m in sh_data and m.endswith(f"/{current_yr}")]
```
**แก้ใน Dashboard/Mobile:** ตัด arrays ให้เหลือแค่ค่า Jan–May 2026 (5 ตัวสุดท้าย)
กฎ: จำนวน elements ใน arrays ต้องเท่ากับจำนวน labels ใน M5 เสมอ

### ผิดพลาด #8: wibwub_update.py อัปเดต M4 แทน M5
wibwub_update.py ใช้ variable `M4` ผิด ต้องเปลี่ยนเป็น `M5` ทุกจุด
ตรวจก่อนรันทุกครั้งว่า `const M5 = {` อยู่ใน Dashboard และ script อัปเดต M5 ไม่ใช่ M4

### ผิดพลาด #9: TK_CANCEL_PCT ไม่ใช่ cancel% ของ TikTok — ห้ามใส่ใน SALES_ARRS
TikTok Sheet col 5 = Gross GMV (ตัวเลขใหญ่มาก ~1.5M) ไม่ใช่ cancel%
ใน wibwub_update.py ห้ามมี `TK_CANCEL_PCT` ใน SALES_ARRS เด็ดขาด
Mobile ใช้ `SH_CANCEL` (array แยก = Shopee cancel% จริงๆ) ส่วน Dashboard ใช้ `SH_CANCEL_PCT` = cost% จาก col 5

### ผิดพลาด #10: Shipnity ไฟล์ใหม่ format เปลี่ยนเป็น order-level — ใช้ Top Products ไม่ได้
ไฟล์เก่า (Data_มกราคม, Data_15-05-2026/กุมภา, Data-มีนา, Data_เมษา): product-level = มีชื่อสินค้า ใช้ aggregate Top Products ได้
ไฟล์ใหม่ (Data_พฤษภา, Data_18-05-2026, Data_กุมภา2, Data_01-06-2026 และหลังจากนี้): order-level = ไม่มีชื่อสินค้า ใช้ Top Products ไม่ได้
ถ้า col[1] ว่างเปล่าหรือเป็น numeric ID = order-level → ข้ามไฟล์นั้นสำหรับ Top Products

### ผิดพลาด #11: git push จาก bash sandbox ล้มเหลว (HTTP 403 proxy)
bash sandbox route GitHub HTTPS ผ่าน proxy ที่ block outbound → ได้รับ "HTTP 403 from proxy after CONNECT"
ห้ามเสียเวลา config proxy หรือ SSH ใน sandbox
**วิธีแก้:** สร้าง `push_now.command` ใน workspace แล้วให้ user double-click รันบนเครื่องจริง:
```bash
#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-.../All"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
```
'

# แทรกเนื้อหาก่อนบรรทัด "## Official Data Sources"
python3 - "$SKILL" "$NEW_CONTENT" << 'PYEOF'
import sys

skill_path = sys.argv[1]
new_content = sys.argv[2]

with open(skill_path, 'r', encoding='utf-8') as f:
    content = f.read()

# แทรกหลัง ผิดพลาด #6 block (หลัง "---\n\n## Official Data Sources")
# หา marker แทรกก่อน "## Official Data Sources"
marker = '\n---\n\n## Official Data Sources'
if marker not in content:
    print("❌ ไม่พบ marker '## Official Data Sources' ในไฟล์")
    sys.exit(1)

updated = content.replace(marker, new_content + '\n---\n\n## Official Data Sources', 1)

with open(skill_path, 'w', encoding='utf-8') as f:
    f.write(updated)

print("✅ เพิ่ม ผิดพลาด #7-#11 สำเร็จ!")
PYEOF

read -p "กด Enter เพื่อปิด..."
