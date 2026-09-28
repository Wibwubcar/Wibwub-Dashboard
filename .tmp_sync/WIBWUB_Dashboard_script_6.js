
// ════════════════════════════════════════
// FIREBASE CONFIG
// กรอก config จาก Firebase Console → Project Settings → Your apps
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

// Secondary Firebase app — admin สร้าง user โดยไม่ logout ตัวเอง
let _secApp = null, _secAuth = null;
function getSecAuth(){
  if(!_secApp){ _secApp=firebase.initializeApp(firebaseConfig,'secondary'); _secAuth=_secApp.auth(); }
  return _secAuth;
}

window._userRole = null;
window._userName = null;

const ROLE_LABEL = {admin:'Admin',head_marketing:'Head Marketing',kol_team:'KOL Team',content_team:'Content Team',hr_team:'HR Team',procurement:'จัดซื้อ'};
let ROLE_SECTIONS_MAP = {
  admin:          ['overview','sales','shopee','tiktok','lazada','products','ads','social','affiliate','hr','projects','procurement','admin'],
  head_marketing: ['overview','sales','shopee','tiktok','lazada','products','ads','social','affiliate','procurement'],
  kol_team:       ['affiliate'],
  content_team:   ['social'],
  hr_team:        ['hr'],
  procurement:    ['procurement'],
};
const ROLE_DEFAULT_PAGE = {admin:'overview',head_marketing:'overview',kol_team:'affiliate',content_team:'social',hr_team:'hr',procurement:'procurement'};

// ── Auth state ──
auth.onAuthStateChanged(async user => {
  if(user){
    let role=null, name=user.email;
    try{
      const snap=await fsGet('users', user.uid);
      if(snap.exists){ role=snap.data().role||null; name=snap.data().name||name; }
    } catch(e){ console.warn('Firestore',e); }
    // ถ้าไม่มี Firestore record = บัญชีถูกลบ → force logout
    if(!role){
      await auth.signOut();
      const errEl=document.getElementById('loginError');
      if(errEl){ errEl.textContent='บัญชีนี้ถูกลบออกจากระบบแล้ว กรุณาติดต่อ Admin'; errEl.style.display='block'; }
      return;
    }
    window._userRole=role; window._userName=name;
    await loadRolePermissions(); // โหลด custom permissions จาก Firestore ก่อน apply nav
    document.getElementById('loginOverlay').style.display='none';
    document.getElementById('sbUserName').textContent=name;
    document.getElementById('sbUserRole').textContent=ROLE_LABEL[role]||role;
    document.getElementById('sbUserAv').textContent=(name||'W')[0].toUpperCase();
    document.getElementById('sbLogout').style.display='';
    applyRoleNav(role);
    // Send token to HR iframe — fixes blank page when Firebase nested-iframe auth is blocked
    _sendHRToken(user, role, name);
  } else {
    window._userRole=null;
    document.getElementById('loginOverlay').style.display='flex';
    document.getElementById('sbLogout').style.display='none';
    document.getElementById('sbUserRole').textContent='กำลังโหลด...';
    resetNavVisibility();
  }
});

function applyRoleNav(role){
  resetNavVisibility();
  const allowed=ROLE_SECTIONS_MAP[role]||ROLE_SECTIONS_MAP['head_marketing'];

  // Show/hide each nav-item by data-sec
  document.querySelectorAll('#sideNav .nav-item').forEach(el=>{
    const sec=el.dataset.sec;
    el.style.display=allowed.includes(sec)?'':'none';
  });

  // Show/hide admin nav group header
  const adminSec=document.getElementById('ns-admin');
  const adminItem=document.getElementById('nav-admin-item');
  if(role==='admin'){ adminSec.style.display=''; adminItem.style.display=''; }
  else { adminSec.style.display='none'; adminItem.style.display='none'; }

  // Hide nav section headers that have no visible items
  [['ns-overview',['overview']],['ns-sales',['sales','shopee','tiktok','lazada']],['ns-marketing',['products','ads','social','affiliate']],['ns-team',['hr','projects','procurement']]].forEach(([headId,secs])=>{
    const hasVisible=secs.some(s=>allowed.includes(s));
    const headEl=document.getElementById(headId);
    if(headEl) headEl.style.display=hasVisible?'':'none';
  });

  // Navigate to default page for this role
  const defaultPage=ROLE_DEFAULT_PAGE[role]||'overview';
  const targetNavEl=document.querySelector(`[data-sec="${defaultPage}"]`);
  if(targetNavEl) go(defaultPage, targetNavEl);
}

function resetNavVisibility(){
  document.querySelectorAll('#sideNav .nav-item').forEach(el=>el.style.display='');
  ['ns-overview','ns-sales','ns-marketing','ns-team'].forEach(id=>{ const el=document.getElementById(id); if(el) el.style.display=''; });
  const adminSec=document.getElementById('ns-admin');
  const adminItem=document.getElementById('nav-admin-item');
  if(adminSec) adminSec.style.display='none';
  if(adminItem) adminItem.style.display='none';
}

// ── Login / Logout ──
function doLogin(){
  const email=document.getElementById('loginEmail').value.trim();
  const pass=document.getElementById('loginPass').value;
  const errEl=document.getElementById('loginErr');
  const btn=document.getElementById('loginBtn');
  errEl.textContent='';
  if(!email||!pass){ errEl.textContent='กรุณากรอกอีเมลและรหัสผ่าน'; return; }
  btn.textContent='กำลังเข้าสู่ระบบ...'; btn.disabled=true;
  auth.signInWithEmailAndPassword(email,pass)
    .catch(err=>{
      const msgs={'auth/user-not-found':'ไม่พบบัญชีนี้','auth/wrong-password':'รหัสผ่านไม่ถูกต้อง','auth/invalid-email':'รูปแบบอีเมลไม่ถูกต้อง','auth/invalid-credential':'อีเมลหรือรหัสผ่านไม่ถูกต้อง','auth/too-many-requests':'พยายามเข้าสู่ระบบมากเกินไป','auth/network-request-failed':'เชื่อมต่อเครือข่ายล้มเหลว'};
      errEl.textContent=msgs[err.code]||('เกิดข้อผิดพลาด: '+err.message);
    })
    .finally(()=>{ btn.textContent='เข้าสู่ระบบ'; btn.disabled=false; });
}
document.getElementById('loginPass').addEventListener('keydown',e=>{ if(e.key==='Enter') doLogin(); });
document.getElementById('loginEmail').addEventListener('keydown',e=>{ if(e.key==='Enter') document.getElementById('loginPass').focus(); });

function doLogout(){
  if(!confirm('ออกจากระบบ?')) return;
  auth.signOut();
}

// ════════════════════════════════════════
// ADMIN: Create + List Users
// ════════════════════════════════════════
async function adminCreateUser(){
  const email=document.getElementById('newEmail').value.trim();
  const pass=document.getElementById('newPass').value;
  const name=document.getElementById('newName').value.trim();
  const role=document.getElementById('newRole').value;
  const msgEl=document.getElementById('createMsg');
  msgEl.className='af2-msg'; msgEl.textContent='';
  if(!email||!pass||!name){ msgEl.className='af2-msg err'; msgEl.textContent='กรุณากรอกให้ครบทุกช่อง'; return; }
  if(pass.length<6){ msgEl.className='af2-msg err'; msgEl.textContent='รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'; return; }
  msgEl.textContent='กำลังสร้าง...';
  try{
    const secAuth=getSecAuth();
    const cred=await secAuth.createUserWithEmailAndPassword(email,pass);
    await fsSet('users', cred.user.uid, { email, name, role, createdAt: new Date() });
    await secAuth.signOut();
    msgEl.className='af2-msg ok'; msgEl.textContent='✓ สร้างบัญชี '+email+' สำเร็จ';
    document.getElementById('newEmail').value=''; document.getElementById('newPass').value=''; document.getElementById('newName').value='';
    loadAdminUsers();
  } catch(err){
    const msgs={'auth/email-already-in-use':'อีเมลนี้มีผู้ใช้แล้ว','auth/invalid-email':'รูปแบบอีเมลไม่ถูกต้อง','auth/weak-password':'รหัสผ่านไม่ปลอดภัยพอ'};
    msgEl.className='af2-msg err'; msgEl.textContent=msgs[err.code]||err.message;
  }
}

// ── เปลี่ยน Password ตัวเอง ──
function showChangePwdModal(){
  // reuse wib-overlay modal system
  document.getElementById('wib-modal-title').textContent='🔑 เปลี่ยน Password';
  document.getElementById('wib-modal-body').innerHTML=`
    <div style="display:flex;flex-direction:column;gap:12px;">
      <div>
        <label style="font-size:12px;font-weight:600;color:#6B7280;display:block;margin-bottom:4px;">Password ปัจจุบัน</label>
        <input type="password" id="cpOld" placeholder="••••••••" style="width:100%;padding:9px 12px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:13px;outline:none;box-sizing:border-box;">
      </div>
      <div>
        <label style="font-size:12px;font-weight:600;color:#6B7280;display:block;margin-bottom:4px;">Password ใหม่ (อย่างน้อย 6 ตัว)</label>
        <input type="password" id="cpNew" placeholder="••••••••" style="width:100%;padding:9px 12px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:13px;outline:none;box-sizing:border-box;">
      </div>
      <div>
        <label style="font-size:12px;font-weight:600;color:#6B7280;display:block;margin-bottom:4px;">ยืนยัน Password ใหม่</label>
        <input type="password" id="cpConfirm" placeholder="••••••••" style="width:100%;padding:9px 12px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:13px;outline:none;box-sizing:border-box;">
      </div>
      <div id="cpMsg" style="font-size:12px;text-align:center;min-height:16px;"></div>
    </div>`;
  // swap footer button
  const footer=document.querySelector('.wib-modal-footer button:last-child');
  footer.textContent='เปลี่ยน Password';
  footer.onclick=doChangePassword;
  document.getElementById('wib-overlay').style.display='flex';
}
async function doChangePassword(){
  const old=document.getElementById('cpOld').value;
  const nw=document.getElementById('cpNew').value;
  const cf=document.getElementById('cpConfirm').value;
  const msg=document.getElementById('cpMsg');
  if(!old||!nw||!cf){msg.style.color='#dc2626';msg.textContent='กรุณากรอกข้อมูลให้ครบ';return;}
  if(nw.length<6){msg.style.color='#dc2626';msg.textContent='Password ใหม่ต้องมีอย่างน้อย 6 ตัวอักษร';return;}
  if(nw!==cf){msg.style.color='#dc2626';msg.textContent='Password ใหม่ไม่ตรงกัน';return;}
  try{
    const user=auth.currentUser;
    const cred=firebase.auth.EmailAuthProvider.credential(user.email,old);
    await user.reauthenticateWithCredential(cred);
    await user.updatePassword(nw);
    msg.style.color='#16a34a';msg.textContent='เปลี่ยน password สำเร็จ ✓';
    setTimeout(()=>closeWibModal(),1500);
  }catch(e){
    msg.style.color='#dc2626';
    if(e.code==='auth/wrong-password'||e.code==='auth/invalid-credential')msg.textContent='Password ปัจจุบันไม่ถูกต้อง';
    else if(e.code==='auth/weak-password')msg.textContent='Password ใหม่ไม่แข็งแรงพอ';
    else msg.textContent='เกิดข้อผิดพลาด: '+e.message;
  }
}
// ── Admin ลบ User ──
async function adminDeleteUser(uid, name){
  if(!confirm('ลบบัญชี "'+name+'" ออกจากระบบ?\n\nUser จะไม่สามารถ login ได้ทันที')) return;
  try{
    await fsDel('users', uid);
    const card=document.getElementById('ucard-'+uid);
    if(card){ card.style.opacity='0.35'; card.style.pointerEvents='none'; }
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

// ════════════════════════════════════════
// PERMISSIONS MANAGEMENT
// ════════════════════════════════════════
const PERM_ROLES = ['head_marketing','kol_team','content_team','hr_team','procurement'];
const PERM_ROLE_LABELS = {head_marketing:'Head Marketing',kol_team:'KOL Team',content_team:'Content Team',hr_team:'HR Team',procurement:'จัดซื้อ'};
const PERM_SECTIONS = [
  {group:'📊 ภาพรวม',    items:[{id:'overview',label:'ภาพรวมธุรกิจ'}]},
  {group:'💰 ยอดขาย',    items:[{id:'sales',label:'ยอดขายรวม'},{id:'shopee',label:'🧡 Shopee'},{id:'tiktok',label:'🎵 TikTok'},{id:'lazada',label:'💙 Lazada'}]},
  {group:'📣 การตลาด',   items:[{id:'products',label:'🏆 Top สินค้า'},{id:'ads',label:'📢 Ads'},{id:'social',label:'Social Media'},{id:'affiliate',label:'🤝 Affiliate'}]},
  {group:'👥 ทีม',       items:[{id:'hr',label:'HR & พนักงาน'},{id:'projects',label:'Projects & Tasks'},{id:'procurement',label:'📦 Forecast / จัดซื้อ'}]},
];

async function loadRolePermissions(){
  try{
    const snap=await fsGet('settings', 'rolePermissions');
    if(snap.exists){
      const data=snap.data();
      PERM_ROLES.forEach(r=>{ if(data[r]&&Array.isArray(data[r])) ROLE_SECTIONS_MAP[r]=data[r]; });
    }
  }catch(e){ console.warn('loadRolePermissions:',e); }
}

function renderPermissionsMatrix(){
  const el=document.getElementById('permsMatrix');
  if(!el) return;
  let html='<div style="overflow-x:auto"><table class="perm-tbl"><thead><tr><th>Section</th>';
  PERM_ROLES.forEach(r=>html+=`<th><span class="role-badge rb-${r}" style="font-size:11px">${PERM_ROLE_LABELS[r]}</span></th>`);
  html+='<th>Admin</th></tr></thead><tbody>';
  PERM_SECTIONS.forEach(grp=>{
    html+=`<tr class="perm-grp"><td colspan="${PERM_ROLES.length+2}">${grp.group}</td></tr>`;
    grp.items.forEach(sec=>{
      html+=`<tr><td style="padding-left:20px">${sec.label}</td>`;
      PERM_ROLES.forEach(r=>{
        const checked=(ROLE_SECTIONS_MAP[r]||[]).includes(sec.id)?'checked':'';
        html+=`<td><input type="checkbox" id="perm-${r}-${sec.id}" ${checked}></td>`;
      });
      html+=`<td><span class="perm-lock">✓ เสมอ</span></td></tr>`;
    });
  });
  // Admin row (always locked)
  html+=`<tr class="perm-grp"><td colspan="${PERM_ROLES.length+2}">⚙️ Admin</td></tr>`;
  html+=`<tr><td style="padding-left:20px">⚙️ จัดการผู้ใช้ (Admin)</td>`;
  PERM_ROLES.forEach(()=>html+=`<td><span class="perm-lock">Admin only</span></td>`);
  html+=`<td><span class="perm-lock">✓ เสมอ</span></td></tr>`;
  html+='</tbody></table></div>';
  el.innerHTML=html;
}

async function saveRolePermissions(){
  const msgEl=document.getElementById('permsMsg');
  msgEl.textContent='กำลังบันทึก...'; msgEl.style.color='#6b7280';
  const perms={};
  PERM_ROLES.forEach(role=>{
    perms[role]=[];
    PERM_SECTIONS.forEach(grp=>grp.items.forEach(sec=>{
      const cb=document.getElementById(`perm-${role}-${sec.id}`);
      if(cb&&cb.checked) perms[role].push(sec.id);
    }));
  });
  try{
    await fsSet('settings', 'rolePermissions', perms);
    PERM_ROLES.forEach(r=>ROLE_SECTIONS_MAP[r]=perms[r]);
    msgEl.textContent='✓ บันทึกสิทธิ์สำเร็จ'; msgEl.style.color='#16a34a';
    // Re-apply nav for the current admin user (admin nav stays the same)
    applyRoleNav(window._userRole);
    setTimeout(()=>{ msgEl.textContent=''; },3000);
  }catch(e){
    msgEl.textContent='เกิดข้อผิดพลาด: '+e.message; msgEl.style.color='#dc2626';
  }
}

async function loadAdminUsers(){
  if(window._userRole!=='admin') return;
  const listEl=document.getElementById('adminUserList');
  if(!listEl) return;
  listEl.innerHTML='<div style="padding:24px;text-align:center;color:var(--muted)">กำลังโหลด...</div>';
  try{
    const docs=await fsList('users');
    docs.sort((a,b)=>{ const da=a.data().createdAt, db2=b.data().createdAt; return ((da instanceof Date?da:new Date(0))-(db2 instanceof Date?db2:new Date(0))); });
    if(!docs.length){ listEl.innerHTML='<div style="padding:24px;text-align:center;color:var(--muted)">ยังไม่มีผู้ใช้ในระบบ</div>'; return; }
    listEl.innerHTML=docs.map(doc=>{
      const d=doc.data();
      const ini=((d.name||d.email)||'?')[0].toUpperCase();
      const esc=d.email.replace(/'/g,"\\'");
      const escName=(d.name||d.email).replace(/'/g,"\\'");
      const uid=doc.id;
      return`<div class="au-row" id="ucard-${uid}">
        <div class="au-av">${ini}</div>
        <div class="au-info">
          <div class="au-name">${d.name||'—'}</div>
          <div class="au-email">${d.email}</div>
          <div style="display:flex;align-items:center;gap:8px;margin-top:4px;flex-wrap:wrap;">
            <span class="role-badge rb-${d.role}">${ROLE_LABEL[d.role]||d.role}</span>
            <button class="au-reset-btn" onclick="adminResetPassword('${esc}')">🔑 รีเซ็ต password</button>
            <button class="au-del-btn" onclick="adminDeleteUser('${uid}','${escName}')">🗑️ ลบบัญชี</button>
          </div>
        </div>
      </div>`;
    }).join('');
  } catch(e){
    listEl.innerHTML='<div style="padding:24px;text-align:center;color:var(--red)">โหลดข้อมูลล้มเหลว</div>';
  }
}
