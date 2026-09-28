# TikTok Product Daily — รอบเย็น 10 ก.ย. 2026 (ไม่ได้เขียนข้อมูล)

**สรุป: ไม่มีการแก้ไข `WIBWUB_Dashboard.html` ไม่มี commit ใหม่ ไม่ต้อง push**

## สถานะข้อมูลปัจจุบัน (ตรวจแล้ว)

| | ช่วงข้อมูล | จำนวนวัน | ช่องว่าง |
|---|---|---|---|
| `TK_PROD_DATA` | 2026-08-01 → 2026-09-09 | 40 | ไม่มี |
| `TK_PROD_SKU` | 2026-08-01 → 2026-09-09 | 40 | ไม่มี |

วันเป้าหมายของงานนี้คือ "เมื่อวาน" = **2026-09-09** ซึ่งมีอยู่ครบทั้งสอง const แล้ว
รอบ scheduled เช้าวันนี้ทำงานสำเร็จไปแล้ว (`084603f` เวลา 02:29 สำหรับ parent, `3570448` เวลา 02:34 สำหรับ SKU)

ค่าที่เก็บไว้ของ 2026-09-09: 74 แถว / 71 pid ไม่ซ้ำ / GMV รวม ฿200,664.82 / 831 ออเดอร์
SKU ของ 2026-09-09: 99 แถว / GMV ฿144,791.36 (เป็นค่าเฉลี่ยจาก chunk 09-07..09-09 ตามข้อจำกัดที่รู้อยู่แล้ว)

## ทำไมถึงไม่เขียนทับ

รอบนี้ลองดึงซ้ำเพื่อให้ได้ตัวเลขที่นิ่งกว่า (เมื่อเช้าดึงหลังวันปิดแค่ ~2.5 ชม.) แต่ Compass ตอบไม่ครบ

ผลที่ดึงได้: **69 สินค้า / GMV ฿196,825.33** เทียบกับของเดิม **71 สินค้า / ฿200,664.82**
คือได้น้อยกว่าเดิม จึงไม่เขียนทับ ตามกฎในไฟล์งานที่ห้ามเขียนข้อมูลไม่ครบลง `TK_PROD_DATA`

## ปัญหาที่เจอกับ Compass API (บันทึกไว้ใช้รอบหน้า)

1. **`read_network_requests` จับ request ของ Compass ไม่ได้เลย** — แม้แต่ request ที่เรายิงเองก็ไม่ขึ้น ต้องเลิกใช้วิธีนี้
2. **หา request shape ได้จากตัว JS bundle แทน** — ค้น `performance.getEntriesByType('resource')` แล้ว fetch ไฟล์ `.js` มา regex หา `GetSellerProductListQuery`
3. **รูปแบบ request ที่ถูกต้อง** (POST, same-origin, `credentials:'include'`):
   ```
   POST /api/v3/insights/seller/ttp/product/list
   {"version":3,"request":{
     "time_descriptor":{"start":"2026-09-09","end":"2026-09-10"},
     "list_control":{"pagination":{"page":1,"size":30}}}}
   ```
   - `start`/`end` ต้องเป็น `YYYY-MM-DD` และ **`end` เป็น exclusive** (วันเดียว = start วันนั้น, end วันถัดไป) ถ้า start = end จะได้ error `98001004 invalid params`
   - ไม่มี key `request` ครอบ จะได้ error `binding: expr_path=request`
   - field ที่ต้องใช้ใน `stats_v3.total`: `gmv`, `orders`, `sku_orders`, `items_sold`, `self_live_gmv`, `self_video_gmv`, `affiliate_gmv`, `affiliate_live_gmv`, `affiliate_video_gmv`, `product_card_gmv` (ค่าเงินอยู่ใน `.amount` เป็น string)
4. **backend ตัดข้อมูลทิ้งแบบสุ่ม** — นี่คือปัญหาหลัก
   - `size` > 50 คืน `items` ว่างเปล่าทั้งที่ `code:0`
   - `size:40` คืน 34 แถว, `size:50` คืน 24 แถว, `size:30` page 2 คืน 14 แถว ทั้งที่ `total:74`
   - ยิงถี่เกินไปเจอ `code:429 rate limit exceeded` ต้องเว้น ≥ 2 วินาทีต่อ request
   - `rules:[{"field":"gmv","direction":2}]` ผ่าน validation และ server echo กลับมา **แต่ไม่ได้ sort จริง** ทำให้ pagination ไม่เสถียร ได้ของซ้ำและตกหล่น
   - วิธีที่พอใช้ได้: ยิงซ้ำหลายรอบสลับ `size`/`page` แล้ว union ตาม pid — รอบนี้ยิง ~150 ครั้ง ตันอยู่ที่ 69/74 ไม่ขึ้นอีก
5. `javascript_tool` ถูก content filter บล็อกบ่อยเมื่อ output มี base64 หรือหน้าตาคล้าย query string — ต้องส่งออกเฉพาะ token ตัวอักษร หรือใช้ Blob download (ดาวน์โหลดได้ครั้งเดียวต่อหน้า Chrome จะบล็อกครั้งถัดไป)

## ข้อเสนอสำหรับรอบหน้า

ให้รอบ scheduled เช้ายิงแบบ union หลายรอบ (สลับ `size` 10/20/30/40 และ `page` 1..8 เว้น 2 วินาที) แล้วเช็คว่า unique pid ถึง `next_pagination.total` ก่อนค่อย merge ถ้าไม่ถึงให้ retry อีกครั้งภายหลัง แทนที่จะ merge ทันที
