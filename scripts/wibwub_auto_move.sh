#!/bin/bash
# WIBWUB Auto-Move Downloads — รันโดย LaunchAgent อัตโนมัติ
DL="$HOME/Downloads"
ALL="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

move() {
  local src="$1"; local dst="$2"
  [ -f "$src" ] && mv "$src" "$dst/" && echo "[WIBWUB] moved: $(basename "$src") → $dst"
}

# Affiliate
for f in "$DL"/Transaction_Analysis_Creator_List_*.xlsx;  do [ -f "$f" ] && mv "$f" "$ALL/Data Affiliate/ครีเอเตอร์/"; done
for f in "$DL"/Transaction_Analysis_Video_List_*.xlsx;    do [ -f "$f" ] && mv "$f" "$ALL/Data Affiliate/วีดีโอ/"; done
for f in "$DL"/Transaction_Analysis_Product_List_*.xlsx;  do [ -f "$f" ] && mv "$f" "$ALL/Data Affiliate/สินค้า/"; done
for f in "$DL"/Transaction_Analysis_Live_List_*.xlsx;     do [ -f "$f" ] && mv "$f" "$ALL/Data Affiliate/ไลฟ์สตรีม/"; done
for f in "$DL"/Creator_List_*.xlsx;                       do [ -f "$f" ] && mv "$f" "$ALL/Data Affiliate/ครีเอเตอร์/"; done

# Orders
for f in "$DL"/Order.all.*.xlsx;                          do [ -f "$f" ] && mv "$f" "$ALL/data ยอดขาย plaform/Shopee/"; done
for f in "$DL"/Order.all.*.zip;                           do [ -f "$f" ] && mv "$f" "$ALL/data ยอดขาย plaform/Shopee/"; done
for f in "$DL"/*คำสั่งซื้อ*.xlsx;                        do [ -f "$f" ] && mv "$f" "$ALL/data ยอดขาย plaform/Tiktok/"; done
for f in "$DL"/Order\ Report\ *.xlsx;                     do [ -f "$f" ] && mv "$f" "$ALL/data ยอดขาย plaform/Line My Shop/"; done
for f in "$DL"/Lazada_Orders_*.xlsx;                      do [ -f "$f" ] && mv "$f" "$ALL/data ยอดขาย plaform/Lazada/"; done

# Shipnity
for f in "$DL"/Data_*.xlsx;                               do [ -f "$f" ] && mv "$f" "$ALL/Data Shipnity/"; done
for f in "$DL"/Data-*.xlsx;                               do [ -f "$f" ] && mv "$f" "$ALL/Data Shipnity/"; done

# Ads
for f in "$DL"/ข้อมูล-Shopee-Ads-*.csv;                  do [ -f "$f" ] && mv "$f" "$ALL/data Ads/Shopee/"; done
for f in "$DL"/WIBWUBCAR-Campaign\ Report-*.xlsx;         do [ -f "$f" ] && mv "$f" "$ALL/data Ads/Tiktok/"; done
for f in "$DL"/Campaign\ overview\ data\ *.xlsx;          do [ -f "$f" ] && mv "$f" "$ALL/data Ads/Tiktok/"; done
for f in "$DL"/creative\ data\ for\ product\ campaigns\ *.xlsx; do [ -f "$f" ] && mv "$f" "$ALL/data Ads/Tiktok/"; done
for f in "$DL"/ExportAds_V2_*.xlsx;                       do [ -f "$f" ] && mv "$f" "$ALL/data Ads/Tiktok/"; done

# Content / Followers
for f in "$DL"/Followers_wibwubcar*.zip;                  do [ -f "$f" ] && mv "$f" "$ALL/data content/"; done

# Affiliate › คำขอสินค้า (CSV จากชีต Top 30 Affiliate แท็บ ขอสินค้า — scripts/affiliate/samp_update.py)
mkdir -p "$ALL/Data Affiliate/ขอสินค้า"
for f in "$DL"/wibwub_samp_req_*.csv;                    do [ -f "$f" ] && mv "$f" "$ALL/Data Affiliate/ขอสินค้า/"; done

# ── ไฟล์ที่งานตั้งเวลาอ่านจาก Downloads โดยตรง (เช่น tiktok product daily โหลด json แล้วอ่านทันที)
#    → ย้ายเฉพาะไฟล์ที่อายุเกิน 1 วัน (1440 นาที) และไม่ทับไฟล์เดิม (ชื่อซ้ำจะต่อท้ายด้วยเวลา)
ARCH="$ALL/downloads_archive"   # อยู่ใน .gitignore แล้ว ไม่ขึ้น GitHub
move_old() {  # $1=pattern (glob ของ find)  $2=ปลายทาง
  local pat="$1" dst="$2"
  find "$DL" -maxdepth 1 -type f -name "$pat" -mmin +1440 -print0 2>/dev/null |
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
move_old 'tiktok_*.json'                              "$ARCH/tiktok_json"
move_old 'tk_*.json'                                  "$ARCH/tiktok_json"
move_old 'Shop+-Ads-Overall-Data-*.csv'               "$ALL/data Ads/Shopee"
move_old 'overview-v2_*.csv'                          "$ARCH/overview-v2"
move_old 'WIBWUBCAR_หน้าแสดงรายละเอียดร้านค้า_*.xlsx' "$ALL/data Ads/TikTok/Business Ads"

exit 0
