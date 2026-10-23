---
name: wibwub-tiktok-live-daily
description: ทุกวัน 08:37/19:37 (รอบเดียวกับ Shopee Live) — ยอดขายไลฟ์ TikTok Shop + งบ Ads ระหว่างไลฟ์ → TK_LIVE_DAILY ใน WIBWUB_Dashboard.html
---

## 📂 ขั้น 0 — หาโฟลเดอร์ All ก่อนเสมอ (ทำก่อนทุกอย่าง)

พรอมป์นี้ถูกเรียกได้จาก **2 ฝั่ง** และโฟลเดอร์ All อยู่คนละที่กัน
จึง**ห้ามฝังพาธตายตัว** ให้หาด้วยคำสั่งนี้ทุกครั้ง แล้วใช้ผลลัพธ์เป็น `BASE`

```bash
for d in "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" "$HOME/mnt/All" /sessions/*/mnt/All; do [ -d "$d/scripts" ] && echo "$d" && break; done
```

- ได้พาธมา → ใช้เป็น `BASE` ในทุกคำสั่งถัดไป (เขียนพาธเต็มเสมอ ห้ามใช้ตัวแปร shell)
- **ไม่เจอ** หรือ shell ตอบว่า `No folders are connected`
  → **หยุดทันที** รายงานว่า `❌ ล้มเหลว — เข้าโฟลเดอร์ All ไม่ได้` แล้วจบงาน
  ห้ามเดาพาธเอง ห้ามไปใช้ `~/Downloads` แทน

---


## WIBWUB — ยอดขายไลฟ์สดรายวัน TikTok Shop

อัปเดตส่วน "📺 ยอดขายไลฟ์สดรายวัน + งบ Ads ระหว่างไลฟ์ — TikTok Shop" (`TK_LIVE_DAILY`)
ใน `WIBWUB_Dashboard.html` — เป็นตัวคู่ของงาน `wibwub-shopee-live-daily`

> **งานนี้ไม่ต้องเปิด Chrome ไม่ต้องโหลดไฟล์** ข้อมูลที่ต้องใช้มีอยู่ในรีโปแล้ว
> ทั้งสองฝั่ง สคริปต์แค่ประกอบให้ — จึงไม่มีทางพังเพราะสิทธิ์โดเมนหรือ login

| ต้องใช้ | มาจาก | ใครเติมให้ |
|---|---|---|
| ยอดขายไลฟ์ (`gmv`) | `TK_PROD_DATA` ในหน้าเดียวกัน (self_live + affiliate_live) | `wibwub-tiktok-product-daily` 08:45/19:45 |
| ค่าโฆษณาระหว่างไลฟ์ (`adsCost`/`adsRev`) | `data Ads/ads_daily.json` → `tk_ads.live` | `wibwub-ads-daily` |

**ลำดับเวลา — อ่านให้เข้าใจก่อนคิดว่างานพัง:** งานนี้ตั้งไว้ **08:37/19:37 รอบเดียวกับ
Shopee Live** ตามที่ผู้ใช้เลือก ซึ่งอยู่ **ก่อน** งานต้นทางทั้งสองตัวของวันนั้น

```
08:37  Shopee Live + TikTok Live (งานนี้)
08:45  ยอดขายรายสินค้า  → เขียน TK_PROD_DATA ของเมื่อวาน
09:47  Ads รายวัน       → เขียน tk_ads.live ของเมื่อวาน
19:37  Shopee Live + TikTok Live (งานนี้)  ← รอบนี้ได้ข้อมูลเมื่อวานครบ
```

ผลที่ถูกต้องคือ:
- **รอบเช้า 08:37 มักได้ `NO_CHANGE`** เพราะต้นทางยังเป็นข้อมูลถึงวันก่อนหน้า
  **นี่ไม่ใช่ error ห้ามไปไล่หาสาเหตุหรือแก้สคริปต์** รายงานแล้วจบรอบได้เลย
- **รอบเย็น 19:37 จะเติมข้อมูลของเมื่อวาน** เพราะผ่านงาน 08:45 และ 09:47 มาแล้ว

สคริปต์สแกนทุกวันใหม่ทุกรอบและเติมเฉพาะวันที่ขาด ต่อให้รอบไหนพลาดไป
รอบถัดไปจะตามเก็บให้เองเสมอ ไม่มีวันไหนหลุดถาวร

---

## ขั้นที่ 1 — ดูก่อนว่าจะเปลี่ยนอะไร

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/tiktok_live_daily.py" --dry-run
```

ดูที่ `added` ควรมีวันเมื่อวาน · `changed` ที่เป็นการเติมช่อง `adsCost`/`adsRev`
ของวันที่เคยเป็น 0 เป็นเรื่องปกติ (ค่าโฆษณาเข้าช้ากว่ายอดขาย)
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน ห้ามแก้ตัวเลขเอง**

## ขั้นที่ 2 — รันจริง + commit

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/tiktok_live_daily.py"
```

exit `0` = อัปเดต + bump sw.js แล้ว · `10` = ไม่มีอะไรเปลี่ยน (ไม่ต้อง commit) · `2` = ไม่ผ่านด่าน

เฉพาะตอน exit 0:

```bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" && git add WIBWUB_Dashboard.html sw.js
```

```bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" && git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" commit -m "auto-update: TikTok Live รายวัน $(date +%Y-%m-%d)"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที
`git add` **เฉพาะ 2 ไฟล์นี้** — รีโปนี้มีงานอื่นทำงานพร้อมกัน ไฟล์ dirty ที่เหลือเป็นของคนอื่น
ถ้า git ติด `index.lock`: รอ 20 วินาทีแล้วลองใหม่ สูงสุด 3 ครั้ง **ห้ามลบ lock ของคนอื่น**

---

## RULES

- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง ห้ามกรอกค่าสมมุติ
- **ห้ามแก้ค่าโฆษณาของวันที่มีข้อมูลอยู่แล้ว** — ช่วง เม.ย.–ส.ค. มาจาก export แคมเปญ
  รายไลฟ์ ซึ่งตัวเลขไม่ตรงกับ `ads_daily.json` เป๊ะ ๆ (เช่น 15 ส.ค. 585.62 vs 185.62)
  นั่นคือคนละแหล่ง ไม่ใช่ข้อมูลอัปเดต สคริปต์กันไว้แล้ว อย่าปลดด่านนี้
- ยอดขายไลฟ์โตขึ้นได้ตามเวลา (ออเดอร์ทยอยยืนยัน) แต่ **ห้ามถอยลง** สคริปต์ข้ามให้เอง
- `adsCampaigns` (จำนวนแคมเปญ) ไม่มีเก็บรายวัน หน้าเว็บจะขึ้น `–` ในช่องนั้น
  **ห้ามเดาใส่ 1** เพราะหน้าเว็บใช้ `adsCost`/`adsRev` เป็นตัวตัดสินว่ามีโฆษณาหรือไม่แล้ว
- ถ้าต้องแก้วิธีคำนวณหรือลำดับคอลัมน์ ให้แก้ `scripts/tiktok_live_daily.py` ที่เดียว
- `grep -oP`, `sed -i "s/.../"`, `find -newermt` เป็น GNU-only **พังบน macOS** ห้ามใช้

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

วันที่เพิ่มเข้าไป + ยอดไลฟ์/ค่าโฆษณาของวันนั้น, จำนวนวันทั้งหมดและวันที่มีไลฟ์,
รายการที่ถูกข้าม, commit id หรือ "ไม่มีข้อมูลใหม่", error ถ้ามี

---

## 🚨 ทำงานไม่ได้ = ต้องรายงานว่าล้มเหลว ห้ามขึ้นว่าสำเร็จ

**กรณีที่ถือว่าล้มเหลว**

1. **เข้าโฟลเดอร์ All ไม่ได้** (ขั้น 0 ไม่เจอพาธ)
2. **เปิดเว็บไม่ได้** — `navigate`/`browser_batch` คืนข้อความใดข้อความหนึ่งนี้
   - `The approval prompt for this browser action went unanswered for 5 minutes` (กล่องขออนุญาตไม่มีคนกด)
   - `Navigation to this domain is not allowed` (สิทธิ์โดเมนถูกปฏิเสธ)
   - `Tab ... is not in Claude's tab group` / เชื่อมต่อส่วนขยายไม่ได้
3. **สคริปต์ที่พรอมป์ระบุหายหรือพัง**

**สิ่งที่ต้องทำเมื่อล้มเหลว**

1. **ลองครั้งเดียวพอ ห้ามวนลองซ้ำ** — เคยเสียเวลา 5 นาทีต่อหนึ่งเว็บโดยไม่ได้อะไร
   (22 ต.ค. 69 งาน HR ลองทั้ง `browser_batch` และ `javascript_tool` ตรงไปที่แท็บที่ล็อกอินค้างอยู่
   ก็โดนกล่องเดียวกันทั้งคู่ — แท็บที่เปิดค้างไว้ช่วยไม่ได้)
2. ปิดแท็บที่เปิดไว้ด้วย `tabs_close_mcp`
3. จบงานโดยขึ้นต้นบรรทัดแรกด้วย
   `❌ ล้มเหลว — <สาเหตุสั้น ๆ> ไม่ได้ข้อมูลใหม่รอบนี้`
   แล้วบอกด้วยว่าข้อมูลล่าสุดในไฟล์อยู่ถึงวันไหน

**ห้ามทำเด็ดขาด**

- ❌ ห้ามหันไปใช้ไฟล์เก่าแล้วรายงานว่า "สำเร็จ" — ถ้าดึงของใหม่ไม่ได้ ถือว่าล้มเหลว
- ❌ ห้ามเขียน ✅ หรือคำว่า "เสร็จ/สำเร็จ/OK" เมื่อขั้นใดขั้นหนึ่งข้างบนไม่ผ่าน
- ❌ ห้ามเดาตัวเลข หรือคัดลอกตัวเลขจากรอบก่อนมาใส่

> ใช้ไฟล์เดิมได้เฉพาะกรณีที่พรอมป์ระบุไว้ชัดเจนว่าเป็นทางสำรองที่ยอมรับได้
> (เช่น ads-daily ใช้ `work/*.json` ที่ครอบช่วง `from→to` พอดี) และต้อง**รายงานตรง ๆ
> ว่ารอบนี้ใช้ของเดิม ไม่ได้ดึงใหม่**

---

## 🚫 กฎคำสั่ง shell (ทุกงาน — รวมคำสั่งที่คิดขึ้นเองระหว่างรัน)

งานตั้งเวลา **ไม่มีคนนั่งกดอนุญาต** ถ้าคำสั่งไม่แมตช์กฎที่อนุญาตไว้แล้ว
(`Bash(python3 *)` / `Bash(git *)` / `Bash(ls *)` ฯลฯ) งานจะค้างทั้งรอบ
สังเกตง่าย ๆ: ถ้ากล่องขออนุญาตมีแค่ปุ่ม **"Allow once"** โดยไม่มี "Always allow"
แปลว่าคำสั่งนั้นสร้างกฎถาวรไม่ได้ จะถามใหม่ทุกครั้งตลอดไป

**เขียนคำสั่งให้เรียบง่ายที่สุด — 1 คำสั่ง = 1 โปรแกรม + พาธเต็ม**

| ❌ ห้าม | เหตุผลที่โดนถาม | ✅ ใช้แบบนี้ |
|---|---|---|
| `git -C "<path>" ...` | **ห้ามใช้** — กฎ deny จับจากคำขึ้นต้น `git push` จึงกัน `git -C <path> push` ไม่ได้ = เปิดช่องให้ push หลุด | `cd "<path เต็ม>" && git status` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion สร้างกฎถาวรไม่ได้ | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for d in ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขใน bash ก็เข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python แล้วเรียกไฟล์นั้น |
| `cmd1; cmd2; cmd3` ต่อกันยาว ๆ | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |

**ถ้าต้องมีตรรกะ (วนลูป / เช็คเงื่อนไข / ประกอบพาธ): เขียนเป็นสคริปต์ python
ไว้ใน `scripts/` แล้วเรียกด้วยพาธเต็ม** เช่น `python3 "<path เต็ม>/scripts/ads/check_downloads.py" tiktok`
วิธีนี้ทั้งอ่านง่ายกว่า ทดสอบแยกได้ และไม่ติดกำแพงสิทธิ์
