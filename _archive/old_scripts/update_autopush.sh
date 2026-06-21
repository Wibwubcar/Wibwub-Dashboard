#!/bin/bash
# รันครั้งเดียวเพื่ออัปเดต autopush script และ push ไฟล์ที่ขาด

FOLDER="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

# 1. อัปเดต autopush script
cat > ~/.wibwub_autopush.sh << 'SCRIPT'
#!/bin/bash
FOLDER="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
cd "$FOLDER"
git add *.html "Data Shipnity/Sales_Dashboard.html" "data Ads/WIBWUB_Ads_Dashboard.html" 2>/dev/null
if ! git diff --cached --quiet; then
    git commit -m "auto: $(date '+%Y-%m-%d %H:%M')"
    git push origin main
fi
SCRIPT
chmod +x ~/.wibwub_autopush.sh
echo "✓ autopush script อัปเดตแล้ว"

# 2. Push Sales_Dashboard ที่อาจยังขาด
cd "$FOLDER"
git add "Data Shipnity/Sales_Dashboard.html"
if ! git diff --cached --quiet; then
    git commit -m "add: Sales_Dashboard to subfolder"
    git push origin main
    echo "✓ Sales_Dashboard.html pushed"
else
    echo "✓ Sales_Dashboard.html อยู่ใน GitHub แล้ว"
fi
