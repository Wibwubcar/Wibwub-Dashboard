
// ════════════════════════════════════════
// FIREBASE CONFIG
// ────────────────────────────────────────
// กรอก config จาก Firebase Console → Project Settings → Your apps
// (Firebase Console: https://console.firebase.google.com)
// ════════════════════════════════════════
const firebaseConfig = {
  apiKey:            "AIzaSyCaOE_1ILOr_Q-wlRR5vEu71-LG4ekVdLk",
  authDomain:        "wibwubcar-e2cbc.firebaseapp.com",
  projectId:         "wibwubcar-e2cbc",
  storageBucket:     "wibwubcar-e2cbc.firebasestorage.app",
  messagingSenderId: "568499433889",
  appId:             "1:568499433889:web:7cbc86f3f14d5034b4dbe0",
  measurementId:     "G-VVCK1TDH2K"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db   = firebase.firestore(); // kept for compat, but NOT used for queries

// ── Firestore REST helpers (bypass WebChannel 400 error) ──
const FS_BASE = 'https://firestore.googleapis.com/v1/projects/wibwubcar-e2cbc/databases/(default)/documents';
async function _fsToken(){ const u=firebase.auth().currentUser; return u ? await u.getIdToken() : null; }
function _fsFromVal(v){ if(v===undefined||v===null) return null; if(v.stringValue!==undefined) return v.stringValue; if(v.integerValue!==undefined) return Number(v.integerValue); if(v.doubleValue!==undefined) return Number(v.doubleValue); if(v.booleanValue!==undefined) return v.booleanValue; if(v.timestampValue!==undefined) return new Date(v.timestampValue); if(v.arrayValue) return (v.arrayValue.values||[]).map(_fsFromVal); if(v.mapValue) return _fsFieldsToObj(v.mapValue.fields||{}); return null; }
function _fsFieldsToObj(fields){ const o={}; for(const [k,v] of Object.entries(fields||{})) o[k]=_fsFromVal(v); return o; }
function _fsToVal(v){ if(v===null||v===undefined) return {nullValue:null}; if(Array.isArray(v)) return {arrayValue:{values:v.map(_fsToVal)}}; if(v instanceof Date) return {timestampValue:v.toISOString()}; if(typeof v==='boolean') return {booleanValue:v}; if(typeof v==='number') return Number.isInteger(v)?{integerValue:String(v)}:{doubleValue:v}; if(typeof v==='object') return {mapValue:{fields:_fsObjToFields(v)}}; return {stringValue:String(v)}; }
function _fsObjToFields(obj){ const f={}; for(const [k,v] of Object.entries(obj)) f[k]=_fsToVal(v); return f; }
async function fsGet(col,id){ const tok=await _fsToken(); const r=await fetch(`${FS_BASE}/${col}/${id}`,{headers:{Authorization:'Bearer '+tok}}); if(r.status===404) return {exists:false,data:()=>({})}; if(!r.ok) throw new Error('fsGet '+r.status); const d=await r.json(); return {exists:true,data:()=>_fsFieldsToObj(d.fields||{})}; }
async function fsSet(col,id,obj){ const tok=await _fsToken(); const r=await fetch(`${FS_BASE}/${col}/${id}`,{method:'PATCH',headers:{Authorization:'Bearer '+tok,'Content-Type':'application/json'},body:JSON.stringify({fields:_fsObjToFields(obj)})}); if(!r.ok) throw new Error('fsSet '+r.status+' '+(await r.text())); }
async function fsDel(col,id){ const tok=await _fsToken(); const r=await fetch(`${FS_BASE}/${col}/${id}`,{method:'DELETE',headers:{Authorization:'Bearer '+tok}}); if(!r.ok) throw new Error('fsDel '+r.status); }
async function fsList(col){ const tok=await _fsToken(); const r=await fetch(`${FS_BASE}/${col}?pageSize=100`,{headers:{Authorization:'Bearer '+tok}}); if(!r.ok) throw new Error('fsList '+r.status); const d=await r.json(); return (d.documents||[]).map(doc=>({id:doc.name.split('/').pop(),data:()=>_fsFieldsToObj(doc.fields||{})})); }
async function fsAdd(col,obj){ const tok=await _fsToken(); const r=await fetch(`${FS_BASE}/${col}`,{method:'POST',headers:{Authorization:'Bearer '+tok,'Content-Type':'application/json'},body:JSON.stringify({fields:_fsObjToFields(obj)})}); if(!r.ok) throw new Error('fsAdd '+r.status+' '+(await r.text())); const d=await r.json(); return d.name.split('/').pop(); }
async function fsQuery(col,filters=[],orderBy=null,limit=200){ const tok=await _fsToken(); if(!tok) return []; const sq={from:[{collectionId:col}],limit:limit}; if(filters.length===1){sq.where={fieldFilter:{field:{fieldPath:filters[0].field},op:filters[0].op||'EQUAL',value:_fsToVal(filters[0].value)}};} else if(filters.length>1){sq.where={compositeFilter:{op:'AND',filters:filters.map(f=>({fieldFilter:{field:{fieldPath:f.field},op:f.op||'EQUAL',value:_fsToVal(f.value)}}))}};} if(orderBy){sq.orderBy=[{field:{fieldPath:orderBy.field},direction:orderBy.dir||'ASCENDING'}];} const r=await fetch(`${FS_BASE}:runQuery`,{method:'POST',headers:{Authorization:'Bearer '+tok,'Content-Type':'application/json'},body:JSON.stringify({structuredQuery:sq})}); if(!r.ok) throw new Error('fsQuery '+r.status); const arr=await r.json(); return arr.filter(item=>item.document).map(item=>({id:item.document.name.split('/').pop(),data:()=>_fsFieldsToObj(item.document.fields||{})})); }

// ════════════════════════════════════════
// HR SYSTEM
// ════════════════════════════════════════
let _hrClockTimer=null, _hrTodayDoc=null, _hrGPS=null, _hrInitialized=false;
const _GAS_SHEETS_DEFAULT = 'https://script.google.com/macros/s/AKfycbz3YukxpkvaKBFkVL2JDe8_fEoZaMV6it9PwrUpka23isdxxpPxn8z9J9bbCZ9xWKiuQg/exec';
let _sheetsGasUrl = localStorage.getItem('wibwub_sheets_url')||_GAS_SHEETS_DEFAULT;

async function sendToSheets(type, data){
  const url = _sheetsGasUrl;
  if(!url) return;
  try{
    await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({type,data}),mode:'cors'});
  }catch(e){ console.warn('Sheets sync:',e.message); }
}

function initHR(){
  if(_hrClockTimer) clearInterval(_hrClockTimer);
  updateHRClock();
  _hrClockTimer=setInterval(updateHRClock,1000);
  loadHRToday();
  loadHRHistory();
  const today=new Date(Date.now()+7*3600*1000).toISOString().split('T')[0];
  const s=document.getElementById('hr-start-date');
  const e=document.getElementById('hr-end-date');
  if(s&&!s.value) s.value=today;
  if(e&&!e.value) e.value=today;
  getHRGeolocation();
}

function updateHRClock(){
  const now=new Date();
  const el=document.getElementById('hr-clock');
  if(el) el.textContent=now.toLocaleTimeString('th-TH',{hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false});
  const lbl=document.getElementById('hr-date-lbl');
  if(lbl){
    const days=['อาทิตย์','จันทร์','อังคาร','พุธ','พฤหัส','ศุกร์','เสาร์'];
    const months=['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'];
    lbl.textContent=`วัน${days[now.getDay()]} ${now.getDate()} ${months[now.getMonth()]} ${now.getFullYear()+543}`;
  }
}

function getHRGeolocation(){
  const gpsEl=document.getElementById('hr-gps-txt');
  if(!navigator.geolocation){if(gpsEl)gpsEl.textContent='GPS ไม่รองรับบนอุปกรณ์นี้';return;}
  if(gpsEl)gpsEl.textContent='กำลังรับตำแหน่ง GPS...';
  navigator.geolocation.getCurrentPosition(
    pos=>{_hrGPS={lat:pos.coords.latitude,lng:pos.coords.longitude,acc:Math.round(pos.coords.accuracy)};if(gpsEl)gpsEl.textContent=`📍 ${_hrGPS.lat.toFixed(5)}, ${_hrGPS.lng.toFixed(5)} (±${_hrGPS.acc}m)`;},
    err=>{_hrGPS=null;if(gpsEl)gpsEl.textContent='ไม่สามารถรับ GPS ได้';},
    {enableHighAccuracy:true,timeout:10000,maximumAge:60000}
  );
}

async function loadHRToday(){
  const user=firebase.auth().currentUser; if(!user) return;
  const today=new Date(Date.now()+7*3600*1000).toISOString().split('T')[0];
  try{
    const doc=await fsGet('attendance',`${user.uid}_${today}`);
    _hrTodayDoc=doc.exists?doc.data():null;
    renderHRTodayCard(_hrTodayDoc);
  }catch(e){console.error('loadHRToday',e);}
}

function fmtT(v){
  if(!v) return '—';
  try{const d=v instanceof Date?v:new Date(v);return d.toLocaleTimeString('th-TH',{hour:'2-digit',minute:'2-digit',hour12:false});}
  catch{return String(v).substring(11,16)||'—';}
}

function renderHRTodayCard(d){
  const btn=document.getElementById('hr-action-btn');
  const pill=document.getElementById('hr-status-pill');
  const inV=document.getElementById('hr-in-val');
  const outV=document.getElementById('hr-out-val');
  if(!btn) return;
  if(!d){
    btn.className='hr-btn hr-btn-in'; btn.textContent='📍 เช็คอิน'; btn.disabled=false;
    if(pill){pill.textContent='ยังไม่ได้เช็คอิน'; pill.style.background='rgba(255,255,255,.2)';}
    if(inV)inV.textContent='—'; if(outV)outV.textContent='—';
  } else if(!d.check_out){
    if(inV)inV.textContent=fmtT(d.check_in); if(outV)outV.textContent='—';
    const late=d.status==='late';
    if(pill){pill.textContent=late?'⚠️ มาสาย':'✅ เช็คอินแล้ว'; pill.style.background=late?'rgba(245,158,11,.4)':'rgba(16,185,129,.35)';}
    btn.className='hr-btn hr-btn-out'; btn.textContent='🚪 เช็คเอาท์'; btn.disabled=false;
  } else {
    if(inV)inV.textContent=fmtT(d.check_in); if(outV)outV.textContent=fmtT(d.check_out);
    if(pill){pill.textContent='✅ เสร็จสิ้น'; pill.style.background='rgba(16,185,129,.35)';}
    btn.className='hr-btn hr-btn-done'; btn.textContent='เช็คเอาท์แล้ว'; btn.disabled=true;
  }
}

async function hrAction(){
  const user=firebase.auth().currentUser; if(!user){alert('กรุณาเข้าสู่ระบบก่อน');return;}
  if(!_hrTodayDoc) openCamera('checkin');
  else if(!_hrTodayDoc.check_out) openCamera('checkout');
}

async function doHRCheckIn(user, photo=''){
  const btn=document.getElementById('hr-action-btn');
  btn.textContent='กำลังเช็คอิน...'; btn.disabled=true;
  try{
    const now=new Date();
    const today=now.toISOString().split('T')[0];
    const h=now.getHours(), m=now.getMinutes();
    const late=(h>8)||(h===8&&m>0);
    const doc={uid:user.uid,name:window._userName||user.email,email:user.email,
      dept:window._userRole||'',date:today,check_in:now.toISOString(),
      check_in_lat:_hrGPS?_hrGPS.lat:null,check_in_lng:_hrGPS?_hrGPS.lng:null,
      check_out:null,check_out_lat:null,check_out_lng:null,status:late?'late':'present',work_hours:0,
      photo_in:photo||''};
    await fsSet('attendance',`${user.uid}_${today}`,doc);
    // sync to Sheets (exclude base64 photo to keep payload small)
    sendToSheets('attendance', {...doc, photo_in: photo?'[photo]':''});
    _hrTodayDoc=doc; renderHRTodayCard(doc); loadHRHistory();
    if(late) alert(`⚠️ เช็คอินสำเร็จ\nเวลา ${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')} (มาสาย)`);
    // 🔔 Line Notify → HR เมื่อพนักงานมาสาย
    if(late && _hrdGasUrl){
      const _empName=window._userName||user.email||'ไม่ทราบชื่อ';
      const _dept=(window._userRole&&window._userRole!=='admin')?window._userRole:'';
      const _ts=`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}`;
      hrdSendLine(`[WIBWUB HR] ⚠️ มาสาย\nพนักงาน: ${_empName}${_dept?' ('+_dept+')':''}\nCheck in: ${_ts} น.\nวันที่: ${today}`);
    }
  }catch(e){alert('เช็คอินไม่สำเร็จ: '+e.message); btn.disabled=false;}
}

async function doHRCheckOut(user, photo=''){
  const btn=document.getElementById('hr-action-btn');
  btn.textContent='กำลังเช็คเอาท์...'; btn.disabled=true;
  try{
    const now=new Date(); const today=now.toISOString().split('T')[0];
    const inD=_hrTodayDoc.check_in instanceof Date?_hrTodayDoc.check_in:new Date(_hrTodayDoc.check_in);
    const hrs=Math.round((now-inD)/36000)/100;
    const upd={..._hrTodayDoc,check_out:now.toISOString(),
      check_out_lat:_hrGPS?_hrGPS.lat:null,check_out_lng:_hrGPS?_hrGPS.lng:null,work_hours:hrs,
      photo_out:photo||''};
    await fsSet('attendance',`${user.uid}_${today}`,upd);
    // sync to Sheets (exclude base64 photos)
    sendToSheets('attendance', {...upd, photo_in:upd.photo_in?'[photo]':'', photo_out:photo?'[photo]':''});
    _hrTodayDoc=upd; renderHRTodayCard(upd); loadHRHistory();
  }catch(e){alert('เช็คเอาท์ไม่สำเร็จ: '+e.message); btn.disabled=false;}
}

// ── Camera ──────────────────────────────────────────────────────
let _camStream=null, _camAction=null, _camPhoto=null;

async function openCamera(action){
  _camAction=action; _camPhoto=null;
  const modal=document.getElementById('cam-modal');
  const header=document.getElementById('cam-header');
  const video=document.getElementById('cam-video');
  header.textContent=action==='checkin'?'📸 ถ่ายรูปเพื่อเช็คอิน':'📸 ถ่ายรูปเพื่อเช็คเอาท์';
  // reset preview
  document.getElementById('cam-preview-wrap').style.display='none';
  document.getElementById('cam-capture-bar').style.display='flex';
  try{
    _camStream=await navigator.mediaDevices.getUserMedia({
      video:{facingMode:'user',width:{ideal:640},height:{ideal:640}},audio:false
    });
    video.srcObject=_camStream;
    modal.style.display='flex';
  }catch(e){
    alert('ไม่สามารถเปิดกล้องได้\nกรุณาอนุญาตการเข้าถึงกล้องในเบราว์เซอร์\n\n'+e.message);
  }
}

function camCapture(){
  const video=document.getElementById('cam-video');
  const canvas=document.getElementById('cam-canvas');
  const img=document.getElementById('cam-img');
  const preview=document.getElementById('cam-preview-wrap');
  // Capture square crop, 320×320, mirrored (selfie style)
  const size=Math.min(video.videoWidth||640, video.videoHeight||640);
  const sx=(video.videoWidth-size)/2, sy=(video.videoHeight-size)/2;
  canvas.width=320; canvas.height=320;
  const ctx=canvas.getContext('2d');
  ctx.translate(320,0); ctx.scale(-1,1); // mirror
  ctx.drawImage(video, sx, sy, size, size, 0, 0, 320, 320);
  _camPhoto=canvas.toDataURL('image/jpeg', 0.55);
  img.src=_camPhoto;
  document.getElementById('cam-capture-bar').style.display='none';
  preview.style.display='flex';
}

function camRetake(){
  _camPhoto=null;
  document.getElementById('cam-preview-wrap').style.display='none';
  document.getElementById('cam-capture-bar').style.display='flex';
}

async function camConfirm(){
  const photo=_camPhoto;
  camClose();
  const user=firebase.auth().currentUser;
  if(!user){alert('กรุณาเข้าสู่ระบบก่อน');return;}
  if(_camAction==='checkin') await doHRCheckIn(user, photo||'');
  else await doHRCheckOut(user, photo||'');
}

function camClose(){
  if(_camStream){_camStream.getTracks().forEach(t=>t.stop()); _camStream=null;}
  document.getElementById('cam-modal').style.display='none';
}
// ────────────────────────────────────────────────────────────────

function toggleHRLeave(){
  const body=document.getElementById('hr-leave-body');
  const arrow=document.getElementById('hr-leave-arrow');
  if(!body) return;
  const open=body.style.display!=='none';
  body.style.display=open?'none':'block';
  if(arrow) arrow.textContent=open?'▼':'▲';
}

async function submitLeaveRequest(){
  const user=firebase.auth().currentUser; if(!user){alert('กรุณาเข้าสู่ระบบก่อน');return;}
  const type=document.getElementById('hr-type').value;
  const start=document.getElementById('hr-start-date').value;
  const end=document.getElementById('hr-end-date').value;
  const reason=document.getElementById('hr-reason').value.trim();
  const msgEl=document.getElementById('hr-leave-msg');
  if(!start||!end){msgEl.textContent='กรุณาเลือกวันที่';msgEl.className='hr-msg err';return;}
  if(end<start){msgEl.textContent='วันสิ้นสุดต้องหลังวันเริ่มต้น';msgEl.className='hr-msg err';return;}
  if(!reason){msgEl.textContent='กรุณาระบุเหตุผล';msgEl.className='hr-msg err';return;}
  const btn=document.querySelector('.hr-submit-btn');
  btn.textContent='กำลังส่ง...'; btn.disabled=true;
  const days=Math.ceil((new Date(end)-new Date(start))/86400000)+1;
  try{
    const leaveData={uid:user.uid,name:window._userName||user.email,
      email:user.email,dept:window._userRole||'',type,start_date:start,end_date:end,
      days,reason,status:'pending',created_at:new Date().toISOString(),
      approved_by:null,approved_at:null,admin_note:null};
    await fsAdd('leave_requests', leaveData);
    sendToSheets('leave_request', leaveData);  // sync → Google Sheets
    msgEl.textContent='✅ ส่งคำร้องเรียบร้อย — HR จะแจ้งผลกลับมา'; msgEl.className='hr-msg ok';
    document.getElementById('hr-reason').value='';
    setTimeout(()=>{msgEl.textContent='';},5000);
    loadHRHistory();
  }catch(e){msgEl.textContent='เกิดข้อผิดพลาด: '+e.message;msgEl.className='hr-msg err';}
  finally{btn.textContent='ส่งคำร้อง';btn.disabled=false;}
}

async function loadHRHistory(){
  const user=firebase.auth().currentUser; if(!user) return;
  const listEl=document.getElementById('hr-history-list'); if(!listEl) return;
  try{
    const [attDocs,lvDocs]=await Promise.all([
      fsQuery('attendance',[{field:'uid',value:user.uid}],{field:'date',dir:'DESCENDING'},10),
      fsQuery('leave_requests',[{field:'uid',value:user.uid}],{field:'created_at',dir:'DESCENDING'},5)
    ]);
    const items=[];
    attDocs.forEach(doc=>{const d=doc.data();items.push({k:d.date+'Z',type:'att',d});});
    lvDocs.forEach(doc=>{const d=doc.data();items.push({k:(d.start_date||'')+'A',type:'lv',d,id:doc.id});});
    items.sort((a,b)=>b.k.localeCompare(a.k));
    if(!items.length){listEl.innerHTML='<div style="text-align:center;padding:20px;color:var(--muted);font-size:12px;">ยังไม่มีประวัติ</div>';return;}
    listEl.innerHTML=items.slice(0,15).map(item=>{
      if(item.type==='att'){
        const d=item.d;
        const inT=fmtT(d.check_in), outT=d.check_out?fmtT(d.check_out):'—';
        const st=d.check_out?'checked-out':d.status||'present';
        const stLbl={present:'มาปกติ',late:'มาสาย','checked-out':'เสร็จสิ้น'}[st]||st;
        const bc={present:'hb-present',late:'hb-late','checked-out':'hb-checked-out'}[st]||'hb-present';
        const dateStr=(d.date||'').replace(/(\d{4})-(\d{2})-(\d{2})/,'$3/$2');
        return `<div class="hr-hist-card"><div class="hr-hist-date">${dateStr}</div><div class="hr-hist-body"><div class="hr-hist-type">🕐 เข้า ${inT} — ออก ${outT}</div><div class="hr-hist-sub">${d.check_out?(d.work_hours||0)+' ชม.':''}</div></div><span class="hr-hist-badge ${bc}">${stLbl}</span></div>`;
      } else {
        const d=item.d;
        const bc={pending:'hb-pending',approved:'hb-approved',rejected:'hb-rejected'}[d.status]||'hb-pending';
        const stLbl={pending:'รอพิจารณา',approved:'อนุมัติ',rejected:'ไม่อนุมัติ'}[d.status]||d.status;
        const dateStr=(d.start_date||'').replace(/(\d{4})-(\d{2})-(\d{2})/,'$3/$2');
        const reasonShort=(d.reason||'').substring(0,28)+((d.reason||'').length>28?'...':'');
        return `<div class="hr-hist-card"><div class="hr-hist-date">${dateStr}</div><div class="hr-hist-body"><div class="hr-hist-type">📝 ${d.type}</div><div class="hr-hist-sub">${d.days}วัน • ${reasonShort}</div></div><span class="hr-hist-badge ${bc}">${stLbl}</span></div>`;
      }
    }).join('');
  }catch(e){listEl.innerHTML='<div style="text-align:center;padding:20px;color:var(--red);font-size:11px;">โหลดไม่สำเร็จ</div>';}
}

// ════════════════════════════════════════
// HR DASHBOARD (admin embedded view)
// ════════════════════════════════════════
const HRD_ADMIN_ROLES = ['admin','hr_team','head_marketing'];
let _hrdGasUrl = '';
let _hrdInited = false;

function initHRDash(){
  if(!_hrdInited){
    _hrdInited = true;
    const el = document.getElementById('hrd-gas-url');
    _hrdGasUrl = localStorage.getItem('wibwub_gas_url')||'https://script.google.com/macros/s/AKfycbz90-p1J94A03ltO38kpOrRw36JPDATXS-TQ4DjOW7hYgaBfFHjaVtJgqdJMYZlzoGN_w/exec';
    if(el) el.value = _hrdGasUrl;
    const elSheets = document.getElementById('hrd-sheets-url');
    _sheetsGasUrl = localStorage.getItem('wibwub_sheets_url')||_GAS_SHEETS_DEFAULT;
    if(elSheets) elSheets.value = _sheetsGasUrl;
    hrdSetTodayDate();
    hrdSetCurrentWeek();
    hrdLoadPendingLeave();
    hrdLoadLeaveHistory();
    hrdLoadTimesheet();
  } else {
    hrdLoadToday();
    hrdLoadPendingLeave();
  }
}

function goHRTab(t){
  document.querySelectorAll('.hrd-tab').forEach(el=>el.classList.remove('active'));
  document.querySelectorAll('.hrd-sec').forEach(el=>el.classList.remove('active'));
  document.getElementById('hrd-tab-'+t)?.classList.add('active');
  document.getElementById('hrd-sec-'+t)?.classList.add('active');
}

// ── Today ──────────────────────────────
function hrdSetTodayDate(){
  const el=document.getElementById('hrd-today-date');
  if(el) el.value=new Date(Date.now()+7*3600*1000).toISOString().split('T')[0];
  hrdLoadToday();
}

async function hrdLoadToday(){
  const date=document.getElementById('hrd-today-date')?.value;
  if(!date) return;
  const wrap=document.getElementById('hrd-today-tbl');
  wrap.innerHTML='<div class="hrd-loading"><span class="hrd-spin"></span> กำลังโหลด...</div>';
  try{
    const docs=await fsQuery('attendance',[{field:'date',value:date}],{field:'check_in',dir:'ASCENDING'});
    hrdUpdateKPIs(docs);
    hrdRenderTodayTable(docs,wrap);
  }catch(e){wrap.innerHTML=`<div class="hrd-loading" style="color:var(--red)">โหลดไม่สำเร็จ: ${e.message}</div>`;}
}

function hrdUpdateKPIs(docs){
  let present=0,late=0,out=0,sumHrs=0,hCnt=0;
  docs.forEach(doc=>{
    const d=doc.data();
    if(d.status==='present'||d.status==='late'){
      present++; if(d.status==='late') late++;
      if(d.check_out){out++;if(d.work_hours){sumHrs+=Number(d.work_hours);hCnt++;}}
    }
  });
  const set=(id,v)=>{const el=document.getElementById(id);if(el)el.textContent=v;};
  set('hrd-kpi-present',present); set('hrd-kpi-late',late); set('hrd-kpi-out',out);
  set('hrd-kpi-hrs',hCnt>0?(sumHrs/hCnt).toFixed(1):'—');
}

function hrdRenderTodayTable(docs,container){
  if(!docs.length){container.innerHTML='<div class="hrd-empty">📭 ไม่มีข้อมูลเช็คอินวันนี้</div>';return;}
  const rows=docs.map(doc=>{
    const d=doc.data();
    const inT=fmtT(d.check_in), outT=fmtT(d.check_out);
    const hrs=d.check_out&&d.check_in?Math.round((new Date(d.check_out)-new Date(d.check_in))/360000)/10:null;
    const st=d.check_out?'checked-out':d.status||'present';
    const badge={'checked-out':'<span class="hrd-badge hb-ok">เสร็จ</span>','late':'<span class="hrd-badge hb-warn">สาย</span>','present':'<span class="hrd-badge hb-ok" style="background:#dbeafe;color:#1e40af">งาน</span>'}[st]||'';
    const loc=d.check_in_lat?`${Number(d.check_in_lat).toFixed(4)},${Number(d.check_in_lng).toFixed(4)}`:'—';
    const pIn=d.photo_in?`<img src="${d.photo_in}" class="cam-photo-thumb cam-photo-in" onclick="hrdViewPhoto(this.src,'เข้างาน ${inT}')" title="รูปเข้างาน">`:`<span style="color:var(--muted);font-size:11px">—</span>`;
    const pOut=d.photo_out?`<img src="${d.photo_out}" class="cam-photo-thumb cam-photo-out" onclick="hrdViewPhoto(this.src,'ออกงาน ${outT}')" title="รูปออกงาน">`:`<span style="color:var(--muted);font-size:11px">—</span>`;
    return `<tr><td><strong>${d.name||d.email||'—'}</strong><br><span style="font-size:10px;color:var(--muted)">${d.email||''}</span></td><td>${d.dept||'—'}</td><td style="font-weight:600">${inT}</td><td>${outT}</td><td style="text-align:center">${hrs!==null?hrs+' ชม.':'—'}</td><td>${badge}</td><td style="text-align:center">${pIn}</td><td style="text-align:center">${pOut}</td><td style="font-size:9px;color:var(--muted)">${loc}</td></tr>`;
  }).join('');
  container.innerHTML=`<div class="hrd-tbl-wrap"><table><thead><tr><th>พนักงาน</th><th>แผนก</th><th>เข้างาน</th><th>ออกงาน</th><th>ชั่วโมง</th><th>สถานะ</th><th>📷 เข้า</th><th>📷 ออก</th><th>GPS</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}

function hrdViewPhoto(src, label){
  // Show full-size photo in a simple overlay
  const ov=document.createElement('div');
  ov.style.cssText='position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.92);display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;';
  ov.innerHTML=`<div style="color:#fff;font-size:13px;margin-bottom:12px;font-weight:600;">${label}</div><img src="${src}" style="max-width:90vw;max-height:75vh;border-radius:12px;object-fit:contain;"><div style="color:rgba(255,255,255,.5);font-size:11px;margin-top:14px;">แตะเพื่อปิด</div>`;
  ov.onclick=()=>document.body.removeChild(ov);
  document.body.appendChild(ov);
}

// ── Leave ──────────────────────────────
async function hrdLoadPendingLeave(){
  const el=document.getElementById('hrd-pending-list');
  el.innerHTML='<div class="hrd-loading"><span class="hrd-spin"></span></div>';
  try{
    const docs=await fsQuery('leave_requests',[{field:'status',value:'pending'}],{field:'created_at',dir:'ASCENDING'},50);
    const cnt=document.getElementById('hrd-pending-count');
    if(cnt) cnt.textContent=docs.length;
    const badge=document.getElementById('hrd-leave-badge');
    if(badge){badge.textContent=docs.length;badge.style.display=docs.length>0?'':'none';}
    if(!docs.length){el.innerHTML='<div class="hrd-empty">✅ ไม่มีคำร้องรอพิจารณา</div>';return;}
    const isAdmin=HRD_ADMIN_ROLES.includes(window._userRole||'');
    el.innerHTML=docs.map(doc=>{
      const d=doc.data();
      const typeIcon={ลาป่วย:'🤒',ลากิจ:'📋',ลาพักร้อน:'🏖️',ลาคลอด:'🍼',ลาบวช:'🙏',WFH:'🏠',อื่นๆ:'📌'}[d.type]||'📝';
      const dr=hrdFmtDateRange(d.start_date,d.end_date,d.days);
      const created=d.created_at?new Date(d.created_at instanceof Date?d.created_at:d.created_at).toLocaleDateString('th-TH'):'—';
      const btns=isAdmin
        ?`<div style="margin-top:8px;display:flex;gap:5px"><button class="hrd-btn-approve" onclick="hrdApproveLeave('${doc.id}','${(d.name||d.email||'').replace(/'/g,'&apos;')}','${d.type}',this)">✓ อนุมัติ</button><button class="hrd-btn-reject" onclick="hrdRejectLeave('${doc.id}','${(d.name||d.email||'').replace(/'/g,'&apos;')}','${d.type}',this)">✗ ปฏิเสธ</button></div>`
        :`<div style="font-size:10px;color:var(--muted);margin-top:4px">รอ HR พิจารณา</div>`;
      return `<div class="hrd-leave-item"><div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px"><div><div style="font-size:12px;font-weight:600">${typeIcon} ${d.type} — <span style="color:var(--bl)">${d.name||d.email||'—'}</span></div><div style="font-size:10px;color:var(--muted);margin-top:2px">${dr} • ยื่นเมื่อ ${created}</div><div style="font-size:11px;margin-top:5px;background:#f8f9fb;padding:5px 9px;border-radius:6px">${d.reason||'—'}</div>${btns}</div><span class="hrd-badge hb-pend">รอ</span></div></div>`;
    }).join('');
  }catch(e){el.innerHTML=`<div class="hrd-loading" style="color:var(--red)">โหลดไม่สำเร็จ: ${e.message}</div>`;}
}

async function hrdLoadLeaveHistory(){
  const el=document.getElementById('hrd-history-list');
  el.innerHTML='<div class="hrd-loading"><span class="hrd-spin"></span></div>';
  const fs=document.getElementById('hrd-lv-filter')?.value||'';
  const cutoff=new Date();cutoff.setDate(cutoff.getDate()-60);
  try{
    let docs=await fsQuery('leave_requests',[],{field:'created_at',dir:'DESCENDING'},200);
    docs=docs.filter(doc=>{
      const d=doc.data();
      if(d.status==='pending')return false;
      if(fs&&d.status!==fs)return false;
      return true;
    });
    if(!docs.length){el.innerHTML='<div class="hrd-empty">📋 ไม่มีประวัติใบลา</div>';return;}
    const rows=docs.map(doc=>{
      const d=doc.data();
      const bc={approved:'hb-approved',rejected:'hb-rejected',pending:'hb-pend'}[d.status]||'hb-pend';
      const sl={approved:'อนุมัติ',rejected:'ไม่อนุมัติ',pending:'รอ'}[d.status]||d.status;
      const created=d.created_at?new Date(d.created_at instanceof Date?d.created_at:d.created_at).toLocaleDateString('th-TH'):'—';
      return `<tr><td><strong>${d.name||d.email||'—'}</strong></td><td>${d.type||'—'}</td><td style="white-space:nowrap;font-size:10px">${hrdFmtDateRange(d.start_date,d.end_date,d.days)}</td><td style="font-size:10px;color:var(--muted);max-width:120px">${(d.reason||'').substring(0,35)}${(d.reason||'').length>35?'...':''}</td><td style="font-size:10px">${created}</td><td><span class="hrd-badge ${bc}">${sl}</span><br><span style="font-size:9px;color:var(--muted)">${d.approved_by||''}</span></td></tr>`;
    }).join('');
    el.innerHTML=`<div class="hrd-tbl-wrap"><table><thead><tr><th>พนักงาน</th><th>ประเภท</th><th>วันที่</th><th>เหตุผล</th><th>ยื่นเมื่อ</th><th>สถานะ</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  }catch(e){el.innerHTML=`<div class="hrd-loading" style="color:var(--red)">โหลดไม่สำเร็จ: ${e.message}</div>`;}
}

async function hrdApproveLeave(id,name,type,btn){
  if(!confirm(`อนุมัติใบลา "${type}" ของ ${name}?`)) return;
  btn.disabled=true;btn.nextElementSibling.disabled=true;
  const note=prompt('หมายเหตุ (เว้นว่างได้):','')||'';
  try{
    const doc=await fsGet('leave_requests',id);
    const data=doc.data();
    const user=firebase.auth().currentUser;
    const approvedData={...data,status:'approved',approved_by:window._userName||user?.email,approved_at:new Date().toISOString(),admin_note:note};
    await fsSet('leave_requests',id,approvedData);
    sendToSheets('leave_update', approvedData);  // sync → Google Sheets
    await hrdSendLine(`[WIBWUB HR] ✅ อนุมัติใบลา\nพนักงาน: ${name}\nประเภท: ${type}\nวันที่: ${hrdFmtDateRange(data.start_date,data.end_date,data.days)}\nอนุมัติโดย: ${window._userName||user?.email}${note?'\nหมายเหตุ: '+note:''}`);
    hrdLoadPendingLeave();hrdLoadLeaveHistory();
  }catch(e){alert('เกิดข้อผิดพลาด: '+e.message);btn.disabled=false;btn.nextElementSibling.disabled=false;}
}

async function hrdRejectLeave(id,name,type,btn){
  const reason=prompt(`เหตุผลที่ปฏิเสธ "${type}" ของ ${name}:`,'');
  if(reason===null) return;
  btn.disabled=true;btn.previousElementSibling.disabled=true;
  try{
    const doc=await fsGet('leave_requests',id);
    const data=doc.data();
    const user=firebase.auth().currentUser;
    const rejectedData={...data,status:'rejected',approved_by:window._userName||user?.email,approved_at:new Date().toISOString(),admin_note:reason||''};
    await fsSet('leave_requests',id,rejectedData);
    sendToSheets('leave_update', rejectedData);  // sync → Google Sheets
    await hrdSendLine(`[WIBWUB HR] ❌ ไม่อนุมัติใบลา\nพนักงาน: ${name}\nประเภท: ${type}\nวันที่: ${hrdFmtDateRange(data.start_date,data.end_date,data.days)}\nเหตุผล: ${reason||'—'}`);
    hrdLoadPendingLeave();hrdLoadLeaveHistory();
  }catch(e){alert('เกิดข้อผิดพลาด: '+e.message);btn.disabled=false;btn.previousElementSibling.disabled=false;}
}

function hrdFmtDateRange(s,e,days){
  const fmt=v=>v?v.replace(/(\d{4})-(\d{2})-(\d{2})/,'$3/$2'):'—';
  return s===e?`${fmt(s)} (${days||1}วัน)`:`${fmt(s)}–${fmt(e)} (${days||1}วัน)`;
}

// ── Timesheet ──────────────────────────
function hrdSetCurrentWeek(){
  const d=new Date(),day=d.getDay(),diff=d.getDate()-day+(day===0?-6:1);
  const mon=new Date(d.setDate(diff));
  const el=document.getElementById('hrd-ts-week');
  if(el) el.value=mon.toISOString().split('T')[0];
  hrdLoadTimesheet();
}
function hrdOffsetWeek(delta){
  const el=document.getElementById('hrd-ts-week');
  if(!el?.value) return;
  const d=new Date(el.value);d.setDate(d.getDate()+delta*7);
  el.value=d.toISOString().split('T')[0];hrdLoadTimesheet();
}

async function hrdLoadTimesheet(){
  const startStr=document.getElementById('hrd-ts-week')?.value;
  if(!startStr) return;
  const container=document.getElementById('hrd-timesheet');
  container.innerHTML='<div class="hrd-loading"><span class="hrd-spin"></span> กำลังโหลด...</div>';
  const startDate=new Date(startStr);
  const thDay=['จ.','อ.','พ.','พฤ.','ศ.'];
  const thMo=['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'];
  const days=[];
  for(let i=0;i<5;i++){const d=new Date(startDate);d.setDate(d.getDate()+i);days.push({str:d.toISOString().split('T')[0],lbl:`${thDay[i]} ${d.getDate()}/${d.getMonth()+1}`});}
  const endDate=new Date(startDate);endDate.setDate(endDate.getDate()+4);
  const fmtD=d=>`${d.getDate()} ${thMo[d.getMonth()]} ${d.getFullYear()+543}`;
  const lbl=document.getElementById('hrd-week-label');
  if(lbl) lbl.textContent=`สัปดาห์ ${fmtD(startDate)} – ${fmtD(endDate)}`;
  try{
    const allDocs=await Promise.all(days.map(day=>fsQuery('attendance',[{field:'date',value:day.str}],{field:'name',dir:'ASCENDING'})));
    const empMap={};
    allDocs.forEach((docs,di)=>{
      docs.forEach(doc=>{
        const d=doc.data();const uid=d.uid||d.email;
        if(!empMap[uid])empMap[uid]={name:d.name||d.email||'—',dept:d.dept||'',days:{}};
        empMap[uid].days[days[di].str]=d;
      });
    });
    const emps=Object.values(empMap).sort((a,b)=>(a.dept+a.name).localeCompare(b.dept+b.name,'th'));
    if(!emps.length){container.innerHTML='<div class="hrd-empty">📭 ไม่มีข้อมูลในสัปดาห์นี้</div>';return;}
    const hdrCells=`<div class="hrd-ts-cell hrd-ts-hdr" style="font-weight:700">พนักงาน</div>`+days.map(d=>`<div class="hrd-ts-cell hrd-ts-hdr" style="text-align:center">${d.lbl}</div>`).join('');
    const rows=emps.map(emp=>{
      const nc=`<div class="hrd-ts-cell hrd-ts-name"><div style="font-size:11px;font-weight:600">${emp.name}</div><div style="font-size:9px;color:var(--muted)">${emp.dept}</div></div>`;
      const dc=days.map(day=>{
        const rec=emp.days[day.str];
        if(!rec) return`<div class="hrd-ts-cell hrd-ts-absent" style="font-size:10px">—</div>`;
        const inT=fmtT(rec.check_in),outT=fmtT(rec.check_out);
        const cls=rec.status==='late'?'hrd-ts-late':'hrd-ts-ok';
        return`<div class="hrd-ts-cell ${cls}" style="text-align:center"><div style="font-weight:700;font-size:11px">${inT}</div><div style="font-size:10px;opacity:.65">${outT}</div>${rec.status==='late'?'<div style="font-size:9px;color:#d97706">⚠สาย</div>':''}</div>`;
      }).join('');
      return nc+dc;
    }).join('');
    container.innerHTML=`<div class="hrd-ts-grid" style="grid-template-columns:120px repeat(5,1fr)">${hdrCells}${rows}</div>`;
  }catch(e){container.innerHTML=`<div class="hrd-loading" style="color:var(--red)">โหลดไม่สำเร็จ: ${e.message}</div>`;}
}

// ── Line Notify ────────────────────────
function hrdSaveGASUrl(){
  _hrdGasUrl=document.getElementById('hrd-gas-url')?.value?.trim()||'';
  localStorage.setItem('wibwub_gas_url',_hrdGasUrl);
}
function hrdSaveSheetsUrl(){
  _sheetsGasUrl=document.getElementById('hrd-sheets-url')?.value?.trim()||'';
  localStorage.setItem('wibwub_sheets_url',_sheetsGasUrl);
  const el=document.getElementById('hrd-sheets-msg');
  if(el){el.textContent='✓ บันทึกแล้ว';el.style.color='#16a34a';setTimeout(()=>el.textContent='',2000);}
}
async function hrdTestSheets(){
  hrdSaveSheetsUrl();
  const el=document.getElementById('hrd-sheets-msg');
  if(!_sheetsGasUrl){if(el){el.textContent='กรุณาใส่ URL';el.style.color='var(--red)';}return;}
  if(el){el.textContent='กำลังทดสอบ...';el.style.color='var(--muted)';}
  try{
    const r=await fetch(_sheetsGasUrl+'?test=1',{mode:'cors'});
    const d=await r.json();
    if(el){el.textContent=d.ok?'✅ เชื่อมต่อสำเร็จ':'❌ '+d.error;el.style.color=d.ok?'#16a34a':'var(--red)';}
  }catch(e){if(el){el.textContent='❌ เชื่อมต่อไม่ได้';el.style.color='var(--red)';}}
}
async function hrdSendLine(msg){
  if(!_hrdGasUrl) return;
  try{await fetch(_hrdGasUrl,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:'\n'+msg}),mode:'cors'});}
  catch(e){console.warn('Line Notify:',e);}
}
async function hrdTestLineNotify(){
  hrdSaveGASUrl();
  const el=document.getElementById('hrd-notify-msg');
  if(!_hrdGasUrl){if(el){el.textContent='กรุณาใส่ GAS Proxy URL';el.style.color='var(--red)';}return;}
  if(el){el.textContent='กำลังส่ง...';el.style.color='var(--muted)';}
  try{
    await hrdSendLine('[WIBWUB HR] 🧪 ทดสอบระบบแจ้งเตือน — ใช้งานได้ปกติ ✅');
    if(el){el.textContent='✅ ส่งสำเร็จ!';el.style.color='#16a34a';}
  }catch(e){if(el){el.textContent='❌ '+e.message;el.style.color='var(--red)';}}
}

// Secondary Firebase app — ใช้สร้าง user ใหม่โดยไม่ logout admin
let _secondaryApp  = null;
let _secondaryAuth = null;
function getSecondaryAuth(){
  if(!_secondaryApp){
    _secondaryApp  = firebase.initializeApp(firebaseConfig,'secondary');
    _secondaryAuth = _secondaryApp.auth();
  }
  return _secondaryAuth;
}

window._userRole = null;
window._userName = null;

// ── Listen for auth state changes ──
auth.onAuthStateChanged(async user => {
  if(user){
    let role=null, name=user.email;
    try{
      const snap = await fsGet('users', user.uid);
      if(snap.exists){ role=snap.data().role||null; name=snap.data().name||name; }
    }catch(e){ console.warn('Firestore read failed',e); }
    // ถ้าไม่มี Firestore record = บัญชีถูกลบ → force logout
    if(!role){
      await auth.signOut();
      const errEl=document.getElementById('loginError');
      if(errEl){ errEl.textContent='บัญชีนี้ถูกลบออกจากระบบแล้ว กรุณาติดต่อ Admin'; errEl.style.display='block'; }
      return;
    }
    window._userRole = role;
    window._userName = name;
    // Show app, hide overlay
    document.getElementById('loginOverlay').style.display = 'none';
    document.getElementById('hdrUser').style.display = '';
    document.getElementById('hdrUserName').textContent = name;
    applyRole(role);
  } else {
    window._userRole = null;
    document.getElementById('loginOverlay').style.display = 'flex';
    document.getElementById('hdrUser').style.display = 'none';
    resetNavVisibility();
  }
});

// ── Apply role: show/hide nav tabs ──
function applyRole(role){
  resetNavVisibility();
  const navHome        = document.getElementById('nav-home');
  const navSales       = document.getElementById('nav-sales');
  const navMk          = document.getElementById('nav-mk');
  const navAdmin       = document.getElementById('nav-admin');
  const navProcurement = document.getElementById('nav-procurement');
  const navHr          = document.getElementById('nav-hr');
  const mkTabs         = document.getElementById('mk-tabs');

  // เข้า-ออกงาน: เปิดให้ทุกคน | HR Dashboard: admin เท่านั้น
  const navAttendance = document.getElementById('nav-attendance');
  if(navAttendance) navAttendance.style.display = '';
  navHr.style.display = 'none';

  if(role === 'admin'){
    navAdmin.style.display       = '';
    navProcurement.style.display = '';
    navHr.style.display          = '';   // admin เห็น HR Dashboard
    nav('home');
  } else if(role === 'head_marketing'){
    nav('home');
  } else if(role === 'kol_team'){
    navHome.style.display  = 'none';
    navSales.style.display = 'none';
    mkTabs.style.display   = 'none';
    nav('mk');
    document.querySelectorAll('[id^="m-sv-"]').forEach(v=>v.classList.remove('active'));
    document.getElementById('m-sv-1').classList.add('active');
    renderAfi();
  } else if(role === 'content_team'){
    navHome.style.display  = 'none';
    navSales.style.display = 'none';
    mkTabs.style.display   = 'none';
    nav('mk');
    document.querySelectorAll('[id^="m-sv-"]').forEach(v=>v.classList.remove('active'));
    document.getElementById('m-sv-3').classList.add('active');
    renderTT();
  } else if(role === 'hr_team'){
    navHome.style.display  = 'none';
    navSales.style.display = 'none';
    navMk.style.display    = 'none';
    nav('attendance');
  } else if(role === 'procurement'){
    navHome.style.display        = 'none';
    navSales.style.display       = 'none';
    navMk.style.display          = 'none';
    navProcurement.style.display = '';
    nav('procurement');
  }
}

function resetNavVisibility(){
  ['nav-home','nav-sales','nav-mk','nav-attendance'].forEach(id=>{
    const el=document.getElementById(id);
    if(el) el.style.display='';
  });
  // HR Dashboard: admin เท่านั้น
  const navHrReset=document.getElementById('nav-hr');
  if(navHrReset) navHrReset.style.display='none';
  const navAdmin=document.getElementById('nav-admin');
  if(navAdmin) navAdmin.style.display='none';
  const navProc=document.getElementById('nav-procurement');
  if(navProc) navProc.style.display='none';
  const mkTabs=document.getElementById('mk-tabs');
  if(mkTabs) mkTabs.style.display='';
}

// ── Login ──
function doLogin(){
  const email = document.getElementById('loginEmail').value.trim();
  const pass  = document.getElementById('loginPass').value;
  const errEl = document.getElementById('loginErr');
  const btn   = document.getElementById('loginBtn');
  errEl.textContent='';
  if(!email||!pass){ errEl.textContent='กรุณากรอกอีเมลและรหัสผ่าน'; return; }
  btn.textContent='กำลังเข้าสู่ระบบ...';
  btn.disabled=true;
  auth.signInWithEmailAndPassword(email,pass)
    .catch(err=>{
      const msgs={
        'auth/user-not-found':'ไม่พบบัญชีนี้ในระบบ',
        'auth/wrong-password':'รหัสผ่านไม่ถูกต้อง',
        'auth/invalid-email':'รูปแบบอีเมลไม่ถูกต้อง',
        'auth/invalid-credential':'อีเมลหรือรหัสผ่านไม่ถูกต้อง',
        'auth/too-many-requests':'พยายามเข้าสู่ระบบมากเกินไป โปรดรอสักครู่',
        'auth/network-request-failed':'เชื่อมต่อเครือข่ายล้มเหลว',
      };
      errEl.textContent=msgs[err.code]||('เกิดข้อผิดพลาด: '+err.message);
    })
    .finally(()=>{ btn.textContent='เข้าสู่ระบบ'; btn.disabled=false; });
}
document.getElementById('loginPass').addEventListener('keydown',e=>{ if(e.key==='Enter') doLogin(); });
document.getElementById('loginEmail').addEventListener('keydown',e=>{ if(e.key==='Enter') document.getElementById('loginPass').focus(); });

// ── Logout ──
function doLogout(){
  if(!confirm('ออกจากระบบ?')) return;
  auth.signOut();
}

// ════════════════════════════════════════
// ADMIN: สร้าง + แสดงรายชื่อผู้ใช้
// ════════════════════════════════════════
async function adminCreateUser(){
  const email = document.getElementById('newEmail').value.trim();
  const pass  = document.getElementById('newPass').value;
  const name  = document.getElementById('newName').value.trim();
  const role  = document.getElementById('newRole').value;
  const msgEl = document.getElementById('createMsg');
  msgEl.className='af-msg';
  msgEl.textContent='';

  if(!email||!pass||!name){ msgEl.className='af-msg err'; msgEl.textContent='กรุณากรอกให้ครบทุกช่อง'; return; }
  if(pass.length<6){ msgEl.className='af-msg err'; msgEl.textContent='รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'; return; }

  msgEl.className='af-msg'; msgEl.textContent='กำลังสร้างบัญชี...';
  try{
    const secAuth = getSecondaryAuth();
    const cred = await secAuth.createUserWithEmailAndPassword(email,pass);
    await fsSet('users', cred.user.uid, { email, name, role, createdAt: new Date() });
    await secAuth.signOut();
    msgEl.className='af-msg ok'; msgEl.textContent='✓ สร้างบัญชี '+email+' สำเร็จ';
    document.getElementById('newEmail').value='';
    document.getElementById('newPass').value='';
    document.getElementById('newName').value='';
    loadAdminUsers();
  } catch(err){
    const msgs={
      'auth/email-already-in-use':'อีเมลนี้มีผู้ใช้แล้ว',
      'auth/invalid-email':'รูปแบบอีเมลไม่ถูกต้อง',
      'auth/weak-password':'รหัสผ่านไม่ปลอดภัยพอ ต้องมีอย่างน้อย 6 ตัว',
    };
    msgEl.className='af-msg err';
    msgEl.textContent=msgs[err.code]||err.message;
  }
}

// ── เปลี่ยน Password ตัวเอง ──
function showChangePasswordModal(){
  document.getElementById('cpOld').value='';
  document.getElementById('cpNew').value='';
  document.getElementById('cpConfirm').value='';
  document.getElementById('cpMsg').textContent='';
  document.getElementById('cpMsg').className='cp-msg';
  document.getElementById('cpOverlay').classList.add('show');
}
async function doChangePassword(){
  const old=document.getElementById('cpOld').value;
  const nw=document.getElementById('cpNew').value;
  const cf=document.getElementById('cpConfirm').value;
  const msg=document.getElementById('cpMsg');
  msg.className='cp-msg';
  if(!old||!nw||!cf){msg.className='cp-msg err';msg.textContent='กรุณากรอกข้อมูลให้ครบ';return;}
  if(nw.length<6){msg.className='cp-msg err';msg.textContent='Password ใหม่ต้องมีอย่างน้อย 6 ตัวอักษร';return;}
  if(nw!==cf){msg.className='cp-msg err';msg.textContent='Password ใหม่ไม่ตรงกัน';return;}
  try{
    const user=auth.currentUser;
    const cred=firebase.auth.EmailAuthProvider.credential(user.email,old);
    await user.reauthenticateWithCredential(cred);
    await user.updatePassword(nw);
    msg.className='cp-msg ok';msg.textContent='เปลี่ยน password สำเร็จ ✓';
    setTimeout(()=>document.getElementById('cpOverlay').classList.remove('show'),1500);
  }catch(e){
    msg.className='cp-msg err';
    if(e.code==='auth/wrong-password'||e.code==='auth/invalid-credential')msg.textContent='Password ปัจจุบันไม่ถูกต้อง';
    else if(e.code==='auth/weak-password')msg.textContent='Password ใหม่ไม่แข็งแรงพอ';
    else msg.textContent='เกิดข้อผิดพลาด: '+e.message;
  }
}
// ── Admin ลบ User ──
async function adminDeleteUser(uid, name){
  if(!confirm('ลบบัญชี "'+name+'" ออกจากระบบ?\n\nUser จะไม่สามารถ login ได้ทันที\n(กดยืนยันเพื่อดำเนินการต่อ)')) return;
  try{
    await fsDel('users', uid);
    const card=document.getElementById('ucard-'+uid);
    if(card){ card.style.opacity='0.4'; card.style.pointerEvents='none'; }
    // show success briefly then reload list
    setTimeout(()=>loadAdminUsers(), 600);
  }catch(e){
    alert('เกิดข้อผิดพลาด: '+e.message);
  }
}
// ── Admin รีเซ็ต Password ──
async function adminResetPassword(email){
  if(!confirm('ส่ง email รีเซ็ต password ไปที่\n'+email+'\nใช่ไหม?')) return;
  try{
    await auth.sendPasswordResetEmail(email);
    alert('ส่ง email รีเซ็ตไปที่ '+email+' แล้ว ✓\nให้ user เช็ค inbox (รวมถึงโฟลเดอร์ spam)');
  }catch(e){
    alert('เกิดข้อผิดพลาด: '+e.message);
  }
}

async function loadAdminUsers(){
  if(window._userRole!=='admin') return;
  const listEl = document.getElementById('adminUserList');
  if(!listEl) return;
  listEl.innerHTML='<div style="text-align:center;padding:20px;color:var(--muted);font-size:13px;">กำลังโหลด...</div>';
  try{
    const docs = await fsList('users');
    docs.sort((a,b)=>{ const da=a.data().createdAt, db2=b.data().createdAt; return ((da instanceof Date?da:new Date(0))-(db2 instanceof Date?db2:new Date(0))); });
    const roleLabel={admin:'Admin',head_marketing:'Head Marketing',kol_team:'KOL Team',content_team:'Content Team',hr_team:'HR Team',procurement:'จัดซื้อ'};
    if(!docs.length){ listEl.innerHTML='<div style="text-align:center;padding:20px;color:var(--muted);font-size:13px;">ยังไม่มีผู้ใช้ในระบบ</div>'; return; }
    listEl.innerHTML=docs.map(doc=>{
      const d=doc.data();
      const ini=((d.name||d.email)||'?')[0].toUpperCase();
      const esc=d.email.replace(/'/g,"\\'");
      const escName=(d.name||d.email).replace(/'/g,"\\'");
      const uid=doc.id;
      return`<div class="admin-ucard" id="ucard-${uid}">
        <div class="admin-uav">${ini}</div>
        <div class="admin-uinfo">
          <div class="admin-uname">${d.name||'—'}</div>
          <div class="admin-uemail">${d.email}</div>
          <div class="au-actions">
            <span class="role-badge rb-${d.role}">${roleLabel[d.role]||d.role}</span>
            <button class="au-reset-btn" onclick="adminResetPassword('${esc}')">🔑 รีเซ็ต</button>
            <button class="au-del-btn" onclick="adminDeleteUser('${uid}','${escName}')">🗑️ ลบ</button>
          </div>
        </div>
      </div>`;
    }).join('');
  } catch(e){
    listEl.innerHTML='<div style="text-align:center;padding:20px;color:var(--red);font-size:13px;">โหลดข้อมูลล้มเหลว</div>';
  }
}
