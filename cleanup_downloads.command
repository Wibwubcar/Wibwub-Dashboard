#!/bin/bash
# WIBWUB Downloads Cleanup — ย้ายไฟล์งานทุกชนิดออกจาก Downloads
# รันทุกครั้งหลังจาก schedule ดาวน์โหลดไฟล์ใหม่

DL="$HOME/Downloads"
ALL="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

move_file() {
  local src="$1"; local dst_dir="$2"
  [ -f "$src" ] && mv "$src" "$dst_dir/" && echo "✅ $(basename "$src")" || true
}

move_glob() {
  local pattern="$1"; local dst_dir="$2"
  for f in $pattern; do
    [ -f "$f" ] && mv "$f" "$dst_dir/" && echo "✅ $(basename "$f")" || true
  done
}

echo "🧹 ย้ายไฟล์งานออกจาก Downloads..."
echo ""

# ── Affiliate (TikTok) ──────────────────────────────────────────
echo "📁 Affiliate →"
move_glob "$DL/Transaction_Analysis_Creator_List_*.xlsx"  "$ALL/Data Affiliate/ครีเอเตอร์"
move_glob "$DL/Transaction_Analysis_Video_List_*.xlsx"    "$ALL/Data Affiliate/วีดีโอ"
move_glob "$DL/Transaction_Analysis_Product_List_*.xlsx"  "$ALL/Data Affiliate/สินค้า"
move_glob "$DL/Transaction_Analysis_Live_List_*.xlsx"     "$ALL/Data Affiliate/ไลฟ์สตรีม"
move_glob "$DL/Creator_List_*.xlsx"                       "$ALL/Data Affiliate/ครีเอเตอร์"
move_glob "$DL/Core_Stats_*.xlsx"                         "$ALL/Data Affiliate/ครีเอเตอร์"

# ── Order files ──────────────────────────────────────────────────
echo ""
echo "📁 Orders →"
move_glob "$DL/Order.all.*.xlsx"                          "$ALL/data ยอดขาย plaform/Shopee"
move_glob "$DL/Order.all.*.zip"                           "$ALL/data ยอดขาย plaform/Shopee"
move_glob "$DL/ทั้งหมด*คำสั่งซื้อ*.xlsx"                "$ALL/data ยอดขาย plaform/Tiktok"
move_glob "$DL/Order Report *.xlsx"                       "$ALL/data ยอดขาย plaform/Line My Shop"
move_glob "$DL/Lazada_Orders_*.xlsx"                      "$ALL/data ยอดขาย plaform/Lazada"

# ── Shipnity ─────────────────────────────────────────────────────
echo ""
echo "📁 Shipnity →"
move_glob "$DL/Data_*.xlsx"                               "$ALL/Data Shipnity"
move_glob "$DL/Data-*.xlsx"                               "$ALL/Data Shipnity"

# ── Ads ──────────────────────────────────────────────────────────
echo ""
echo "📁 Ads →"
move_glob "$DL/ข้อมูล-Shopee-Ads-*.csv"                 "$ALL/data Ads/Shopee"
move_glob "$DL/WIBWUBCAR-Campaign Report-*.xlsx"          "$ALL/data Ads/Tiktok"
move_glob "$DL/Campaign overview data *.xlsx"             "$ALL/data Ads/Tiktok"
move_glob "$DL/creative data for product campaigns *.xlsx" "$ALL/data Ads/Tiktok"
move_glob "$DL/livestream data for live campaigns *.xlsx"  "$ALL/data Ads/Tiktok"
move_glob "$DL/ExportAds_V2_*.xlsx"                       "$ALL/data Ads/Tiktok"

# ── Content / Followers ───────────────────────────────────────────
echo ""
echo "📁 Content →"
move_glob "$DL/Followers_wibwubcar*.zip"                  "$ALL/data content"

echo ""
echo "✅ เสร็จแล้ว!"
echo "Done! กด Enter เพื่อปิด"
read
