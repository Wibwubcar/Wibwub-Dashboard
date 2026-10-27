#!/usr/bin/env python3
"""WIBWUB ads daily — รวมผลจาก collect.js 4 ชุดเข้า data Ads/ads_daily.json

ใช้:
  python3 ads_daily_update.py state                       → บอกช่วงวันที่ที่ควรดึง (from/to)
  python3 ads_daily_update.py merge work/sh_real.json work/sh_ads.json work/tk_real.json work/tk_ads.json [--dry]
  python3 ads_daily_update.py camp work/tk_camp.json            → แคมเปญย่อย GMV Max รายเดือน → ads_tk_campaigns.json
  python3 ads_daily_update.py commit                      → sync ads_periods.json + bump sw.js + commit (เฉพาะไฟล์ที่เกี่ยวข้อง)
exit 10 = ไม่มีอะไรเปลี่ยน
"""
import json, os, sys, subprocess, datetime, re, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); ALL=os.path.abspath(os.path.join(HERE,'..','..'))
DAILY=os.path.join(ALL,'data Ads','ads_daily.json')
REFETCH_DAYS=3   # ดึงซ้ำย้อนหลัง 3 วันเสมอ เพราะยอด "ยืนยันแล้ว" ของวันล่าสุดยังขยับได้
def bkk_today(): return (datetime.datetime.utcnow()+datetime.timedelta(hours=7)).date()
def load(): return json.load(open(DAILY,encoding='utf-8'))
def iso(d): return d.isoformat()
def state():
    d=load(); last=max(d['days']); y=bkk_today()-datetime.timedelta(days=1)
    frm=min(datetime.date.fromisoformat(last)+datetime.timedelta(days=1), y-datetime.timedelta(days=REFETCH_DAYS-1))
    print(json.dumps({'last':last,'yesterday':iso(y),'from':iso(frm),'to':iso(y),'up_to_date': last>=iso(y)},ensure_ascii=False))
def readpart(p):
    o=json.load(open(p,encoding='utf-8')); return o['kind'],o['data']
def merge(paths, dry=False):
    parts={}
    for p in paths:
        k,data=readpart(p); parts[k]=data
    need={'sh_real','sh_ads','tk_real','tk_ads'}; opt={'lz_real','lz_ads'}
    miss=need-set(parts)
    if miss: sys.exit('ขาดชุดบังคับ: %s'%sorted(miss))
    extra=set(parts)-need-opt
    if extra: sys.exit('ชุดที่ไม่รู้จัก: %s'%sorted(extra))
    # Lazada เป็นออปชัน แต่ถ้าให้มาต้องให้ครบคู่ (กันเขียนข้างเดียวแล้วตัวเลขไม่สอดคล้อง)
    has_lz = bool(opt & set(parts))
    if has_lz and not opt <= set(parts): sys.exit('ถ้าจะอัปเดต Lazada ต้องให้ทั้ง lz_real และ lz_ads')
    y=iso(bkk_today()-datetime.timedelta(days=1))
    dates=sorted(set(parts['sh_real'])&set(parts['sh_ads'])&set(parts['tk_real'])&set(parts['tk_ads']))
    missing=sorted((set().union(*[set(parts[k]) for k in need]))-set(dates))
    if missing: sys.exit('บางชุดขาดวันที่: %s — ห้ามเขียนข้อมูลไม่ครบ'%missing)
    lz_dates=sorted(set(parts['lz_real'])&set(parts['lz_ads'])) if has_lz else []
    d=load(); changed=[]; warn=[]
    def neg(e,dt):
        for sec in e.values():
            for v in (sec.values() if all(isinstance(x,dict) for x in sec.values()) else [sec]):
                if any((isinstance(x,(int,float)) and x<0) for x in v.values()): sys.exit('ค่าติดลบวันที่ %s'%dt)
    def lz_entry(dt):
        return ({'gmv':round(float(parts['lz_real'][dt]['gmv']),2),'orders':int(parts['lz_real'][dt]['orders'])},
                {f:(int(parts['lz_ads'][dt][f]) if f in ('orders','imp','clicks') else round(float(parts['lz_ads'][dt][f]),2))
                 for f in ('spend','revenue','orders','imp','clicks')})
    for dt in sorted(set(dates)|set(lz_dates)):
        if dt>y: warn.append('ข้าม %s (ยังไม่จบวัน)'%dt); continue
        old=d['days'].get(dt)
        if dt in dates:
            e={'sh_real':{'gmv':int(round(parts['sh_real'][dt]['gmv'])),'orders':int(parts['sh_real'][dt]['orders'])},
               'sh_ads':{k:{f:int(parts['sh_ads'][dt][k][f]) for f in ('gmv_broad','gmv_direct','spend','orders')} for k in ('product','search','live')},
               'tk_real':{'gmv':round(float(parts['tk_real'][dt]['gmv']),2),'orders':int(parts['tk_real'][dt]['orders'])},
               'tk_ads':{k:{'gmv':round(float(parts['tk_ads'][dt][k]['gmv']),2),'spend':round(float(parts['tk_ads'][dt][k]['spend']),2),'orders':int(parts['tk_ads'][dt][k]['orders'])} for k in ('product','live')}}
            if e['sh_real']['gmv']==0 or e['tk_real']['gmv']==0: warn.append('%s ยอดขายจริงเป็น 0 — ตรวจสอบ'%dt)
        elif old:
            e={k:old[k] for k in need if k in old}      # Lazada อย่างเดียว: คง Shopee/TikTok เดิมไว้
        else:
            warn.append('ข้าม %s (มีแต่ Lazada ยังไม่มี Shopee/TikTok ของวันนี้)'%dt); continue
        if dt in lz_dates:
            e['lz_real'],e['lz_ads']=lz_entry(dt)
        elif old:                                       # ไม่ได้ส่ง Lazada มา -> ห้ามลบของเดิม
            for k in opt:
                if k in old: e[k]=old[k]
        neg(e,dt)
        if old!=e: changed.append((dt, old, e)); d['days'][dt]=e
    def tot(e):
        return (e['sh_real']['gmv'], sum(x['spend'] for x in e['sh_ads'].values()), e['tk_real']['gmv'],
                sum(x['spend'] for x in e['tk_ads'].values()),
                (e.get('lz_real') or {}).get('gmv'), (e.get('lz_ads') or {}).get('spend'))
    rows=[]
    for dt,old,e in changed:
        a=tot(e); b=tot(old) if old else None
        row={'date':dt,'new':not old,'sh_real':a[0],'sh_spend':a[1],'tk_real':a[2],'tk_spend':round(a[3],2)}
        if a[4] is not None: row['lz_real']=a[4]; row['lz_spend']=a[5]
        row['prev']=None if not b else {'sh_real':b[0],'sh_spend':b[1],'tk_real':b[2],'tk_spend':round(b[3],2),'lz_real':b[4],'lz_spend':b[5]}
        rows.append(row)
    d['days']=dict(sorted(d['days'].items())); last=max(d['days'])
    cov={'shopee':last,'tiktok':last}
    lzd=[k for k,v in d['days'].items() if 'lz_real' in v]
    if lzd: cov['lazada']=max(lzd)
    d['coverage']=cov
    m=last[:7]; ds=[v for k,v in d['days'].items() if k.startswith(m)]
    month={'month':m,'days':len(ds),'sh_real':sum(x['sh_real']['gmv'] for x in ds),'sh_spend':sum(sum(t['spend'] for t in x['sh_ads'].values()) for x in ds),
           'tk_real':round(sum(x['tk_real']['gmv'] for x in ds),2),'tk_spend':round(sum(sum(t['spend'] for t in x['tk_ads'].values()) for x in ds),2)}
    lzm=[x for x in ds if 'lz_real' in x]
    if lzm: month['lz_days']=len(lzm); month['lz_real']=round(sum(x['lz_real']['gmv'] for x in lzm),2); month['lz_spend']=round(sum(x['lz_ads']['spend'] for x in lzm),2)
    print(json.dumps({'changed':rows,'warnings':warn,'coverage':cov,'month_to_date':month},ensure_ascii=False,indent=1))
    if not changed: sys.exit(10)
    if not dry:
        shutil.copy2(DAILY, DAILY+'.bak')
        tmp=DAILY+'.tmp'; json.dump(d,open(tmp,'w',encoding='utf-8'),ensure_ascii=False,indent=1); os.replace(tmp,DAILY)
TKC=os.path.join(ALL,'data Ads','ads_tk_campaigns.json')
def camp(path):
    o=json.load(open(path,encoding='utf-8'))
    if o.get('kind')!='tk_camp': sys.exit('ไฟล์ไม่ใช่ tk_camp')
    d=json.load(open(TKC,encoding='utf-8')) if os.path.exists(TKC) else {'note':'','months':{}}
    rep=[]; changed=False
    for m,v in o['data'].items():
        for k in ('product','live'):
            s=round(sum(x['spend'] for x in v[k]),2); t=round(float(v.get(k+'_total',s)),2)
            if abs(s-t)>1: sys.exit('%s %s ผลรวมแคมเปญ %.2f ไม่ตรงยอดรวม %.2f'%(m,k,s,t))
        new={'from':v['from'],'to':v['to'],'product':v['product'],'live':v['live']}
        if d['months'].get(m)!=new: d['months'][m]=new; changed=True
        rep.append({'month':m,'to':v['to'],'product_campaigns':len(v['product']),'product_spend':round(sum(x['spend'] for x in v['product']),2),'live_campaigns':len(v['live']),'live_spend':round(sum(x['spend'] for x in v['live']),2)})
    print(json.dumps({'tk_camp':rep,'changed':changed},ensure_ascii=False))
    if not changed: sys.exit(10)
    tmp=TKC+'.tmp'; json.dump(d,open(tmp,'w',encoding='utf-8'),ensure_ascii=False,indent=1); os.replace(tmp,TKC)
def git(*a): return subprocess.run(['git',*a],cwd=ALL,capture_output=True,text=True,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
def unlock():
    for f in ('index.lock','HEAD.lock','objects/maintenance.lock'):
        p=os.path.join(ALL,'.git',f)
        if os.path.exists(p): os.rename(p, os.path.join(ALL,'.git','stale-%d-%s'%(datetime.datetime.now().timestamp()*1e6, os.path.basename(f))))
def commit():
    r=subprocess.run(['node',os.path.join(HERE,'sync_periods.js')],cwd=ALL,capture_output=True,text=True); print(r.stdout.strip()); 
    if r.returncode: sys.exit('sync_periods ล้มเหลว: '+r.stderr[-500:])
    files=['data Ads/ads_daily.json','data Ads/ads_periods.json','data Ads/ads_tk_campaigns.json']
    unlock(); st=git('status','--porcelain','--',*files).stdout.strip()
    if not st: print('NO_CHANGE'); sys.exit(10)
    sw=os.path.join(ALL,'sw.js'); s=open(sw,encoding='utf-8').read(); mm=re.search(r'wibwub-v(\d+)',s)
    s=s.replace(mm.group(0),'wibwub-v%d'%(int(mm.group(1))+1),1); open(sw,'w',encoding='utf-8').write(s)
    d=load()
    for _ in range(3):   # โฟลเดอร์ Google Drive บางครั้งเขียน .git/index ไม่ทัน ("unable to write new_index file") ให้ลองใหม่
        unlock(); r=git('add','--',*files,'sw.js'); unlock()
        if r.returncode==0: break
        import time; time.sleep(3)
    else: sys.exit('git add ล้มเหลว: '+r.stderr[-300:])
    # ข้อความ commit ต้องบอกว่ารอบนี้ "เพิ่มข้อมูลรายวันจริงไหม" ไม่ใช่บอกวันสูงสุดที่มีอยู่แล้วในไฟล์
    # (27 ต.ค. 69: รอบ 08:35 merge ไม่ได้รันเพราะ TikTok Shop login หลุด แต่ขั้น commit ยังเขียน
    #  "ถึง 2026-10-25" จาก max(d['days']) เดิม = commit 67c564c ที่แตะแค่ ads_periods/ads_tk_campaigns/sw.js
    #  แต่ดูเหมือนรอบปกติทุกประการ ทำให้ไม่มีใครรู้ว่าวันที่ 26 หายไป)
    dirty={l[3:].strip().strip('"') for l in st.splitlines() if l.strip()}
    if 'data Ads/ads_daily.json' in dirty:
        msg='auto: ads daily (ยอดจริง vs Ads) ถึง %s'%max(d['days'])
    else:
        other=sorted(x.split('/')[-1] for x in dirty)
        msg='auto: ads daily — ไม่มีข้อมูลรายวันใหม่ (รายวันยังถึง %s) · อัปเดตเฉพาะ %s'%(max(d['days']),', '.join(other))
    r=git('-c','user.name=WIBWUB Bot','-c','user.email=marketingwibwub@gmail.com','commit','-m',msg,'--',*files,'sw.js'); unlock()
    print(r.stdout.strip() or r.stderr.strip()); print(git('log','-1','--format=%h %s').stdout.strip())
if __name__=='__main__':
    a=sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0]=='state': state()
    elif a[0]=='merge': merge([x for x in a[1:] if not x.startswith('--')], dry='--dry' in a)
    elif a[0]=='camp': camp(a[1])
    elif a[0]=='commit': commit()
    else: sys.exit(__doc__)
