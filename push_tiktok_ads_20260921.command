#!/bin/bash
# Fix stuck git locks (sandbox can't unlink under .git/ on this Drive-synced folder),
# then commit + push today's TikTok Ads Sep 1-21 dashboard update.
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

rm -f .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock
find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null

git add "data Ads/WIBWUB_Ads_Dashboard.html" sw.js

if git diff --cached --quiet; then
  echo "ℹ️  ไม่มีอะไรต้อง commit ใหม่ (อาจ commit ไปแล้วก่อนหน้านี้)"
else
  git commit -m "TikTok Ads: update Sep 1-21 data (GMV Max daily-summed + Business Ads 97 campaigns)

- GMV Max: schedule's date-range formula pulled 31 Aug-22 Sep (timezone offset
  bug). Excluded 31 Aug + 22 Sep rows, summed 1-21 Sep daily rows directly
  instead of using the Total row verbatim: spend 583,464.27 / orders 10,290 /
  revenue 2,232,646.39 / ROI 3.83 / CPA 56.70.
- Business Ads: 97 campaigns, Total row spend 17,141.51 / imp 248,538 /
  clicks 3,034 / CPM 68.97 / CTR 1.22%. Verified 6 nonzero campaigns sum to
  the Total row exactly.
- Combined TikTok (DATA_PERIODS.sep.tiktok): spend 600,605.78 / revenue
  2,232,646.39 / orders 10,290 / ROAS 3.72 / CPA 58.37.
- cover.tiktokDay 20->21, tiktokPull + #ads-updated title refreshed.
- sw.js cache bumped v1194->v1195." \
    && echo "✅ Commit สำเร็จ"
fi

git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
echo ""
read -p "กด Enter เพื่อปิดหน้าต่าง..."
