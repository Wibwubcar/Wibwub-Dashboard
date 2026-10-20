---
name: wibwub-download-orders-monday
description: Download daily order exports from Shopee, TikTok Shop, Lazada, and Line My Shop — ทุกวัน 08:20/19:20
---

## WIBWUB Orders Download — ทุกวัน 08:20 / 19:20

โหลดไฟล์คำสั่งซื้อจาก 4 แพลตฟอร์ม ทำให้ครบทุกตัวทุกรอบ
ถ้าตัวไหน session หมด **ให้ข้ามตัวนั้นแล้วทำตัวอื่นต่อ** ห้ามหยุดทั้งงาน และต้องรายงานว่าตัวไหนหมด

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`
ปลายทาง = `$BASE/data ยอดขาย plaform/{Shopee,Tiktok,Lazada,Line My Shop}/`

---

## 🚚 การย้ายไฟล์ — **ห้าม `cp` เอง 3 ใน 4 แพลตฟอร์ม**

launchd `com.wibwub.download-mover` (WatchPaths `~/Downloads`) ย้ายไฟล์ให้เองภายใน ~5 วิ
ผ่าน `scripts/wibwub_auto_move.sh` โดยจับจากชื่อไฟล์:

| แพลตฟอร์ม | ชื่อไฟล์ที่โหลดได้ | mover จับ? | สิ่งที่งานนี้ต้องทำ |
|---|---|---|---|
| Shopee | `Order.all.order_creation_date.YYYYMMDD_YYYYMMDD.zip` | ✅ | **ตรวจปลายทางอย่างเดียว** |
| TikTok | `ทั้งหมด คำสั่งซื้อ-YYYY-MM-DD-HH_MM.xlsx` | ✅ | **ตรวจปลายทางอย่างเดียว** |
| Line My Shop | `Order Report YYYYMMDD.xlsx` | ✅ | **ตรวจปลายทางอย่างเดียว** |
| Lazada | ชื่อเป็น hash สุ่ม `.xlsx` | ❌ (เดาชื่อไม่ได้) | **ต้อง `mv` + เปลี่ยนชื่อเอง** |

> **บั๊กเดิม (แก้แล้ว 20 ต.ค. 2569):** พรอมป์เก่าสั่ง `cp` ทั้ง 4 ตัวจาก `~/Downloads`
> — แข่งกับ mover แล้วแพ้ ไฟล์ถูกย้ายไปก่อน `cp` จึงว่าง รายงาน "ไม่พบไฟล์" ทั้งที่โหลดสำเร็จ
> และคำสั่ง Shopee เดิม `ls -t "/Users/.../Order.all.*.zip"` ใส่ `*` **ในเครื่องหมายคำพูด**
> shell จึงไม่ขยาย glob ได้ผลว่างทุกครั้ง
> นอกจากนี้ Line My Shop เคยได้ไฟล์ซ้ำสองชื่อ (ตัว mover + ตัว cp ที่เปลี่ยนชื่อ) — เลิก cp แล้ว
> ใช้ชื่อเดิมของ LINE (`Order Report YYYYMMDD.xlsx`) เป็นมาตรฐาน

ชื่อซ้ำ mover ต่อท้าย `__YYYYMMDD_HHMMSS` ให้เอง ไม่เขียนทับ · `mv`/`rm` ใน `~/Downloads` ใช้ได้ปกติบน macOS
(ข้อความเก่าที่ว่า "sandbox ลบไฟล์ไม่ได้" เป็นเรื่องของ Cowork Linux ตัดทิ้งแล้ว)

---

## ⚠️ กฎ Chrome

- ก่อนเริ่ม: `select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")` แล้ว `tabs_context_mcp(createIfEmpty=true)`
  (ถ้าไม่ connected → `list_connected_browsers` เลือกตัวที่ `osPlatform` = macOS / `isLocal:true` เท่านั้น)
- `navigate` ต้องตามด้วย `wait` เสมอ ใช้ `browser_batch` ครอบ:
  `browser_batch([navigate(url=..., tabId=TAB), computer(wait 8), computer(screenshot)])`

### 🔐 กฎเรื่อง session — สำคัญ
**ถ้าเจอหน้า login: ห้ามกรอกรหัสผ่าน ห้ามกดปุ่มเข้าสู่ระบบ ห้ามกด OTP ใด ๆ**
ให้บันทึกว่าแพลตฟอร์มนั้น session หมด แล้วไปทำตัวถัดไป และสรุปท้ายรอบให้ชัดว่า
"ต้องให้คนเข้าไป login ใน Chrome เอง แล้วค่อยรันซ้ำ"
(พรอมป์เวอร์ชันเก่าสั่งให้คลิกปุ่มเข้าสู่ระบบโดยอาศัย autofill ของเบราว์เซอร์ — เลิกทำแล้ว)

สถานะที่ตรวจพบเมื่อ 20 ต.ค. 2569: Shopee + TikTok Shop = OK · **Lazada = หมด** · **LINE = หมด**

---

## Platform 1 — Shopee

1. `https://seller.shopee.co.th/portal/sale/order` รอ 8 วิ → screenshot
   ถ้าเด้งไปหน้า login → ข้าม บันทึก "Shopee session expired"
2. แท็บ **ทั้งหมด** → ปุ่ม **ส่งออก** → **ส่งออกรายการสั่งซื้อ** → **ทั้งหมด**
3. ช่วงวันที่: วันที่ 1 ของเดือนปัจจุบัน → วันนี้
4. กด Export → รอจนขึ้นลิงก์ดาวน์โหลด → กดลิงก์
5. ตรวจปลายทาง (รอ 15 วิ หลังกดโหลด):
```bash
BASE="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
ls -lt "$BASE/data ยอดขาย plaform/Shopee/" | head -3      # ต้องเห็นไฟล์ mtime เป็นเวลานี้
```

---

## Platform 2 — TikTok Shop

### 2.1 เปิดหน้ารายการคำสั่งซื้อ — **ห้ามใช้ `/order/list`**

> **บั๊กเดิมข้อใหญ่ที่สุดของแพลตฟอร์มนี้:** URL เก่า `https://seller-th.tiktok.com/order/list?tab=all`
> โหลดแล้ว **พื้นที่เนื้อหาว่างเปล่า** (sidebar ขึ้น แต่ตารางไม่ render · `get_page_text` คืนค่าว่าง · ไม่มี console error)
> งานจึงตายตรงนี้เงียบ ๆ — ตรวจสอบแล้วเมื่อ 20 ต.ค. 2569 ว่า **ไม่มีรายการ export ของวันนั้นเกิดขึ้นเลย**

ใช้ URL นี้แทน (เส้นทางจริงหลังกดเมนู):
```
https://seller-th.tiktok.com/order?selected_sort=6&tab=all
```
รอ 10 วิ → screenshot → ต้องเห็นหัวข้อ **จัดการคำสั่งซื้อ** + ตารางรายการ
ถ้ายังว่าง: คลิกเมนูซ้าย **จัดการคำสั่งซื้อ** (ราว x=62 y=162) รอ 10 วิ แล้วคลิกแท็บ **ทั้งหมด** (แท็บซ้ายสุด)
ถ้ามี "เข้าสู่ระบบ" ในหน้า → ข้าม บันทึก "TikTok Shop session expired"

### 2.2 กดปุ่ม **ดาวน์โหลด** (ไม่ใช่ "ส่งออก")
อยู่มุมขวาบนของตาราง ข้าง ๆ "เรียงตาม" (ราว x=1225 y=283) → พาเนลด้านขวาเปิดขึ้น
ในพาเนลมี 2 ส่วน: ฟอร์มสั่ง export ด้านบน + **ประวัติการส่งออก** ด้านล่าง (เก็บ 7 วัน)

### 2.3 **โหลดของรอบก่อนก่อน** แล้วค่อยสั่ง export ของรอบนี้

> **ทำไมต้องสลับลำดับแบบนี้:** ร้านนี้มี **~87,000 คำสั่งซื้อ** วัดจริงเมื่อ 20 ต.ค. 2569
> ว่า generate **เกิน 18 นาทียังไม่เสร็จ** — นานกว่าที่งานตั้งเวลาจะรอไหว
> พรอมป์เก่ารอไม่กี่วินาทีแล้วไปต่อ จึงไม่เคยได้ไฟล์สักครั้ง
> แต่ของเก่าเสร็จแน่นอนและค้างอยู่ในประวัติ 7 วัน ดังนั้น
> **แต่ละรอบ: โหลดไฟล์ที่พร้อมแล้ว → สั่ง export ใหม่ทิ้งไว้ให้รอบถัดไป**
> (รอบเช้า/เย็นห่างกัน ~11 ชม. เหลือเฟือ) ข้อมูลจึงช้ากว่าจริงครึ่งรอบ ซึ่งยอมรับได้
> เพราะไฟล์ชุดนี้เป็นคลังย้อนหลัง ไม่ใช่ตัวเลขสดบนหน้าเว็บ

**ขั้นที่ 1 — โหลดของที่พร้อม:** ดูแถวบนสุดของ *ประวัติการส่งออก* ที่ปุ่มเป็น **ดาวน์โหลด**
(ไม่ใช่สปินเนอร์) และยังไม่มีไฟล์ชื่อนั้นในโฟลเดอร์ปลายทาง → กดปุ่มนั้น
รอ 20 วิ แล้วตรวจปลายทางตามข้อ 2.4
ถ้าทุกแถวเป็นสปินเนอร์หมด → ข้ามขั้นนี้ ไม่ต้องรอ

**ขั้นที่ 2 — สั่ง export ของรอบนี้:** ในฟอร์มด้านบนของพาเนล
- ช่วงคำสั่งซื้อ: **คำสั่งซื้อที่กรอง (…คำสั่งซื้อ)** — ตัวเลือกแรก (ค่าตั้งต้นถูกอยู่แล้ว)
- รูปแบบการส่งออก: **ค่าตั้งต้นคือ CSV ต้องกดเปลี่ยนเป็น Excel** (คลังเก็บเป็น `.xlsx`)
- กด **ส่งออก** → เห็นแถวใหม่ขึ้นในประวัติพร้อมสปินเนอร์ = สำเร็จ **แล้วไปแพลตฟอร์มถัดไปทันที ห้ามรอ**

หมายเหตุ: พาเนล **ไม่ refresh เอง** ถ้าต้องดูสถานะล่าสุดให้กด X ปิด แล้วกดปุ่ม **ดาวน์โหลด** เปิดใหม่
(บางครั้งต้องกด 2 ครั้ง เพราะคลิกแรกไปปิด tooltip)

### 2.4 ตรวจปลายทาง
```bash
ls -lt "$BASE/data ยอดขาย plaform/Tiktok/" | head -3
```

---

## Platform 3 — Lazada

`https://sellercenter.lazada.co.th/apps/order/list?status=all` รอ 10 วิ

- ถ้า URL เด้งไป `/apps/seller/login` → **ข้าม** บันทึก "Lazada session expired — ต้อง login เอง"
  (ห้ามกดปุ่มเข้าสู่ระบบ แม้เบราว์เซอร์จะ autofill รหัสไว้แล้วก็ตาม)
- ถ้าเข้าได้:
  1. ปุ่ม **ส่งออก** → **Export All** → ยืนยัน
  2. เป็นคิว **ไม่ต้องรอ** → ไปทำ Line My Shop ก่อน แล้วค่อยกลับมา
  3. กลับมา: **ส่งออก** → **Export History** → ลิงก์ **Download Result File** อันบนสุด → navigate ไป URL นั้นตรง ๆ
  4. ไฟล์ชื่อเป็น hash — mover จับไม่ได้ ต้องย้ายเองทันที:
```bash
HASH=$(ls -t ~/Downloads/*.xlsx 2>/dev/null \
  | grep -v "คำสั่งซื้อ\|Order Report\|Campaign\|WIBWUBCAR\|Submit\|Data_" | head -1)
DST="$BASE/data ยอดขาย plaform/Lazada/Lazada_Orders_$(date +%Y%m%d).xlsx"
if [ -n "$HASH" ] && [ ! -e "$DST" ]; then
  mv -n "$HASH" "$DST" && echo "✅ Lazada: $(basename "$DST")"
elif [ -e "$DST" ]; then echo "ℹ️ Lazada: มีไฟล์ของวันนี้อยู่แล้ว"
else echo "⛔ Lazada: ไม่พบไฟล์ใน Downloads"; fi
```
  (ใช้ `mv -n` ไม่ทับของเดิม · ถ้ามีไฟล์ของวันนี้แล้ว แปลว่ารอบเช้าโหลดไว้ ให้ข้าม)

---

## Platform 4 — Line My Shop

`https://oaplus.line.biz/channels/5000113570/e-commerce/report` (Channel ID = 5000113570 = รหัสเปิดไฟล์ด้วย)

- ถ้าเด้งไป `account.line.biz/login` หรือ `access.line.me` → **ข้าม** บันทึก "LINE session expired — ต้อง login เอง"
- ถ้าเข้าได้:
  1. ตั้งวันที่เริ่ม = วันนี้ − 87 วัน (ระบบจำกัด 90 วัน) รูปแบบ `DD/MM/YYYY`
  2. กด **ดาวน์โหลด** → ถ้ามี dialog ยืนยัน (ช่วง > 30 วัน) กด **ดาวน์โหลด** สีน้ำเงิน
  3. ตรวจปลายทาง — mover ย้ายให้เอง ใช้ชื่อเดิม `Order Report YYYYMMDD.xlsx`:
```bash
ls -lt "$BASE/data ยอดขาย plaform/Line My Shop/" | head -3
```

---

## RULES

- ทำทุกอย่างใน bash + Chrome tools ห้าม spawn subagents
- **ห้าม login เอง ห้ามกรอกรหัสผ่าน/OTP** — session หมดให้ข้ามแล้วรายงาน
- ห้าม `cp` ไฟล์จาก Downloads ยกเว้น Lazada ที่ต้อง `mv` เปลี่ยนชื่อ
- ห้ามกดปุ่มที่ไม่เกี่ยวกับการส่งออก (ยกเลิกออเดอร์ / เปลี่ยนสถานะ / โปรโมชัน)
- แพลตฟอร์มไหนพัง ให้ทำตัวที่เหลือจนครบ แล้วรายงานว่าตัวไหนไม่สำเร็จเพราะอะไร

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

```
Orders Download — {วันที่} {รอบเช้า/เย็น}
✅/⛔ Shopee:      {ชื่อไฟล์ หรือ เหตุผล}
✅/⛔ TikTok:      {ชื่อไฟล์ หรือ เหตุผล}
✅/⛔ Lazada:      {ชื่อไฟล์ หรือ เหตุผล}
✅/⛔ Line My Shop:{ชื่อไฟล์ หรือ เหตุผล}
🔐 ต้อง login เอง: {รายชื่อแพลตฟอร์มที่ session หมด — ถ้าไม่มีเขียน "ไม่มี"}
```
