## 🧹 ปิดแท็บ Chrome เมื่อจบงาน (ทำทุกครั้ง)
ก่อนจบงาน ไม่ว่าจะสำเร็จ ไม่มีข้อมูลใหม่ หรือเจอ error: เรียก `tabs_context_mcp` ดู tabId ทั้งหมดในกลุ่มแท็บของรอบนี้ แล้วปิดทุกแท็บด้วย `tabs_close_mcp` (ยกเว้นหน้าที่ต้องให้ผู้ใช้ login เอง ให้เหลือแท็บนั้นแท็บเดียวและบอกในรายงาน)

## WIBWUB Ads Dashboard — เติมข้อมูลรายวัน "ยอดขายจริง vs ยอดจาก Ads" + แคมเปญย่อย TikTok GMV Max

หน้าเว็บ `data Ads/WIBWUB_Ads_Dashboard_new.html` อ่านข้อมูลจาก `data Ads/ads_daily.json` (รายวัน — Shopee/TikTok/Lazada), `data Ads/ads_periods.json` (รายเดือน) และ `data Ads/ads_tk_campaigns.json` (แคมเปญย่อย GMV Max) งานนี้ทำให้ไฟล์เหล่านี้ทันสมัยถึง "เมื่อวาน" — ห้ามแก้ HTML

### ขั้น 0 — หาโฟลเดอร์ All (สำคัญ)
ใน shell ให้หาโฟลเดอร์ All ที่เชื่อมไว้กับงานนี้ ตามลำดับ:
`for d in "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" "$HOME/mnt/All" /sessions/*/mnt/All; do [ -f "$d/scripts/ads/ads_daily_update.py" ] && echo "$d" && break; done`
ใช้ผลลัพธ์เป็น `BASE` ในทุกคำสั่ง ถ้าไม่เจอ หรือ shell ตอบว่า "No folders are connected": หยุดและรายงานทันทีว่าต้องเชื่อมโฟลเดอร์ All ให้งานนี้

สคริปต์: `scripts/ads/hook.js`, `scripts/ads/collect.js`, `scripts/ads/ads_daily_update.py`, `scripts/ads/sync_periods.js` — ถ้าหายหรือพัง ให้หยุดและรายงาน ห้ามเขียนวิธีอื่นเอง ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดหรือแก้เอง

### ขั้นตอน
1. `python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/ads_daily_update.py" state` → ได้ `from` และ `to` (ดึงซ้ำย้อนหลัง 3 วันเสมอ ตั้งใจให้เป็นแบบนั้น)
2. อ่านเนื้อหา `hook.js` และ `collect.js` ด้วย `cat` (ใช้วางใน javascript_tool แบบคัดลอกตรงตัว)
3. Chrome: `list_connected_browsers` แล้ว `select_browser` ตัวที่เป็น macOS เท่านั้น (deviceId ปกติคือ b75a6bb0-5b78-4e44-92a8-75224f1ce4ee) → `tabs_context_mcp(createIfEmpty=true)` ใช้ `browser_batch` เสมอ ห้าม navigate เดี่ยว ห้าม wait เกิน 10 วิ
4. แต่ละ kind: navigate → วาง hook.js ทันที → รอหน้าโหลด → เช็คว่า `window.__cap` มี request ที่ต้องใช้ (ดูชื่อจาก `window.__cap.map(c=>c.u.split('?')[0].split('/').pop())`) ถ้ายังไม่มี ให้กดตามวิธีสำรองด้านล่าง → วาง `window.__ADS={kind:'<kind>',from:'<from>',to:'<to>'};` ตามด้วยเนื้อหา collect.js → poll `window.__adsJob` จน `done:true` (ต้องไม่มี `err`) → อ่าน `window.__adsExport(0,900)`, `(900,1800)`, `(1800,2700)`… จนครบ `__adsJob.len` (ผลของ javascript_tool ถูกตัดที่ ~1000 ตัวอักษร ห้ามอ่านทีละมากกว่า 900) → ต่อกันแล้วบันทึกเป็นไฟล์ `scripts/ads/work/<kind>.json` ด้วย heredoc คัดลอกตรงตัว
   - `sh_real` (ต้องมี key-metrics): https://seller.shopee.co.th/datacenter/overview — สำรอง: เปิด dropdown ช่วงเวลาแล้วเลือก "เมื่อวาน"
   - `sh_ads` (ต้องมี get_time_graph): https://seller.shopee.co.th/portal/marketing/pas/index — สำรอง: รีโหลดหน้าแล้ววาง hook.js ใหม่ทันที
   - `tk_real` (ต้องมี us_overview_day_trend): https://seller-th.tiktok.com/compass/data-overview — ต้องกดช่อง "วันที่เริ่มต้น" แล้วเลือก "7 วันที่ผ่านมา" เสมอ (ใช้ find หา element)
   - `tk_ads` (ต้องมี post_overview_stat) และ `tk_camp` (ต้องมี post_campaign_list_v2) ทำในหน้าเดียวกัน: https://ads.tiktok.com/i18n/gmv-max/dashboard?aadvid=7229166192752148482&oec_seller_id=7494549095358892612&bc_id=7229165256428240898&type=product — ถ้าไม่มี post_overview_stat ให้กดปุ่มรีเฟรช (ไอคอนไม่มีชื่อ ถัดจากช่องวันที่ของ Campaign list ใช้ find); ถ้าไม่มี post_campaign_list_v2 ให้กดแท็บ "LIVE GMV Max" ในส่วน Campaign list — รัน `tk_ads` ก่อน แล้วรัน `tk_camp` ในหน้าเดิม
   - `lz_real` และ `lz_ads` (**Lazada — ไม่ต้องใช้ hook.js เลย** ยิง fetch same-origin ตรงได้ ไม่มี signature):
     · `lz_real`: เปิด https://sellercenter.lazada.co.th/ba/dashboard ก่อน แล้ววาง `window.__ADS={kind:'lz_real',...}` + collect.js
     · `lz_ads`: เปิด https://sellercenter.lazada.co.th/sponsor/solutions/ads/productads/#!/overview ก่อน แล้ววาง `window.__ADS={kind:'lz_ads',...}` + collect.js
     · หน้า Ads มีป๊อปอัปหลายอัน (แคมเปญ 11.11 / เติมเงิน) — **กด X หรือ Escape ปิดเท่านั้น ห้ามกด "เข้าร่วมเลย" / "เติมยอด" / เปลี่ยน ROAS** · ป๊อปอัปไม่บล็อก fetch ถ้าปิดไม่ได้ก็ดึงข้อมูลต่อได้
     · ค่า spend = 0 เป็นค่าจริงได้ (กระเป๋าเงิน Ads ติดลบ แคมเปญหยุด) ไม่ใช่ bug — ดูที่ `imp` ถ้ายังมีเลขน้อย ๆ แปลว่าแคมเปญหยุดจริง
     · **ก่อนดึง Lazada ให้ดูก่อนว่ามีของสดอยู่แล้วไหม** งาน `wibwub-lazada-collect`
       รอบ 08:25/19:25 เขียน `work/lz_real.json` + `work/lz_ads.json` ไว้ให้แล้ว
       ถ้าสองไฟล์นี้ถูกแก้ไขภายใน ~3 ชั่วโมงที่ผ่านมาและครอบคลุมช่วง `from`→`to`
       **ให้ใช้ของเดิมเลย ข้ามการเปิด Chrome ไปหา Lazada** (เช็คด้วย `ls -l work/`)
       จะได้ไม่ต้องเสี่ยงว่า session หลุดไปแล้วในรอบนี้
     · **Lazada เป็นออปชัน** ถ้าดึงไม่ได้ (login หลุด / endpoint เปลี่ยน) ให้ข้ามไป merge เฉพาะ Shopee/TikTok แล้วรายงานว่า Lazada ล้มเพราะอะไร — ข้อมูล Lazada เดิมในไฟล์จะไม่ถูกลบ
     · **ห้ามกรอกรหัสผ่าน และห้ามกดปุ่มเข้าสู่ระบบ Lazada** แม้ช่องจะถูกกรอกไว้ให้แล้วก็ตาม
   - ถ้าหน้าใดขึ้นหน้า login: หยุดและรายงาน ห้ามกรอกรหัสผ่าน · ห้ามเดา/สร้าง signature หรือ token เอง ใช้เฉพาะ request ที่ hook จับได้
**4.9 ด่านก่อน merge — พิมพ์ตารางความครอบคลุมเสมอ (เพิ่ม 27 ต.ค. 69)**

```bash
python3 -c "
import json,glob,os,time
for k in ['sh_real','sh_ads','tk_real','tk_ads','lz_real','lz_ads']:
    f='work/%s.json'%k
    if not os.path.exists(f): print(k.ljust(8),'— ไม่มีไฟล์'); continue
    d=json.load(open(f)); ds=sorted(d['data'])
    age=(time.time()-os.path.getmtime(f))/60
    print(k.ljust(8), ds[0],'->',ds[-1], '(%d วัน, ไฟล์อายุ %.0f นาที)'%(len(ds),age))
"
```

ให้วางตารางนี้ลงในรายงานท้ายรอบทุกครั้ง **ไม่ว่าจะ merge สำเร็จหรือไม่**

- ถ้า 4 ชุดบังคับ (`sh_real`/`sh_ads`/`tk_real`/`tk_ads`) ครอบคลุมวันไม่ตรงกัน **merge จะ exit error ทันที**
  (ด่าน `ads_daily_update.py` บรรทัด `บางชุดขาดวันที่`) ห้ามแก้ด้วยการตัดวันหรือใช้ไฟล์เก่า
  ให้รายงานตรง ๆ ว่า **`ชุด <kind> มีถึง <วัน> → วันที่ <วัน> ถูกตัดทิ้งทั้งแถว`**
  แล้วบอกว่าต้องดึงชุดไหนใหม่ถึงจะเติมวันนั้นได้
- **ห้ามเขียนว่า "ถึง <วัน>" เฉย ๆ** ถ้า merge ไม่ได้รันหรือไม่ได้เพิ่มวันใหม่ —
  ตัวเลขนั้นคือวันสูงสุดที่อยู่ในไฟล์มาก่อนแล้ว ไม่ใช่ผลของรอบนี้
  (27 ต.ค. 69: commit `67c564c` เขียน "ถึง 2026-10-25" ทั้งที่ merge ไม่ได้รันเลย
   แตะแค่ ads_periods/ads_tk_campaigns/sw.js — ไม่มีใครรู้ว่าวันที่ 26 หายไปจนผู้ใช้มาเจอเอง
   ตอนนี้ `ads_daily_update.py commit` แยกข้อความ 2 แบบให้แล้ว แต่รายงานของเอเจนต์ต้องตรงกันด้วย)

5. `python3 ads_daily_update.py merge work/sh_real.json work/sh_ads.json work/tk_real.json work/tk_ads.json work/lz_real.json work/lz_ads.json`
   (ถ้า Lazada ล้ม ให้ตัด 2 ไฟล์ท้ายออก — สคริปต์รับ Lazada แบบไม่บังคับ แต่ถ้าจะใส่ต้องใส่ทั้งคู่) — exit 10 = ข้อมูลรายวันไม่เปลี่ยน (ทำขั้นต่อไปได้) · ถ้า error ว่าขาดวันที่/ค่าติดลบ: หยุดและรายงาน ห้ามเขียนไฟล์เอง
6. `python3 ads_daily_update.py camp work/tk_camp.json` — exit 10 = แคมเปญไม่เปลี่ยน · ถ้า error ว่าผลรวมไม่ตรงหรือมีมากกว่า 100 แคมเปญ: รายงาน (ขั้นอื่นทำต่อได้)
7. `python3 ads_daily_update.py commit` — sync รายเดือน + bump sw.js + commit เฉพาะไฟล์ Ads (exit 10 = ไม่มีอะไรเปลี่ยน) · auto-push จะ push เอง ไม่ต้อง push
   - ถ้า git ล็อกค้าง ให้ย้ายไป .git/stale-* (ห้ามลบไฟล์): `for f in HEAD.lock objects/maintenance.lock index.lock; do [ -e "$BASE/.git/$f" ] && mv "$BASE/.git/$f" "$BASE/.git/stale-$(date +%s)-$(basename $f)"; done`

8. **เมนู "การตลาด vs ยอดขาย"** — ทำต่อทุกครั้งหลังขั้น 7 (ไม่ว่าขั้น 7 จะ exit 0 หรือ 10):
```bash
cd "$BASE"
python3 scripts/marketing/kol_fetch.py          # ดึงยอด KOL จากชีต -> data Ads/kol_monthly.json
python3 scripts/marketing/marketing_update.py   # รวม Ads + KOL + ยอดขาย -> เขียนลง 2 หน้า
```
   exit `0` = อัปเดตแล้ว · `10` = ไม่มีอะไรเปลี่ยน (ทั้งคู่ถือว่าผ่าน) · `2` = ไม่ผ่านด่านตรวจ ให้รายงานแล้วไปต่อ
   ถ้ามีไฟล์เปลี่ยน ให้ commit:
```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" add "data Ads/kol_monthly.json" WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: การตลาด vs ยอดขาย $(date +%Y-%m-%d)"
```
   > ⚠️ ชีต KOL (`1NEkm1bcHvXO0Ehs6cwaNDkBUUM1A9assALMp5V7S7lo`) มีชื่อ-นามสกุล เลขบัตรประชาชน
   > เลขบัญชีธนาคาร ที่อยู่ เบอร์โทร — **`kol_fetch.py` อ่านแค่ 4 คอลัมน์และเขียนออกเป็นผลรวมรายเดือนเท่านั้น**
   > ห้ามเปิดชีตนี้ด้วยวิธีอื่น ห้ามนำแถวรายบุคคลขึ้นหน้าเว็บ และห้าม commit อะไรที่มีข้อมูลส่วนบุคคล
   > ถ้า `kol_fetch.py` พัง: รายงานแล้วข้าม — ห้าม copy ตัวเลขจากชีตมาใส่มือ

### สรุปท้ายรอบ (สั้นๆ ภาษาไทย)
ช่วงวันที่ที่ดึง, วันที่ที่เพิ่ม/เปลี่ยน (จาก `changed`), ยอดเดือนนี้ถึงวันล่าสุด: Shopee ยอดจริง / ค่าโฆษณา, TikTok ยอดจริง / ค่าโฆษณา, Lazada ยอดจริง / ค่าโฆษณา (จาก `month_to_date` — คีย์ `lz_real` / `lz_spend`), จำนวนแคมเปญ GMV Max และค่าโฆษณารวม, คำเตือนถ้ามี, commit id หรือ "ไม่มีข้อมูลใหม่", และ error ถ้ามี

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
| `git ...` ทุกรูปแบบ | `git -C` เปิดช่องให้ push หลุด · `cd ... && git` ขึ้นต้นด้วย cd จึงไม่แมตช์กฎ `Bash(git add:*)` → งานค้างรออนุญาต | `python3 "<BASE>/scripts/gitw.py" add/commit/status/log` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion สร้างกฎถาวรไม่ได้ | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for d in ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขใน bash ก็เข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python แล้วเรียกไฟล์นั้น |
| `cmd1; cmd2; cmd3` ต่อกันยาว ๆ | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |

**ถ้าต้องมีตรรกะ (วนลูป / เช็คเงื่อนไข / ประกอบพาธ): เขียนเป็นสคริปต์ python
ไว้ใน `scripts/` แล้วเรียกด้วยพาธเต็ม** เช่น `python3 "<path เต็ม>/scripts/ads/check_downloads.py" tiktok`
วิธีนี้ทั้งอ่านง่ายกว่า ทดสอบแยกได้ และไม่ติดกำแพงสิทธิ์
