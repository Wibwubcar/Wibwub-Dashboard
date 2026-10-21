---
name: wibwub-platform-fee-monthly
description: ทุกวันที่ 5 ของเดือน 10:30 — อัปเดตอัตราค่าธรรมเนียมแพลตฟอร์มของ "เดือนที่แล้ว" (Shopee จากหน้าเว็บ · TikTok จาก Seller Center) → data Ads/platform_fee.json
---

## WIBWUB — อัตราค่าธรรมเนียมแพลตฟอร์มรายเดือน

หน้า "การตลาด vs ยอดขาย" คำนวณ **ยอดขายหลังหักค่าธรรมเนียม** จากอัตราใน
`data Ads/platform_fee.json` งานนี้เติมอัตราของ **เดือนที่เพิ่งจบ** เข้าไปทุกเดือน

> **ทำไมต้องมี:** ปี 2569 ทั้ง Shopee และ TikTok ปรับค่าธรรมเนียมขึ้นหลายครั้ง
> (Shopee 21.54% → 29.96% · TikTok 23.81% → 32.75% ขึ้นพร้อมกันช่วง พ.ค. และ ก.ค.)
> ถ้าไม่ตามอัปเดต ตัวเลขกำไรบนหน้าเว็บจะค่อย ๆ ผิดมากขึ้นโดยไม่มีอะไรเตือน

> **ทำไมวันที่ 5:** ยอด settlement ของ TikTok ต้องรอให้เดือนปิดและเงินเข้าครบก่อน
> ถ้าดึงวันที่ 1-2 จะได้ตัวเลขไม่ครบแล้วอัตราจะเพี้ยน

---

## ขั้นที่ 1 — Shopee (ไม่ต้องเปิดเบราว์เซอร์)

อัตรา Shopee ถอดจาก `SH_FEE ÷ SH_REV` ในหน้า `WIBWUB_Dashboard.html` ซึ่งฝ่ายบัญชี
กรอกไว้อยู่แล้ว — แทนที่ `<เดือนที่แล้ว>` ด้วย `YYYY-MM`

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/marketing/fee_update.py" shopee --month <เดือนที่แล้ว>
```

exit `0` = เพิ่มแล้ว · `10` = มีอยู่แล้วค่าตรงกัน (ปกติ) · `2` = ไม่ผ่านด่าน
ถ้าได้ error ว่า **SH_FEE = 0** แปลว่าฝ่ายบัญชียังไม่กรอกค่าธรรมเนียมเดือนนั้น
→ **ข้ามขั้นนี้ไปทำ TikTok ต่อ แล้วรายงานว่า Shopee ยังรอฝ่ายบัญชี** ห้ามเดาตัวเลขเอง

## ขั้นที่ 2 — TikTok (ต้องเปิด Chrome)

1. Chrome: `list_connected_browsers` → `select_browser` ตัว macOS
   (deviceId `b75a6bb0-5b78-4e44-92a8-75224f1ce4ee`) → `tabs_context_mcp(createIfEmpty=true)`
   → `tabs_create_mcp` แท็บใหม่
2. navigate ไป `https://seller-th.tiktok.com/finance/transactions?shop_region=TH&tab=settled_tab`
   รอ 10 วินาที · ถ้าขึ้นหน้า login: **หยุดและรายงาน ห้ามกรอกรหัสผ่าน**
3. `find` หา **"เพิ่มเติม" ที่อยู่ถัดจาก "ค่าธรรมเนียมทั้งหมด"** แล้วคลิก รอ 7 วินาที
   แผง "รายงานธุรกิจ" จะเปิดทางขวา
4. วางตัวช่วยเลือกเดือน (คัดลอกจาก `scripts/marketing/fee_scrape.js` ส่วนท้ายไฟล์
   หัวข้อ "ตัวช่วยเลือกเดือน") แล้วเรียก `await __pickMonth(<เดือน>, <ปี>)`
   — ตัวช่วยนี้กดปุ่มเลื่อนปฏิทินและคลิกวันที่ 1 กับวันสุดท้ายให้เอง
   **อย่าคลิกปฏิทินด้วยพิกัดพิกเซล** ตำแหน่งเปลี่ยนตามเดือน เคยพลาดมาแล้ว
5. วางเนื้อหา `scripts/marketing/fee_scrape.js` (อ่านด้วย `cat`) ใน `javascript_tool`
   → ได้ JSON `{revenue, fee, aff, aff_ads, range}`
   **ตรวจ `range` ให้ตรงกับเดือนที่ต้องการก่อนใช้ตัวเลข** ถ้าไม่ตรงให้เลือกใหม่
6. ปิดแท็บด้วย `tabs_close_mcp`

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/marketing/fee_update.py" tiktok --month <เดือนที่แล้ว> --revenue <revenue> --fee <fee> --aff <aff> --aff-ads <aff_ads>
```

สคริปต์จะ **หักคอมแอฟฟิลิเอตออกจากอัตราค่าธรรมเนียมให้เอง** แล้วเก็บเป็นอีกก้อน
(`marketing_rates.aff_tk`) ที่หน้าเว็บวางไว้ข้างค่าจ้าง KOL — ไม่นับซ้ำ

## ขั้นที่ 3 — เขียนลงหน้าเว็บ + commit

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/marketing/marketing_update.py"
```

```bash
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add "data Ads/platform_fee.json" WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
```

```bash
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" commit -m "auto: อัตราค่าธรรมเนียมแพลตฟอร์ม $(date +%Y-%m)"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที

---

## RULES

- **ห้ามเดาอัตราเอง** ทุกตัวเลขต้องมาจากหน้าเว็บหรือ Seller Center เท่านั้น
- **ห้ามแก้อัตราของเดือนที่เคยบันทึกแล้ว** สคริปต์กันไว้ (ต้องใส่ `--force`)
  อัตราเก่าถูกใช้คำนวณย้อนหลังไปแล้ว การแก้เงียบ ๆ ทำให้ตัวเลขทั้งปีขยับโดยไม่มีใครรู้
  ถ้าเจอว่าค่าไม่ตรง **ให้รายงาน ห้ามใส่ --force เอง**
- ถ้าอัตราเดือนใหม่ **ต่างจากเดือนก่อนเกิน 3 จุด** ให้ใส่ไว้ในรายงานเด่น ๆ
  เพราะแปลว่าแพลตฟอร์มปรับค่าธรรมเนียมอีกรอบ
- Lazada คงที่ 17.66% มาตลอด ไม่ต้องทำอะไร เว้นแต่เห็นว่าเปลี่ยน
- `grep -oP`, `sed -i "s/.../"` เป็น GNU-only **พังบน macOS** ห้ามใช้

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

เดือนที่อัปเดต, อัตราใหม่ของแต่ละแพลตฟอร์มและเปลี่ยนจากเดือนก่อนกี่จุด,
คอมแอฟฟิลิเอตกี่ %, commit id หรือ "ไม่มีอะไรเปลี่ยน", error ถ้ามี

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
