// WIBWUB HR — scraper for #รายงานการผลิตbyฝ่ายผลิต (free-text production reports)
// Usage (Claude in Chrome, on https://discord.com/channels/1331888082802315295/1392059303669792889):
//   1) window.__PRP = {sinceTs:'2026-09-01'};   // re-read every message posted on/after this date (edits happen in place)
//   2) paste this file -> 'started' ; 3) poll window.__pj until {done:true}
//   4) window.__prExport(0,40), (40,80) ... -> one JSON object per line {id,ts,by,text}
(() => {
  const P = window.__PRP || { sinceTs: new Date(Date.now() - 45 * 864e5).toISOString().slice(0, 10) };
  window.__pj = { done: false, started: Date.now(), sinceTs: P.sinceTs };
  let sleep = ms => new Promise(r => setTimeout(r, ms));
  try {
    const w = new Worker(URL.createObjectURL(new Blob(['onmessage=e=>setTimeout(()=>postMessage(e.data.id),e.data.ms)'], { type: 'text/javascript' })));
    const W = {}; let q = 0; w.onmessage = e => { const f = W[e.data]; delete W[e.data]; if (f) f(); };
    sleep = ms => new Promise(r => { const id = ++q; W[id] = r; w.postMessage({ id, ms }); });
  } catch (e) {}
  const store = window.__pr = {};
  // message body only (no header/timestamps/"(edited)"); author comes from the header, or from the previous message in a group
  const body = li => { const c = li.querySelector('[id^="message-content-"]'); if (!c) return ''; const x = c.cloneNode(true);
    x.querySelectorAll('[class*="timestamp"],[class*="edited"]').forEach(n => n.remove()); return x.innerText.replace(/\u00a0/g, ' ').trim(); };
  const grab = () => { let a = 0; for (const li of document.querySelectorAll('li[id^="chat-messages-"]')) { const t = li.querySelector('time');
      const u = li.querySelector('[id^="message-username-"] [class*="username"]'); const prev = store[li.id]; if (!prev) a++;
      store[li.id] = { ts: t ? t.getAttribute('datetime') : (prev && prev.ts) || '', author: u ? u.textContent.trim() : (prev && prev.author) || '', text: body(li) }; } return a; };
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
      grab(); window.__pj.reachedStart = reached();
    } catch (e) { window.__pj.err = String(e); }
    // fill authors of grouped messages (no header) from the closest earlier message
    const E = Object.entries(store).sort((a, b) => a[1].ts.localeCompare(b[1].ts)); let last = '';
    E.forEach(([k, v]) => { if (v.author) last = v.author; else v.author = last; });
    window.__prLines = E.filter(([k, v]) => v.ts && v.ts.slice(0, 10) >= P.sinceTs && v.text)
      .map(([k, v]) => JSON.stringify({ id: k.replace('chat-messages-', ''), ts: v.ts.slice(0, 16), by: v.author, text: v.text.slice(0, 1500) }));
    window.__pj.count = window.__prLines.length; window.__pj.noName = E.filter(([k, v]) => !v.author).length;
    window.__pj.secs = Math.round((Date.now() - window.__pj.started) / 1000); window.__pj.done = true;
  })();
  window.__prExport = (a = 0, b = 40) => (window.__prLines || []).slice(a, b).join('\n');
  return 'started';
})();
