---
name: wibwub-download-shopee-ads
description: ดาวน์โหลด Shopee Ads CSV ทุกวัน 08:00/19:00 → บันทึกใน data Ads/Shopee/
---

ดาวน์โหลดรายงาน Shopee Ads CSV ล่าสุดเข้าโฟลเดอร์ data Ads/Shopee/ 

## URL ที่ถูกต้อง (Shopee เปลี่ยน URL structure แล้ว)
- ✅ ใช้ได้: https://seller.shopee.co.th/portal/marketing/pas/index
- ❌ ใช้ไม่ได้: /portal/marketing/ads, /portal/download-centre, /portal/marketing/shopee-ads/report

## ขั้นตอน

1. ⚠️ **ต้องระบุ browser ที่ Mac เสมอ ห้ามปล่อยให้เลือกอัตโนมัติ**:
   `select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")` แล้วค่อย **เปิด Chrome tab** ด้วย tabs_context_mcp(createIfEmpty=true)
   (ถ้า deviceId นี้ไม่ connected แล้ว ให้เรียก `list_connected_browsers` ก่อน แล้วเลือกตัวที่ `osPlatform` เป็น macOS / `isLocal:true` เท่านั้น — ห้ามเลือก Windows/PC)

2. **Navigate ไป Shopee Ads** ด้วย browser_batch:
   - URL: https://seller.shopee.co.th/portal/marketing/pas/index
   - wait 5 วินาที → screenshot
   - ตรวจ: URL ต้องมี `/portal/marketing/pas/` ไม่ใช่ `/404`
   - ถ้า `/404`: navigate ไป https://seller.shopee.co.th แล้ว navigate อีกครั้ง

3. **ปิด popup** ถ้ามี:
   ```javascript
   document.querySelectorAll('[class*="modal"],[class*="popup"]').forEach(m=>m.style.display='none');
   document.querySelectorAll('[class*="close"]').forEach(b=>b.click());
   ```

4. **Scroll ลง** ประมาณ 400px เพื่อหา "สถิติโฆษณา CPC ทั้งหมด"

5. **คลิก "ดาวน์โหลดข้อมูล"** (ใช้ find tool หา button ชื่อ "ดาวน์โหลดข้อมูล")

6. **เลือก "ภาพรวมข้อมูลโฆษณา"** จาก dropdown

7. **เปิด panel "รายงานล่าสุด"** — ⚠️ dialog ไม่ได้เปิดแบบ inline อัตโนมัติ ต้องคลิกไอคอน "≡" (สามขีด/รายการ) เพื่อเปิด side panel ที่แสดงรายการ report ที่กำลังสร้าง/พร้อมแล้ว รอ report พร้อม (จาก "กำลังดำเนินการ" → "ดาวน์โหลด") ≈10 วินาที

8. **⚠️ ห้ามคลิกปุ่ม "ดาวน์โหลด" ของ Shopee ตรงๆ — ROOT CAUSE ที่แก้แล้ว:**
   ปุ่ม "ดาวน์โหลด" ของเว็บ Shopee เรียก `window.open(downloadUrl,'_blank')` ภายใน ซึ่งจะถูก **popup blocker ของ Chrome บล็อกแบบเงียบๆ** เมื่อคลิกผ่าน browser automation (ไม่ error, ไม่มี dialog, ไฟล์ไม่ลงเลย) — นี่คือสาเหตุหลักที่ pipeline นี้ล้มเหลวมานาน

   **วิธีที่ถูกต้อง (bypass ปุ่ม native):**
   1. หา `download_url` ของ report ที่พร้อมแล้ว — ดักจาก network request (patch `XMLHttpRequest.prototype.open`/`.send()` เพราะเว็บ Shopee ใช้ XHR ไม่ใช่ `fetch`) หรือคลิกแถว report แล้วดู request `get_download_url` ที่ยิงออกไป
   2. Fetch เนื้อหาไฟล์ตรงๆ ด้วย credentials (ไม่ใช้ `window.open`/`location.href` เพราะ endpoint อาจตอบ 503 ชั่วคราว ให้ retry ด้วย export_id ใหม่ถ้าเจอ):
      ```javascript
      fetch(downloadUrl, {credentials:'include'}).then(r => r.text()).then(text => {
        window.__csvText = text;
        const blob = new Blob([text], {type:'text/csv;charset=utf-8'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ข้อมูล-Shopee-Ads-DD_MM_YYYY-DD_MM_YYYY.csv'; // ชื่อไฟล์ต้องตรงรูปแบบจริง
        document.body.appendChild(a);
        a.click();
        setTimeout(() => { document.body.removeChild(a); URL.revokeObjectURL(url); }, 1000);
        window.__downloadDone = true;
      });
      ```
   3. การสร้าง `<a download>` แล้ว `.click()` แบบนี้ **ไม่ถูก popup blocker บล็อก** (ต่างจาก `window.open`) → เป็น native browser download จริง

9. **รอไฟล์ลง Downloads แล้วให้ LaunchAgent ย้ายไฟล์ — ⚠️ ใช้เวลานานกว่าปกติ**
   หลัง `.click()` ไฟล์อาจไม่ปรากฏใน Downloads ทันที (เคยพบว่าใช้เวลานานถึง 5-10+ นาทีกว่า `com.wibwub.download-mover` LaunchAgent จะย้ายไฟล์ไปโฟลเดอร์ปลายทาง) — **ห้าม fail fast** ถ้าเช็คครั้งแรกหลัง wait ไม่กี่วินาทีแล้วไม่เจอไฟล์ ให้ retry เช็คซ้ำเป็นระยะ (เช่นทุก 30-60 วินาที นานสุด ~10 นาที) ก่อนสรุปว่าล้มเหลว:
   ```bash
   # เช็คซ้ำเป็นระยะจนกว่าจะเจอไฟล์ใหม่ใน destination folder โดยตรง (ไม่ใช่แค่ Downloads)
   ls -la "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data Ads/Shopee/" | tail -5
   ```

10. **บันทึกไฟล์** (ถ้า LaunchAgent ยังไม่ย้ายไฟล์ให้ หรือต้องการ fallback):
   ```bash
   NEW_CSV=$(ls -t /Users/thanasablilutanon/Downloads/ข้อมูล-Shopee-Ads-*.csv 2>/dev/null | head -1)
   if [ -n "$NEW_CSV" ]; then
     cp "$NEW_CSV" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data Ads/Shopee/"
     echo "✅ Saved: $NEW_CSV"
   else
     echo "❌ No new CSV found — เช็ค destination folder ตรงๆ ด้วย อาจถูก LaunchAgent ย้ายไปแล้ว"
   fi
   ```
   หมายเหตุ: `<mnt>` คือ sandbox mount prefix ของ session นั้นๆ (เปลี่ยนทุกครั้งที่ session ใหม่ เช่น `nifty-friendly-thompson`, `hopeful-serene-fermi`) — เช็คด้วย `pwd`/list ก่อนใช้จริง

11. **รายงานผล**: แจ้งชื่อไฟล์ที่ดาวน์โหลด และ date range ที่ครอบคลุม

## ⚠️ ขั้นตอนที่ 12 (สำคัญ — ห้ามข้าม): อัปเดต WIBWUB_Ads_Dashboard.html หลังดาวน์โหลด

**Root cause ของปัญหาเดิม (พบ 2026-07-30):** Schedule นี้ดาวน์โหลดไฟล์ดิบเข้า `data Ads/Shopee/` เท่านั้น
ไม่เคย parse/อัปเดต `data Ads/WIBWUB_Ads_Dashboard.html` เอง ทำให้ Dashboard ค้างข้อมูลเก่าแม้ดาวน์โหลดไฟล์ใหม่ทุกวัน
→ ทุกครั้งที่ดาวน์โหลดไฟล์ CSV ใหม่เสร็จ (Step 11) ให้ทำต่อทันที ห้ามจบงานแค่ download:

1. อ่าน CSV ใหม่ล่าสุดใน `data Ads/Shopee/` (skip 7 header rows, header จริงอยู่แถวที่มี "ลำดับ")
   **Column index ที่ยืนยันแล้วถูกต้อง (ตรวจกับ header จริง 2026-07-30):**
   `11`=การมองเห็น(impressions), `12`=จำนวนคลิก(clicks), `16`=การสั่งซื้อ(orders),
   `24`=ยอดขาย(revenue), `26`=ค่าโฆษณา(spend), `27`=ROAS
   (อย่าเชื่อ column index เก่าที่เคยเขียนไว้ในเอกสารอื่น — เช็คกับ header แถวจริงทุกครั้งที่ Shopee เปลี่ยน format)
2. Sum เป็นยอดรวมเดือนปัจจุบัน + สร้าง top5/worst5/all campaign arrays (sort by spend/revenue ตามที่ dashboard ใช้)
3. แก้ `DATA_PERIODS.<เดือนปัจจุบัน>.shopee` ใน `data Ads/WIBWUB_Ads_Dashboard.html` ด้วยค่าใหม่ (ใช้ Python อ่าน/แทนที่ substring แบบ exact-match — ไฟล์นี้ minified บรรทัดเดียวยาวมาก อย่าใช้ Edit tool บรรทัดปกติ)
4. อัปเดต `SH_ADS[idx]` ใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` ให้ตรงกับ spend เดือนปัจจุบัน (idx นับจาก array `M5`)
5. อัปเดต badge `#ads-updated` และ `.pb-sub` labels ให้ตรงกับวันที่ข้อมูลล่าสุดจริง (ห้ามปล่อยข้อความเดิมที่อ้างวันที่เก่า)
6. Validate JS (`node --check` หลัง extract `<script>` blocks), bump `sw.js` cache version, `git add`+`git commit` (push ต้องให้ user double-click `push_now.command`)

## หมายเหตุ
- ไฟล์ชื่อ `ข้อมูล-Shopee-Ads-DD_MM_YYYY-DD_MM_YYYY.csv`
- ถ้า login หมดอายุ: หยุดและรายงาน "ต้องการ login Shopee Seller Centre"
- Paths: workspace=/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/, downloads=/Users/thanasablilutanon/Downloads/ (mount prefix เปลี่ยนทุก session)
- **ROOT CAUSE ของปัญหาเดิม (แก้แล้ว 2026-07-20):** ปุ่ม "ดาวน์โหลด" ของ Shopee ใช้ `window.open()` ซึ่งโดน popup blocker บล็อกเงียบๆ เมื่อคลิกผ่าน automation → ใช้วิธี fetch+Blob+`<a download>`.click() แทน (ดู Step 8)
- `direct_download` API endpoint อาจตอบ 503 ชั่วคราว — ถ้าเจอให้คลิก report แถวอื่น/ใหม่เพื่อได้ export_id/download_url ใหม่แล้ว retry
- Content filter ของ javascript_tool จะ block ข้อมูลที่หน้าตาเหมือน cookie/query string — อย่า return raw URL ที่มี token หรือ raw headers ทั้งก้อน ให้ derive/filter ก่อน return
- ผลลัพธ์จาก javascript_tool ถูก truncate ที่ ~900-1000 ตัวอักษร — ถ้าต้องการ string ยาวๆ ให้ slice เป็นก้อนละ ~800 ตัวอักษรแล้ว relay หลายรอบ

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