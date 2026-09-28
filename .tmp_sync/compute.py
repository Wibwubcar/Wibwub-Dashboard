import csv, io, json, sys

CSV_PATH = '/sessions/vigilant-epic-cannon/mnt/All/data Ads/Shopee/ข้อมูล-Shopee-Ads-01_09_2026-20_09_2026.csv'

with open(CSV_PATH, encoding='utf-8-sig') as f:
    lines = f.readlines()
header_idx = next(i for i, l in enumerate(lines) if l.startswith('ลำดับ'))
reader = csv.reader(io.StringIO(''.join(lines[header_idx:])))
headers = next(reader)
rows = [r for r in reader if r and r[0].strip() and r[0].strip().isdigit()]

def num(s):
    if s is None:
        return 0.0
    s = s.strip().replace(',', '').replace('%', '')
    if s == '' or s == '-':
        return 0.0
    return float(s)

campaigns = []
tot_spend = 0.0
tot_revenue = 0.0
tot_imp = 0
tot_clicks = 0
tot_orders = 0

for r in rows:
    name = r[1].strip()
    status = r[2].strip()
    imp = int(num(r[11]))
    clicks = int(num(r[12]))
    orders = int(num(r[16]))
    revenue = num(r[24])
    spend = num(r[26])
    roas_col = num(r[27])

    tot_spend += spend
    tot_revenue += revenue
    tot_imp += imp
    tot_clicks += clicks
    tot_orders += orders

    roas = round(revenue / spend, 2) if spend > 0 else 0.0
    ctr = round((clicks / imp) * 100, 2) if imp > 0 else 0.0
    cvr = round((orders / clicks) * 100, 2) if clicks > 0 else 0.0
    cpa = round(spend / orders, 2) if orders > 0 else 0.0

    campaigns.append({
        'name': name,
        'status': status,
        'spend': round(spend, 2),
        'revenue': round(revenue, 1) if revenue != int(revenue) else float(int(revenue)),
        'orders': orders,
        'imp': imp,
        'clicks': clicks,
        'roas': roas,
        'ctr': ctr,
        'cvr': cvr,
        'cpa': cpa,
    })

overall_roas = round(tot_revenue / tot_spend, 2) if tot_spend > 0 else 0.0
overall_ctr = round((tot_clicks / tot_imp) * 100, 2) if tot_imp > 0 else 0.0
overall_cvr = round((tot_orders / tot_clicks) * 100, 2) if tot_clicks > 0 else 0.0
overall_cpa = round(tot_spend / tot_orders, 2) if tot_orders > 0 else 0.0

print("=== TOTALS Sep 1-20 2026 ===")
print("spend:", round(tot_spend,2))
print("revenue:", round(tot_revenue,2))
print("orders:", tot_orders)
print("imp:", tot_imp)
print("clicks:", tot_clicks)
print("roas:", overall_roas)
print("ctr:", overall_ctr)
print("cvr:", overall_cvr)
print("cpa:", overall_cpa)
print("num campaigns:", len(campaigns))

# sort helpers
top5 = sorted(campaigns, key=lambda c: c['spend'], reverse=True)[:5]
worst5 = sorted(campaigns, key=lambda c: c['roas'])[:5]
all_sorted = sorted(campaigns, key=lambda c: c['spend'], reverse=True)

def fmt_entry(c):
    # match structure used in existing file: name, spend, revenue, orders, imp, clicks, roas, ctr, cvr, cpa
    rev = c['revenue']
    rev_str = f"{rev:.1f}" if isinstance(rev, float) else str(rev)
    name_escaped = c['name'].replace('\\', '\\\\').replace('"', '\\"')
    return ('{name:"%s",spend:%s,revenue:%s,orders:%d,imp:%d,clicks:%d,roas:%s,ctr:%s,cvr:%s,cpa:%s}' % (
        name_escaped,
        _num_str(c['spend']),
        rev_str,
        c['orders'],
        c['imp'],
        c['clicks'],
        _num_str(c['roas']),
        _num_str(c['ctr']),
        _num_str(c['cvr']),
        _num_str(c['cpa']),
    ))

def _num_str(x):
    if x == int(x):
        return str(int(x)) if abs(x) >= 1 else "0"
    return str(x)

top5_js = '[' + ','.join(fmt_entry(c) for c in top5) + ']'
worst5_js = '[' + ','.join(fmt_entry(c) for c in worst5) + ']'
all_js = '[' + ','.join(fmt_entry(c) for c in all_sorted) + ']'

def _snum(x):
    if x == int(x):
        return str(int(x))
    return str(x)

shopee_obj = (
    'shopee:{spend:%s,revenue:%s,orders:%d,imp:%d,clicks:%d,roas:%s,ctr:%s,cvr:%s,cpa:%s,'
    'top5:%s,worst5:%s,all:%s}'
) % (
    _snum(round(tot_spend, 2)),
    (f"{round(tot_revenue,1):.1f}" if round(tot_revenue,1) != int(round(tot_revenue,1)) else str(int(round(tot_revenue,1)))),
    tot_orders,
    tot_imp,
    tot_clicks,
    _snum(overall_roas),
    _snum(overall_ctr),
    _snum(overall_cvr),
    _snum(overall_cpa),
    top5_js,
    worst5_js,
    all_js,
)

with open('/sessions/vigilant-epic-cannon/mnt/All/.tmp_sync/shopee_obj.txt', 'w', encoding='utf-8') as f:
    f.write(shopee_obj)

with open('/sessions/vigilant-epic-cannon/mnt/All/.tmp_sync/summary.json', 'w', encoding='utf-8') as f:
    json.dump({
        'spend': round(tot_spend,2), 'revenue': round(tot_revenue,2), 'roas': overall_roas,
        'imp': tot_imp, 'clicks': tot_clicks, 'orders': tot_orders,
        'num_campaigns': len(campaigns)
    }, f, ensure_ascii=False, indent=2)

print()
print("shopee_obj length:", len(shopee_obj))
print(shopee_obj[:400])
