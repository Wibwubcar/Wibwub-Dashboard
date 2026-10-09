// WIBWUB HR — scraper for #การลาที่รออนุมัติ (leave requests posted/edited by WibWubBot)
// Usage (Claude in Chrome, on https://discord.com/channels/1331888082802315295/1331942184739667979):
//   1) window.__LVP = {sinceTs:'2026-09-01'};   // re-read every message posted on/after this date (status edits happen in place)
//   2) paste this file -> 'started' ; 3) poll window.__lj until {done:true}
//   4) window.__lvExport(0,40), (40,80) ... -> lines "msgId|postedAt(UTC)|status|full name|leave type|leave date|reason (all lines, ≤300)|considered at"
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
  // 3 รูปแบบข้อความของ WibWubBot:
  //  A (พ.ค. 2026+): "คำขอลา\n อนุมัติแล้ว" + ชื่อ-นามสกุล/ประเภทการลา/วันที่ลา/เหตุผล/เวลาพิจารณา
  //  B (ก.พ.–เม.ย. 2026): ป้ายสองภาษา "ชื่อ-นามสกุล (Name)" … ยังมีปุ่ม อนุมัติ/ไม่อนุมัติ = ยังไม่ได้พิจารณา (รออนุมัติ)
  //  C (ธ.ค. 2025–เม.ย. 2026): ข้อความที่ถูกแก้เป็น "คำขอได้รับการอนุมัติ (Request Approved)" — เหลือแค่ ID ผู้ร้องขอ ไม่มีประเภท/วันที่ลา
  const buildLeaveLines = (store, sinceTs) => {
    const clean = x => String(x || '').trim().replace(/\|/g, '/').replace(/`/g, "'").replace(/\$\{/g, '$ {');
    const f = (t, k) => { const m = t.match(new RegExp(k + '(?: \\([^)\\n]*\\))?\\n([^\\n]*)')); return m ? clean(m[1]) : ''; };
    const why = t => { const m = t.match(/\nเหตุผล(?: \(Reason\))?\n([\s\S]*?)(?:\nเวลาพิจารณา\n|\nWibWub HR System|\n\d{1,2}\/\d{1,2}\/\d{2}, \d|$)/); if (!m) return '';
      return clean(m[1].split('\n').map(x => x.trim()).filter(x => x && !/^\u200b+$/.test(x)).join(' / ')).slice(0, 300); };
    const rqId = t => (t.match(/ผู้ร้องขอ(?: \(Requester\))?\n<?@?(\d{6,})/) || [])[1] || '';
    const bkk = ts => new Date(Date.parse(ts) + 7 * 3600e3).toISOString();
    const E = Object.entries(store).filter(([id, v]) => v.ts && v.ts.slice(0, 10) >= sinceTs).sort((a, b) => a[1].ts.localeCompare(b[1].ts));
    const names = {}; E.forEach(([id, v]) => { const n = f(v.text, 'ชื่อ-นามสกุล'), r = rqId(v.text); if (n && r && !/^(test|\.|-)$/i.test(n)) names[r] = n; });
    const out = [];
    E.forEach(([id, v]) => { const t = v.text, mid = id.replace('chat-messages-', ''), ts = v.ts.slice(0, 16);
      const dec = (t.match(/Request (Approved|Rejected)/) || [])[1];
      if (dec) { const r = rqId(t), d = bkk(v.ts); const ed = (t.match(/\(edited\)\n(\w+day, \w+ \d+, \d{4} at [\d:]+ [AP]M)/) || [])[1] || '';
        out.push([mid, ts, dec === 'Approved' ? 'อนุมัติแล้ว' : 'ไม่อนุมัติ', names[r] || ('ID ' + r), 'ไม่ทราบประเภท', `${+d.slice(8, 10)}/${+d.slice(5, 7)}/${d.slice(0, 4)}`,
          'ข้อความเก่า: ระบบแก้ข้อความหลังพิจารณา ไม่มีประเภท/วันที่ลา/เหตุผล (วันที่ = วันที่ยื่น)', clean(ed)].join('|')); return; }
      const n = f(t, 'ชื่อ-นามสกุล'); if (!n || /^(test|\.|-)$/i.test(n)) return;
      const bilingual = /ชื่อ-นามสกุล \(Name\)/.test(t);
      const st = bilingual ? 'ค้างในระบบเก่า' : ((t.match(/คำขอลา\n\s*(อนุมัติแล้ว|ไม่อนุมัติ|รออนุมัติ|ยกเลิก)/) || t.match(/(อนุมัติแล้ว|ไม่อนุมัติ|รออนุมัติ|ยกเลิก)/) || [''])[1] || 'รออนุมัติ');
      out.push([mid, ts, st || 'รออนุมัติ', n, f(t, 'ประเภทการลา'), f(t, 'วันที่ลา'), why(t), f(t, 'เวลาพิจารณา')].join('|')); });
    return out;
  };
  window.__lvBuild = buildLeaveLines;
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
    window.__lvLines = buildLeaveLines(store, P.sinceTs);
    window.__lj.count = window.__lvLines.length; window.__lj.secs = Math.round((Date.now() - window.__lj.started) / 1000); window.__lj.done = true;
  })();
  window.__lvExport = (a = 0, b = 40) => (window.__lvLines || []).slice(a, b).join('\n');
  return 'started';
})();
