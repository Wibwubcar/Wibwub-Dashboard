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

exit 0
