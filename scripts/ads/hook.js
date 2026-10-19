// WIBWUB ads daily — ดักจับ request จริงที่หน้าเว็บยิง (วางใน javascript_tool หลัง navigate แล้วค่อยกด/รีเฟรชให้หน้าโหลดข้อมูล)
// หมายเหตุ: ads.tiktok.com เขียนทับ window.fetch ของตัวเองทับ hook ตอน bootstrap เสร็จ (ทำให้ __cap ว่างตลอด)
// hook นี้จึงคอยเช็คทุก 500ms เป็นเวลา 60 วิ แล้วติดตั้งทับใหม่ถ้าโดนล้าง — วางครั้งเดียวพอ
(function(){
  const RX=/key-metrics|get_time_graph|us_overview_day_trend|post_overview_stat|post_campaign_list_v2/;
  if(!Array.isArray(window.__cap)) window.__cap=[];

  // XHR: prototype ไม่ค่อยโดนเขียนทับ ติดตั้งครั้งเดียว
  if(!XMLHttpRequest.prototype.send.__adsWrap){
    const oo=XMLHttpRequest.prototype.open, os=XMLHttpRequest.prototype.send, sh=XMLHttpRequest.prototype.setRequestHeader;
    XMLHttpRequest.prototype.open=function(m,u){this.__u=String(u);this.__m=m;this.__h={};return oo.apply(this,arguments)};
    XMLHttpRequest.prototype.setRequestHeader=function(k,v){if(this.__h)this.__h[k]=v;return sh.apply(this,arguments)};
    const send=function(b){ if(RX.test(this.__u)) window.__cap.push({m:this.__m,u:this.__u,b:b?String(b):null,h:this.__h}); return os.apply(this,arguments)};
    send.__adsWrap=true; XMLHttpRequest.prototype.send=send;
  }

  // fetch: ห่อ fetch ตัวปัจจุบันเสมอ (ถ้ายังไม่ใช่ของเรา) เพื่อให้ได้ทั้ง hook ของเราและของหน้าเว็บ
  function patchFetch(){
    if(typeof window.fetch!=='function' || window.fetch.__adsWrap) return false;
    const of=window.fetch;
    const wrapped=function(i,o){
      const isReq=(typeof Request!=='undefined') && i instanceof Request; const u=typeof i==='string'?i:(i&&i.url)||'';
      if(RX.test(u)){ const rec={m:(o&&o.method)||(isReq&&i.method)||'GET',u:String(u),b:o&&o.body?String(o.body):null,h:{}};
        let h=(o&&o.headers)||(isReq&&i.headers); if(h instanceof Headers){ h.forEach((v,k)=>rec.h[k]=v); } else if(h){ rec.h={...h}; }
        if(!rec.b && isReq){ try{ i.clone().text().then(t=>{ rec.b=t||null; }); }catch(e){} }
        window.__cap.push(rec); }
      return of.apply(this,arguments)};
    wrapped.__adsWrap=true; window.fetch=wrapped; return true;
  }

  const first=patchFetch();
  // คอยติดตั้งทับใหม่ถ้าหน้าเว็บเขียนทับ (TikTok Ads ทำตอน bootstrap)
  if(!window.__adsGuard){
    let n=0; window.__adsRepatch=0;
    window.__adsGuard=setInterval(function(){
      if(patchFetch()) window.__adsRepatch++;
      if(++n>120){ clearInterval(window.__adsGuard); window.__adsGuard=null; }
    },500);
  }
  window.__adsHooked=true;
  return first?'hooked':'already';
})();
