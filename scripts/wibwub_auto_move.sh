#!/bin/bash
# WIBWUB Auto-Move Downloads — รันโดย LaunchAgent อัตโนมัติ
DL="$HOME/Downloads"
ALL="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

ARCH="$ALL/downloads_archive"   # อยู่ใน .gitignore แล้ว ไม่ขึ้น GitHub
# ย้ายไฟล์แบบไม่ทับของเดิมเด็ดขาด — ก่อน 20 ต.ค. 2569 ทุกบรรทัดด้านล่างใช้ `mv` เปล่า
# ทำให้ไฟล์ชื่อซ้ำถูกทับเงียบ ๆ (เกิดจริง: CSV Shopee Ads รอบเช้าถูกไฟล์รอบสายทับ
# ข้อมูลหายถาวรเพราะไฟล์พวกนี้ไม่ได้ track ใน git)
safe_mv() {  # $1=ไฟล์ต้นทาง  $2=โฟลเดอร์ปลายทาง
  local f="$1" dst="$2" b stamp
  [ -f "$f" ] || return 0
  mkdir -p "$dst"
  b=$(basename "$f")
  if [ -e "$dst/$b" ]; then
    stamp=$(date -r "$f" +%Y%m%d_%H%M%S)
    if cmp -s "$f" "$dst/$b"; then            # เหมือนกันทุกไบต์ -> เก็บเข้า dup ไม่รก
      mkdir -p "$ARCH/dup"; mv -n "$f" "$ARCH/dup/${b%.*}__$stamp.${b##*.}"
    else                                      # ชื่อซ้ำแต่เนื้อหาต่าง -> เก็บทั้งคู่
      mv -n "$f" "$dst/${b%.*}__$stamp.${b##*.}"
    fi
  else
    mv -n "$f" "$dst/$b"
  fi
}


move() {
  local src="$1"; local dst="$2"
  [ -f "$src" ] && mv "$src" "$dst/" && echo "[WIBWUB] moved: $(basename "$src") → $dst"
}

# Affiliate
for f in "$DL"/Transaction_Analysis_Creator_List_*.xlsx;  do safe_mv "$f" "$ALL/Data Affiliate/ครีเอเตอร์/"; done
for f in "$DL"/Transaction_Analysis_Video_List_*.xlsx;    do safe_mv "$f" "$ALL/Data Affiliate/วีดีโอ/"; done
for f in "$DL"/Transaction_Analysis_Product_List_*.xlsx;  do safe_mv "$f" "$ALL/Data Affiliate/สินค้า/"; done
for f in "$DL"/Transaction_Analysis_Live_List_*.xlsx;     do safe_mv "$f" "$ALL/Data Affiliate/ไลฟ์สตรีม/"; done
for f in "$DL"/Creator_List_*.xlsx;                       do safe_mv "$f" "$ALL/Data Affiliate/ครีเอเตอร์/"; done

# Orders
for f in "$DL"/Order.all.*.xlsx;                          do safe_mv "$f" "$ALL/data ยอดขาย plaform/Shopee/"; done
for f in "$DL"/Order.all.*.zip;                           do safe_mv "$f" "$ALL/data ยอดขาย plaform/Shopee/"; done
for f in "$DL"/*คำสั่งซื้อ*.xlsx;                        do safe_mv "$f" "$ALL/data ยอดขาย plaform/Tiktok/"; done
for f in "$DL"/Order\ Report\ *.xlsx;                     do safe_mv "$f" "$ALL/data ยอดขาย plaform/Line My Shop/"; done
for f in "$DL"/Lazada_Orders_*.xlsx;                      do safe_mv "$f" "$ALL/data ยอดขาย plaform/Lazada/"; done

# Shipnity
for f in "$DL"/Data_*.xlsx;                               do safe_mv "$f" "$ALL/Data Shipnity/"; done
for f in "$DL"/Data-*.xlsx;                               do safe_mv "$f" "$ALL/Data Shipnity/"; done

# Ads
for f in "$DL"/ข้อมูล-Shopee-Ads-*.csv;                  do safe_mv "$f" "$ALL/data Ads/Shopee/"; done
# ปลายทางต้องเป็นโฟลเดอร์ย่อยที่สคริปต์อ่านจริง (Business Ads / GMV Max)
# เดิมทิ้งไว้ที่ "data Ads/Tiktok/" เฉย ๆ -> ไฟล์ไปกองที่ราก งาน download ต้อง cp ซ้ำเอง
# และ cp นั้นแข่งกับ mover (WatchPaths ยิงภายใน ~5 วิ) มักแพ้ -> รายงาน "ไม่พบไฟล์" ทั้งที่โหลดสำเร็จ
for f in "$DL"/WIBWUBCAR-Campaign\ Report-*.xlsx;         do safe_mv "$f" "$ALL/data Ads/TikTok/Business Ads/"; done
for f in "$DL"/Campaign\ overview\ data\ *.xlsx;          do safe_mv "$f" "$ALL/data Ads/TikTok/GMV Max/"; done
for f in "$DL"/creative\ data\ for\ product\ campaigns\ *.xlsx; do safe_mv "$f" "$ALL/data Ads/Tiktok/"; done
for f in "$DL"/ExportAds_V2_*.xlsx;                       do safe_mv "$f" "$ALL/data Ads/Tiktok/"; done

# Content / Followers
for f in "$DL"/Followers_wibwubcar*.zip;                  do safe_mv "$f" "$ALL/data content/"; done

# Affiliate › คำขอสินค้า (CSV จากชีต Top 30 Affiliate แท็บ ขอสินค้า — scripts/affiliate/samp_update.py)
mkdir -p "$ALL/Data Affiliate/ขอสินค้า"
for f in "$DL"/wibwub_samp_req_*.csv;                    do safe_mv "$f" "$ALL/Data Affiliate/ขอสินค้า/"; done

# ── ไฟล์ที่งานตั้งเวลาอ่านจาก Downloads โดยตรง (เช่น tiktok product daily โหลด json แล้วอ่านทันที)
#    → ย้ายเฉพาะไฟล์ที่อายุเกิน OLD_MIN นาที และไม่ทับไฟล์เดิม (ชื่อซ้ำจะต่อท้ายด้วยเวลา)
#
# 2 พ.ย. 69: ลด 1440 -> 180 นาที ตามที่ผู้ใช้อนุมัติ · เกณฑ์เดิมคือ "ข้ามวัน" ทำให้ไฟล์
# ของรอบเช้าค้างใน Downloads ทั้งวันจนปนกับรอบเย็น แล้วสคริปต์ที่เลือกไฟล์ด้วย `ls -t`
# หยิบผิดตัว · 180 นาที ยาวพอสำหรับทุกงาน เพราะงานที่โหลดแล้วอ่านทันทีใช้เวลาไม่เกิน ~20 นาที
# และรอบเช้า/เย็นห่างกัน ~11 ชม.
OLD_MIN=180

move_old() {  # $1=pattern (glob ของ find)  $2=ปลายทาง
  local pat="$1" dst="$2"
  find "$DL" -maxdepth 1 -type f -name "$pat" -mmin +$OLD_MIN -print0 2>/dev/null |
  while IFS= read -r -d '' f; do
    mkdir -p "$dst"
    local b; b=$(basename "$f")
    if [ -e "$dst/$b" ]; then
      local dst2="$dst" stamp
      if cmp -s "$f" "$dst/$b"; then dst2="$ARCH/dup"; mkdir -p "$dst2"; fi   # ซ้ำทุกไบต์ → เก็บแยกไว้ใน dup
      stamp=$(date -r "$f" +%Y%m%d_%H%M%S)
      mv -n "$f" "$dst2/${b%.*}__$stamp.${b##*.}"
    else
      mv -n "$f" "$dst/$b"
    fi
  done
}

move_old 'tiktok_*.json'                              "$ARCH/TikTok json"
move_old 'tk_*.json'                                  "$ARCH/TikTok json"
move_old 'Shop+-Ads-Overall-Data-*.csv'               "$ALL/data Ads/Shopee"
move_old 'overview-v2_*.csv'                          "$ARCH/overview-v2"
move_old 'WIBWUBCAR_หน้าแสดงรายละเอียดร้านค้า_*.xlsx' "$ALL/data Ads/TikTok/Business Ads"

# ── เพิ่ม 29 ต.ค. 69: ไฟล์ที่งานตั้งเวลาโหลดแล้ว "คัดลอก" เข้าโฟลเดอร์งาน (sandbox ลบต้นทางไม่ได้) → ค้างใน Downloads
#    ย้ายเฉพาะไฟล์อายุเกิน 1 วัน ไปเก็บใน downloads_archive (ไม่ลบ)
move_old 'AD-1-*.csv'                                  "$ARCH/facebook"
move_old 'AD-2-*.csv'                                  "$ARCH/facebook"
move_old 'AD3-*.csv'                                   "$ARCH/facebook"
move_old 'AD-4-*.csv'                                  "$ARCH/facebook"
move_old 'Wi-Wu-AD-1*.csv'                             "$ARCH/facebook"
move_old 'Top 30 Affiliate*ขอสินค้า*.csv'              "$ARCH/ขอสินค้า"
move_old 'supply-sellercenter-export-sc_live_stream_list_export_*.xlsx' "$ARCH/shopee live list"
move_old 'shopee-ads-*.csv'                            "$ARCH/shopee-ads"
move_old 'wibwub_tk_prod_sku_*.json'                   "$ARCH/TikTok json"

# ── Lazada: ไฟล์ออเดอร์ที่โหลดมาชื่อเป็น hash 32 ตัว (เช่น d46d670c....xlsx) ────────
# ไม่มีกฎ safe_mv เพราะเดาไม่ได้ว่าไฟล์ hash ตัวไหนคือ Lazada (Downloads มี .xlsx จากหลายที่)
# งาน download-orders คัดลอกเข้าโฟลเดอร์งานเองพร้อมเปลี่ยนชื่อเป็น Lazada_Orders_YYYYMMDD.xlsx
# ตัวต้นฉบับจึงค้างอยู่ตลอด (2 พ.ย. 69 ค้างอยู่ 3 ตัวตั้งแต่ 1 พ.ย.)
#
# ⛔ เงื่อนไขที่ผู้ใช้กำหนด: **ย้ายเฉพาะไฟล์ที่ตรงกับสำเนาในโฟลเดอร์งานทุกไบต์** เท่านั้น
#    ไฟล์ที่ยังไม่มีสำเนา = ยังไม่ถูกคัดลอก ห้ามแตะ (เกิดจริง: รอบเช้า 1-2 พ.ย. ไม่ได้คัดลอก
#    ถ้าย้ายทิ้งไปด้วยจะเสียข้อมูลวันนั้นถาวร เพราะไฟล์พวกนี้ไม่ได้ track ใน git)
#    ย้ายไป downloads_archive **ไม่ลบ**
LZ_WORK="$ALL/data ยอดขาย plaform/Lazada"
lz_hash_move() {
  local f b stamp g matched
  for f in "$DL"/*.xlsx; do
    [ -f "$f" ] || continue
    b=$(basename "$f")
    # ชื่อต้องเป็น hash 32 ตัวพอดี (รับท้าย " (1)" ของเบราว์เซอร์ด้วย) — ห้ามใช้ glob หลวม ๆ
    # แบบ [0-9a-f]*.xlsx เพราะมันแมตช์ชื่อไทย/ชื่อร้านที่ขึ้นต้นด้วยตัวเลขด้วย
    [[ "$b" =~ ^[0-9a-f]{32}(\ \([0-9]+\))?\.xlsx$ ]] || continue
    matched=""
    for g in "$LZ_WORK"/*.xlsx; do
      [ -f "$g" ] || continue
      if cmp -s "$f" "$g"; then matched="$g"; break; fi
    done
    if [ -z "$matched" ]; then
      echo "[WIBWUB] ข้าม (ยังไม่มีสำเนาในโฟลเดอร์งาน): $b"
      continue
    fi
    mkdir -p "$ARCH/lazada-hash"
    stamp=$(date -r "$f" +%Y%m%d_%H%M%S)
    mv -n "$f" "$ARCH/lazada-hash/${b%.xlsx}__$stamp.xlsx" &&
      echo "[WIBWUB] moved: $b → downloads_archive/lazada-hash (ตรงกับ $(basename "$matched"))"
  done
}
lz_hash_move

exit 0
