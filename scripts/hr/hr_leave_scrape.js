// WIBWUB HR — scraper for #การลาที่รออนุมัติ (leave requests posted/edited by WibWubBot)
// Usage (Claude in Chrome, on https://discord.com/channels/1331888082802315295/1331942184739667979):
//   1) window.__LVP = {sinceTs:'2026-09-01'};   // re-read every message posted on/after this date (status edits happen in place)
//   2) paste this file -> 'started' ; 3) poll window.__lj until {done:true}
//   4) window.__lvExport(0,40), (40,80) ... -> lines "msgId|postedAt|status|full name|leave type|leave date|reason|considered at"
(() => {
  const P = window.__LVP || { sinceTs: new Date(Date.now() - 45 * 864e5).toISOString().slice(0, 10) };
  window.__lj = { done: false, started: Date.now(), sinceTs: P.sinceTs };
  let sleep = ms => new Promise(r => setTimeout(r, ms));
  try {
    const w = new Worker(URL.createObjectURL(new Blob(['onmessage=e=>setTimeout(()=>postMessage(e.data.id),e.data.ms)'], { type: 'text/javascript' })));
    const W = {}; let q = 0; w.onmessage = e => { const f = W[e.data]; delete W[e.data]; if (f) f(); };
    sleep = ms => new Promise(r => { const id = ++q; W[id] = r; w.postMessage({ id, ms }); });
  } catch (e) {}
  const store = window.__lv = {};
  const grab = () => { let a = 0; for (const li of document.querySelectorAll('li[id^="chat-messages-"]')) { const t = li.querySelector('time');
    const prev = store[li.id]; if (!prev) a++; store[li.id] = { ts: t ? t.getAttribute('datetime') : (prev && prev.ts) || '', text: li.innerText }; } return a; };
  const sc = () => { let e = document.querySelector('li[id^="chat-messages-"]'); while (e) { const cs = getComputedStyle(e); if (e.scrollHeight > e.clientHeight + 10 && /auto|scroll/.test(cs.overflowY)) return e; e = e.parentElement; } };
  const reached = () => Object.values(store).some(v => v.ts && v.ts < P.sinceTs);
  (async () => {
    try {
      for (let i = 0; i < 60 && !(document.querySelector('li[id^="chat-messages-"]') && sc()); i++) await sleep(500);
      if (!sc()) throw new Error('channel did not load (no messages after 30 s) — run again');
      const jump = [...document.querySelectorAll('button,div[role="button"]')].find(b => /Jump to Present|ข้ามไปยังปัจจุบัน/i.test(b.textContent || ''));
      if (jump) { jump.click(); await sleep(2500); }
      let st = 0;
      for (let i = 0; i < 40; i++) { const a = grab(); const s = sc(); if (s.scrollTop + s.clientHeight >= s.scrollHeight - 3 || !a) { if (++st > 3) break; } else st = 0; s.scrollTop = s.scrollHeight; await sleep(500); }
      st = 0;
      for (let i = 0; i < 800; i++) {
        const a = grab(); if (reached()) break; const s = sc();
        if (s.scrollTop <= 2) { if (!a && ++st > 12) break;
          for (let k = 0; k < 3; k++) { s.dispatchEvent(new WheelEvent('wheel', { deltaY: -800, bubbles: true, cancelable: true })); s.scrollTop = 0; s.dispatchEvent(new Event('scroll', { bubbles: true })); await sleep(150); }
        } else { st = 0; s.scrollTop = Math.max(0, s.scrollTop - 1500); }
        await sleep(650);
      }
      grab(); window.__lj.reachedStart = reached();
    } catch (e) { window.__lj.err = String(e); }
    const f = (t, k) => { const m = t.match(new RegExp(k + '\\n([^\\n]*)')); return m ? m[1].trim().replace(/\|/g, '/') : ''; };
    window.__lvLines = Object.entries(store).filter(([id, v]) => /ชื่อ-นามสกุล/.test(v.text) && v.ts && v.ts.slice(0, 10) >= P.sinceTs)
      .sort((a, b) => a[1].ts.localeCompare(b[1].ts))
      .map(([id, v]) => { const t = v.text; const st = (t.match(/(อนุมัติแล้ว|ไม่อนุมัติ|รออนุมัติ|ยกเลิก)/) || [''])[0];
        return [id.replace('chat-messages-', ''), v.ts.slice(0, 16), st, f(t, 'ชื่อ-นามสกุล'), f(t, 'ประเภทการลา'), f(t, 'วันที่ลา'), f(t, 'เหตุผล').slice(0, 80), f(t, 'เวลาพิจารณา')].join('|'); });
    window.__lj.count = window.__lvLines.length; window.__lj.secs = Math.round((Date.now() - window.__lj.started) / 1000); window.__lj.done = true;
  })();
  window.__lvExport = (a = 0, b = 40) => (window.__lvLines || []).slice(a, b).join('\n');
  return 'started';
})();
