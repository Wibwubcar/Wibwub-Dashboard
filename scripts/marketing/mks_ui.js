/* เมนู "การตลาด vs ยอดขาย"
   ข้อมูลรายวันอยู่ใน MKT_SPEND (เขียนโดย scripts/marketing/marketing_update.py)
   หน้าเว็บคำนวณทุกตัวเลขเองตามช่วงวันที่ที่เลือก — อย่าแก้ไฟล์นี้ในหน้า HTML
   แก้ที่ scripts/marketing/mks_ui.js แล้วรัน scripts/marketing/marketing_ui.py

   Facebook Ads / Event ยังไม่มีข้อมูล -> na:true
   ห้ามนับเป็น 0 ในสูตร % ต่อยอดขาย ให้ข้ามไปและขึ้นหมายเหตุแทน */

/* g = กลุ่มของวง "ยอดขาย เทียบ ค่าการตลาด" — เพิ่มหมวดใหม่แล้ววงนั้นคิดเองอัตโนมัติ
   พอ Event / Facebook Ads มีข้อมูลจริง แค่ปลด na ออก ไม่ต้องแก้สูตรที่อื่น */
const MKS_CAT = [
  {k:'ads_sh', n:'Ads Shopee',   c:'#ee4d2d', g:'ads'},
  {k:'ads_tk', n:'Ads TikTok',   c:'#111111', g:'ads'},
  {k:'ads_lz', n:'Ads Lazada',   c:'#1b04a1', g:'ads'},
  {k:'ads_fb', n:'Ads Facebook', c:'#1877f2', g:'ads'},
  {k:'kol',    n:'KOL',          c:'#8b5cf6', g:'kol'},
  {k:'event',  n:'Event',        c:'#f59e0b', g:'event'}
];
/* หมวดไหน "รอข้อมูล" ไม่ได้ hardcode ไว้ — marketing_update.py ส่ง missing มาให้
   พอกรอกค่า Event/Facebook ลง data Ads/mkt_manual.json แล้วรันสคริปต์
   คีย์นั้นจะหลุดจาก missing เอง ทุกกราฟและสูตร % จะเริ่มนับทันที ไม่ต้องแก้ไฟล์นี้ */
function mksNA(k){ return ((typeof MKT_SPEND!=='undefined' && MKT_SPEND.missing)||[]).indexOf(k)>=0; }
MKS_CAT.forEach(c=>Object.defineProperty(c,'na',{get:function(){return mksNA(this.k);}}));
/* ชื่อ/สีของแต่ละกลุ่มในวงรวม */
const MKS_GRP = [
  {g:'ads',   n:'ค่า Ads',   c:'#1A5CDB'},
  {g:'kol',   n:'ค่า KOL',   c:'#8b5cf6'},
  {g:'event', n:'ค่า Event', c:'#f59e0b'}
];
/* ช่องทางยอดขาย — ต้องครบเท่าสูตร TOTAL_REV บนหน้าเว็บ (เรียงตามยอดปกติ)
   ถ้า marketing_update.py เพิ่มคีย์ใหม่ ต้องเพิ่มที่นี่ด้วย ไม่งั้นยอดรวมจะขาด */
const MKS_REV_CAT = [
  {k:'sh',   n:'Shopee',    c:'#ee4d2d'},
  {k:'tk',   n:'TikTok',    c:'#111111'},
  {k:'fb',   n:'Facebook',  c:'#1877f2'},
  {k:'line', n:'Line',      c:'#06c755'},
  {k:'care', n:'Carcare',   c:'#14b8a6'},
  {k:'lz',   n:'Lazada',    c:'#1b04a1'},
  {k:'pos',  n:'POS',       c:'#f59e0b'},
  {k:'web',  n:'Website',   c:'#64748b'},
  {k:'mkt',  n:'สินค้าการตลาด', c:'#a855f7'},
  {k:'beuk', n:'เบิกของ',    c:'#94a3b8'},
  {k:'oth',  n:'อื่น ๆ',     c:'#cbd5e1'}
];
const MKS_REVK = MKS_REV_CAT.map(c=>c.k);
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

/* วันทั้งหมดที่มีข้อมูล (เรียงแล้ว) */
function mksAll(){ return Object.keys(MKT_SPEND.days).sort(); }

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

/* รวมตัวเลขในช่วง — คืน null สำหรับหมวดที่ยังไม่มีข้อมูล */
function mksAgg(from,to){
  const K=MKT_SPEND.keys, ix={}; K.forEach((k,i)=>ix[k]=i);
  let rev=0, days=0; const sp={}, rv={};
  MKS_CAT.forEach(c=>{ sp[c.k]= c.na ? null : 0; });
  MKS_REVK.forEach(k=>rv[k]=0);
  mksAll().forEach(d=>{
    if(d<from||d>to) return;
    const r=MKT_SPEND.days[d]; days++;
    MKS_REVK.forEach(k=>{ if(ix[k]!=null){ rev+=r[ix[k]]||0; rv[k]+=r[ix[k]]||0; } });
    MKS_CAT.forEach(c=>{ if(!c.na && ix[c.k]!=null) sp[c.k]+=r[ix[c.k]]||0; });
  });
  const spend=MKS_CAT.reduce((s,c)=>s+(sp[c.k]||0),0);
  return {rev, rv, sp, spend, days, pct: rev? spend/rev*100 : null, roi: spend? rev/spend : null};
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
  if(prev==null||cur==null||!prev) return '';
  const d=(cur-prev)/Math.abs(prev)*100;
  if(!isFinite(d)) return '';
  const up=d>=0, good=inv? !up : up;
  return '<span class="'+(good?'mks-up':'mks-dn')+'">'+(up?'▲':'▼')+' '+Math.abs(d).toFixed(1)+'%</span>';
}

/* ── กราฟแนวโน้มรายวัน: แท่งค่าการตลาด (ซ้อนสี) + เส้นยอดขาย ───────────── */
function mksTrend(from,to,w){
  const K=MKT_SPEND.keys, ix={}; K.forEach((k,i)=>ix[k]=i);
  const ds=mksAll().filter(d=>d>=from&&d<=to);
  if(!ds.length) return '<div class="mks-empty">ไม่มีข้อมูลในช่วงนี้</div>';
  const H=200, PL=4, PB=20, PT=8;
  const bw=Math.max(7, Math.min(26, (w-PL*2)/ds.length - 3));
  const step=bw+3, W=Math.max(w, ds.length*step+PL*2);
  const cats=MKS_CAT.filter(c=>!c.na);
  const rev=ds.map(d=>MKS_REVK.reduce((s,k)=>s+(ix[k]!=null?MKT_SPEND.days[d][ix[k]]||0:0),0));
  const spd=ds.map(d=>cats.reduce((s,c)=>s+(MKT_SPEND.days[d][ix[c.k]]||0),0));
  const rMax=Math.max(1,...rev), sMax=Math.max(1,...spd);
  const bh=H-PT-PB;
  let g='';
  ds.forEach((d,i)=>{
    const x=PL+i*step; let y=H-PB;
    cats.forEach(c=>{
      const v=MKT_SPEND.days[d][ix[c.k]]||0; if(v<=0) return;
      const h=v/sMax*bh; y-=h;
      g+='<rect x="'+x+'" y="'+y.toFixed(1)+'" width="'+bw+'" height="'+h.toFixed(1)+'" fill="'+c.c+'"><title>'+
         mksD(d)+' · '+c.n+' '+mksN(v)+'</title></rect>';
    });
  });
  const pts=ds.map((d,i)=>(PL+i*step+bw/2).toFixed(1)+','+(H-PB-rev[i]/rMax*bh).toFixed(1)).join(' ');
  g+='<polyline points="'+pts+'" fill="none" stroke="#16a34a" stroke-width="2" stroke-linejoin="round"/>';
  ds.forEach((d,i)=>{
    g+='<circle cx="'+(PL+i*step+bw/2).toFixed(1)+'" cy="'+(H-PB-rev[i]/rMax*bh).toFixed(1)+
       '" r="2.6" fill="#16a34a"><title>'+mksD(d)+' · ยอดขาย '+mksN(rev[i])+'</title></circle>';
  });
  const every=Math.ceil(ds.length/14);
  ds.forEach((d,i)=>{ if(i%every) return;
    g+='<text x="'+(PL+i*step+bw/2).toFixed(1)+'" y="'+(H-6)+'" font-size="9.5" fill="#999" text-anchor="middle">'+
       mksD(d)+'</text>'; });
  return '<div class="mks-chart"><svg width="'+W+'" height="'+H+'" viewBox="0 0 '+W+' '+H+'">'+
    '<line x1="'+PL+'" y1="'+(H-PB)+'" x2="'+(W-PL)+'" y2="'+(H-PB)+'" stroke="#e8e8e8"/>'+g+'</svg></div>'+
    '<div class="mks-leg"><span><i style="background:#16a34a"></i>ยอดขาย (สูงสุด '+mksN(rMax)+'/วัน)</span>'+
    cats.map(c=>'<span><i style="background:'+c.c+'"></i>'+c.n+'</span>').join('')+
    '<span>แท่งรวมสูงสุด '+mksN(sMax)+'/วัน</span></div>';
}

/* ── สัดส่วนค่าการตลาด: แท่งแนวนอน (ยอดเล็กอ่านออกเสมอ) ─────────────── */
function mksSplit(A){
  const mx=Math.max(1,...MKS_CAT.map(c=>A.sp[c.k]||0));
  const pie=mksDonut(MKS_CAT.filter(c=>!c.na).map(c=>({n:c.n,c:c.c,v:A.sp[c.k]||0})),
                     A.spend, 'ค่าการตลาด');
  return '<div class="mks-pie">'+pie+'<div class="mks-bars">'+MKS_CAT.map(c=>{
    const v=A.sp[c.k];
    if(v==null) return '<div class="mks-h"><div class="mks-hn"><i style="background:'+c.c+
      ';opacity:.25"></i>'+c.n+'</div><div class="mks-ht"></div>'+
      '<div class="mks-hv mks-wait">รอข้อมูล</div><div class="mks-hp">–</div></div>';
    const pct=A.spend? v/A.spend*100 : 0;
    return '<div class="mks-h"><div class="mks-hn"><i style="background:'+c.c+'"></i>'+c.n+'</div>'+
      '<div class="mks-ht"><div class="mks-hf" style="width:'+(v/mx*100).toFixed(2)+'%;background:'+c.c+'"></div></div>'+
      '<div class="mks-hv">'+mksN(v)+'</div><div class="mks-hp">'+pct.toFixed(1)+'%</div></div>';
  }).join('')+'</div></div>';
}

/* ── โดนัท: สัดส่วนเป็นชิ้นเค้ก ──────────────────────────────────────────
   ใช้ stroke-dasharray บนวงกลม (เส้นเดียวต่อชิ้น) แทนการเขียน path arc เอง
   ชิ้นที่ใหญ่พอ (>=6%) ใส่ตัวเลข % ลงบนวง ชิ้นเล็กกว่านั้นอ่านจากแท่งด้านข้าง
   title ของแต่ละชิ้นมีชื่อ+ยอด+% ครบทุกชิ้นเสมอ                       */
function mksDonut(items,total,label){
  if(!total) return '';
  const S=168, cx=S/2, cy=S/2, r=58, sw=28, C=2*Math.PI*r;
  let off=0, arcs='', labs='';
  items.forEach(it=>{
    const v=it.v||0; if(v<=0) return;
    const frac=v/total, len=frac*C;
    arcs+='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="'+it.c+'" stroke-width="'+sw+
      '" stroke-dasharray="'+len.toFixed(2)+' '+(C-len).toFixed(2)+'" stroke-dashoffset="'+(-off).toFixed(2)+
      '" transform="rotate(-90 '+cx+' '+cy+')"><title>'+it.n+' · '+mksN(v)+' บาท · '+
      (frac*100).toFixed(1)+'%</title></circle>';
    if(frac>=0.06){
      const mid=(off+len/2)/C*2*Math.PI - Math.PI/2;
      labs+='<text x="'+(cx+Math.cos(mid)*r).toFixed(1)+'" y="'+(cy+Math.sin(mid)*r+3.5).toFixed(1)+
        '" font-size="10.5" font-weight="700" fill="#fff" text-anchor="middle">'+
        Math.round(frac*100)+'%</text>';
    }
    off+=len;
  });
  return '<svg class="mks-donut" viewBox="0 0 '+S+' '+S+'" width="'+S+'" height="'+S+
    '" role="img" aria-label="สัดส่วน'+label+'">'+arcs+labs+
    '<text x="'+cx+'" y="'+(cy-4)+'" font-size="15" font-weight="800" fill="currentColor" text-anchor="middle">'+
    mksN(total)+'</text>'+
    '<text x="'+cx+'" y="'+(cy+12)+'" font-size="10" fill="#8a8f9c" text-anchor="middle">บาท</text></svg>';
}

/* ── วงรวม: ยอดขาย vs ค่า Ads vs ค่า KOL ────────────────────────────────
   ค่าการตลาดเป็น "ส่วนหนึ่งของ" ยอดขาย ไม่ใช่ก้อนแยก วงนี้จึงเอายอดขายเป็นวงเต็ม
   แล้วแบ่งเป็น ค่า Ads / ค่า KOL / ส่วนที่เหลือ — อ่านได้ทันทีว่าขายได้ 100 บาท
   จ่ายค่าโฆษณากี่บาท จ่าย KOL กี่บาท                                      */
function mksRatio(A){
  const items=[], gaps=[];
  MKS_GRP.forEach(G=>{
    const mem=MKS_CAT.filter(c=>c.g===G.g);
    const have=mem.filter(c=>!c.na);
    if(!have.length){ gaps.push(G.n); return; }          // ทั้งกลุ่มยังไม่มีข้อมูล -> ไม่ใส่ชิ้น
    const miss=mem.filter(c=>c.na).map(c=>c.n);
    items.push({n:G.n, c:G.c, v:have.reduce((s,c)=>s+(A.sp[c.k]||0),0),
                d:have.map(c=>c.n.replace('Ads ','')).join(' + ')+
                  (miss.length? ' (ยังไม่รวม '+miss.join(', ')+')':'')});
  });
  const used=items.reduce((s,i)=>s+i.v,0);
  items.unshift({n:'ยอดขายส่วนที่เหลือ', c:'#16a34a', v:Math.max(0,A.rev-used),
                 d:'หลังหักค่าการตลาดที่มีข้อมูลแล้ว'});
  const rows=items.map(it=>'<div class="mks-h"><div class="mks-hn"><i style="background:'+it.c+'"></i>'+it.n+
    '</div><div class="mks-ht"><div class="mks-hf" style="width:'+(A.rev?it.v/A.rev*100:0).toFixed(2)+
    '%;background:'+it.c+'"></div></div><div class="mks-hv">'+mksN(it.v)+'</div>'+
    '<div class="mks-hp">'+(A.rev?(it.v/A.rev*100).toFixed(2):'0')+'%</div></div>'+
    '<div class="mks-sub">'+it.d+'</div>').join('')+
    (gaps.length? '<div class="mks-sub" style="margin-left:0;color:#b45309">ยังไม่มีข้อมูล '+
       gaps.join(' และ ')+' จึงยังไม่มีชิ้นในวงนี้</div>':'');
  return '<div class="mks-pie">'+mksDonut(items, A.rev, 'ยอดขายเทียบค่าการตลาด')+
    '<div class="mks-bars">'+rows+'</div></div>';
}

/* ── ยอดขายแยกตามช่องทาง ───────────────────────────────────────────── */
function mksSplitRev(A,P){
  const cats=MKS_REV_CAT.filter(c=>(A.rv[c.k]||0)>0 || (P&&(P.rv[c.k]||0)>0))
    .sort((a,b)=>(A.rv[b.k]||0)-(A.rv[a.k]||0));
  const mx=Math.max(1,...cats.map(c=>A.rv[c.k]||0));
  const pie=mksDonut(cats.map(c=>({n:c.n,c:c.c,v:A.rv[c.k]||0})), A.rev, 'ยอดขายรายช่องทาง');
  return '<div class="mks-pie">'+pie+'<div class="mks-bars">'+cats.map(c=>{
    const v=A.rv[c.k]||0, pct=A.rev? v/A.rev*100 : 0;
    const d=P? mksDelta(v,P.rv[c.k]) : '';
    return '<div class="mks-h"><div class="mks-hn"><i style="background:'+c.c+'"></i>'+c.n+'</div>'+
      '<div class="mks-ht"><div class="mks-hf" style="width:'+(v/mx*100).toFixed(2)+'%;background:'+c.c+'"></div></div>'+
      '<div class="mks-hv">'+mksN(v)+'</div><div class="mks-hp">'+pct.toFixed(1)+'%</div>'+
      '<div class="mks-hd">'+(d||'<span style="color:var(--muted,#999)">–</span>')+'</div></div>';
  }).join('')+'</div></div>';
}

/* ── KOL ─────────────────────────────────────────────────────────────── */
function mksKol(from,to){
  const all=MKT_SPEND.kol||[];
  const done=all.filter(r=>r.st==='done'&&r.d>=from&&r.d<=to);
  /* แถว "รอจ่าย" มักลงวันทำจ่ายเป็นวันข้างหน้า (เลย asof) ถ้ากรองด้วยช่วงเดียวกัน
     จะหายไปทั้งหมด -> เอาเฉพาะที่อยู่ในเดือนของช่วงที่เลือก หรือหลังช่วงนั้น */
  const pend=all.filter(r=>r.st!=='done'&&r.d>=from);
  const rows=done.concat(pend);
  if(!rows.length) return '<div class="mks-empty">ไม่มีรายการ KOL ในช่วงนี้</div>';
  const tiers={};
  done.forEach(r=>{ const t=r.tier||'ยังไม่ระบุระดับ';
    const o=tiers[t]||(tiers[t]={amt:0,ppl:new Set()}); o.amt+=r.amt; o.ppl.add(r.kol||'?'); });
  const tot=done.reduce((s,r)=>s+r.amt,0);
  let h='<div class="mks-t">สรุปตามระดับ KOL <small>เฉพาะที่จ่ายแล้ว · รวม '+mksN(tot)+' บาท</small></div>';
  h+='<div class="mks-scroll"><table class="mks-tb"><thead><tr><th>ระดับ</th><th>จำนวนคน</th>'+
     '<th>ยอดจ่าย</th><th>%</th></tr></thead><tbody>';
  Object.keys(tiers).sort((a,b)=>tiers[b].amt-tiers[a].amt).forEach(t=>{
    const o=tiers[t];
    h+='<tr><td><span class="mks-tier'+(t==='ยังไม่ระบุระดับ'?' na':'')+'">'+t+'</span></td>'+
       '<td>'+o.ppl.size+'</td><td>'+mksN(o.amt)+'</td><td>'+(tot?(o.amt/tot*100).toFixed(1):'0')+'%</td></tr>';
  });
  h+='</tbody></table></div>';

  h+='<div class="mks-t" style="margin-top:15px">รายแคมเปญ <small>'+rows.length+' รายการ</small></div>';
  h+='<div class="mks-scroll"><table class="mks-tb"><thead><tr><th>แคมเปญ</th><th>KOL</th>'+
     '<th>วันที่จ่าย</th><th>ระดับ</th><th>ยอด</th><th>สถานะ</th></tr></thead><tbody>';
  rows.slice().sort((a,b)=> a.d===b.d ? b.amt-a.amt : (a.d<b.d?1:-1)).forEach(r=>{
    h+='<tr><td>'+r.camp+'</td><td>'+(r.kol||'–')+'</td><td>'+r.d+'</td>'+
       '<td><span class="mks-tier'+(r.tier?'':' na')+'">'+(r.tier||'ยังไม่ระบุ')+'</span></td>'+
       '<td>'+mksN(r.amt)+'</td><td><span class="mks-pill '+(r.st==='done'?'mks-paid">จ่ายแล้ว':'mks-pend">รอจ่าย')+
       '</span></td></tr>';
  });
  h+='</tbody></table></div>';
  if(pend.length){
    const pt=pend.reduce((s,r)=>s+r.amt,0);
    h+='<div class="mks-note" style="margin-top:9px"><b>รอจ่าย '+mksN(pt)+' บาท ('+pend.length+
       ' รายการ)</b> — ยังไม่นับรวมในยอดค่าการตลาดด้านบน</div>';
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
    const w=Math.max(300,(el.clientWidth||680)-34);

    let h='<div class="mks">';

    /* แถบเลือกช่วง */
    h+='<div class="mks-bar"><div class="mks-pre">'+
       [['7','7 วัน'],['30','30 วัน'],['mtd','เดือนนี้'],['prev','เดือนก่อน']]
         .map(p=>'<button class="mks-b'+(MKS_ST.preset===p[0]?' on':'')+
           '" onclick="mksSet(\''+p[0]+'\')">'+p[1]+'</button>').join('')+
       '</div><div class="mks-dates"><input type="date" id="'+id+'-f" value="'+f+'" min="'+lo+'" max="'+hi+'">'+
       '<span style="color:var(--muted,#999)">ถึง</span>'+
       '<input type="date" id="'+id+'-t" value="'+t+'" min="'+lo+'" max="'+hi+'">'+
       '<button class="mks-b" onclick="mksCustom(\''+id+'\')">ใช้ช่วงนี้</button></div>'+
       '<div class="mks-range">ช่วงที่เลือก '+f+' ถึง '+t+' ('+A.days+' วัน)'+
       (P?' · เทียบกับ '+pf+' ถึง '+pt:' · ไม่มีช่วงก่อนหน้าให้เทียบ (ข้อมูลเริ่ม '+lo+')')+'</div></div>';

    /* ป้ายวันที่ข้อมูล */
    const C=MKT_SPEND.cov||{};
    h+='<div class="mks-badges">'+MKS_SRC.map(s=>'<span class="mks-bd">'+s.n+' <b>'+(C[s.k]||'–')+'</b></span>').join('')+
       miss.map(c=>'<span class="mks-bd warn">'+c.n+' <b>รอข้อมูล</b></span>').join('')+'</div>';

    /* KPI */
    const kpi=[
      {l:'ยอดขายรวม', v:mksN(A.rev), c:'#16a34a', d:P?mksDelta(A.rev,P.rev):'', s:'บาท'},
      {l:'ค่าการตลาดรวม', v:mksN(A.spend), c:'#1A5CDB', d:P?mksDelta(A.spend,P.spend):'', s:'บาท'},
      {l:'% ต่อยอดขาย', v:(A.pct!=null?A.pct.toFixed(2)+'%':'–'), c:'#f59e0b',
       d:P&&P.pct!=null?mksDelta(A.pct,P.pct,true):'', s:'ยิ่งต่ำยิ่งดี'},
      {l:'ยอดขาย/ค่าการตลาด', v:(A.roi!=null?A.roi.toFixed(2)+'x':'–'), c:'#8b5cf6',
       d:P&&P.roi!=null?mksDelta(A.roi,P.roi):'', s:'ยิ่งสูงยิ่งดี'}
    ];
    h+='<div class="mks-kpi">'+kpi.map(k=>'<div class="mks-k" style="--kc:'+k.c+'">'+
       '<div class="mks-kl">'+k.l+'</div><div class="mks-kv">'+k.v+'</div>'+
       '<div class="mks-ks">'+(k.d||k.s)+(k.d?' จากช่วงก่อน':'')+'</div></div>').join('')+'</div>';

    /* วงรวม: ขายได้เท่าไร จ่าย Ads เท่าไร จ่าย KOL เท่าไร */
    h+='<div class="mks-card"><div class="mks-t">ยอดขาย เทียบ ค่า Ads และ ค่า KOL '+
       '<small>วงเต็ม = ยอดขายรวม '+mksN(A.rev)+' บาท</small></div>'+mksRatio(A)+'</div>';

    /* ยอดขายแยกช่องทาง + สัดส่วนค่าการตลาด (เรียงคู่กันบนจอกว้าง) */
    h+='<div class="mks-two">';
    h+='<div class="mks-card"><div class="mks-t">ยอดขายแยกตามช่องทาง <small>รวม '+mksN(A.rev)+' บาท'+
       (P?' · ▲▼ เทียบช่วงก่อน':'')+'</small></div>'+mksSplitRev(A,P)+'</div>';
    h+='<div class="mks-card"><div class="mks-t">สัดส่วนค่าการตลาด <small>รวม '+mksN(A.spend)+' บาท</small></div>'+
       mksSplit(A)+'</div>';
    h+='</div>';

    /* แนวโน้มรายวัน */
    h+='<div class="mks-card"><div class="mks-t">แนวโน้มรายวัน <small>เส้น = ยอดขาย · แท่ง = ค่าการตลาด</small></div>'+
       mksTrend(f,t,w)+'</div>';

    /* KOL */
    h+='<div class="mks-card">'+mksKol(f,t)+'</div>';

    /* หมายเหตุ */
    h+='<div class="mks-note">';
    if(miss.length) h+='<b>⚠️ % ต่อยอดขายยังไม่รวม '+miss.map(c=>c.n).join(' และ ')+
      '</b> — ยังไม่มีข้อมูล จึงเว้นไว้ ไม่ได้นับเป็น 0<br>';
    if((MKT_SPEND.tiers_unmapped||[]).length)
      h+='แคมเปญที่ยังไม่ได้ระบุระดับ KOL: '+MKT_SPEND.tiers_unmapped.join(' · ')+
         ' (แก้ที่ <code>data Ads/kol_campaign_tier.json</code>)<br>';
    h+='ยอดขาย TikTok รายวันเป็นยอดก่อนหักคำสั่งซื้อที่ยกเลิก จึงสูงกว่าหน้า Sales '+
       'ราว 1% (ต.ค. ต่างกัน 24,572 บาท) ช่องอื่นตรงกันทุกบาท<br>';
    h+='ยอดขาย Shopee/TikTok/Lazada ใช้ข้อมูลรายวันจาก Ads Dashboard · ช่องทางที่เหลือจาก Shipnity · '+
       'KOL นับตามวันที่ทำจ่าย เฉพาะ Status = Done<br>ข้อมูลรายวันมีตั้งแต่ '+lo+' ถึง '+hi;
    h+='</div></div>';
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
