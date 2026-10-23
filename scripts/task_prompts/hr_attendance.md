## 🧹 ปิดแท็บ Chrome เมื่อจบงาน (ทำทุกครั้ง)
ก่อนจบงาน ไม่ว่าจะสำเร็จ ไม่มีข้อมูลใหม่ หรือเจอ error: เรียก `tabs_context_mcp` ดู tabId ทั้งหมดในกลุ่มแท็บของรอบนี้ แล้วปิดทุกแท็บด้วย `tabs_close_mcp` จนกลุ่มแท็บหายไป (ยกเว้นหน้าที่ต้องให้ผู้ใช้ login เอง ให้เหลือแท็บนั้นแท็บเดียวและบอกในรายงาน)

## WIBWUB HR — อัปเดตเข้า-ออกงานจาก Discord (ดึงต่อจากรอบก่อน + การลา + รายงานการผลิต)

ใช้สกิล **wibwub-hr-attendance** เป็นคู่มือหลัก อ่านสกิลก่อนเริ่มทุกครั้ง แล้วทำตาม "Standard run" ในสกิลทีละขั้นจนครบ ตัวเลขทุกอย่างให้สคริปต์คำนวณ ห้ามคิดเอง

### ขั้น 0 — หาโฟลเดอร์ All (สำคัญ)
`for d in "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" "$HOME/mnt/All" /sessions/*/mnt/All; do [ -f "$d/scripts/hr/hr_update.py" ] && echo "$d" && break; done`
ใช้ผลลัพธ์เป็น `BASE` ถ้าไม่เจอ หรือ shell ตอบว่า "No folders are connected": หยุดและรายงานทันทีว่าต้องเชื่อมโฟลเดอร์ All ให้งานนี้
สคริปต์: `scripts/hr/hr_update.py`, `hr_scrape.js`, `hr_leave_scrape.js`, `hr_prod_scrape.js`

### ขั้นตอนย่อ
1. `python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/hr/hr_update.py" state` → ได้ `since` และ `scrape_params` (ถ้า `new_month: true` ทำหัวข้อ "Month change" ในสกิลก่อน)
2. ดึงห้อง #บันทึกเข้างาน และ #บันทึกออกงาน **เฉพาะตั้งแต่วัน `since`** ด้วย `hr_scrape.js` (อ่านด้วย `cat` แล้ววางใน javascript_tool ต่อจาก `window.__HR={key,cur,prev,since}`) poll `window.__job` จนได้ `done:true, unparsed:0, reachedStart:true`
3. บันทึกบรรทัดลง `work/new_in.txt` / `work/new_out.txt` (heredoc คัดลอกตรงตัว)
3b. **การลา:** เปิด https://discord.com/channels/1331888082802315295/1331942184739667979 แล้ววาง `window.__LVP={sinceTs:'<leave_params.sinceTs>'}` ตามด้วย `hr_leave_scrape.js` → poll `window.__lj` จน `done:true` (ไม่มี `err`) → export `window.__lvExport(0,40)`, `(40,80)`… → บันทึก `work/new_leave.txt`
3c. **รายงานการผลิต:** เปิด https://discord.com/channels/1331888082802315295/1392059303669792889 แล้ววาง `window.__PRP={sinceTs:'<prod_params.sinceTs>'}` ตามด้วย `hr_prod_scrape.js` → poll `window.__pj` จน `done:true` → export `window.__prExport(0,10)`, `(10,20)`… → บันทึก `work/new_prod.txt`
4. `python3 hr_update.py merge --in work/new_in.txt --out work/new_out.txt --since <since>` — exit 10 = ไม่มีใหม่ · exit 3 = ดึงใหม่ทั้งเดือน `since:1` แล้ว `merge --full` · exit 4 = ดึงใหม่
4b. `python3 hr_update.py leave --in work/new_leave.txt` — exit 10 = ไม่เปลี่ยน · มี `warnings` ให้ใส่ในรายงาน
4c. `python3 hr_update.py prod --in work/new_prod.txt` — exit 10 = ไม่เปลี่ยน · มี `warnings` ให้ใส่ในรายงาน
   - ถ้า 4, 4b, 4c ได้ exit 10 ทั้งหมด = ไม่มีอะไรใหม่ หยุดได้เลย
5. `python3 hr_update.py commit` (bump sw.js + commit เฉพาะไฟล์ HR; auto-push จะ push เอง)
6. Google Sheet id `1Ng8dK5bOGZ26vl-mfiZOuNan7-bh0eW-8jyu6OC6O7U` — **เติมได้เฉพาะช่องว่างใหม่ ห้ามแก้ค่าที่มีอยู่แล้ว**: get_values `'MON YY'!A1:BK29` → `work/grid_current.json` และ get_values `'MON YY confirm ot'!A1:J300` → `work/confirm_current.json` (ถ้าแท็บ confirm ot ไม่มี ให้ข้ามส่วน confirm และรายงาน ห้ามสร้างแท็บเอง) → `python3 hr_update.py sheet --grid-current work/grid_current.json --confirm-sheet-id <id> --confirm-current work/confirm_current.json` → ส่งเฉพาะไฟล์ที่สคริปต์สร้าง → รัน `python3 hr_update.py sheet-done` ทุกครั้งที่เขียนลงชีต · ถ้า `confirm_blocked_hr_edits` ไม่ว่าง ห้ามแตะ ให้รายงาน · ห้ามใช้ `--force-confirm`
7. ตรวจด้วย get_values 1 ครั้ง

### กฎเบราว์เซอร์
- `list_connected_browsers` → `select_browser` ตัวที่เป็น Mac (ปกติ b75a6bb0-5b78-4e44-92a8-75224f1ce4ee) → `tabs_context_mcp(createIfEmpty=true)`
- ใช้ `browser_batch([navigate, computer wait 4, javascript_tool])` ห้าม navigate เดี่ยว ห้าม wait เกิน 10 วิ
- ถ้า Discord ขึ้นหน้า login: หยุดและรายงาน ห้ามกรอกรหัสผ่าน

### ห้ามทำโดยอัตโนมัติ
- ห้ามเพิ่มชื่อพนักงาน/ชื่อเล่น ห้ามเปลี่ยนกฎ OT/สาย ห้ามลบหรือแก้ค่าที่มีอยู่แล้วใน Google Sheet ห้ามแก้/ลบ/สร้างแท็บ ห้ามคัดลอกเงินเดือน เงินเบิก เลขบัญชี หรือยอดเงิน OT
- ถ้าสคริปต์ใน `scripts/hr/` หายหรือพัง: หยุดและรายงาน

### สรุปท้ายรอบ (สั้นๆ ภาษาไทย)
เวลารอบนี้, ดึงตั้งแต่วันที่, จำนวนที่เพิ่ม (เข้า/ออก), การลาใหม่ + คำเตือน, รายงานการผลิตใหม่ + คำพิมพ์ผิด, ชื่อที่ไม่รู้จัก, ลืมเช็คเอาท์, มาสายวันนี้, OT รวมเดือนนี้, อัปเดต Google Sheet แล้วหรือไม่, และ error ถ้ามี

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
| `cd "<path>" && git status` | cd + git = ตัวตรวจตีธง (รัน hook ได้) | `git -C "<path เต็ม>" status` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion สร้างกฎถาวรไม่ได้ | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for d in ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขใน bash ก็เข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python แล้วเรียกไฟล์นั้น |
| `cmd1; cmd2; cmd3` ต่อกันยาว ๆ | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |

**ถ้าต้องมีตรรกะ (วนลูป / เช็คเงื่อนไข / ประกอบพาธ): เขียนเป็นสคริปต์ python
ไว้ใน `scripts/` แล้วเรียกด้วยพาธเต็ม** เช่น `python3 "<path เต็ม>/scripts/ads/check_downloads.py" tiktok`
วิธีนี้ทั้งอ่านง่ายกว่า ทดสอบแยกได้ และไม่ติดกำแพงสิทธิ์
