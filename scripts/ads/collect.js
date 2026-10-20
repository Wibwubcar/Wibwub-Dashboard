// WIBWUB ads daily — ดึงข้อมูลรายวันด้วยการ replay request จริงที่ hook.js จับไว้
// ใช้: window.__ADS={kind:'sh_real'|'sh_ads'|'tk_real'|'tk_ads'|'tk_camp'|'lz_real'|'lz_ads', from:'YYYY-MM-DD', to:'YYYY-MM-DD'} แล้ววางไฟล์นี้
// แล้ว poll: window.__adsJob  → {done:true, n, len, err?}   อ่านผล: window.__adsExport(0,900), (900,1800) … (ผลของ javascript_tool ถูกตัดที่ ~1000 ตัวอักษร)
(function(){
const P=window.__ADS||{}; const J=window.__adsJob={done:false,kind:P.kind};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const nextDay=d=>{const x=new Date(d+'T00:00:00Z'); x.setUTCDate(x.getUTCDate()+1); return x.toISOString().slice(0,10);};
const prevDay=d=>{const x=new Date(d+'T00:00:00Z'); x.setUTCDate(x.getUTCDate()-1); return x.toISOString().slice(0,10);};
const needHost=h=>{ if(!location.hostname.endsWith(h)) throw new Error('ต้องรันบนหน้า '+h+' (ตอนนี้อยู่ '+location.hostname+')'); };
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
    return out; },
  // แคมเปญย่อย GMV Max รายเดือน: ดึงเดือนของ to (ตั้งแต่วันที่ 1) และเดือนก่อนหน้าถ้า from อยู่ในเดือนก่อน
  async tk_camp(){ const c=cap(/post_campaign_list_v2/); const MK=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']; const out={};
    const ranges=[]; const mStart=P.to.slice(0,8)+'01'; ranges.push([mStart,P.to]);
    if (P.from<mStart){ const e=new Date(mStart+'T00:00:00Z'); e.setUTCDate(0); const ps=e.toISOString().slice(0,8)+'01'; ranges.push([ps,e.toISOString().slice(0,10)]); }
    for(const [a,b] of ranges){ const m=MK[+a.slice(5,7)-1]; out[m]={from:a,to:b};
      for(const [k,types] of [['product',['304','307']],['live',['305']]]){
        const o=JSON.parse(c.b); o.start_time=a; o.end_time=b; o.page=1; o.page_size=100;
        // ตั้ง filter เองให้เหมือนกันทุกครั้ง (ไม่ขึ้นกับว่าจับ request มาจากแท็บ Product หรือ LIVE) และไม่กรองแคมเปญที่ลบแล้ว
        o.filters=[{field:'external_type',filter_type:0,in_field_values:types},{field:'gmv_roi_mode',in_field_values:['2'],filter_type:10}];
        o.query_list=Array.from(new Set([...(o.query_list||[]),'campaign_name','cost','onsite_roi2_shopping_sku','onsite_roi2_shopping_value']));
        const j=await postJSON(c,o); if(j.code!==0) throw new Error(m+' '+k+' code '+j.code+' '+j.msg);
        if((j.data.pagination||{}).page_count>1) throw new Error(m+' '+k+' มีมากกว่า 100 แคมเปญ (หลายหน้า)');
        const rows=j.data.table_v2.map(r=>Object.fromEntries(r.map(x=>[x.name,x.data])));
        out[m][k]=rows.map(r=>({name:r.campaign_name,spend:+r.cost||0,orders:+r.onsite_roi2_shopping_sku||0,revenue:+r.onsite_roi2_shopping_value||0})).filter(r=>r.spend>0||r.revenue>0).sort((x,y)=>y.spend-x.spend);
        out[m][k+'_total']=+((j.data.statistics||{}).cost||0); await sleep(500); } }
    return out; },
  // ── Lazada ───────────────────────────────────────────────────────────────
  // ไม่ต้องใช้ hook/signature — ยิง same-origin ตรงได้ แต่ต้องเปิดหน้าที่ถูกต้องก่อน
  // (cookie/permission ผูกกับ path) ดูรายละเอียดใน scripts/task_prompts/ads_daily.md
  async lz_real(){ needHost('sellercenter.lazada.co.th'); const out={};
    for(const d of days){ const u='/ba/sycm/lazada/faas/dashboard/key/overviewV2.json?dateRange='+encodeURIComponent(d+'|'+d)+'&dateType=day';
      const j=await (await fetch(u,{credentials:'include'})).json();
      if(j.code!==0) throw new Error(d+' code '+j.code);
      const q=j.data||{}; if(!q.payAmount||!q.paidOrderAmount) throw new Error(d+' ไม่มี payAmount/paidOrderAmount');
      out[d]={gmv:+q.payAmount.value||0, orders:+q.paidOrderAmount.value||0}; await sleep(250); }
    return out; },
  async lz_ads(){ needHost('sellercenter.lazada.co.th'); const out={};
    for(const d of days){ const p=prevDay(d);
      const u='/sponsor/solutions/performance/report/overview.json?useRtTable=0&startDate='+d+'&endDate='+d+
              '&lastStartDate='+p+'&lastEndDate='+p+'&sceneIds=12020,12021,12022,12023,12024&attributionType=2';
      const j=await (await fetch(u,{credentials:'include'})).json();
      const o=j&&j.result&&j.result.reportOverview;
      if(!o) throw new Error(d+' ไม่มี reportOverview (success='+(j&&j.success)+' msg='+(j&&j.msg)+')');
      out[d]={spend:+o.spend||0, revenue:+o.revenue||0, orders:+o.order||0, imp:+o.impressions||0, clicks:+o.clicks||0};
      await sleep(300); }
    return out; }
};
if(!run[P.kind]){ J.err='kind ไม่ถูกต้อง'; J.done=true; return 'bad kind'; }
run[P.kind]().then(d=>{ J.data=d; J.n=Object.keys(d).length; J.done=true; J.text=JSON.stringify({kind:P.kind,from:P.from,to:P.to,data:d}); J.len=J.text.length; })
  .catch(e=>{ J.err=String(e&&e.message||e); J.done=true; });
window.__adsExport=(a,b)=>J.text?J.text.slice(a,b):'';
return 'started '+P.kind+' '+days.length+' วัน';
})();
