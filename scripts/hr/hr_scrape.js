// WIBWUB HR — Discord scraper for #บันทึกเข้างาน / #บันทึกออกงาน
// Usage (Claude in Chrome, javascript_tool, on the channel page):
//   1) set params:  window.__HR = {key:'__ci', cur:'ตุลาคม', prev:'กันยายน', since:7};
//      key: '__ci' check-in / '__co' check-out. cur: Thai month name of the target month.
//      prev: Thai name of the month before it. since: first day to collect (1 = whole month).
//   2) paste this whole file -> starts a background job, returns 'started'
//   3) poll:   window.__job            -> {done:true,...} when finished
//   4) export: window.__hrExport(0,80) -> lines "day|HH:MM|name|LOC|dist" (slice start,end)
(() => {
  const P = window.__HR; if (!P) return 'set window.__HR first';
  window.__job = { done: false, started: Date.now() };
  // Chrome throttles timers to ~1/min when the window is hidden/minimised; a Worker's timers are not throttled
  let sleep = ms => new Promise(r => setTimeout(r, ms));
  try {
    const w = new Worker(URL.createObjectURL(new Blob(['onmessage=e=>setTimeout(()=>postMessage(e.data.id),e.data.ms)'], { type: 'text/javascript' })));
    const waiting = {}; let seq = 0; w.onmessage = e => { const f = waiting[e.data]; delete waiting[e.data]; if (f) f(); };
    sleep = ms => new Promise(r => { const id = ++seq; waiting[id] = r; w.postMessage({ id, ms }); });
    window.__job.timer = 'worker';
  } catch (e) { window.__job.timer = 'setTimeout'; }
  const store = window[P.key] = {};
  const parse = li => {
    const t = li.innerText;
    const m = t.match(/\n([^\n]+?) (เข้างาน|ออกงาน) \(([^)]*)\)\n/);
    const tm = t.match(/เวลา\n(\d+) (\S+) (\d{4})(?: เวลา)? (\d{1,2}:\d{2})/);
    if (!m || !tm) return { raw: t.slice(0, 200) };
    const dist = t.match(/ระยะห่าง:\s*([\d,\.]+)/);
    return { name: m[1].trim(), loc: m[3], d: +tm[1], mon: tm[2], time: tm[4], dist: dist ? dist[1] : '' };
  };
  const grab = () => { let a = 0; for (const li of document.querySelectorAll('li[id^="chat-messages-"]')) { if (!store[li.id] || !store[li.id].mon) { if (!store[li.id]) a++; store[li.id] = parse(li); } } return a; };
  const sc = () => { let e = document.querySelector('li[id^="chat-messages-"]'); while (e) { const cs = getComputedStyle(e); if (e.scrollHeight > e.clientHeight + 10 && /auto|scroll/.test(cs.overflowY)) return e; e = e.parentElement; } };
  const reachedStart = () => Object.values(store).some(v => v.mon === P.prev || (v.mon === P.cur && v.d < P.since));
  (async () => {
    try {
      // 0) wait for Discord to render the channel (a hidden/just-opened tab can take a while)
      for (let i = 0; i < 60 && !(document.querySelector('li[id^="chat-messages-"]') && sc()); i++) await sleep(500);
      if (!sc()) throw new Error('channel did not load (no messages after 30 s) — run this channel again');
      // 1) make sure we start at the newest messages
      const jump = [...document.querySelectorAll('button,div[role="button"]')].find(b => /Jump to Present|ข้ามไปยังปัจจุบัน/i.test(b.textContent || ''));
      if (jump) { jump.click(); await sleep(2500); }
      let st = 0;
      for (let i = 0; i < 40; i++) { const a = grab(); const s = sc(); const atEnd = s.scrollTop + s.clientHeight >= s.scrollHeight - 3; if (atEnd || !a) { if (++st > 3) break; } else st = 0; s.scrollTop = s.scrollHeight; await sleep(500); }
      st = 0; // 2) scroll back until a message older than `since`
      for (let i = 0; i < 1500; i++) {
        const a = grab(); if (reachedStart()) break; const s = sc();
        if (s.scrollTop <= 2) {            // at the top: nudge so Discord fires a scroll event and loads older messages
          if (!a && ++st > 10) break;
          // Discord only loads older messages on real wheel input at the top
          for (let k = 0; k < 3; k++) { s.dispatchEvent(new WheelEvent('wheel', { deltaY: -800, deltaMode: 0, bubbles: true, cancelable: true })); s.scrollTop = 0; s.dispatchEvent(new Event('scroll', { bubbles: true })); await sleep(150); }
        } else { st = 0; s.scrollTop = Math.max(0, s.scrollTop - 1500); }
        await sleep(650);
      }
      grab();
      window.__job.reachedStart = reachedStart();
    } catch (e) { window.__job.err = String(e); }
    const vals = Object.values(store);
    window.__job.unparsed = vals.filter(v => !v.mon).length;
    window.__hrLines = Object.entries(store).filter(([k, v]) => v.mon === P.cur && v.d >= P.since)
      .sort((a, b) => (a[0].length - b[0].length) || a[0].localeCompare(b[0]))
      .map(([k, v]) => [v.d, v.time, v.name, v.loc === 'WAREHOUSE' ? 'W' : v.loc, v.dist].join('|'));
    window.__job.count = window.__hrLines.length;
    window.__job.secs = Math.round((Date.now() - window.__job.started) / 1000);
    window.__job.done = true;
  })();
  window.__hrExport = (a = 0, b = 100) => (window.__hrLines || []).slice(a, b).join('\n');
  return 'started';
})();
