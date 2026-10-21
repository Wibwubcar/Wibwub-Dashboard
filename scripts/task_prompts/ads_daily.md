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
     · **Lazada เป็นออปชัน** ถ้าดึงไม่ได้ (login หลุด / endpoint เปลี่ยน) ให้ข้ามไป merge เฉพาะ Shopee/TikTok แล้วรายงานว่า Lazada ล้มเพราะอะไร — ข้อมูล Lazada เดิมในไฟล์จะไม่ถูกลบ
   - ถ้าหน้าใดขึ้นหน้า login: หยุดและรายงาน ห้ามกรอกรหัสผ่าน · ห้ามเดา/สร้าง signature หรือ token เอง ใช้เฉพาะ request ที่ hook จับได้
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
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add "data Ads/kol_monthly.json" WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: การตลาด vs ยอดขาย $(date +%Y-%m-%d)"
```
   > ⚠️ ชีต KOL (`1NEkm1bcHvXO0Ehs6cwaNDkBUUM1A9assALMp5V7S7lo`) มีชื่อ-นามสกุล เลขบัตรประชาชน
   > เลขบัญชีธนาคาร ที่อยู่ เบอร์โทร — **`kol_fetch.py` อ่านแค่ 4 คอลัมน์และเขียนออกเป็นผลรวมรายเดือนเท่านั้น**
   > ห้ามเปิดชีตนี้ด้วยวิธีอื่น ห้ามนำแถวรายบุคคลขึ้นหน้าเว็บ และห้าม commit อะไรที่มีข้อมูลส่วนบุคคล
   > ถ้า `kol_fetch.py` พัง: รายงานแล้วข้าม — ห้าม copy ตัวเลขจากชีตมาใส่มือ

### สรุปท้ายรอบ (สั้นๆ ภาษาไทย)
ช่วงวันที่ที่ดึง, วันที่ที่เพิ่ม/เปลี่ยน (จาก `changed`), ยอดเดือนนี้ถึงวันล่าสุด: Shopee ยอดจริง / ค่าโฆษณา, TikTok ยอดจริง / ค่าโฆษณา, Lazada ยอดจริง / ค่าโฆษณา (จาก `month_to_date` — คีย์ `lz_real` / `lz_spend`), จำนวนแคมเปญ GMV Max และค่าโฆษณารวม, คำเตือนถ้ามี, commit id หรือ "ไม่มีข้อมูลใหม่", และ error ถ้ามี

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
