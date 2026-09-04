import zipfile, re, os, glob
from collections import Counter
from datetime import date

_BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID_DIR=os.path.join(_BASE,'Data Affiliate','วีดีโอ')+'/'
HTML=os.path.join(_BASE,'WIBWUB_Affiliate_Dashboard.html')
fpath=sorted(glob.glob(VID_DIR+'*.xlsx'), key=os.path.getmtime, reverse=True)[0]
print("Using:", os.path.basename(fpath))

zf=zipfile.ZipFile(fpath)
content=zf.open('xl/worksheets/sheet1.xml').read().decode('utf-8',errors='replace')
row_pattern=re.compile(r'<row r="(\d+)"[^>]*>(.*?)</row>', re.DOTALL)
cell_pattern=re.compile(r'<c r="([A-Z]+)(\d+)"[^>]*>(?:<is><t[^>]*>(.*?)</t></is>|<v>(.*?)</v>)?</c>')
def col_to_idx(c):
    i=0
    for ch in c: i=i*26+(ord(ch)-64)
    return i-1
def parse_thb(s):
    if not s: return 0.0
    s=s.replace('฿','').replace(',','').strip()
    try: return float(s)
    except: return 0.0
rows={}
for rm in row_pattern.finditer(content):
    rnum=int(rm.group(1))
    if rnum<3: continue
    rd={}
    for cm in cell_pattern.finditer(rm.group(2)):
        col,r,tv,nv=cm.groups(); idx=col_to_idx(col)
        val=tv if tv is not None else nv
        if val is not None:
            val=val.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&apos;',"'")
        rd[idx]=val
    if rd: rows[rnum]=rd
new_data={}
for r in rows.values():
    vid=r.get(1)
    if not vid: continue
    new_data[vid]={'creator':r.get(4,''),'product_id':r.get(5,''),'gmv':parse_thb(r.get(6))}
print("parsed video rows:", len(new_data))

html=open(HTML,encoding='utf-8').read()
m=re.search(r'const VIDEOS = \[(.*?)\n\];', html, re.DOTALL); block=m.group(1)
fm=re.search(r'monthly:\{([a-z:,\d.]+)\}', block)
schema_keys=re.findall(r'([a-z]+):', fm.group(1)) if fm else []
print("schema:", schema_keys)
MONTH_KEY={1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',8:'aug',9:'sep',10:'oct',11:'nov',12:'dec'}
THAI={'jan':'ม.ค.','feb':'ก.พ.','mar':'มี.ค.','apr':'เม.ย.','may':'พ.ค.','jun':'มิ.ย.','jul':'ก.ค.','aug':'ส.ค.','sep':'ก.ย.','oct':'ต.ค.','nov':'พ.ย.','dec':'ธ.ค.'}
_dm=re.search(r'(\d{8})-(\d{8})', os.path.basename(fpath))
if _dm:
    cur_key=MONTH_KEY[int(_dm.group(2)[4:6])]
    print("month key from filename:", cur_key)
else:
    cur_key=MONTH_KEY[date.today().month]
    print("WARNING: no date range in filename, falling back to today ->", cur_key)
if cur_key not in schema_keys:
    last=schema_keys[-1]
    block,n=re.subn(r"("+last+r":[\d.]+)\}", r"\1,"+cur_key+r":0}", block)
    print(f"extended {n} entries with '{cur_key}'"); schema_keys.append(cur_key)

entry_re=re.compile(
 r"\{creator:'(?P<creator>[^']*)',product:'(?P<product>[^']*)',vid_id:'(?P<vid_id>[^']*)',"
 r"caption:'(?P<caption>[^']*)',gmv:(?P<gmv>[\d.]+),units:(?P<units>[\d.]+),date:'(?P<date>[^']*)',"
 r"monthly:\{"+",".join(f"{k}:(?P<{k}>[\\d.]+)" for k in schema_keys)+r"\}\}")
existing=[]
for em in entry_re.finditer(block):
    d=em.groupdict()
    for k in ['gmv','units']+schema_keys: d[k]=float(d[k])
    existing.append(d)
print("parsed existing VIDEOS entries:", len(existing))
if not existing:
    raise SystemExit("STOP: entry_re matched 0 — schema changed, not writing")

vid_to_product={e['vid_id']:e['product'] for e in existing}
existing_vids=set(vid_to_product)
pid_names={}
for vid,rec in new_data.items():
    if vid in vid_to_product:
        for pid in (rec.get('product_id') or '').split(','):
            pid=pid.strip()
            if pid: pid_names.setdefault(pid,Counter())[vid_to_product[vid]]+=1
pid_to_name={p:c.most_common(1)[0][0] for p,c in pid_names.items()}

def date_label(e):
    active=[k for k in schema_keys if e[k]>0]
    if not active: return ''
    if len(active)==1: return THAI[active[0]]
    # convention in VIDEOS is FIRST active month – LAST active month (not last-two)
    return f"{THAI[active[0]]}–{THAI[active[-1]]}"

updated=0
for e in existing:
    v=e['vid_id']
    if v in new_data:
        ng=round(new_data[v]['gmv'])
        if ng!=e[cur_key]: updated+=1
        e[cur_key]=ng
    e['gmv']=sum(e[k] for k in schema_keys)
    e['date']=date_label(e)
print("updated current-month(",cur_key,") values:",updated)

min_gmv=min(e['gmv'] for e in existing)
new_only=[v for v in new_data if v not in existing_vids]
cands=sorted(({**new_data[v],'vid_id':v} for v in new_only if new_data[v]['gmv']>=min_gmv), key=lambda x:-x['gmv'])
new_entries=[]
for c in cands:
    name=None
    for p in (c.get('product_id') or '').split(','):
        p=p.strip()
        if p in pid_to_name: name=pid_to_name[p]; break
    monthly={k:0.0 for k in schema_keys}; monthly[cur_key]=round(c['gmv'])
    new_entries.append({'creator':c['creator'],'product':name or 'Unknown','vid_id':c['vid_id'],
        'caption':'','gmv':round(c['gmv']),'units':0.0,'date':THAI[cur_key],**monthly})
print("new video entries added:", len(new_entries))

def esc(s): return s.replace('\\','\\\\').replace("'","\\'")
def fmt(e):
    ms=",".join(f"{k}:{round(e[k])}" for k in schema_keys)
    return "  {creator:'%s',product:'%s',vid_id:'%s',caption:'%s',gmv:%d,units:%d,date:'%s',monthly:{%s}}"%(
        esc(e['creator']),esc(e['product']),e['vid_id'],esc(e['caption']),round(e['gmv']),round(e['units']),e['date'],ms)
lines=[fmt(e) for e in existing]+[fmt(e) for e in new_entries]
new_block="const VIDEOS = [\n"+",\n".join(lines)+",\n];"
html2=re.sub(r'const VIDEOS = \[.*?\n\];', lambda _: new_block, html, count=1, flags=re.DOTALL)
assert html2!=html, "rewrite failed"
open(HTML,'w',encoding='utf-8').write(html2)
print("TOTAL VIDEOS written:",len(lines),"| updated:",updated,"| new:",len(new_entries))
