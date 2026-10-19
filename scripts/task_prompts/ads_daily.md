## 🧹 ปิดแท็บ Chrome เมื่อจบงาน (ทำทุกครั้ง)
ก่อนจบงาน ไม่ว่าจะสำเร็จ ไม่มีข้อมูลใหม่ หรือเจอ error: เรียก `tabs_context_mcp` ดู tabId ทั้งหมดในกลุ่มแท็บของรอบนี้ แล้วปิดทุกแท็บด้วย `tabs_close_mcp` (ยกเว้นหน้าที่ต้องให้ผู้ใช้ login เอง ให้เหลือแท็บนั้นแท็บเดียวและบอกในรายงาน)

## WIBWUB Ads Dashboard — เติมข้อมูลรายวัน "ยอดขายจริง vs ยอดจาก Ads" + แคมเปญย่อย TikTok GMV Max

หน้าเว็บ `data Ads/WIBWUB_Ads_Dashboard_new.html` อ่านข้อมูลจาก `data Ads/ads_daily.json` (รายวัน), `data Ads/ads_periods.json` (รายเดือน) และ `data Ads/ads_tk_campaigns.json` (แคมเปญย่อย GMV Max) งานนี้ทำให้ไฟล์เหล่านี้ทันสมัยถึง "เมื่อวาน" — ห้ามแก้ HTML

### ขั้น 0 — หาโฟลเดอร์ All (สำคัญ)
ใน shell ให้หาโฟลเดอร์ All ที่เชื่อมไว้กับงานนี้ ตามลำดับ:
`for d in "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" "$HOME/mnt/All" /sessions/*/mnt/All; do [ -f "$d/scripts/ads/ads_daily_update.py" ] && echo "$d" && break; done`
ใช้ผลลัพธ์เป็น `BASE` ในทุกคำสั่ง ถ้าไม่เจอ หรือ shell ตอบว่า "No folders are connected": หยุดและรายงานทันทีว่าต้องเชื่อมโฟลเดอร์ All ให้งานนี้

สคริปต์: `scripts/ads/hook.js`, `scripts/ads/collect.js`, `scripts/ads/ads_daily_update.py`, `scripts/ads/sync_periods.js` — ถ้าหายหรือพัง ให้หยุดและรายงาน ห้ามเขียนวิธีอื่นเอง ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดหรือแก้เอง

### ขั้นตอน
1. `cd "$BASE/scripts/ads" && python3 ads_daily_update.py state` → ได้ `from` และ `to` (ดึงซ้ำย้อนหลัง 3 วันเสมอ ตั้งใจให้เป็นแบบนั้น)
2. อ่านเนื้อหา `hook.js` และ `collect.js` ด้วย `cat` (ใช้วางใน javascript_tool แบบคัดลอกตรงตัว)
3. Chrome: `list_connected_browsers` แล้ว `select_browser` ตัวที่เป็น macOS เท่านั้น (deviceId ปกติคือ b75a6bb0-5b78-4e44-92a8-75224f1ce4ee) → `tabs_context_mcp(createIfEmpty=true)` ใช้ `browser_batch` เสมอ ห้าม navigate เดี่ยว ห้าม wait เกิน 10 วิ
4. แต่ละ kind: navigate → วาง hook.js ทันที → รอหน้าโหลด → เช็คว่า `window.__cap` มี request ที่ต้องใช้ (ดูชื่อจาก `window.__cap.map(c=>c.u.split('?')[0].split('/').pop())`) ถ้ายังไม่มี ให้กดตามวิธีสำรองด้านล่าง → วาง `window.__ADS={kind:'<kind>',from:'<from>',to:'<to>'};` ตามด้วยเนื้อหา collect.js → poll `window.__adsJob` จน `done:true` (ต้องไม่มี `err`) → อ่าน `window.__adsExport(0,900)`, `(900,1800)`, `(1800,2700)`… จนครบ `__adsJob.len` (ผลของ javascript_tool ถูกตัดที่ ~1000 ตัวอักษร ห้ามอ่านทีละมากกว่า 900) → ต่อกันแล้วบันทึกเป็นไฟล์ `scripts/ads/work/<kind>.json` ด้วย heredoc คัดลอกตรงตัว
   - `sh_real` (ต้องมี key-metrics): https://seller.shopee.co.th/datacenter/overview — สำรอง: เปิด dropdown ช่วงเวลาแล้วเลือก "เมื่อวาน"
   - `sh_ads` (ต้องมี get_time_graph): https://seller.shopee.co.th/portal/marketing/pas/index — สำรอง: รีโหลดหน้าแล้ววาง hook.js ใหม่ทันที
   - `tk_real` (ต้องมี us_overview_day_trend): https://seller-th.tiktok.com/compass/data-overview — ต้องกดช่อง "วันที่เริ่มต้น" แล้วเลือก "7 วันที่ผ่านมา" เสมอ (ใช้ find หา element)
   - `tk_ads` (ต้องมี post_overview_stat) และ `tk_camp` (ต้องมี post_campaign_list_v2) ทำในหน้าเดียวกัน: https://ads.tiktok.com/i18n/gmv-max/dashboard?aadvid=7229166192752148482&oec_seller_id=7494549095358892612&bc_id=7229165256428240898&type=product — ถ้าไม่มี post_overview_stat ให้กดปุ่มรีเฟรช (ไอคอนไม่มีชื่อ ถัดจากช่องวันที่ของ Campaign list ใช้ find); ถ้าไม่มี post_campaign_list_v2 ให้กดแท็บ "LIVE GMV Max" ในส่วน Campaign list — รัน `tk_ads` ก่อน แล้วรัน `tk_camp` ในหน้าเดิม
   - ถ้าหน้าใดขึ้นหน้า login: หยุดและรายงาน ห้ามกรอกรหัสผ่าน · ห้ามเดา/สร้าง signature หรือ token เอง ใช้เฉพาะ request ที่ hook จับได้
5. `python3 ads_daily_update.py merge work/sh_real.json work/sh_ads.json work/tk_real.json work/tk_ads.json` — exit 10 = ข้อมูลรายวันไม่เปลี่ยน (ทำขั้นต่อไปได้) · ถ้า error ว่าขาดวันที่/ค่าติดลบ: หยุดและรายงาน ห้ามเขียนไฟล์เอง
6. `python3 ads_daily_update.py camp work/tk_camp.json` — exit 10 = แคมเปญไม่เปลี่ยน · ถ้า error ว่าผลรวมไม่ตรงหรือมีมากกว่า 100 แคมเปญ: รายงาน (ขั้นอื่นทำต่อได้)
7. `python3 ads_daily_update.py commit` — sync รายเดือน + bump sw.js + commit เฉพาะไฟล์ Ads (exit 10 = ไม่มีอะไรเปลี่ยน) · auto-push จะ push เอง ไม่ต้อง push
   - ถ้า git ล็อกค้าง ให้ย้ายไป .git/stale-* (ห้ามลบไฟล์): `cd "$BASE" && for f in HEAD.lock objects/maintenance.lock index.lock; do [ -e .git/$f ] && mv .git/$f .git/stale-$(date +%s)-$(basename $f); done`

### สรุปท้ายรอบ (สั้นๆ ภาษาไทย)
ช่วงวันที่ที่ดึง, วันที่ที่เพิ่ม/เปลี่ยน (จาก `changed`), ยอดเดือนนี้ถึงวันล่าสุด: Shopee ยอดจริง / ค่าโฆษณา, TikTok ยอดจริง / ค่าโฆษณา (จาก `month_to_date`), จำนวนแคมเปญ GMV Max และค่าโฆษณารวม, คำเตือนถ้ามี, commit id หรือ "ไม่มีข้อมูลใหม่", และ error ถ้ามี
