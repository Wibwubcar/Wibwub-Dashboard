// คัดลอกข้อมูลรายเดือน (DATA_PERIODS / TK_BREAKDOWN) จากหน้าเดิม WIBWUB_Ads_Dashboard.html → ads_periods.json
// งาน Shopee Ads / TikTok Ads ยังอัปเดตหน้าเดิมเหมือนเดิม สคริปต์นี้ทำให้หน้าใหม่ได้ตัวเลขรายเดือนเดียวกัน
const fs=require('fs'), path=require('path');
const DIR=path.join(__dirname,'..','..','data Ads');
const h=fs.readFileSync(path.join(DIR,'WIBWUB_Ads_Dashboard.html'),'utf8');
function grab(name){ const i=h.indexOf('const '+name+' ='); if(i<0) throw new Error('ไม่พบ '+name); let j=h.indexOf('=',i)+1; while(/\s/.test(h[j]))j++;
  const open=h[j], close=open==='{'?'}':']'; let d=0,k=j,inS=null;
  for(;k<h.length;k++){ const c=h[k],n=h[k+1];
    if(inS){ if(c==='\\'){k++;continue} if(c===inS) inS=null; continue }
    if(c==='/'&&n==='/'){ k=h.indexOf('\n',k); continue } if(c==='/'&&n==='*'){ k=h.indexOf('*/',k)+1; continue }
    if(c==='"'||c==="'"||c==='`'){ inS=c; continue }
    if(c===open)d++; else if(c===close){ d--; if(d===0) break } }
  return eval('('+h.slice(j,k+1)+')'); }
const DP=grab('DATA_PERIODS'), TK=grab('TK_BREAKDOWN');
const pick=(x,ks)=>Object.fromEntries(ks.filter(k=>x&&x[k]!==undefined).map(k=>[k,x[k]]));
const out={note:'ดึงจาก DATA_PERIODS/TK_BREAKDOWN ใน WIBWUB_Ads_Dashboard.html (ไฟล์ export รายเดือน) — sync โดย scripts/ads/sync_periods.js',months:{}};
for(const m of Object.keys(DP)){ const d=DP[m], t=TK[m]||{};
  out.months[m]={cover:d.cover?pick(d.cover,['shopeeDay','tiktokDay']):null,
    shopee:{...pick(d.shopee,['spend','revenue','orders','imp','clicks','roas','ctr','cvr','cpa']),campaigns:(d.shopee&&d.shopee.all)||[]},
    tiktok:{...pick(d.tiktok,['spend','revenue','orders','roas','cpa']),
      gmvMax:t.gmvMax?{total:t.gmvMax.total,campaigns:t.gmvMax.campaigns||[]}:null,
      gmvLive:t.gmvLive?{total:t.gmvLive.total,sessions:t.gmvLive.sessions||[]}:null,
      bizAds:t.bizAds?{total:t.bizAds.total,campaigns:t.bizAds.campaigns||[]}:null}}; }
const f=path.join(DIR,'ads_periods.json'); const s=JSON.stringify(out,null,1);
const old=fs.existsSync(f)?fs.readFileSync(f,'utf8'):''; if(old!==s) fs.writeFileSync(f,s);
console.log(JSON.stringify({periods_changed:old!==s, months:Object.keys(out.months)}));
