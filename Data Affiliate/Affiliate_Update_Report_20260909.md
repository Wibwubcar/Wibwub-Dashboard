# รายงานอัปเดต Affiliate — 9 ก.ย. 2569 (รอบเช้า)

## สรุปสั้น: ข้อมูล TikTok ยังไม่ขยับ — รอบนี้เป็น "รอบตรวจสอบ" ไม่ใช่รอบอัปเดต

TikTok Affiliate Center ยังไม่ปล่อยข้อมูลใหม่นับจากรอบวันที่ 8 ก.ย.
- หน้าเว็บระบุ: **"อัปเดตเมื่อ: 6 ก.ย. 2026 0:00 (GMT+7:00)"**
- ปฏิทินยังปิด (เทา) วันที่ 7, 8, 9 ก.ย. เป็นต้นไป
- วันสิ้นสุดที่เลือกได้สูงสุด = **6 ก.ย. 2569** เท่ากับรอบเมื่อวาน

ผลคือค่าที่คำนวณใหม่ทุกตัว **ตรงกับค่าที่มีอยู่บนแดชบอร์ดแล้วทุกประการ** ไม่มีการเขียนทับข้อมูลตัวเลขใด ๆ

---

## STEP 1–3: ดาวน์โหลดไฟล์ (สำเร็จ 4/4)

ช่วงวันที่ที่ export: **1–6 ก.ย. 2569** (`20260901-20260906`)

| Tab | ไฟล์ | ขนาด | ปลายทาง |
|---|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260901-20260906.xlsx | 377,827 B | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260901-20260906.xlsx | 19,133 B | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260901-20260906.xlsx | 831,444 B | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260901-20260906.xlsx | 37,401 B | Data Affiliate/ไลฟ์สตรีม/ |

LaunchAgent `com.wibwub.download-mover` ย้ายไฟล์ต้นฉบับออกจาก Downloads ให้อัตโนมัติตามปกติ

---

## STEP 4: Affiliate arrays — ตรวจแล้ว ไม่มีการเปลี่ยนแปลง

ค่าที่คำนวณจากไฟล์ครีเอเตอร์ (ก.ย. 1–6):

| ตัวชี้วัด | ค่าที่คำนวณได้ | ค่าบนแดชบอร์ด | ผล |
|---|---|---|---|
| GMV | 376,263 | 376,263 | ตรงกัน |
| Net (หลังคืนเงิน) | 369,252 | 369,252 | ตรงกัน |
| Commission | 42,917 | 42,917 | ตรงกัน |
| Active Creators | 314 | 314 | ตรงกัน |

- `WIBWUB_Affiliate_Dashboard.html` — `AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR` ท้ายอาร์เรย์คือ `"ก.ย. (1-6)"` อยู่แล้ว → **ไม่แก้**
- `WIBWUB_Mobile.html` — `AFI_MONTHS` ท้ายอาร์เรย์คือ `"กย.69 (1-6)"` พร้อมค่าตรงกัน → **ไม่แก้**

ทำตามกฎ rolling-window: อ่าน label array ก่อน พบเดือนปัจจุบันเป็นตัวสุดท้ายแล้ว จึงเทียบค่าแทนการ append

---

## STEP 5: PRODUCTS cr/vid — ตรวจแล้ว ตรงกันทั้ง 7 รายการ

| สินค้า | cr | vid |
|---|---|---|
| WIBWUB Refresh Leather Wipes | 48 | 105 |
| WIBWUB Interior wipes | 25 | 73 |
| WIBWUB Sugar | 21 | 25 |
| WIBWUB CLEANER | 5 | 3 |
| WIBWUB Interior | 5 | 22 |
| WIBWUB Refresh | 3 | 8 |
| WIBWUB Visible | 1 | 7 |

ไม่แตะฟิลด์ gmv/units/monthly/ret ตามกฎ

---

## STEP 5B: VIDEOS merge

```
parsed video rows: 4154
parsed existing VIDEOS entries: 8082
literal entry count in block: 8082   (regex match ครบทุก entry)
updated current-month (sep) values: 0
new video entries: 0
total entries after write: 8082
```

**การเปลี่ยนแปลงเดียวในไฟล์รอบนี้:** 84 entry ที่ GMV = 0 มี label ค้างอยู่เป็น `date:'ก.ย.'` ถูกแก้เป็น `date:''` (พฤติกรรมที่ถูกต้องของ `date_label()`)

การตรวจสอบความปลอดภัย:
- diff เทียบ backup = 168 บรรทัด (เก่า 84 / ใหม่ 84) — ต่ำกว่าเกณฑ์ยกเลิก ~50% มาก
- ฝั่งบรรทัดใหม่ทั้ง 84 เป็นรูปแบบ `gmv:0,units:0,date:''` ครบ 100% → ไม่มีค่า GMV/units/monthly ใดถูกแตะ
- `node -e` eval VIDEOS array ผ่าน ไม่ throw (8082 entries)
- Backup ก่อนแก้: `outputs/AFF_BACKUP.html`

---

## STEP 6: Cache version

- `sw.js`: `wibwub-v1048` → **`wibwub-v1049`**
- เขียน `push_now.command` ใหม่แล้ว (chmod +x เรียบร้อย)

**⚠️ ต้องทำด้วยตัวเอง:** sandbox ลบ `.git/index.lock` ไม่ได้ (Operation not permitted) จึง commit จากในนี้ไม่สำเร็จ
→ **ดับเบิลคลิก `push_now.command`** เพื่อ commit + push

---

## ⚠️ พบบั๊กในไฟล์ skill (STEP 4) — ควรแก้

สคริปต์ STEP 4 ในไฟล์ task พังทันทีที่รัน:
`ValueError: could not convert string to float: 'GMV ที่เกิดจากลูกค้าที่แตะลิงก์สินค้า...'`

สาเหตุ 2 อย่าง:
1. ไฟล์ครีเอเตอร์มี **header 2 แถว** (แถว 0 = ชื่อคอลัมน์, แถว 1 = คำอธิบาย) — สคริปต์ใช้ `df.iloc[1:]` ต้องเป็น `raw.iloc[2:]`
2. index คอลัมน์ที่ hardcode ไว้ล้าสมัย — "การคืนเงิน" คือคอลัมน์ **4** (ไม่ใช่ 2), "ค่าคอมมิชชั่นโดยประมาณ" คือคอลัมน์ **21** (ไม่ใช่ 10)

วิธีที่ใช้แก้รอบนี้ (แนะนำให้ย้ายไปใส่ใน skill): resolve คอลัมน์ด้วย **ชื่อ header** แทน index

```python
raw = pd.read_excel(f, header=None)
hdr = [str(v).strip() for v in raw.iloc[0].tolist()]
idx = {h: i for i, h in enumerate(hdr)}
c_gmv = idx['GMV จากครีเอเตอร์']
c_ret = idx['การคืนเงิน']
c_com = idx['ค่าคอมมิชชั่นโดยประมาณ']
df = raw.iloc[2:]
```

---

## หมายเหตุอื่น

- `WIBWUB_Affiliate_Dashboard.html` บรรทัด ~314 มีข้อความ KPI hardcode: *"Active Creator โตจากเดือนก่อน +18.5% / 720 คน (ก.ค.) → 853 คน (ส.ค.)"* — ยังเป็น ก.ค.→ส.ค. อยู่ ไม่ได้แก้เพราะอยู่นอกขอบเขตงานวันนี้ แต่จะกลายเป็นข้อมูลเก่าเมื่อ ก.ย. จบเดือน
- ปัญหาที่เจอระหว่างทางและแก้ได้: date picker ของตาราง "รายละเอียด" เป็นคนละตัวกับ picker ด้านบน (ต้องตั้งตัวในส่วนรายละเอียดถึงจะมีผลกับไฟล์ export), reports panel ค้างที่ "กำลังส่งออก" → แก้ด้วยการ reload หน้าเว็บ
