// WIBWUB ads daily — ดักจับ request จริงที่หน้าเว็บยิง (วางใน javascript_tool หลัง navigate แล้วค่อยกด/รีเฟรชให้หน้าโหลดข้อมูล)
(function(){ if (window.__adsHooked) return 'already';
  window.__adsHooked=true; window.__cap=[]; const RX=/key-metrics|get_time_graph|us_overview_day_trend|post_overview_stat/;
  const oo=XMLHttpRequest.prototype.open, os=XMLHttpRequest.prototype.send, sh=XMLHttpRequest.prototype.setRequestHeader;
  XMLHttpRequest.prototype.open=function(m,u){this.__u=String(u);this.__m=m;this.__h={};return oo.apply(this,arguments)};
  XMLHttpRequest.prototype.setRequestHeader=function(k,v){if(this.__h)this.__h[k]=v;return sh.apply(this,arguments)};
  XMLHttpRequest.prototype.send=function(b){ if(RX.test(this.__u)) window.__cap.push({m:this.__m,u:this.__u,b:b?String(b):null,h:this.__h}); return os.apply(this,arguments)};
  const of=window.fetch; window.fetch=function(i,o){
    const isReq=(typeof Request!=='undefined') && i instanceof Request; const u=typeof i==='string'?i:(i&&i.url)||'';
    if(RX.test(u)){ const rec={m:(o&&o.method)||(isReq&&i.method)||'GET',u:String(u),b:o&&o.body?String(o.body):null,h:{}};
      let h=(o&&o.headers)||(isReq&&i.headers); if(h instanceof Headers){ h.forEach((v,k)=>rec.h[k]=v); } else if(h){ rec.h={...h}; }
      if(!rec.b && isReq){ try{ i.clone().text().then(t=>{ rec.b=t||null; }); }catch(e){} }
      window.__cap.push(rec); }
    return of.apply(this,arguments)};
  return 'hooked';
})();
