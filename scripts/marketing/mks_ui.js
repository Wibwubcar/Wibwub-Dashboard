/* เมนู "การตลาด vs ยอดขาย" — ดีไซน์ที่ผู้ใช้อนุมัติ 28 ต.ค. 69
   ข้อมูลรายวันอยู่ใน MKT_SPEND (เขียนโดย scripts/marketing/marketing_update.py)
   หน้าเว็บคำนวณทุกตัวเลขเองตามช่วงวันที่ที่เลือก — อย่าแก้ไฟล์นี้ในหน้า HTML
   แก้ที่ scripts/marketing/mks_ui.js แล้วรัน scripts/marketing/marketing_ui.py

   กราฟวาดเป็น SVG เอง ไม่ใช้ Chart.js เพราะ WIBWUB_Mobile.html ไม่ได้โหลดไลบรารีนั้น

   นิยามที่ผู้ใช้อนุมัติ: ค่าการตลาดทั้งหมด = ค่าแอด 4 แพลตฟอร์ม + KOL
   + คอมแอฟฟิลิเอต TikTok (+ Event เมื่อมีข้อมูล) — ใช้ชุดเดียวกันทุกจุดในหน้านี้
   ของเดิมการ์ดไม่รวมคอมแอฟแต่วงกลมรวม ทำให้สัดส่วนรวมได้ 110.8% ซึ่งเป็นบั๊ก */

/* g = กลุ่มของแถบ "เงินไปไหน" — เพิ่มหมวดใหม่แล้วสูตรคิดเองอัตโนมัติ
   พอ Event / Facebook Ads มีข้อมูลจริง แค่ปลด na ออก ไม่ต้องแก้สูตรที่อื่น */
const MKS_CAT = [
  {k:'ads_sh', n:'Ads Shopee',   c:'#EE4D2D', g:'ads'},
  {k:'ads_tk', n:'Ads TikTok',   c:'#111827', g:'ads'},
  {k:'ads_lz', n:'Ads Lazada',   c:'#3B2CC4', g:'ads'},
  {k:'ads_fb', n:'Ads Facebook', c:'#1877F2', g:'ads'},
  {k:'kol',    n:'KOL',          c:'#A78BFA', g:'kol'},
  {k:'event',  n:'Event',        c:'#D1D5DB', g:'event'}
];
/* หมวดไหน "รอข้อมูล" ไม่ได้ hardcode ไว้ — marketing_update.py ส่ง missing มาให้
   พอกรอกค่า Event/Facebook ลง data Ads/mkt_manual.json แล้วรันสคริปต์
   คีย์นั้นจะหลุดจาก missing เอง ทุกกราฟและสูตร % จะเริ่มนับทันที ไม่ต้องแก้ไฟล์นี้ */
function mksNA(k){ return ((typeof MKT_SPEND!=='undefined' && MKT_SPEND.missing)||[]).indexOf(k)>=0; }
MKS_CAT.forEach(c=>Object.defineProperty(c,'na',{get:function(){return mksNA(this.k);}}));

/* ช่องทางยอดขาย — ต้องครบเท่าคีย์ที่ marketing_update.py ส่งมา ไม่งั้นยอดรวมจะขาด
   ⚠️ `kol` ใน keys เป็น "ค่าใช้จ่าย" ไม่ใช่ช่องทางขาย ห้ามเอามารวมเป็นยอดขาย */
const MKS_REV_CAT = [
  {k:'sh',   n:'Shopee',    c:'#EE4D2D'},
  {k:'tk',   n:'TikTok',    c:'#111827'},
  {k:'fb',   n:'Facebook',  c:'#1877F2'},
  {k:'line', n:'LINE',      c:'#06A755'},
  {k:'care', n:'Carcare',   c:'#0E7490'},
  {k:'lz',   n:'Lazada',    c:'#3B2CC4'},
  {k:'pos',  n:'POS',       c:'#0F766E'},
  {k:'web',  n:'Website',   c:'#64748B'},
  {k:'mkt',  n:'สินค้าการตลาด', c:'#A855F7'},
  {k:'beuk', n:'เบิกของ',    c:'#9CA3AF'},
  {k:'oth',  n:'อื่น ๆ',     c:'#CBD5E1'}
];
const MKS_REVK = MKS_REV_CAT.map(c=>c.k);

/* ── ค่าธรรมเนียมแพลตฟอร์ม ────────────────────────────────────────────
   อัตราคงที่ที่ผู้ใช้กำหนด มาจาก data Ads/platform_fee.json (ไม่ hardcode ที่นี่)
   คิดจาก "ยอดขายของช่องทางนั้น × อัตรา" ไม่ใช่ยอดรวม เพราะแต่ละเจ้าคิดคนละอัตรา
   ช่องทางขายตรง (Facebook/LINE/POS/เว็บ) ไม่มีค่าธรรมเนียมจริง ๆ ไม่ใช่ขาดข้อมูล */
function mksFeeRates(){ return (typeof MKT_SPEND!=='undefined' && MKT_SPEND.fee_rates) || {}; }
/* อัตราของช่องทางหนึ่งเขียนได้ 2 แบบ
     0.30                                   = คงที่ตลอด
     [{from:'2026-01-01',rate:0.2154}, …]   = เปลี่ยนตามวันที่ (เรียงจากเก่าไปใหม่) */
function mksRateOn(spec, d){
  if(typeof spec==='number') return spec;
  if(!Array.isArray(spec) || !spec.length) return 0;
  let r=spec[0].rate;
  for(const s of spec){ if(d>=s.from) r=s.rate; else break; }
  return r;
}
/* ค่าการตลาดบางก้อนไม่มีคอลัมน์รายวัน แต่คิดจาก "ยอดขายช่องทางนั้น × อัตรา"
   เช่น คอมแอฟฟิลิเอต TikTok ที่หักผ่านระบบ settlement ของแพลตฟอร์ม
   นิยามอยู่ใน data Ads/platform_fee.json -> marketing_rates (ไม่ hardcode ที่นี่)
   ⚠️ อัตราค่าธรรมเนียมของช่องทางนั้นต้องหักก้อนนี้ออกไปแล้ว ไม่งั้นนับซ้ำ */
function mksMktRateCats(){
  const M=(typeof MKT_SPEND!=='undefined' && MKT_SPEND.mkt_rates)||{};
  return Object.keys(M).map(k=>({k:k, n:M[k].label||k, c:M[k].color||'#8B5CF6',
                                 g:M[k].group||'kol', base:M[k].base, spec:M[k].rates||[],
                                 na:false, rate:true}));
}
function mksFeeCats(){
  const R=mksFeeRates(), L=(typeof MKT_SPEND!=='undefined' && MKT_SPEND.fee_labels)||{};
  return Object.keys(R).map(k=>{ const c=MKS_REV_CAT.find(x=>x.k===k)||{};
    return {k:k, n:L[k]||c.n||k, c:c.c||'#6B7280', spec:R[k]}; });
}
const MKS_SRC = [
  {k:'sales',   n:'ยอดขาย'},
  {k:'shopee',  n:'Ads Shopee'},
  {k:'tiktok',  n:'Ads TikTok'},
  {k:'lazada',  n:'Ads Lazada'},
  {k:'shipnity',n:'ช่องทาง Shipnity'},
  {k:'kol',     n:'KOL (จ่ายล่าสุด)'}
];
let MKS_ST = {preset:'mtd', from:null, to:null};

function mksN(v){ return Math.round(v||0).toLocaleString('en-US'); }
function mksB(v){ return '฿'+mksN(v); }
function mksP(v,d){ return isFinite(v)&&v!=null ? (v*100).toFixed(d==null?1:d)+'%' : '–'; }
function mksX(v){ return isFinite(v)&&v>0 ? v.toFixed(2)+'x' : '–'; }
function mksDiv(a,b){ return b? a/b : NaN; }
function mksEsc(s){ return String(s==null?'':s).replace(/[&<>"]/g,
  c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function mksD(s){ const p=(s||'').split('-'); return p.length===3 ? (+p[2])+'/'+(+p[1]) : (s||'-'); }
/* บวก/ลบวันแบบ UTC ล้วน — ห้ามใช้ new Date('YYYY-MM-DD') + toISOString()
   เพราะสตริงเปล่าถูกตีเป็น UTC แต่ setDate/getDate ทำงานตามเขตเวลาเครื่อง (+07)
   ทำให้ผลลัพธ์เลื่อนไป 1 วัน (เคยทำให้ "7 วัน" ได้ 8 วัน และ "เดือนก่อน" จบที่ 29 ก.ย.) */
function mksAdd(s,n){
  const p=s.split('-').map(Number);
  const d=new Date(Date.UTC(p[0],p[1]-1,p[2]+n));
  return d.getUTCFullYear()+'-'+String(d.getUTCMonth()+1).padStart(2,'0')+
         '-'+String(d.getUTCDate()).padStart(2,'0');
}
function mksDiffDays(a,b){
  const x=a.split('-').map(Number), y=b.split('-').map(Number);
  return Math.round((Date.UTC(y[0],y[1]-1,y[2])-Date.UTC(x[0],x[1]-1,x[2]))/864e5);
}
const MKS_TH=['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'];
function mksTH(d,y){ return (+d.slice(8,10))+' '+MKS_TH[+d.slice(5,7)-1]+
  (y?' '+((+d.slice(0,4))+543):''); }
function mksTHR(a,b){ return a===b? mksTH(a,1) : mksTH(a)+' – '+mksTH(b,1); }
function TH_MF_SHORT(m){ return MKS_TH[+m.slice(5,7)-1]+' '+((+m.slice(0,4)+543)%100); }
function mksMonthEnd(d){ const x=new Date(Date.UTC(+d.slice(0,4), +d.slice(5,7), 0));
  return x.toISOString().slice(0,10); }

/* วันทั้งหมดที่มีข้อมูล (เรียงแล้ว) */
function mksAll(){ return Object.keys(MKT_SPEND.days).sort(); }
/* หมวดค่าการตลาดทั้งหมด = หมวดที่มีคอลัมน์รายวัน + หมวดที่คิดจากอัตรา */
function mksSpendCats(){ return MKS_CAT.concat(mksMktRateCats()); }

/* คำนวณช่วงของปุ่มลัด — ยึด asof เป็น "วันนี้" ของข้อมูล ไม่ใช่วันจริงของเครื่อง */
function mksPreset(p){
  const all=mksAll(), last=MKT_SPEND.asof, lo=all[0];
  if(p==='7')   return [mksAdd(last,-6), last];
  if(p==='30')  return [mksAdd(last,-29), last];
  if(p==='mtd') return [last.slice(0,8)+'01', last];
  if(p==='prev'){
    const first=last.slice(0,8)+'01', end=mksAdd(first,-1);
    return [end.slice(0,8)+'01', end];
  }
  return [lo, last];
}

/* อัตราที่ใช้จริงในช่วงที่เลือก = ค่าธรรมเนียม ÷ ยอดขายของช่องทางนั้น
   ถ้าช่วงคร่อมการปรับอัตรา ตัวเลขนี้จะเป็นค่าเฉลี่ยถ่วงน้ำหนัก และต่อท้ายด้วย ~ */
function mksRatePct(A,c){
  const base=A.rv[c.k]||0; if(!base) return '–';
  const eff=(A.fv[c.k]||0)/base*100;
  const many=Array.isArray(c.spec) && c.spec.length>1;
  return (many?'~':'')+eff.toFixed(2)+'%';
}
function mksFeeLabel(A){ return mksFeeCats().map(c=>c.n+' '+mksRatePct(A,c)).join(' · '); }
/* เดือนที่ยอด settlement ยังไหลเข้าไม่ครบ จะถูกทำเครื่องหมาย prov ไว้
   ถ้าช่วงที่เลือกคร่อมเดือนพวกนั้น ต้องบอกผู้ใช้ว่าตัวเลขยังขยับได้ */
function mksProvMonths(from,to){
  const out=new Set();
  const all=mksFeeCats().concat(mksMktRateCats());
  all.forEach(c=>{ if(!Array.isArray(c.spec)) return;
    c.spec.forEach(s=>{ if(s.prov && s.from<=to){
      const e=mksMonthEnd(s.from); if(e>=from) out.add(s.from.slice(0,7)); } }); });
  return [...out].sort();
}

/* รวมตัวเลขในช่วง — คืน null สำหรับหมวดที่ยังไม่มีข้อมูล (ห้ามนับเป็น 0) */
function mksAgg(from,to){
  const K=MKT_SPEND.keys, ix={}; K.forEach((k,i)=>ix[k]=i);
  let rev=0, days=0; const sp={}, rv={};
  MKS_CAT.forEach(c=>{ sp[c.k]= c.na ? null : 0; });
  MKS_REVK.forEach(k=>rv[k]=0);
  const fv={}; let fee=0;
  mksFeeCats().forEach(c=>{ fv[c.k]=0; });
  const MR=mksMktRateCats();
  MR.forEach(c=>{ sp[c.k]=0; });
  mksAll().forEach(d=>{
    if(d<from||d>to) return;
    const r=MKT_SPEND.days[d]; days++;
    MKS_REVK.forEach(k=>{ if(ix[k]!=null){ rev+=r[ix[k]]||0; rv[k]+=r[ix[k]]||0; } });
    MKS_CAT.forEach(c=>{ if(!c.na && ix[c.k]!=null) sp[c.k]+=r[ix[c.k]]||0; });
    mksFeeCats().forEach(c=>{ if(ix[c.k]==null) return;
      fv[c.k]+=(r[ix[c.k]]||0)*mksRateOn(c.spec,d); });
    MR.forEach(c=>{ if(ix[c.base]==null) return;
      sp[c.k]+=(r[ix[c.base]]||0)*mksRateOn(c.spec,d); });
  });
  mksFeeCats().forEach(c=>{ fee+=fv[c.k]; });
  /* ⚠️ ต้องรวม "หลัง" ลูปเสมอ — ของเดิมรวมก่อน ทำให้คอมแอฟฟิลิเอตหล่นหายจากการ์ด
     ทั้งที่ยังอยู่ในวงกลม สัดส่วนเลยรวมกันได้ 110.8% */
  const spend=mksSpendCats().reduce((s,c)=>s+(sp[c.k]||0),0);
  const ads=MKS_CAT.filter(c=>c.g==='ads').reduce((s,c)=>s+(sp[c.k]||0),0);
  const kol=MKS_CAT.filter(c=>c.g==='kol').reduce((s,c)=>s+(sp[c.k]||0),0)
          + MR.reduce((s,c)=>s+(sp[c.k]||0),0);
  const net=rev-fee;
  return {rev, rv, sp, spend, ads, kol, days, fv, fee, net, left:rev-fee-spend,
          pct: rev? spend/rev*100 : null, roi: spend? rev/spend : null,
          pctNet: net>0? spend/net*100 : null, roiNet: spend? net/spend : null};
}

/* ช่วงก่อนหน้าที่ยาวเท่ากัน จบก่อนวันเริ่มของช่วงปัจจุบัน 1 วัน */
function mksPrevRange(from,to){
  const n=mksDiffDays(from,to);
  const pe=mksAdd(from,-1);
  return [mksAdd(pe,-n), pe];
}

/* inv = true สำหรับตัวชี้วัดที่ "ลดลง = ดี" (เช่น % ค่าการตลาดต่อยอดขาย)
   ลูกศรยังชี้ตามทิศจริงเสมอ เปลี่ยนแค่สี ไม่งั้นอ่านผิดว่ายอดลด */
function mksDelta(cur,prev,inv){
  if(prev==null||cur==null||!prev||!isFinite(cur)||!isFinite(prev)) return '<span class="mks-fl">–</span>';
  const d=(cur-prev)/Math.abs(prev)*100;
  if(!isFinite(d)) return '<span class="mks-fl">–</span>';
  if(Math.abs(d)<0.5) return '<span class="mks-fl">เท่าเดิม</span>';
  const up=d>=0, good=inv? !up : up;
  return '<span class="'+(good?'mks-up':'mks-dn')+'">'+(up?'▲':'▼')+' '+Math.abs(d).toFixed(1)+'%</span>';
}

/* ── กราฟแนวโน้มรายวัน: แท่งค่าการตลาด (ซ้อนสี) + เส้นยอดขาย ─────────────
   วาดเป็น SVG เอง — หน้า Mobile ไม่ได้โหลด Chart.js */
function mksTrend(from,to,w){
  const K=MKT_SPEND.keys, ix={}; K.forEach((k,i)=>ix[k]=i);
  const ds=mksAll().filter(d=>d>=from&&d<=to);
  if(!ds.length) return '<div class="mks-empty">ไม่มีข้อมูลในช่วงนี้</div>';
  const H=220, PL=4, PB=20, PT=8;
  const bw=Math.max(7, Math.min(26, (w-PL*2)/ds.length - 3));
  const step=bw+3, W=Math.max(w, ds.length*step+PL*2);
  const cats=mksSpendCats().filter(c=>!c.na);
  const rev=ds.map(d=>MKS_REVK.reduce((s,k)=>s+(ix[k]!=null?MKT_SPEND.days[d][ix[k]]||0:0),0));
  const spd=ds.map(d=>cats.reduce((s,c)=>s+(c.rate
      ? (MKT_SPEND.days[d][ix[c.base]]||0)*mksRateOn(c.spec,d)
      : (MKT_SPEND.days[d][ix[c.k]]||0)),0));
  const rMax=Math.max(1,...rev), sMax=Math.max(1,...spd);
  const bh=H-PT-PB;
  let g='';
  ds.forEach((d,i)=>{
    const x=PL+i*step; let y=H-PB;
    cats.forEach(c=>{
      const v=c.rate? (MKT_SPEND.days[d][ix[c.base]]||0)*mksRateOn(c.spec,d)
                    : (MKT_SPEND.days[d][ix[c.k]]||0);
      if(v<=0) return;
      const h=v/sMax*bh; y-=h;
      g+='<rect x="'+x+'" y="'+y.toFixed(1)+'" width="'+bw+'" height="'+h.toFixed(1)+'" fill="'+c.c+'"><title>'+
         mksD(d)+' · '+c.n+' '+mksN(v)+'</title></rect>';
    });
  });
  const pts=ds.map((d,i)=>(PL+i*step+bw/2).toFixed(1)+','+(H-PB-rev[i]/rMax*bh).toFixed(1)).join(' ');
  g+='<polyline points="'+pts+'" fill="none" stroke="#0F7B4F" stroke-width="2" stroke-linejoin="round"/>';
  ds.forEach((d,i)=>{
    g+='<circle cx="'+(PL+i*step+bw/2).toFixed(1)+'" cy="'+(H-PB-rev[i]/rMax*bh).toFixed(1)+
       '" r="2.6" fill="#0F7B4F"><title>'+mksD(d)+' · ยอดขาย '+mksN(rev[i])+'</title></circle>';
  });
  const every=Math.ceil(ds.length/14);
  ds.forEach((d,i)=>{ if(i%every) return;
    g+='<text x="'+(PL+i*step+bw/2).toFixed(1)+'" y="'+(H-6)+'" font-size="9.5" fill="#9AA0AA" text-anchor="middle">'+
       mksD(d)+'</text>'; });
  return '<div class="mks-chart"><svg width="'+W+'" height="'+H+'" viewBox="0 0 '+W+' '+H+'">'+
    '<line x1="'+PL+'" y1="'+(H-PB)+'" x2="'+(W-PL)+'" y2="'+(H-PB)+'" stroke="#E8EAEE"/>'+g+'</svg></div>'+
    '<div class="mks-leg"><span><i style="background:#0F7B4F"></i>ยอดขาย (สูงสุด '+mksN(rMax)+'/วัน)</span>'+
    cats.map(c=>'<span><i style="background:'+c.c+'"></i>'+c.n+'</span>').join('')+
    '<span>แท่งรวมสูงสุด '+mksN(sMax)+'/วัน</span></div>';
}

/* ── แถวแถบแนวนอน (ใช้ทั้ง 2 กล่อง) ───────────────────────────────── */
function mksRow(n,c,v,mx,right,dl){
  return '<div class="mks-row"><div class="mks-nm"><i style="background:'+c+'"></i>'+n+'</div>'+
    '<div class="mks-tr"><span style="width:'+(mx?Math.max(0,v/mx*100):0).toFixed(1)+'%;background:'+c+'"></span></div>'+
    '<div class="mks-rv mks-n">'+right+'</div><div class="mks-rd mks-n">'+(dl||'')+'</div></div>';
}

/* ── KOL ตามระดับ (ไม่มีรายชื่อรายคน — ข้อมูลส่วนบุคคล) ──────────────── */
function mksKol(from,to){
  const td=(typeof MKT_SPEND!=='undefined' && MKT_SPEND.kol_tier)||{};
  const tiers={};
  Object.keys(td).forEach(d=>{ if(d<from||d>to) return;
    Object.keys(td[d]).forEach(k=>tiers[k]=(tiers[k]||0)+td[d][k]); });
  const tot=Object.keys(tiers).reduce((s,k)=>s+tiers[k],0);
  let h='';
  if(!tot) h='<div class="mks-empty">ไม่มีรายการ KOL ที่จ่ายแล้วในช่วงนี้</div>';
  else {
    h='<div class="mks-scroll"><table class="mks-tb"><thead><tr><th>ระดับ</th><th>ยอดจ่าย</th><th>%</th></tr></thead><tbody>'+
      Object.keys(tiers).sort((a,b)=>tiers[b]-tiers[a]).map(k=>
        '<tr><td>'+mksEsc(k)+'</td><td class="mks-n">'+mksB(tiers[k])+'</td>'+
        '<td class="mks-n">'+mksP(tiers[k]/tot)+'</td></tr>').join('')+
      '<tr><td><b>รวม</b></td><td class="mks-n"><b>'+mksB(tot)+'</b></td><td class="mks-n"><b>100%</b></td></tr>'+
      '</tbody></table></div><div class="mks-sub">ไม่มีรายชื่อรายคนบนหน้านี้ (ข้อมูลส่วนบุคคล) '+
      'รายละเอียดรายคนอยู่ในไฟล์ที่ไม่ถูก commit</div>';
  }
  const pend=(typeof MKT_SPEND!=='undefined' && MKT_SPEND.kol_pend)||{};
  const pk=Object.keys(pend).filter(d=>d>=from);
  if(pk.length){
    const pt=pk.reduce((s,d)=>s+pend[d],0);
    h+='<div class="mks-warn" style="margin-top:12px"><b>รอจ่าย '+mksB(pt)+' ('+pk.length+
       ' รายการ)</b> — ยังไม่นับรวมในค่าการตลาดด้านบน</div>';
  }
  return h;
}

/* ── render ──────────────────────────────────────────────────────────── */
function mksRender(){
  ['mks-dash','mks-mob'].forEach(id=>{
    const el=document.getElementById(id); if(!el) return;
    if(typeof MKT_SPEND==='undefined'||!MKT_SPEND.days||!Object.keys(MKT_SPEND.days).length){
      el.innerHTML='<div class="mks-empty">ยังไม่มีข้อมูล</div>'; return; }
    const all=mksAll(), lo=all[0], hi=MKT_SPEND.asof;
    let [f,t]=MKS_ST.preset ? mksPreset(MKS_ST.preset) : [MKS_ST.from,MKS_ST.to];
    if(f<lo) f=lo; if(t>hi) t=hi; if(f>t) f=t;
    const A=mksAgg(f,t), [pf,pt]=mksPrevRange(f,t);
    const P=(pf>=lo)? mksAgg(pf,pt) : null;
    const miss=MKS_CAT.filter(c=>c.na);
    const w=Math.max(300,(el.clientWidth||680)-38);

    let h='<div class="mks">';

    /* แถบเลือกช่วง */
    h+='<div class="mks-bar"><div class="mks-pre">'+
       [['7','7 วัน'],['30','30 วัน'],['mtd','เดือนนี้'],['prev','เดือนก่อน']]
         .map(p=>'<button class="mks-b'+(MKS_ST.preset===p[0]?' on':'')+
           '" onclick="mksSet(\''+p[0]+'\')">'+p[1]+'</button>').join('')+
       '</div><div class="mks-dates"><input type="date" id="'+id+'-f" value="'+f+'" min="'+lo+'" max="'+hi+'">'+
       '<span style="color:var(--muted,#6B7280)">–</span>'+
       '<input type="date" id="'+id+'-t" value="'+t+'" min="'+lo+'" max="'+hi+'">'+
       '<button class="mks-b" onclick="mksCustom(\''+id+'\')">ใช้ช่วงนี้</button></div>'+
       '<div class="mks-range">ช่วงที่เลือก <b>'+mksTHR(f,t)+'</b> ('+A.days+' วัน)'+
       (P?' · เทียบกับ '+mksTHR(pf,pt):' · ไม่มีช่วงก่อนหน้าให้เทียบ (ข้อมูลเริ่ม '+mksTH(lo,1)+')')+'</div></div>';

    /* วันที่ขาดจะ "ไม่ถูกนับเป็น 0" อยู่แล้ว เพราะ mksAgg วนเฉพาะวันที่มีจริง
       ป้ายนี้มีไว้กันอ่านผิดว่ายอดเดือนนั้นต่ำ ทั้งที่จริงคือข้อมูลยังดึงมาไม่ครบ */
    const want=mksDiffDays(f,t)+1, gap=Math.max(0, want-A.days);

    /* 1 ─ ขายได้ 100 บาท เงินไปไหนบ้าง */
    const parts=[{n:'ค่าธรรมเนียมแพลตฟอร์ม', v:A.fee,  c:'#6B7280'},
                 {n:'ค่าแอด 4 แพลตฟอร์ม',    v:A.ads,  c:'#2457F5'},
                 {n:'KOL + คอมแอฟฟิลิเอต',   v:A.kol,  c:'#8B5CF6'},
                 {n:'เหลือ',                 v:Math.max(0,A.left), c:'#0F7B4F'}];
    const ptot=parts.reduce((s,p)=>s+p.v,0)||1;
    const per100=A.rev? A.left/A.rev*100 : null;
    h+='<div class="mks-card"><div class="mks-h2">ขายได้ 100 บาท เงินไปไหนบ้าง</div>'+
       '<div class="mks-line">ขายได้ <b>'+mksB(A.rev)+'</b> · เหลือหลังหักค่าแพลตฟอร์มและการตลาด <b>'+
       mksB(A.left)+'</b> (<b>'+(per100!=null?per100.toFixed(1):'–')+' บาท</b> ต่อ 100)</div>'+
       '<div class="mks-stack">'+parts.map(p=>'<span style="width:'+(p.v/ptot*100).toFixed(3)+
         '%;background:'+p.c+'" title="'+p.n+' '+mksB(p.v)+'"></span>').join('')+'</div>'+
       '<div class="mks-slegs">'+parts.map(p=>'<div class="mks-sl"><div class="t"><i style="background:'+p.c+
         '"></i>'+p.n+'</div><div class="v mks-n">'+mksB(p.v)+'</div>'+
         '<div class="p mks-n">'+mksP(mksDiv(p.v,A.rev))+' ของยอดขาย</div></div>').join('')+'</div>'+
       (miss.length? '<div class="mks-warn">ยังไม่มีข้อมูล '+miss.map(c=>c.n).join(' และ ')+
         ' ในช่วงนี้ — “ค่าการตลาดทั้งหมด” จึงยังไม่รวมก้อนนี้ (ไม่ได้นับเป็น 0)</div>':'')+
       (gap>0? '<div class="mks-warn">ช่วงที่เลือกมีข้อมูลจริง '+A.days+' วัน จาก '+want+
         ' วัน — '+gap+' วันที่ขาดไม่ถูกนับเป็น 0 แต่ยอดรวมของช่วงนี้จึงต่ำกว่าความเป็นจริง</div>':'')+
       '</div>';

    /* 2 ─ การ์ด 4 ใบ */
    const kpi=[
      {l:'ยอดขายรวม', v:mksB(A.rev), s:'นับครบ '+MKS_REV_CAT.length+' ช่องทาง', d:P?mksDelta(A.rev,P.rev):''},
      {l:'ค่าการตลาดทั้งหมด', v:mksB(A.spend), s:'ค่าแอด 4 แพลตฟอร์ม + KOL + คอมแอฟ',
       d:P?mksDelta(A.spend,P.spend,true):''},
      {l:'การตลาด ÷ ยอดขาย', v:(A.pct!=null?A.pct.toFixed(1)+'%':'–'), s:'ยิ่งต่ำยิ่งดี',
       d:P&&P.pct!=null?mksDelta(A.pct,P.pct,true):''},
      {l:'ยอดขาย ÷ การตลาด', v:mksX(A.roi), s:'ได้ยอดขายกี่เท่าของเงินที่ลง',
       d:P&&P.roi!=null?mksDelta(A.roi,P.roi):''}
    ];
    h+='<div class="mks-kpi">'+kpi.map(k=>'<div class="mks-k">'+
       '<div class="mks-kl">'+k.l+'</div><div class="mks-kv mks-n">'+k.v+'</div>'+
       '<div class="mks-ks">'+k.s+'</div><div class="mks-ks">'+(k.d||'')+'</div></div>').join('')+'</div>';

    /* 3 ─ 2 กล่องข้างกัน */
    const chs=MKS_REV_CAT.map(c=>({c:c, v:A.rv[c.k]||0, p:P?(P.rv[c.k]||0):null}))
      .filter(x=>x.v>0||(x.p||0)>0).sort((a,b)=>b.v-a.v);
    const mx1=Math.max(1,...chs.map(x=>x.v));
    let box1='<div class="mks-card"><div class="mks-h2">ยอดขายมาจากช่องทางไหน<small>รวม '+mksB(A.rev)+
      (P?' · ▲▼ เทียบช่วงก่อน':'')+'</small></div><div class="mks-rows">'+
      chs.map(x=>mksRow(x.c.n, x.c.c, x.v, mx1, mksB(x.v), P?mksDelta(x.v,x.p):'')).join('')+'</div></div>';
    const mkCats=mksSpendCats().slice().sort((a,b)=>{
      const av=a.na?-1:(A.sp[a.k]||0), bv=b.na?-1:(A.sp[b.k]||0); return bv-av; });
    const mx2=Math.max(1,...mkCats.map(c=>A.sp[c.k]||0));
    const shown=mkCats.reduce((s,c)=>s+(A.sp[c.k]||0),0);
    let box2='<div class="mks-card"><div class="mks-h2">ค่าการตลาดไปลงที่ไหน<small>รวม '+mksB(A.spend)+
      '</small></div><div class="mks-rows">'+
      mkCats.map(c=>{ const v=A.sp[c.k];
        return v==null ? mksRow(c.n, c.c, 0, mx2, '<span class="mks-fl">รอข้อมูล</span>', '')
                       : mksRow(c.n, c.c, v, mx2, mksB(v), mksP(mksDiv(v,A.spend))); }).join('')+
      '</div><div class="mks-sub">รวม '+mksP(mksDiv(shown,A.spend))+' ของค่าการตลาดทั้งหมด'+
      (miss.length? ' · ยังไม่รวม '+miss.map(c=>c.n).join(' และ ')+' (รอข้อมูล)':'')+'</div></div>';
    h+='<div class="mks-two">'+box1+box2+'</div>';

    /* 4 ─ แนวโน้มรายวัน */
    h+='<div class="mks-card" style="margin-top:14px"><div class="mks-h2">ยอดขายและค่าการตลาดรายวัน'+
       '<small>เส้น = ยอดขาย · แท่ง = ค่าการตลาด (ซ้อนตามหมวด)</small></div>'+mksTrend(f,t,w)+'</div>';

    /* 5 ─ KOL ตามระดับ (พับ) */
    h+='<details class="mks-det"><summary>KOL ตามระดับ</summary><div class="mks-body">'+
       mksKol(f,t)+'</div></details>';

    /* 6 ─ ที่มาของตัวเลข + หมายเหตุทั้งหมด (พับ) */
    const C=MKT_SPEND.cov||{};
    let nt='';
    nt+='<p><b>ค่าการตลาดทั้งหมด = ค่าแอด 4 แพลตฟอร์ม + KOL + คอมแอฟฟิลิเอต TikTok</b> '+
        '(บวก Event เมื่อมีข้อมูล) ใช้นิยามนี้ทุกจุดในหน้า ทั้งการ์ด แถบสัดส่วน และกล่อง “ไปลงที่ไหน” '+
        'จึงรวมกันได้ 100% พอดี</p>';
    if(miss.length) nt+='<p><b>⚠️ ยังไม่รวม '+miss.map(c=>c.n).join(' และ ')+
        '</b> — ยังไม่มีข้อมูล จึงเว้นไว้ ไม่ได้นับเป็น 0</p>';
    const un=MKT_SPEND.tiers_unmapped_n||0;
    if(un) nt+='<p>มีแคมเปญ KOL ที่ยังไม่ได้ระบุระดับ <b>'+un+' รายการ</b> '+
        '(แก้ที่ <code>data Ads/kol_campaign_tier.json</code>)</p>';
    const rc=MKT_SPEND.recon;
    if(rc && t>rc){
      const n2=mksDiffDays(mksAdd(rc,1), t)+1;
      nt+='<p><b>ℹ️ '+n2+' วันล่าสุด ('+mksTH(mksAdd(rc,1))+' – '+mksTH(t)+') ยังไม่ผ่านการกระทบยอด</b>'+
         ' — เป็นข้อมูลสดจากแพลตฟอร์มและ Shipnity ตัวเลขอาจขยับเล็กน้อยเมื่อกระทบยอดแล้ว'+
         ' · ช่วงถึง '+mksTH(rc)+' ตรงกับหน้า “ยอดขาย &amp; รายได้” ทุกบาท</p>';
    }
    const prov=A.fee>0? mksProvMonths(f,t) : [];
    if(prov.length) nt+='<p><b>⚠️ '+prov.map(m=>TH_MF_SHORT(m)).join(' · ')+
      ' ยังเป็นอัตราชั่วคราว</b> — ยอดเงินจากแพลตฟอร์มยังเข้าไม่ครบเดือน '+
      'ตัวเลขค่าธรรมเนียมและยอดหลังหักยังขยับได้ จะปิดยอดเป็นตัวจริงวันที่ 5 ของเดือนถัดไป</p>';
    if(A.fee>0) nt+='<p><b>ค่าธรรมเนียมแพลตฟอร์มเป็นอัตราที่ตั้งไว้เอง</b> ('+mksFeeLabel(A)+
      ') คิดจากยอดขายรายวันของช่องทางนั้น ไม่ใช่ยอดเรียกเก็บจริงจากแพลตฟอร์ม · '+
      'ช่องทางขายตรง (Facebook · LINE · POS · เว็บไซต์ ฯลฯ) ไม่มีค่าธรรมเนียม · '+
      'แก้อัตราได้ที่ <code>data Ads/platform_fee.json</code></p>';
    nt+='<p><b>คอมแอฟฟิลิเอต TikTok</b> ไม่มีคอลัมน์รายวัน คิดเป็นอัตราของยอดขาย TikTok รายวันตาม '+
        '<code>marketing_rates</code> ใน <code>data Ads/platform_fee.json</code></p>';
    nt+='<p><b>ยอดขายหน้านี้นับครบทุกช่องทาง</b> รวม Facebook · LINE · Carcare · POS · เว็บไซต์ · เบิกของ '+
      'จึงมากกว่าหน้า <b>Ads Dashboard</b> ที่นับเฉพาะ 3 ช่องทางที่ยิงโฆษณา (ต่างกันราว 8–9%) '+
      'ช่องทางที่ซ้ำกันตรงกันทุกบาท</p>';
    nt+='<p>ยอดขาย TikTok รายวันเป็นยอดก่อนหักคำสั่งซื้อที่ยกเลิก จึงสูงกว่าหน้า Sales ราว 1% '+
        'ช่องอื่นตรงกันทุกบาท</p>';
    nt+='<p>ยอดขาย Shopee/TikTok/Lazada ใช้ข้อมูลรายวันจาก Ads Dashboard · ช่องทางที่เหลือจาก Shipnity · '+
        'KOL นับตามวันที่ทำจ่าย เฉพาะ Status = Done · ค่าแอด Facebook มาจากไฟล์เดียวกับหน้า Ads '+
        '(<code>facebook/fb_daily.json</code>)</p>';
    nt+='<p><b>ข้อมูลถึงวันไหน</b></p><div class="mks-chips">'+
        MKS_SRC.map(s=>'<span class="mks-chip">'+s.n+' ถึง '+(C[s.k]?mksTH(C[s.k],1):'–')+'</span>').join('')+
        '</div>';
    nt+='<p class="mks-sub">ข้อมูลรายวันมีตั้งแต่ '+mksTH(lo,1)+' ถึง '+mksTH(hi,1)+'</p>';
    h+='<details class="mks-det"><summary>ตัวเลขในหน้านี้มาจากไหน</summary><div class="mks-body">'+nt+'</div></details>';

    h+='</div>';
    el.innerHTML=h;
  });
}
function mksSet(p){ MKS_ST={preset:p,from:null,to:null}; mksRender(); }
function mksCustom(id){
  const f=document.getElementById(id+'-f').value, t=document.getElementById(id+'-t').value;
  if(!f||!t||f>t) return;
  MKS_ST={preset:null,from:f,to:t}; mksRender();
}
function renderMktSpend(){ try{ mksRender(); }catch(e){ console.error('mks',e); } }
