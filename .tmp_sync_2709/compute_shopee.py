import csv, json, sys

fn = sys.argv[1] if len(sys.argv) > 1 else 'ข้อออล-Shopee-Ads-01_09_2026-27_09_2026-full43.csv'

with open(fn, encoding='utf-8') as f:
    lines = f.readlines()

header_idx = None
for i, l in enumerate(lines):
    if 'ลำดับ' in l:
        header_idx = i
        break
assert header_idx is not None

reader = csv.reader(lines[header_idx:])
header = next(reader)
rows = [r for r in reader if r and r[0].strip()]

def num(x):
    x = x.replace(',', '').strip()
    try:
        return float(x)
    except Exception:
        return 0.0

def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

campaigns = []
for r in rows:
    name = r[1]
    spend = num(r[26])
    revenue = num(r[24])
    orders = int(num(r[16]))
    imp = int(num(r[11]))
    clicks = int(num(r[12]))
    if spend <= 0:
        continue
    roas = revenue / spend if spend else 0.0
    ctr = clicks / imp * 100 if imp else 0.0
    cvr = orders / clicks * 100 if clicks else 0.0
    cpa = spend / orders if orders else 0.0
    campaigns.append({
        'name': name, 'spend': spend, 'revenue': revenue, 'orders': orders,
        'imp': imp, 'clicks': clicks, 'roas': roas, 'ctr': ctr, 'cvr': cvr, 'cpa': cpa
    })

total_spend = sum(c['spend'] for c in campaigns)
total_revenue = sum(c['revenue'] for c in campaigns)
total_orders = sum(c['orders'] for c in campaigns)
total_imp = sum(c['imp'] for c in campaigns)
total_clicks = sum(c['clicks'] for c in campaigns)
total_roas = total_revenue / total_spend if total_spend else 0.0
total_ctr = total_clicks / total_imp * 100 if total_imp else 0.0
total_cvr = total_orders / total_clicks * 100 if total_clicks else 0.0
total_cpa = total_spend / total_orders if total_orders else 0.0

top5 = sorted(campaigns, key=lambda c: c['revenue'], reverse=True)[:5]
worst5 = sorted(campaigns, key=lambda c: c['roas'])[:5]
all_c = campaigns  # CSV order, spend>0 only

def fmt_campaign(c):
    return ('{{name:"{name}",spend:{spend:.2f},revenue:{revenue:.2f},orders:{orders},'
            'imp:{imp},clicks:{clicks},roas:{roas:.2f},ctr:{ctr:.2f},cvr:{cvr:.2f},cpa:{cpa:.2f}}}').format(
        name=esc(c['name']), spend=c['spend'], revenue=c['revenue'], orders=c['orders'],
        imp=c['imp'], clicks=c['clicks'], roas=c['roas'], ctr=c['ctr'], cvr=c['cvr'], cpa=c['cpa'])

top5_js = '[' + ','.join(fmt_campaign(c) for c in top5) + ']'
worst5_js = '[' + ','.join(fmt_campaign(c) for c in worst5) + ']'
all_js = '[' + ','.join(fmt_campaign(c) for c in all_c) + ']'

shopee_obj = (
    'shopee:{{spend:{spend:.2f},revenue:{revenue:.2f},orders:{orders},imp:{imp},clicks:{clicks},'
    'roas:{roas:.2f},ctr:{ctr:.2f},cvr:{cvr:.2f},cpa:{cpa:.2f},top5:{top5},worst5:{worst5},all:{all}}}'
).format(
    spend=total_spend, revenue=total_revenue, orders=total_orders, imp=total_imp, clicks=total_clicks,
    roas=total_roas, ctr=total_ctr, cvr=total_cvr, cpa=total_cpa, top5=top5_js, worst5=worst5_js, all=all_js
)

print('CAMPAIGN_COUNT', len(campaigns))
print('TOTALS', json.dumps({
    'spend': round(total_spend,2), 'revenue': round(total_revenue,2), 'orders': total_orders,
    'imp': total_imp, 'clicks': total_clicks, 'roas': round(total_roas,2),
    'ctr': round(total_ctr,2), 'cvr': round(total_cvr,2), 'cpa': round(total_cpa,2)
}, ensure_ascii=False))
print('OBJ_LEN', len(shopee_obj))

with open('shopee_obj.txt', 'w', encoding='utf-8') as f:
    f.write(shopee_obj)

print('TOP5_NAMES', json.dumps([c['name'] for c in top5], ensure_ascii=False))
print('WORST5_NAMES', json.dumps([c['name'] for c in worst5], ensure_ascii=False))
