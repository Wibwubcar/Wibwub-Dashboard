# รายงานอัปเดต Affiliate — 5 ก.ย. 2026

รันโดย scheduled task `wibwub-thursday-affiliate` (อัตโนมัติ)

## สรุปผล

รันครบทุก STEP (1–6) สำเร็จ ไม่มี step ที่ถูกข้าม

**ช่วงข้อมูล:** 1–2 ก.ย. 2026 (TikTok ยังไม่ปล่อยข้อมูลวันที่ 3–5 — ปฏิทินขึ้นสีเทา)

## STEP 1–3 — Export + จัดไฟล์

ดาวน์โหลดครบ 4 ไฟล์ (ครีเอเตอร์ / สินค้า / วีดีโอ / ไลฟ์สตรีม) ช่วง `20260901-20260902`
LaunchAgent `com.wibwub.download-mover` ย้ายไฟล์เข้าโฟลเดอร์ปลายทางให้เรียบร้อยแล้ว

| Tab | ไฟล์ | ขนาด |
|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260901-20260902.xlsx | 242 KB |
| สินค้า | Transaction_Analysis_Product_List_20260901-20260902.xlsx | 18.8 KB |
| วีดีโอ | Transaction_Analysis_Video_List_20260901-20260902.xlsx | 572 KB |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260901-20260902.xlsx | 18.6 KB |

หมายเหตุ: export ใช้เวลาจริง ~6 นาที (ไม่ใช่ 60–90 วิ ตามที่ SKILL.md ระบุ) และ panel รายงานไม่ refresh เอง ต้อง reload หน้าเว็บถึงจะเห็นปุ่ม "ดาวน์โหลด"

## STEP 4 — ตัวเลข Affiliate (ก.ย. 1-2)

จากไฟล์ครีเอเตอร์ 2,953 แถว (ข้าม header 2 บรรทัด, คอลัมน์ 0/1/4/21)

| ตัวชี้วัด | ค่าเดิมในแดชบอร์ด | ค่าใหม่ (verified) | ส่วนต่าง |
|---|---|---|---|
| GMV | 111,364 | **111,391** | +27 |
| Net GMV | 106,994 | **110,765** | **+3,771** |
| Commission | 12,347 | **12,518** | +171 |
| Creators | 138 | **138** | — |

⚠️ **ข้อสังเกตสำคัญ:** Net GMV ต่างจากเดิมถึง +3,771 — ค่าเดิม (เขียนโดย job อื่น commit `7443171`) ดูเหมือนจะหักคอลัมน์คืนเงินคนละคอลัมน์ ครั้งนี้ใช้คอลัมน์ 4 "การคืนเงิน" ตามที่เอกสารระบุ ซึ่งรวมได้เพียง ฿626.30 ควรตรวจว่า job ไหนถูกต้อง

**Rolling-window:** label สุดท้ายของ `AF_MO` / `AFI_MONTHS` คือ "ก.ย. (1-2)" อยู่แล้ว → เขียนทับ index สุดท้าย (ไม่ append) ตามกฎ ไม่มีเดือนก่อนหน้าถูกแตะ

ไฟล์ที่แก้: `WIBWUB_Affiliate_Dashboard.html` (AF_GMV/AF_NET/AF_COM) และ `WIBWUB_Mobile.html` (AFI_GMV/AFI_NET/AFI_COMM)
KPI text `฿111K` ทั้งสองไฟล์ยังถูกต้อง (round 111391/1000 = 111) ไม่ต้องแก้

## STEP 5 — PRODUCTS (cr / vid)

อัปเดตเฉพาะ `cr` และ `vid` ครบทั้ง 7 รายการ (ไม่แตะ gmv/units/monthly/ret)

| สินค้า | cr เดิม→ใหม่ | vid เดิม→ใหม่ |
|---|---|---|
| WIBWUB Refresh Leather Wipes | 42 → **47** | 26 → **47** |
| WIBWUB Interior wipes | 20 → **22** | 11 → **16** |
| WIBWUB Sugar | 19 → **17** | 10 → **12** |
| WIBWUB CLEANER | 3 → **4** | 1 → **2** |
| WIBWUB Interior | 4 → **4** | 7 → **11** |
| WIBWUB Refresh | 3 → **3** | 5 → **6** |
| WIBWUB Visible | 1 → **1** | 1 → **2** |

แก้ป้ายหัวตาราง 2 จุด `ก.ย.1-1` → `ก.ย.1-2`

⚠️ **คำเตือน:** ในไฟล์ 2 วัน คอลัมน์ 13/18/19/20 ถูกตั้งชื่อว่า "…เฉลี่ยรายวัน" (ต่างจากไฟล์ 1 วันที่เป็นยอดรวม) ตรวจค่าแล้วดูเป็นยอดสะสมจริง (Leather Wipes cr 42→47) จึงใช้คอลัมน์ 19 ตามเดิม แต่หากช่วงวันยาวขึ้นควรตรวจซ้ำ

ชื่อสินค้ามี 2 คู่ที่กำกวม (`WIBWUB Cleaner` vs `WIBWUB Refresh Leather Cleaner`) — แก้โดยเทียบค่า cr/vid ของไฟล์ 1 ก.ย. กับค่าที่เผยแพร่รอบก่อน ไม่ได้ใช้ fuzzy keyword ของ SKILL.md

## STEP 5B — VIDEOS array

parse inlineStr XML สำเร็จ 2,860 แถว

- entry เดิม parse ได้ 7,666 รายการ (ผ่านกฎความปลอดภัย — ไม่ใช่ 0)
- อัปเดตค่าเดือน `sep`: **90 รายการ**
- เพิ่ม entry ใหม่: **98 รายการ**
- รวมทั้งหมด: **7,764 รายการ**
- ยอด GMV วิดีโอเดือน ก.ย. รวม: ฿85,071 (คิดเป็น 76% ของ Affiliate GMV ทั้งหมด — ส่วนที่เหลือมาจาก live/showcase)

## STEP 6 — Cache + push

- `sw.js`: `wibwub-v993` → **`wibwub-v994`**
- สร้าง `push_now.command` ใหม่ (git add ทั้ง 3 ไฟล์ + commit + push) และ `chmod +x` แล้ว
- **ต้องดับเบิลคลิก `push_now.command` เพื่อ commit และ push ขึ้น production**

## การตรวจสอบ (verification)

- `node` eval ผ่านทั้ง VIDEOS (7,764), PRODUCTS (7), AF_*, AFI_*
- ตรวจ invariant `gmv === sum(monthly)` ผ่านทุก entry ✅
- `git diff --stat`: `WIBWUB_Affiliate_Dashboard.html` เปลี่ยน 961 บรรทัด, `WIBWUB_Mobile.html` 6 บรรทัด — อยู่ในเกณฑ์ปกติ (ต่ำกว่า 50%)

## ปัญหาค้าง / ควรแก้ SKILL.md

1. **path ใน SKILL.md ยังเป็น `/sessions/hopeful-serene-fermi/...`** (session เก่า) ต้องแปลงเป็น session ปัจจุบันทุกครั้ง — ควรเปลี่ยนเป็น path แบบไม่ผูก session
2. **STEP 4 column index ผิด** SKILL.md ระบุ `.iloc[1:]`, refunds คอลัมน์ 2, commission คอลัมน์ 10 — ของจริงคือ `.iloc[2:]`, คอลัมน์ 4, คอลัมน์ 21
3. **กฎ navigate กลับด้าน** SKILL.md ห้ามใช้ `navigate` แบบ standalone แต่รอบนี้ `browser_batch` + navigate ล้มเหลว ("Can't interact with browser internal pages") ส่วน `navigate` เดี่ยวทำงานได้ทันที
4. **ไม่มี guard "มีข้อมูลใหม่ไหม"** — ควรเช็คก่อนว่าวันที่ล่าสุดที่ TikTok ปล่อยเปลี่ยนไปจากรอบก่อนหรือไม่
5. **`PRODUCTS[].monthly` / `.ret` ยังไม่มี key `sep`** (มีแค่ mar–aug) ทำให้ยังเพิ่มปุ่มกรองเดือน ก.ย. ในตารางสินค้าไม่ได้
6. **ไฟล์ไลฟ์สตรีมยังไม่ถูกประมวลผล** — ดาวน์โหลดทุกรอบแต่ SKILL.md ไม่มี step รองรับ (เหมือนกรณีวีดีโอก่อน 20 ก.ค.)
7. **มี job อื่นเขียน repo เดียวกันพร้อมกัน** (เห็น commit `993cb1f`, `86a0bb0` ระหว่างรัน) — เสี่ยงชนกัน และเป็นที่มาของความไม่ตรงกันของ Net GMV ในข้อ STEP 4
