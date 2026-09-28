# WIBWUB Affiliate Auto-Update — 4 ก.ย. 2026 (wibwub-thursday-affiliate)

## ช่วงข้อมูล
TikTok Affiliate Center อัปเดตล่าสุดถึง **1 ก.ย. 2026** ตอนที่ export
ช่วงที่ดึง: **01/09/2026 – 01/09/2026** (เดือน ก.ย. มีข้อมูลวันเดียว)

## ไฟล์ที่ดาวน์โหลด (STEP 2–3)
ทั้ง 4 ไฟล์ถูก LaunchAgent `com.wibwub.download-mover` ย้ายเข้าโฟลเดอร์ปลายทางอัตโนมัติ

| แท็บ | ไฟล์ | ขนาด |
|---|---|---|
| ครีเอเตอร์ | `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260901-20260901.xlsx` | 175,518 B |
| สินค้า | `Data Affiliate/สินค้า/Transaction_Analysis_Product_List_20260901-20260901.xlsx` | 18,653 B |
| วีดีโอ | `Data Affiliate/วีดีโอ/Transaction_Analysis_Video_List_20260901-20260901.xlsx` | 445,545 B |
| ไลฟ์สตรีม | `Data Affiliate/ไลฟ์สตรีม/Transaction_Analysis_Live_List_20260901-20260901.xlsx` | 13,399 B |

## STEP 4 — AF_* / AFI_* arrays
เพิ่ม index ใหม่ของเดือน ก.ย. (ไม่ทับเดือนเก่า — label `ก.ย.` ยังไม่มีใน array จึง append)

ตัวเลขที่คำนวณจากไฟล์ ครีเอเตอร์ 01/09 (ตรวจสอบตรงกับหน้าจอ TikTok):
GMV ฿46,902.60 · คืนเงิน ฿86.10 · Net ฿46,817 · คอมมิชชั่น ฿5,431.59 · ครีเอเตอร์มียอด 85 คน

**หมายเหตุสำคัญ:** ระหว่างที่รันงานนี้ มี scheduled job อีกตัว (commit `7443171`, 09:04) เขียนทับ AF_*/AFI_* ด้วยข้อมูลที่ใหม่กว่า — **ก.ย. (1-2)**: GMV ฿111,364 · Net ฿106,994 · Comm ฿12,347 · 138 creators
ค่าที่ใหม่กว่านี้ถูกคงไว้ และผมได้ sync label + KPI ฝั่ง Mobile ให้ตรงกัน (`กย.69 (1-2)`, `฿111K`, `138 creators`)

## STEP 5 — PRODUCTS cr/vid
แก้เฉพาะ `cr` และ `vid` (ไม่แตะ gmv/units/monthly/ret)

| สินค้า | cr | vid |
|---|---|---|
| WIBWUB Refresh Leather Wipes | 42 | 26 |
| WIBWUB Interior wipes | 20 | 11 |
| WIBWUB Sugar | 19 | 10 |
| WIBWUB CLEANER | 3 | 1 |
| WIBWUB Interior | 4 | 7 |
| WIBWUB Refresh | 3 | 5 |
| WIBWUB Visible | 1 | 1 |
| **รวม** | **92** | **61** |

หัวตารางคอลัมน์ ครีเอเตอร์/วีดีโอ เปลี่ยน label `ส.ค.1-24` → `ก.ย.1-1`

## STEP 5B — VIDEOS array
- entry_re จับได้ **7,554 entries** (ผ่านเกณฑ์ safety — ไม่ใช่ 0)
- parse ไฟล์วีดีโอด้วย `zipfile` + regex (inlineStr) ได้ **2,216 rows**
- ขยาย schema `monthly` เพิ่ม key `sep` ให้ทุก entry (เดิมมีถึง `aug`)
- **updated 2,101 entries · new 115 entries** → รวม **7,669 entries**
- unknown product = 0 (map product_id → ชื่อ สำเร็จทั้งหมด)
- ก.ย. GMV จากวีดีโอ ฿35,264 · 210 ชิ้น
- เพิ่ม `sep:'ก.ย.'` ใน mLabel maps 3 จุด
- ตรวจแล้ว: `gmv === sum(monthly)` ทุก entry (0 รายการผิด), ไม่มี entry ที่ขาด key `sep`

## STEP 6 — Cache / push
- `sw.js`: `wibwub-v977` → **`wibwub-v978`**
- `push_now.command` regenerate ใหม่ (chmod +x เรียบร้อย)
- commits: `f4acd81` (affiliate update) และ `08ce824` (sync mobile + push_now)

## ตรวจสอบขั้นสุดท้าย
- `node -e` eval VIDEOS (7,669) และ PRODUCTS (7) ผ่าน — ไม่มี syntax error
- `WIBWUB_Mobile.html` AFI arrays ยาว 11 เท่ากันทั้ง 4 array
- script tag เปิด/ปิดครบทั้งสองไฟล์

---

## ⚠️ ประเด็นที่ควรแก้ใน SKILL.md / dashboard

1. **สคริปต์ STEP 4 ใน SKILL.md ใช้คอลัมน์ผิด** — ไฟล์ ครีเอเตอร์ มี header 2 แถว ต้อง `.iloc[2:]` (ไม่ใช่ `[1:]`) และคอลัมน์ที่ถูกคือ **คืนเงิน = col 4, คอมมิชชั่น = col 21** (SKILL.md ระบุ col 2 และ col 10)
2. **path ใน SKILL.md เป็น session เก่า** (`/sessions/hopeful-serene-fermi/...`) — session ปัจจุบันคือ `/sessions/gallant-amazing-faraday/...` ควรเขียนเป็น path แบบ relative หรือ resolve อัตโนมัติ
3. **ยังไม่มีปุ่มเดือน ก.ย. 2569** ในแถบ month filter (`.mfbtn`) ของ Affiliate Dashboard — VIDEOS มีข้อมูล `sep` แล้วแต่กรองดูไม่ได้ **และ `PRODUCTS.monthly` ยังไม่มี key `sep`** จึงยังไม่เพิ่มปุ่มให้ (เสี่ยง NaN ในแท็บสินค้า) — ต้องตัดสินใจก่อนว่าจะเติม `sep` ใน PRODUCTS.monthly/ret ด้วยหรือไม่
4. **KPI strip หน้า Overview ยังค้างที่ ส.ค. 1-29** (`฿1603.6K`, `฿1578.5K`, `853`, `฿184.7K`, Live `฿87.7K`) และ note ที่บอก "อัปเดตล่าสุดถึง 29 ส.ค. 2026" — เป็น hardcoded ที่ SKILL.md ไม่ได้ครอบคลุม
5. **KPI ค้างที่บรรทัด 314** — `Active Creator โตจากเดือนก่อน +80% · 398 คน (มิ.ย.) → 716 คน (ก.ค.)` ยังเป็นตัวเลขเก่า
6. **STEP 5 ระบุ KPI `ผ่าน X,XXX creators` ในแท็บสินค้า** — ปัจจุบัน KPI แท็บนั้นคำนวณแบบ dynamic (`kk-prod-active-sub`) ไม่มีข้อความนี้แล้ว จึงอัปเดต label หัวตารางแทน
7. **units ใน VIDEOS ยังไม่ idempotent 100%** — ถ้ารันซ้ำวันเดียวกัน entry ที่ `monthly.sep > 0` จะไม่บวก units ซ้ำ (ปลอดภัย) แต่ entry ที่ GMV = 0 อาจบวกซ้ำได้ ควรเพิ่มการเก็บ units รายเดือนในอนาคต
8. **git index.lock ชนกับ auto-push job บ่อย** — ต้อง retry loop; และมี job อื่นเขียนทับ AF_* ระหว่างทาง ควรจัดตารางให้ไม่ทับกัน
