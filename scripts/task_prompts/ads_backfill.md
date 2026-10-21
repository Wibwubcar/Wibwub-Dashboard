---
name: wibwub-ads-backfill
description: ดึงข้อมูล Ads ย้อนหลัง ม.ค.–ส.ค. 69 เข้า ads_daily.json (2 รอบ: 21:45 และ 00:15)
---

## WIBWUB — ดึงข้อมูล Ads ย้อนหลังถึง 1 ม.ค. 2569

งานนี้รัน **2 รอบ**: 21:45 (หลัง samp-request-sync จบ) และ 00:15 (หลัง HR ปิดวันจบ)
เป้าหมาย: `data Ads/ads_daily.json` ซึ่งตอนนี้เริ่ม 1 ก.ย. 69 ให้ย้อนไปถึง 1 ม.ค. 69
เพื่อให้เมนู "การตลาด vs ยอดขาย" และหน้า Ads เลือกช่วงย้อนหลังได้ทั้งปี

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

> **ตัวช่วยคือ `scripts/ads/backfill.py` ไม่ใช่ `ads_daily_update.py`**
> ตัวหลังงานประจำวันใช้อยู่และ **ตั้งใจให้เขียนทับย้อนหลัง 3 วัน** — ห้ามเอามาใช้ที่นี่
> `backfill.py merge` จะ **ข้ามทุกวันที่มีข้อมูลอยู่แล้ว** (ก.ย.–ต.ค. จะไม่ถูกแตะ)

---

## 🚦 ขั้น 0 — ตรวจก่อนเสมอ (ทำซ้ำก่อนเริ่มดึงทุกเดือน)

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/backfill.py" guard --minutes 30
```
- `status: OK` → ทำต่อได้
- `status: WAIT` (exit 2) → **หยุด** รอจนถึงเวลาที่ปลอดภัย แล้วเช็คใหม่ ห้ามฝืนดึง
- `status: WARN` → ไม่มีงานตามตาราง แต่มี session อื่นเขียนไฟล์อยู่ ให้รอ 5 นาทีแล้วเช็คซ้ำ 1 ครั้ง
  ถ้ายัง WARN ให้ทำต่อได้ (น่าจะเป็นเซสชันของคน ไม่ใช่งานตั้งเวลา)

**ถ้าระหว่างดึงแล้วงานตั้งเวลาตัวไหนล้ม หรือ guard กลายเป็น WAIT: หยุดทันที** บันทึกว่าหยุดที่เดือนไหน

### ⏱ งานนี้แบ่งเป็น 2 รอบโดยตั้งใจ
รอบแรกเริ่มหลัง `samp-request-sync` (21:10) จบ — มีเวลาว่างถึงราว **23:20**
(หลังจากนั้น guard จะเป็น WAIT เพราะ HR ปิดวัน 23:50)
**ทำได้เท่าไรก็หยุดเท่านั้น ไม่ต้องฝืน** แล้วรอบที่สองเวลา **00:15** จะมาทำเดือนที่เหลือต่อ
`backfill.py merge` ข้ามวันที่มีอยู่แล้วเสมอ จึงรันซ้ำได้ปลอดภัย ไม่มีข้อมูลซ้ำซ้อน
ก่อนเริ่มทุกครั้งให้ดู `python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/backfill.py" status` ว่าเดือนไหนยังขาด แล้วทำต่อจากตรงนั้น

---

## ขั้น 1 — ตรวจสถานะปัจจุบัน + ทดสอบว่าย้อนได้ไกลแค่ไหน

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/backfill.py" status
```

### กฎเบราว์เซอร์ (เหมือน ads-daily)
`list_connected_browsers` → เลือกตัว macOS (`b75a6bb0-5b78-4e44-92a8-75224f1ce4ee`) →
`tabs_context_mcp(createIfEmpty=true)` · ใช้ `browser_batch` เสมอ · `wait` ห้ามเกิน 10 วิ

> ⚠️ **ถ้า navigate ตอบ "Navigation to this domain is not allowed"** แปลว่าสิทธิ์โดเมนของ
> ส่วนขยาย Claude in Chrome หลุด (เกิดจริง 20 ต.ค. เช้า ทำให้ ads-daily ล้มทั้งรอบ)
> งานตั้งเวลากดอนุญาตเองไม่ได้ → **หยุดทันที บันทึกในรายงาน แล้วจบงาน**
> ห้ามลองเปลี่ยนรูป URL ห้ามสลับไปเบราว์เซอร์ในตัว (ไม่มี session ของ TikTok/Lazada)

### ทดสอบขอบเขตย้อนหลังของแต่ละแหล่ง
ดึง **วันเดียว** คือ `2026-01-01` ต่อหนึ่งแหล่ง แล้วดูว่าได้ข้อมูลหรือ error
วิธีเดียวกับ ads-daily ทุกประการ (hook.js → ทำให้หน้าโหลดข้อมูล → collect.js) แต่ตั้ง
`from` และ `to` เป็น `2026-01-01`

| แหล่ง | kind | หน้าที่ต้องเปิด |
|---|---|---|
| Shopee ยอดขายจริง | `sh_real` | seller.shopee.co.th/datacenter/overview |
| Shopee Ads | `sh_ads` | seller.shopee.co.th/portal/marketing/pas/index |
| TikTok ยอดขายจริง | `tk_real` | seller-th.tiktok.com/compass/data-overview |
| TikTok Ads (GMV Max) | `tk_ads` + `tk_camp` | ads.tiktok.com/i18n/gmv-max/dashboard?aadvid=7229166192752148482&oec_seller_id=7494549095358892612&bc_id=7229165256428240898&type=product |
| Lazada ยอดขายจริง | `lz_real` | sellercenter.lazada.co.th/ba/dashboard |
| Lazada Ads | `lz_ads` | sellercenter.lazada.co.th/sponsor/solutions/ads/productads/#!/overview |

ถ้าแหล่งไหนย้อนไม่ถึง 1 ม.ค. ให้ **ไล่หาวันที่เก่าสุดที่ยังได้** (ลองเป็นเดือน: 1 มี.ค. → 1 พ.ค. → 1 ก.ค.)
แล้วบันทึกไว้ ไม่ต้องหยุดงาน — ดึงเท่าที่ได้

**หมายเหตุที่รู้อยู่แล้ว:** `tk_camp` ดึงเป็นรายเดือน (ไม่ใช่รายวัน) และ `backfill.py camp`
จะไม่ทับเดือนที่มีอยู่แล้ว · Business Ads (ไฟล์ .xlsx) **ไม่เกี่ยวกับงานนี้** ไม่ต้องแตะ

---

## ขั้น 2 — ดึงทีละเดือน ไล่จาก ส.ค. ลงไป ม.ค.

ลำดับ: **ส.ค. → ก.ค. → มิ.ย. → พ.ค. → เม.ย. → มี.ค. → ก.พ. → ม.ค.**

สำหรับแต่ละเดือน:
1. `python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/backfill.py" guard --minutes 30` — ไม่ OK ให้หยุด
2. ตั้ง `window.__ADS={kind:'<kind>', from:'<YYYY-MM-01>', to:'<วันสุดท้ายของเดือน>'}` แล้ววาง collect.js
   - **วาง collect.js โดยคงการขึ้นบรรทัดใหม่ไว้** ถ้าแปลงเป็นบรรทัดเดียว `//` จะกินทั้งไฟล์
   - ดึงทีละ kind: `sh_real` → `sh_ads` → `tk_real` → `tk_ads` → `lz_real` → `lz_ads`
   - poll `window.__adsJob` จน `done:true` และ **ต้องไม่มี `err`**
   - อ่านด้วย `window.__adsExport(0,900)`, `(900,1800)`, … จนครบ `__adsJob.len`
   - บันทึกเป็น `work/<kind>.json` ด้วย heredoc คัดลอกตรงตัว
3. รวมเข้าไฟล์:
```bash
W="$BASE/scripts/ads/work"
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/backfill.py" merge "$W/sh_real.json" "$W/sh_ads.json" "$W/tk_real.json" "$W/tk_ads.json" "$W/lz_real.json" "$W/lz_ads.json" --dry-run
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/backfill.py" merge "$W/sh_real.json" "$W/sh_ads.json" "$W/tk_real.json" "$W/tk_ads.json" "$W/lz_real.json" "$W/lz_ads.json"
```
   (ถ้า Lazada ย้อนไม่ถึงเดือนนั้น ให้ตัด 2 ไฟล์ท้ายออก — Lazada เป็นออปชัน)
   `exit 10` = ไม่มีวันใหม่ (ปกติถ้าเดือนนั้นมีอยู่แล้ว) · `exit 2` = ไม่ผ่านด่านตรวจ ให้หยุดและบันทึก
4. แคมเปญ: `python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/backfill.py" camp "$BASE/scripts/ads/work/tk_camp.json"`

### ✅ เดือนแรก (ส.ค.) ต้องตรวจก่อนไปต่อ
หลังดึง ส.ค. เสร็จ **สุ่ม 2–3 วัน** เทียบกับตัวเลขบนหน้าเว็บจริง (ตั้งช่วงวันที่เป็นวันนั้นวันเดียว
แล้วอ่านตัวเลขจากหน้า): ยอดขายจริง Shopee, ค่าโฆษณา Shopee, ยอดขายจริง TikTok, ค่าโฆษณา TikTok
- **ตรงกัน** → ดึงเดือนที่เหลือต่อได้เลย ไม่ต้องรอใครตอบ
- **ไม่ตรง** → **หยุดทั้งหมด** บันทึกว่าต่างกันตรงไหน วันไหน ตัวเลขฝั่งไหนเท่าไร

---

## ขั้น 3 — อัปเดตหน้าเว็บ

> **อย่ารวม `cd` กับ `git` ไว้ในคำสั่งเดียวกัน** — ตัวตรวจความปลอดภัยจะเด้งถาม
> ("changes directory before running git, which can execute untrusted hooks")
> ใช้ `git -C "$BASE"` และเรียกสคริปต์ด้วย path เต็มแทน งานจะรันเองได้ไม่ต้องรอคนกด

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/marketing/kol_fetch.py"          # ยอด KOL (ตั้งแต่ ม.ค. — ดู ROWS_FROM)
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/marketing/marketing_ui.py"       # ฝัง CSS/JS เวอร์ชันล่าสุดลง 2 หน้า
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/marketing/marketing_update.py"   # รวมเข้าเมนู "การตลาด vs ยอดขาย"
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/ads_daily_update.py" commit  # sync ads_periods + bump sw.js + commit
```
```bash
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add "data Ads/kol_monthly.json" WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "backfill: ข้อมูล Ads ย้อนหลังถึง $(date +%Y-%m-%d)"
```
ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เอง

---

## ขั้น 4 — เขียนรายงานไว้ให้ดูตอนเช้า

เขียนไฟล์ `scripts/ads/work/backfill_report.md` (ภาษาไทย) ให้มีครบทุกหัวข้อ:

1. **งานตั้งเวลาคืนนี้** — แต่ละตัวสำเร็จไหม มี commit อะไรบ้าง
   (`git log --oneline --since="20 hours ago"`) และ `ads_daily.json` มีวันที่ 19 ครบ 3 แพลตฟอร์มไหม
2. **ขอบเขตย้อนหลังของแต่ละแหล่ง** — แหล่งไหนได้ถึงวันไหน ถ้าไม่ถึง 1 ม.ค. บอกวันที่เก่าสุดที่ได้
3. **ผลตรวจเดือน ส.ค.** — สุ่มวันไหนบ้าง ตัวเลขตรงกับหน้าเว็บหรือไม่
4. **ยอดรวมรายเดือน ม.ค.–ต.ค.** — จาก `python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/backfill.py" report`
5. **รายการ KOL ที่ปีน่าจะพิมพ์ผิด** — จาก `data Ads/kol_monthly.json` เดือน `2025-01` / `2025-02` /
   `2025-03` (ยอด 26,000 / 2,000 / 1,000) ให้ลิสต์ว่าอยู่แท็บไหน วันที่อะไร ยอดเท่าไร
   **ห้ามแก้เอง** แค่ลิสต์ไว้ให้เจ้าของงานตัดสิน
6. **ปัญหาที่เจอ / เดือนที่ยังดึงไม่ได้ และเพราะอะไร**

---

## RULES

- ทำทุกอย่างใน bash + Chrome tools ห้าม spawn subagents
- **ห้ามเขียนทับวันที่มีข้อมูลแล้ว** — ใช้ `backfill.py` เท่านั้น ห้ามใช้ `ads_daily_update.py merge`
- **ห้ามแก้ตัวเลขเอง** ถ้าสคริปต์ไม่ผ่านด่านตรวจให้หยุดและบันทึก
- ห้าม login ห้ามกรอกรหัสผ่าน/OTP · ห้ามกดปุ่มที่ไม่เกี่ยวกับการดูข้อมูล
  (เติมเงิน / เข้าร่วมแคมเปญ / แก้ ROAS / แก้ budget) ป๊อปอัปให้กด X ปิดอย่างเดียว
- ปิดแท็บ Chrome ทั้งกลุ่มเมื่อจบงาน
- เมื่อ `backfill.py status` บอกว่า ม.ค.–ส.ค. ครบหมดแล้ว ให้บันทึกในรายงานว่า
  "เสร็จสมบูรณ์ ลบงานตั้งเวลา wibwub-ads-backfill และ wibwub-ads-backfill-2 ได้"

---

## 🚫 กฎคำสั่ง shell (ทุกงาน — รวมคำสั่งที่คิดขึ้นเองระหว่างรัน)

งานตั้งเวลา **ไม่มีคนนั่งกดอนุญาต** ถ้าคำสั่งไม่แมตช์กฎที่อนุญาตไว้แล้ว
(`Bash(python3 *)` / `Bash(git *)` / `Bash(ls *)` ฯลฯ) งานจะค้างทั้งรอบ
สังเกตง่าย ๆ: ถ้ากล่องขออนุญาตมีแค่ปุ่ม **"Allow once"** โดยไม่มี "Always allow"
แปลว่าคำสั่งนั้นสร้างกฎถาวรไม่ได้ จะถามใหม่ทุกครั้งตลอดไป

**เขียนคำสั่งให้เรียบง่ายที่สุด — 1 คำสั่ง = 1 โปรแกรม + พาธเต็ม**

| ❌ ห้าม | เหตุผลที่โดนถาม | ✅ ใช้แบบนี้ |
|---|---|---|
| `cd "<path>" && git status` | cd + git = ตัวตรวจตีธง (รัน hook ได้) | `git -C "<path เต็ม>" status` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion สร้างกฎถาวรไม่ได้ | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for d in ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขใน bash ก็เข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python แล้วเรียกไฟล์นั้น |
| `cmd1; cmd2; cmd3` ต่อกันยาว ๆ | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |

**ถ้าต้องมีตรรกะ (วนลูป / เช็คเงื่อนไข / ประกอบพาธ): เขียนเป็นสคริปต์ python
ไว้ใน `scripts/` แล้วเรียกด้วยพาธเต็ม** เช่น `python3 "<path เต็ม>/scripts/ads/check_downloads.py" tiktok`
วิธีนี้ทั้งอ่านง่ายกว่า ทดสอบแยกได้ และไม่ติดกำแพงสิทธิ์
