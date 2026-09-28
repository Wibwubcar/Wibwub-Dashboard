
// ── SERVICE WORKER: auto-update ──
if('serviceWorker' in navigator){
  navigator.serviceWorker.register('/Wibwub-Dashboard/sw.js').then(reg=>{
    // ตรวจสอบเวอร์ชั่นใหม่ทุกครั้งที่เปิด app
    reg.update();
    reg.addEventListener('updatefound',()=>{
      const sw=reg.installing;
      const wasControlled=!!navigator.serviceWorker.controller;
      sw.addEventListener('statechange',()=>{
        // ถ้ามีเวอร์ชั่นใหม่ (ไม่ใช่ install ครั้งแรก) → reload อัตโนมัติ
        if(sw.state==='activated' && wasControlled){
          window.location.reload();
        }
      });
    });
  });
}
