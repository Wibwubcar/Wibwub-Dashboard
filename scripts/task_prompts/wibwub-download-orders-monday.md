---
name: wibwub-download-orders-monday
description: Download daily order exports from Shopee, TikTok Shop, Lazada, and Line My Shop — ทุกวัน 08:20/19:20
---

Download order export files from all 4 WIBWUB e-commerce platforms and save them to the correct folders. Complete all 4 platforms every time.

## ⚠️ Chrome Navigation Rule — สำคัญมาก
ห้ามใช้ `navigate` แบบ standalone เด็ดขาด — จะค้างไม่ return ทำให้ task หยุดทำงาน
ต้องใช้ `navigate` + `wait` ในคู่เสมอ:
```
navigate(url="...", tabId=TAB_ID)  # ผ่าน browser_batch หรือ standalone ก็ได้
computer(action="wait", duration=4, tabId=TAB_ID)
computer(action="screenshot", tabId=TAB_ID)
```

## ⚡ Session Recovery — ทำก่อนทุก platform
ถ้า page redirect ไปหน้า login ให้ทำตาม Recovery Steps ของแต่ละ platform ด้านล่างทันที อย่ายอมแพ้และ skip

## Save folder base
All files go under:
/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data ยอดขาย plaform/
  ├── Shopee/
  ├── Tiktok/
  ├── Lazada/
  └── Line My Shop/

Use the Chrome MCP (`mcp__Claude_in_Chrome__*`) for all browser automation.
Use bash for file operations (copy from Downloads).

⚠️ **ต้องระบุ browser ที่ Mac เสมอ ห้ามปล่อยให้เลือกอัตโนมัติ** — ก่อนเริ่ม platform แรก:
`select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")` แล้วค่อย `tabs_context_mcp(createIfEmpty=true)`
(ถ้า deviceId นี้ไม่ connected แล้ว ให้เรียก `list_connected_browsers` ก่อน แล้วเลือกตัวที่ `osPlatform` เป็น macOS / `isLocal:true` เท่านั้น — ห้ามเลือก Windows/PC)

---

## Platform 1 — Shopee
URL: https://seller.shopee.co.th/portal/sale/order

### Session Check
ถ้า page URL ยังเป็น `/sale/order` = session OK
ถ้า redirect ไปหน้าอื่น = session expired → navigate ไปที่ https://seller.shopee.co.th แล้วรอ 5 วินาที แล้ว navigate กลับ

### Steps
1. Navigate to: https://seller.shopee.co.th/portal/sale/order
2. Wait 5 seconds → screenshot
3. Click tab "ทั้งหมด" (use find tool with query "ทั้งหมด tab")
4. Click "ส่งออก" dropdown
5. Select "ส่งออกรายการสั่งซื้อ" → "ทั้งหมด"
6. Set date range: first day of current month → today
7. Click Export → wait for download
8. Click download link when ready

File: ZIP named `Order.all.YYYYMMDD_YYYYMMDD.zip`
Save:
```bash
NEW_ZIP=$(ls -t "/Users/thanasablilutanon/Downloads/Order.all.*.zip" 2>/dev/null | head -1)
if [ -n "$NEW_ZIP" ]; then
  cp "$NEW_ZIP" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data ยอดขาย plaform/Shopee/"
  echo "✅ Shopee: $(basename "$NEW_ZIP")"
fi
```

---

## Platform 2 — TikTok Shop
URL: https://seller-th.tiktok.com/order/list?tab=all

### Session Check + Recovery
1. Navigate to URL, wait 5s, take screenshot
2. Check page text with get_page_text:
   - ถ้ามี "จัดการคำสั่งซื้อ" หรือ "WIBWUBCAR" = session OK
   - ถ้ามี "เข้าสู่ระบบ" หรือ "login" = session expired

### Recovery Steps (ถ้า session หมด)
Navigate to https://seller-th.tiktok.com/ แล้วรอ 10 วินาที — ถ้า TikTok Shop ใช้ cookie เดียวกับ TikTok Ads ที่ login อยู่ จะ auto-login
ถ้าไม่ได้ → navigate ไปที่ https://seller-th.tiktok.com/ → find "เข้าสู่ระบบ" button → คลิก → รอ

### Steps (หลัง session OK)
1. Click เมนูซ้าย "จัดการคำสั่งซื้อ" ถ้าไม่เห็นรายการ
2. Click tab "ทั้งหมด" 
3. Click "ดาวน์โหลด" button (top-right area, ไม่ใช่ "ส่งออก"):
   ```javascript
   // หา ดาวน์โหลด button
   const btn = Array.from(document.querySelectorAll('button'))
     .find(b => (b.textContent||'').trim().includes('ดาวน์โหลด') && 
                 b.getBoundingClientRect().top > 0);
   if (btn) btn.click();
   ```
4. Dialog เปิด → เลือก "คำสั่งซื้อที่กรอง" → เลือก Excel
5. Click "ส่งออก" ใน dialog
6. รอ progress circle เปลี่ยนเป็น "ดาวน์โหลด" (สีแดง) ใน Export History
7. Click "ดาวน์โหลด" button ใน history row

File: `ทั้งหมด คำสั่งซื้อ-YYYY-MM-DD-HH_MM.xlsx`
Save:
```bash
NEW_FILE=$(ls -t "/Users/thanasablilutanon/Downloads/"*"คำสั่งซื้อ"*.xlsx 2>/dev/null | head -1)
if [ -n "$NEW_FILE" ]; then
  cp "$NEW_FILE" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data ยอดขาย plaform/Tiktok/"
  echo "✅ TikTok: $(basename "$NEW_FILE")"
fi
```

---

## Platform 3 — Lazada
URL: https://sellercenter.lazada.co.th/apps/order/list?status=all

Lazada uses queue-based export — trigger, then do Line My Shop, then come back.

### Session Check + Recovery
1. Navigate to URL, wait 5s
2. Check URL after navigation:
   - ถ้า URL เป็น `/apps/order/list` = session OK
   - ถ้า redirect ไป `/apps/seller/login` = session expired → Recovery

### Recovery Steps (ถ้า session หมด)
```javascript
// ตรวจ URL ปัจจุบัน
window.location.href
```
ถ้าเป็น login page → หา "เข้าสู่ระบบ" button (credentials อยู่ใน browser แล้ว):
```javascript
// Click เข้าสู่ระบบ — browser จะ autofill user/pass
const loginBtn = Array.from(document.querySelectorAll('button'))
  .find(b => b.type === 'submit' || b.textContent.trim() === 'เข้าสู่ระบบ');
if (loginBtn) loginBtn.click();
```
Wait 5s → navigate กลับไปที่ order list URL

### Steps (หลัง session OK)
1. Export (JS):
```javascript
// Step 1: Open dropdown
const exportBtn = Array.from(document.querySelectorAll('button'))
  .find(b => b.textContent.trim() === 'ส่งออก');
exportBtn.click();
```
```javascript
// Step 2: Click Export All
const exportAll = Array.from(document.querySelectorAll('li, a, div, span, button'))
  .find(el => el.textContent.trim() === 'Export All' && el.offsetParent !== null);
exportAll.click();
```
2. Confirm dialog: find "ยืนยัน" button → click
3. **Do NOT wait** — proceed to Line My Shop immediately

### Come back after Line My Shop — check Export History:
```javascript
// Click Export → Export History
const exportBtn = Array.from(document.querySelectorAll('button'))
  .find(b => b.textContent.trim() === 'ส่งออก');
exportBtn.click();
// Then click Export History in dropdown
const hist = Array.from(document.querySelectorAll('li,a,div,span'))
  .find(el => el.textContent.trim() === 'Export History' && el.offsetParent);
if (hist) hist.click();
```
```javascript
// Get download links
const links = Array.from(document.querySelectorAll('a'))
  .filter(a => a.textContent.trim() === 'Download Result File');
links.map(a => a.href) // index 0 = newest
```
Navigate directly to the CDN URL: `https://sg-test-11.slatic.net/other/batch/[HASH].xlsx`

File: hash-named `.xlsx`
Save:
```bash
HASH_FILE=$(ls -t "/Users/thanasablilutanon/Downloads/"*.xlsx 2>/dev/null | \
  grep -v "คำสั่งซื้อ\|Order Report\|Campaign\|WIBWUBCAR\|Submit\|Data_" | head -1)
if [ -n "$HASH_FILE" ]; then
  cp "$HASH_FILE" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data ยอดขาย plaform/Lazada/Lazada_Orders_$(date +%Y%m%d).xlsx"
  echo "✅ Lazada: Lazada_Orders_$(date +%Y%m%d).xlsx"
fi
```

---

## Platform 4 — Line My Shop
URL: https://oaplus.line.biz/channels/5000113570/e-commerce/report

Channel ID = 5000113570 (also the file password)

### ⚡ สำคัญ: Domain นี้ใช้งานได้ใน Claude Chrome ถ้า session ยังอยู่
### Session Check + Recovery
1. Navigate to https://oaplus.line.biz/channels/5000113570/e-commerce/report
2. Wait 5s → screenshot
3. Check page title/content:
   - ถ้ามี "รายงาน" หรือ "WIBWUB.CAR" = session OK ✅
   - ถ้า redirect ไป `access.line.me` = session expired → Recovery

### Recovery Steps (ถ้า session หมด)
Tab 1415001339 (LINE Login tab) มักจะเปิดอยู่แล้วในกลุ่ม Claude Chrome
Navigate tab นั้นไปที่ https://access.line.me → รอ user login (หรือถ้ามี auto-login จะเข้าเองเลย)
แล้ว navigate tab ใหม่ไปที่ https://oaplus.line.biz/channels/5000113570/e-commerce/report

หรือสร้าง tab ใหม่:
```python
# tabs_create_mcp() แล้ว navigate ไปที่ URL
```
ถ้า session ยังไม่กลับมา → แจ้ง user ว่าต้อง login LINE ใน Claude Chrome tab แล้วรัน schedule ใหม่

### Steps (หลัง session OK)
1. คำนวณวันที่:
```python
from datetime import datetime, timedelta
today = datetime.now()
start = today - timedelta(days=87)  # 87 วัน = ไม่เกิน 90
start_str = start.strftime("%d/%m/%Y")
# เช่น "05/04/2026"
```

2. Click start date field (find tool: "วันที่เริ่ม" หรือ triple_click ที่ field แรก)
3. พิมพ์ start date ใหม่ (เช่น "05/04/2026") → Enter
4. Calendar จะเปิด → navigate ไปเดือนที่ถูกต้อง (กดลูกศรซ้าย) แล้วคลิกวันที่
5. Find "ดาวน์โหลด" button → click (ref-based)
6. ถ้ามี confirmation dialog (>30 วัน) → find "ดาวน์โหลด" blue button → click

File: `Order Report YYYYMMDD.xlsx` (password-encrypted, password = 5000113570)
Save:
```bash
NEW_RPT=$(ls -t "/Users/thanasablilutanon/Downloads/Order Report "*.xlsx 2>/dev/null | head -1)
START_DATE=$(date -d "87 days ago" +%Y%m%d 2>/dev/null || date -v-87d +%Y%m%d)
END_DATE=$(date +%Y%m%d)
if [ -n "$NEW_RPT" ]; then
  cp "$NEW_RPT" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data ยอดขาย plaform/Line My Shop/LineMyShop_Orders_${START_DATE}_${END_DATE}.xlsx"
  echo "✅ Line My Shop: LineMyShop_Orders_${START_DATE}_${END_DATE}.xlsx"
fi
```

---

## Summary Table
| Platform | URL | Format | Recovery |
|---|---|---|---|
| Shopee | seller.shopee.co.th | ZIP | Auto via cookies |
| TikTok | seller-th.tiktok.com | .xlsx | Navigate homepage |
| Lazada | sellercenter.lazada.co.th | .xlsx | Click login btn (browser autofill) |
| Line My Shop | oaplus.line.biz | .xlsx encrypted (pw=5000113570) | Needs manual LINE login if expired |

## Completion Report
After all platforms done:
- ✅ Shopee: [filename] (covers YYYY/MM/DD–DD)
- ✅ TikTok: [filename]
- ✅ Lazada: [filename]
- ✅ Line My Shop: [filename]
- ⛔ [platform]: session expired — [action taken]


## ⚠️ กฎการย้ายไฟล์จาก Downloads (สำคัญมาก)

**ปัญหา:** Sandbox (Linux) ลบไฟล์จาก Downloads ไม่ได้ — `mv` และ `rm` จาก Downloads ล้มเหลวด้วย "Operation not permitted"

**วิธีที่ถูกต้องสำหรับ sandbox:**
- ใช้ `cp` เพื่อ copy ไปยังโฟลเดอร์งาน (ทำได้ ✅)
- ห้ามใช้ `mv` หรือ `rm` กับไฟล์ใน Downloads จาก sandbox (ล้มเหลว ❌)

**ระบบย้ายอัตโนมัติ (ไม่ต้องทำอะไรเพิ่ม):**
มี macOS LaunchAgent `com.wibwub.download-mover` ทำงานอยู่เบื้องหลังตลอดเวลา
เมื่อ schedule cp ไฟล์ไปโฟลเดอร์งานแล้ว LaunchAgent จะ **mv (ย้าย)** ไฟล์ต้นฉบับออกจาก Downloads อัตโนมัติภายใน 5 วินาที
— ไม่ต้อง double-click อะไรทั้งนั้น ทุกอย่างเป็นอัตโนมัติ

**Script ที่เกี่ยวข้อง (อยู่ใน All/scripts/):**
- `wibwub_auto_move.sh` — script ย้ายไฟล์ (ถูกเรียกโดย LaunchAgent)
- `com.wibwub.download-mover.plist` — LaunchAgent config (WatchPaths ~/Downloads)