---
name: wibwub-hr-sheet
description: ทุกวัน 10:30 · 20:30 · 00:30 — เขียนตารางเข้า-ออกงานและแท็บ confirm ot ลง Google Sheet ด้วย hr_update.py sheet-auto (service account บน Mac ไม่ใช้ Chrome ไม่ใช้ Sheets MCP จึงไม่โดน safety filter) · รันหลังรอบ HR หลัก (08:55/09:55/12:55/17:55/18:55/23:55 ที่งาน local fastmoss) · เติมเฉพาะช่องว่าง ห้ามทับค่าที่ HR แก้
---

## 🔗 งาน HR มี 2 ตัว แยกหน้าที่กัน — อ่านให้ชัดก่อนลงมือ

| งาน | ฝั่ง | เวลา | ทำอะไร | พรอมป์ |
|---|---|---|---|---|
| `wibwub-fastmoss-competitor` ส่วน A | local | 08:55 · 09:55 · 12:55 · 17:55 · 18:55 · 23:55 | Discord → **Dashboard** (`WIBWUB_HR_Attendance.html`) | `scripts/task_prompts/hr_attendance.md` |
| **`wibwub-hr-attendance-1200-2200`** (ไฟล์นี้) | **code** | **10:30 · 20:30 · 00:30** | → **Google Sheet** (`hr_update.py sheet-auto`) | ไฟล์นี้ |

**ตัวนี้ไม่ดึง Discord และไม่แตะ Dashboard** · **ตัวโน้นไม่เขียนชีต** — ตั้งใจให้แยกกัน
เพราะตัวเขียนชีตใช้ service account ไม่ต้องใช้ Chrome จึงรันฝั่ง code ได้
และไม่กินโควตาเพดาน 3 งานพร้อมกันของฝั่ง local

> 28 ต.ค. 69: เคยมีคนสงสัยว่า "รอบเช้าอัปเดต Dashboard แล้วทำไมไม่เขียนชีต"
> คำตอบคือคนละงานกัน ชีตเขียนตอน 10:30 — ความหน่วงจริงจากตอกบัตรเช้าถึงชีตคือ ~1.5 ชม.

## ขั้น 0 — หาโฟลเดอร์ All ก่อนเสมอ

พรอมป์นี้ถูกเรียกได้จากหลายฝั่งและโฟลเดอร์ All อยู่คนละที่กัน **ห้ามฝังพาธตายตัว**

```bash
for d in "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" "$HOME/mnt/All" /sessions/*/mnt/All; do
  [ -f "$d/scripts/hr/hr_update.py" ] && BASE="$d" && break
done
echo "BASE=$BASE"
```

ไม่เจอ → **หยุดและรายงานว่าล้มเหลวทันที** ห้ามเดาพาธเอง


งานนี้เขียนข้อมูล HR ลง Google Sheet อย่างเดียว **ไม่ต้องเปิดเบราว์เซอร์ ไม่ต้องดึง Discord ไม่ต้องใช้เครื่องมือ Google Sheets ของ MCP เลย** การดึงข้อมูลจาก Discord เป็นหน้าที่ของงาน local "wibwub-fastmoss-competitor" ส่วน A ที่รัน 6 รอบต่อวันอยู่แล้ว

ถ้าคิดว่าต้องเปิด Chrome หรือเรียก `get_values`/`update_values` แปลว่าอ่านผิด ให้อ่านใหม่

## 🚫 กฎคำสั่ง shell — ผิดข้อนี้งานจะค้างตลอดไป

**ห้ามใช้ `cd` เด็ดขาด ไม่ว่าจะเป็น `cd X && ...` หรือ `cd X` บรรทัดเดียว**
คำสั่งที่ขึ้นต้นด้วย `cd` ไม่แมตช์กฎอนุญาต `Bash(python3:*)` จึงเด้งกล่องขออนุญาตที่ไม่มีใครกด
แล้วงานจะค้างไปเรื่อย ๆ (เกิดจริงกับงานการตลาด 24 ต.ค. 69 ค้าง 1 ชม. 45 นาที)

**ทุกคำสั่งต้องขึ้นต้นด้วย `python3` แล้วตามด้วยพาธเต็ม** สคริปต์หาโฟลเดอร์ All เองจากตำแหน่งไฟล์

## ขั้นตอน — คำสั่งเดียว

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/hr/hr_update.py" sheet-auto
```

จบแค่นี้ สคริปต์อ่านชีต คำนวณ เขียนกลับ และบันทึกสถานะให้เองทั้งหมดผ่าน service account บนเครื่อง

**อ่านผลจาก JSON ที่มันพิมพ์ออกมา**
- `mode: "APPLIED"` = เขียนแล้ว · ดู `applied.grid` ว่าเติมกี่ช่อง
- `mode: "BLOCKED"` + `exit 2` = **HR แก้แท็บ confirm ot เอง** สคริปต์ไม่แตะอะไรเลย
  ให้รายงานรายการใน `confirm_blocked_hr_edits` แล้วจบ **ห้ามพยายามเขียนทับ**
- `grid_cells_to_write: 0` = ไม่มีอะไรใหม่ ถือว่าปกติ
- `skipped_cells_not_empty` = ช่องที่ระบบมีค่าแต่ชีตมีคนกรอกไว้แล้ว **ระบบไม่ทับ** ให้รายงานจำนวน
  ถ้ามีเยอะผิดปกติ (เกิน 40 ช่อง) ให้แจ้งเตือนในรายงาน

## ห้ามเด็ดขาด

- ห้ามใส่ `--force-confirm` (สคริปต์ปิดตายไว้แล้ว แต่ห้ามพยายามหาทางอื่น)
- ห้ามแก้หรือลบค่าที่มีอยู่แล้วในชีต ห้ามสร้าง/ลบ/เปลี่ยนชื่อแท็บ
- ห้ามเพิ่มชื่อพนักงานเอง ถ้าสคริปต์บอกว่า `names missing from sheet` ให้หยุดและรายงาน
  ให้คนเพิ่มแถวเอง
- ห้ามคัดลอกเงินเดือน เงินเบิก เลขบัญชี หรือยอดเงิน OT ออกมาในรายงาน
- ถ้าสคริปต์คืน exit 2 ด้วยเหตุอื่น (ไม่พบ service account / ไม่พบแท็บ) ให้รายงานตรง ๆ
  **ห้ามเดาทางแก้เอง**

## รายงานท้ายรอบ (สั้น ๆ ภาษาไทย)

โหมดที่ได้ · แท็บ · จำนวนช่องที่เติม · confirm ot อัปเดตไหม · จำนวนช่องที่ข้ามเพราะมีค่าแล้ว · error ถ้ามี