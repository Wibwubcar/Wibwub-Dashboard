# สำเนา SKILL.md ของงาน local (ไฟล์ที่อยู่นอก repo)

งานตั้งเวลาอ่านพรอมป์จากไฟล์ที่**อยู่นอก repo** จึงไม่มีประวัติใน git เลย
- ฝั่ง local: `~/Documents/Claude/Scheduled/<ชื่องาน>/SKILL.md`
- ฝั่ง code: `~/.claude/scheduled-tasks/<ชื่องาน>/SKILL.md` — แก้แล้วย้อนไม่ได้ และมองไม่เห็นว่าใครแก้อะไร

โฟลเดอร์นี้เก็บ**สำเนา**ของไฟล์พวกนั้นไว้ให้ git ดูแลประวัติ

## กฎ

1. **ตัวจริงคือไฟล์ใน `~/Documents/Claude/Scheduled/`** · แก้ที่นี่แล้วไม่มีผล
2. แก้ตัวจริงก่อน แล้วคัดลอกมาทับไฟล์ในโฟลเดอร์นี้ **ในคอมมิตเดียวกัน**
3. ถ้างานไหนมีพรอมป์เต็มอยู่ใน `scripts/task_prompts/<ชื่องาน>.md` แล้ว
   (SKILL.md เป็นแค่ wrapper ที่สั่งให้ไปอ่านไฟล์นั้น) ให้เก็บ wrapper ไว้ที่นี่
   ส่วนเนื้อหาจริงอยู่ที่ไฟล์เดิม — ห้ามเขียนทับกัน

## รายการที่ยังต้องทำสำเนา

| งาน | สถานะ |
|---|---|
| wibwub-thursday-affiliate | ✅ มีสำเนาแล้ว (wrapper · ฝั่ง local) |
| wibwub-ads-daily | ✅ มีสำเนาแล้ว (**ฝั่ง code** · พรอมป์เต็มในตัว) |
| wibwub-tiktok-product-daily | ⏳ ยังไม่ได้ทำสำเนา |
| wibwub-fastmoss-competitor (มีส่วน HR ด้วย) | ⏳ ยังไม่ได้ทำสำเนา |
| wibwub-daily-followers | ✅ ตัวจริงตรงกับ `scripts/task_prompts/wibwub-daily-followers.md` แล้ว |
| wibwub-daily-stock | ✅ ตัวจริงตรงกับ `scripts/task_prompts/wibwub-daily-stock.md` แล้ว |
| wibwub-download-orders-monday | ✅ ตัวจริงตรงกับ `scripts/task_prompts/wibwub-download-orders-monday.md` แล้ว |
| wibwub-download-tiktok-ads | ✅ ตัวจริงตรงกับ `scripts/task_prompts/wibwub-download-tiktok-ads.md` แล้ว |
