---
name: wibwub-thursday-affiliate
description: ทุกวัน 10:20/21:20 — โหลด 4 ไฟล์ TikTok Affiliate → อัปเดต Dashboard ด้วย affiliate_update.py + vid_merge.py
---

อ่านไฟล์นี้ด้วย Read tool แล้วทำตามทุกขั้นตอนในไฟล์ให้ครบ:

`/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/task_prompts/wibwub-thursday-affiliate.md`

**ไฟล์นั้นคือแหล่งความจริงเพียงที่เดียวของงานนี้** ห้ามทำตามความจำหรือพรอมป์เวอร์ชันเก่า

> **ทำไมไฟล์นี้ถึงเหลือแค่นี้ (27 ต.ค. 69)**
> ก่อนหน้านี้ไฟล์นี้เก็บพรอมป์เต็ม 22,500 ตัวอักษรที่**ไม่เคยเรียก `affiliate_update.py`
> หรือ `vid_merge.py` เลย** เอเจนต์ไปเขียนสคริปต์ของตัวเองที่ `/tmp/s5b.py` และ
> `outputs/scripts/videos.py` แทน ผลที่ตรวจเจอ:
> - `AF_GMV` ต.ค. เขียนเกินจริง **416 บาท** (2,368,177 แทนที่จะเป็น 2,367,761)
> - VIDEOS: ได้ `vid_id` ครบถูกต้องทั้ง 417 ตัว **แต่ `date` ผิด 669 แถว** — เว้นว่างไว้
>   265 แถวใหม่ และใช้ "สองเดือนล่าสุด" แทนคอนเวนชัน "เดือนแรก–เดือนล่าสุด" อีก 404 แถว
> - ยังฝังพาธ `/sessions/hopeful-serene-fermi/mnt/...` ที่ไม่มีอยู่จริงแล้ว
> ตัวคำนวณจริงมีด่านที่เขียนเองแล้วลืมเสมอ (จับคอลัมน์จากชื่อ header ไม่ใช่ตำแหน่ง ·
> เลือกไฟล์ตามช่วงวันที่ในชื่อ ไม่ใช่ mtime) — **ห้ามเขียนสคริปต์คำนวณเองทุกกรณี**

## ขั้น 0 — ยืนยันว่าไฟล์พรอมป์อยู่ที่เดิม

งานนี้รันบนเครื่อง Mac มีพาธเดียว · **คำสั่ง shell แรกของรอบต้องเป็น `python3`**
ห้ามเป็นลูป `for` ของ bash (สร้างกฎอนุญาตถาวรไม่ได้ → รอบค้างจนหมดเวลา)

```bash
python3 -c "
import os
P = '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/task_prompts/wibwub-thursday-affiliate.md'
print('พรอมป์ OK' if os.path.isfile(P) else '⛔ ไม่พบไฟล์พรอมป์')
"
```

`⛔ ไม่พบไฟล์พรอมป์` หรือ shell ตอบว่า "No folders are connected" → **หยุดและรายงานว่าล้มเหลวทันที**
**ห้ามเดาพาธเอง และห้ามใช้พาธ `/sessions/<ชื่อ>/mnt/...` ที่ฝังไว้ในเอกสารเก่า (ตายแล้วทั้งหมด)**

## กติกาประจำรอบ

- **ตัวคำนวณจริงมี 2 ตัวเท่านั้น**: `scripts/affiliate_update.py` (AF_GMV/AF_NET/AF_COM/AF_CR)
  และ `scripts/vid_merge.py` (VIDEOS) · ห้ามเขียนสคริปต์เอง ห้ามแก้อาเรย์ด้วยมือ
- `vid_merge.py` **ไม่มีโหมด dry** ต้อง `cp` ไฟล์เป็น `.bak` ก่อนรันทุกครั้ง
  แล้วหลังรันเทียบจำนวน `vid_id` กับก่อนรัน — **ถ้ามีวีดีโอหายแม้แต่ตัวเดียว ให้ย้อนจาก .bak
  แล้วรายงาน ห้าม commit**
- `vid_merge.py` ขึ้น `AssertionError` + exit 1 ตอนไม่มีวีดีโอใหม่ = **ปกติ ไม่ได้เขียนไฟล์**
  ห้ามไปแก้อาเรย์ VIDEOS ด้วยมือเพราะเห็น error นี้
- ไฟล์ใน `Data Affiliate/` มี 2 รูปแบบที่ตำแหน่งคอลัมน์ไม่เหมือนกัน — สคริปต์จับจากชื่อ header เอง
  **ห้าม hardcode เลขคอลัมน์**
- download-mover ย้ายไฟล์จาก Downloads ให้เองใน 5 วินาที **ห้าม cp/mv เอง**
- ถ้า TikTok ขึ้นหน้า login: หยุดและรายงาน `⛔ ต้อง login ใหม่: <โดเมน>` เป็นบรรทัดแรกสุด
  **ห้ามกรอกรหัสผ่านหรือกดปุ่มเข้าสู่ระบบเองทุกกรณี**
- **หน้า `WIBWUB_Affiliate_Dashboard.html` มีงานอื่นแก้ด้วย** (`wibwub-samp-request-sync`)
  ถ้า `git diff` มี `SAMPLE_*` ปนอยู่ **ห้าม commit** ให้เขียนไฟล์แล้วรายงานว่ามีงานค้างของใคร
- git add เฉพาะไฟล์ที่พรอมป์ระบุ · auto-push (launchd `com.wibwub.autopush`) push ให้เอง
  ภายใน 2 นาที **ไม่ต้อง `git push` และห้ามบอกผู้ใช้ให้กด `push_now.command`**
- จบงานให้ปิดแท็บ Chrome ที่เปิดในรอบนี้
- รายงานท้ายรอบเป็นภาษาไทย บอก AF_GMV/AF_CR ของเดือนปัจจุบัน และจำนวน VIDEOS ก่อน/หลัง ทุกครั้ง
