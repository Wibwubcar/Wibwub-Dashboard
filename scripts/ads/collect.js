// WIBWUB ads daily — ดึงข้อมูลรายวันด้วยการ replay request จริงที่ hook.js จับไว้
// ใช้: window.__ADS={kind:'sh_real'|'sh_ads'|'tk_real'|'tk_ads', from:'YYYY-MM-DD', to:'YYYY-MM-DD'} แล้ววางไฟล์นี้
// แล้ว poll: window.__adsJob  → {done:true, n, err?}   อ่านผล: window.__adsExport(0,1500), (1500,3000) …
(function(){
const P=window.__ADS||{}; const J=window.__adsJob={done:false,kind:P.kind};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const nextDay=d=>{const x=new Date(d+'T00:00:00Z'); x.setUTCDate(x.getUTCDate()+1); return x.toISOString().slice(0,10);};
const ts=d=>Math.floor(new Date(d+'T00:00:00+07:00')/1000);
const days=[]; for(let d=P.from; d<=P.to; d=nextDay(d)) days.push(d);
const cap=re=>{ const c=(window.__cap||[]).filter(c=>re.test(c.u)).pop(); if(!c) throw new Error('ยังไม่ได้จับ request '+re+' — ให้หน้าเว็บโหลดข้อมูลก่อน'); return c; };
async function postJSON(c, body){ const r=await fetch(c.u,{method:'POST',credentials:'include',headers:c.h,body:JSON.stringify(body)}); return r.json(); }
const run={
  async sh_real(){ const c=cap(/key-metrics/); const out={};
    for(const d of days){ const u=new URL(c.u,location.origin); u.searchParams.set('start_time',ts(d)); u.searchParams.set('end_time',ts(d)+86400); u.searchParams.set('period','day');
      const j=await (await fetch(u.toString(),{credentials:'include'})).json(); if(j.code!==0) throw new Error(d+' code '+j.code+' '+j.msg);
      out[d]={gmv:j.result.confirmed_gmv.value, orders:j.result.confirmed_orders.value}; await sleep(400); }
    return out; },
  async sh_ads(){ const c=cap(/get_time_graph/); const out={}; days.forEach(d=>out[d]={});
    for(const [k,ct] of [['product','product_homepage_v2'],['search','shop_homepage'],['live','live_stream_homepage']]){
      const o=JSON.parse(c.b); o.campaign_type=ct; o.start_time=ts(P.from); o.end_time=ts(P.to)+86399;
      const j=await postJSON(c,o); if(j.code!==0) throw new Error(k+' code '+j.code+' '+j.msg);
      for(const r of j.data.report_by_time){ const d=new Date((+r.key+7*3600)*1000).toISOString().slice(0,10); if(!out[d]) continue; const m=r.metrics;
        out[d][k]={gmv_broad:Math.round(m.broad_gmv/1e5), gmv_direct:Math.round((m.direct_gmv||0)/1e5), spend:Math.round(m.cost/1e5), orders:m.broad_order||0}; }
      await sleep(500); }
    for(const d of days) for(const k of ['product','search','live']) if(!out[d][k]) throw new Error('ขาด '+k+' วันที่ '+d);
    return out; },
  async tk_real(){ const c=cap(/us_overview_day_trend/); const o=JSON.parse(c.b); const q=o.query_condition[0];
    const n=days.length, cs=new Date(P.from+'T00:00:00Z'); cs.setUTCDate(cs.getUTCDate()-n); const ce=new Date(P.from+'T00:00:00Z'); ce.setUTCDate(ce.getUTCDate()-1);
    q.query_time.start=P.from; q.query_time.end=P.to; q.compare_to_time={start:cs.toISOString().slice(0,10), end:ce.toISOString().slice(0,10)};
    const j=await postJSON(c,o); if(j.code!==0) throw new Error('code '+j.code+' '+j.message);
    const amt=v=>{ try{ return +JSON.parse(v).amount; }catch(e){ return +v; } }; const out={};
    for(const iv of j.data[0].intervals){ const v=iv.rows[0].values; out[iv.start_date]={gmv:amt(v['4211']), orders:+v['4214']}; }
    for(const d of days) if(!out[d]) throw new Error('ขาดวันที่ '+d);
    return out; },
  async tk_ads(){ const c=cap(/post_overview_stat/); const out={}; days.forEach(d=>out[d]={});
    for(const [k,t] of [['product','304'],['live','305']]){ const o=JSON.parse(c.b); o.external_type_list=[t]; o.start_time=P.from; o.end_time=P.to;
      const j=await postJSON(c,o); if(j.code!==0) throw new Error(k+' code '+j.code+' '+j.msg);
      const ch=j.data.chart, S=n=>ch.series.find(s=>s.name===n).data;
      const cost=S('cost'), ord=S('onsite_roi2_shopping_sku'), val=S('onsite_roi2_shopping_value');
      ch.categories.forEach((d,i)=>{ if(out[d]) out[d][k]={gmv:+val[i]||0, spend:+cost[i]||0, orders:+ord[i]||0}; });
      await sleep(500); }
    for(const d of days) for(const k of ['product','live']) if(!out[d][k]) throw new Error('ขาด '+k+' วันที่ '+d);
    return out; }
};
if(!run[P.kind]){ J.err='kind ไม่ถูกต้อง'; J.done=true; return 'bad kind'; }
run[P.kind]().then(d=>{ J.data=d; J.n=Object.keys(d).length; J.done=true; J.text=JSON.stringify({kind:P.kind,from:P.from,to:P.to,data:d}); J.len=J.text.length; })
  .catch(e=>{ J.err=String(e&&e.message||e); J.done=true; });
window.__adsExport=(a,b)=>J.text?J.text.slice(a,b):'';
return 'started '+P.kind+' '+days.length+' วัน';
})();
