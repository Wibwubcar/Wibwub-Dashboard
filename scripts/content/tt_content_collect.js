// WIBWUB — เก็บตัวเลขคลิป TikTok จากหน้า "วิเคราะห์" รายคลิป
// หน้า: https://www.tiktok.com/tiktokstudio/analytics/<videoId>?qa_enter_from=analytics
//
// ใช้: วางไฟล์นี้ใน javascript_tool หลัง navigate + รอโหลด จะคืน JSON บรรทัดเดียว
//
// ⚠️ กับดักที่เสียเวลาไปเยอะตอนทำครั้งแรก (22 ต.ค. 69) — อย่าทำซ้ำ:
// 1. ค่า "5 วินาทีแรก" ไม่มีใน API และไม่มีใน DOM ตอนโหลดหน้า
//    มันอยู่ในแถบเลื่อนใต้กราฟ ซึ่งผูกกับ <video> ของหน้า
//    วิธีที่ใช้ได้คือ **ตั้ง video.currentTime = 5** แล้วป้ายจะเปลี่ยนเป็น "0:05 (22%)" เอง
//    - ลาก/คลิก slider ด้วยพิกัดพิกเซล: ไม่ขยับ
//    - hover บนกราฟ: ไม่ขยับ
//    - อ่าน pixel จาก canvas แล้วคำนวณเอง: ได้ 23.9% ขณะที่ของจริง 22% (เพี้ยน ~2 จุด) ห้ามใช้
// 2. endpoint /tiktok/v1/analytics/insights/ ยิงซ้ำได้แต่คืน data ว่าง (ขาด header บางตัว)
//    อย่าเสียเวลาไล่ ใช้ DOM อย่างเดียว
// 3. ยอดวิวเกิน ~100K หน้าเว็บย่อเป็น "232K" ไม่มีเลขเต็มที่ไหนเลย
//    (tooltip/attribute/หน้ารายการ ย่อหมด · คำนวณจากเวลาเล่นรวม ÷ เวลาดูเฉลี่ย เพี้ยน 23%)
//    ตกลงกับผู้ใช้ 22 ต.ค. 69 ว่าให้แปลงเป็นเลขเต็ม (232K -> 232000)
(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const T0 = document.body.innerText;

  // กล่องที่มีแถบเลื่อน retention — จับจากข้อความ "(100%)" หรือ "(nn%)" ที่สั้น ๆ
  const findHost = () => [...document.querySelectorAll('div')]
    .find(d => /\(\d+%\)/.test(d.innerText || '') && (d.innerText || '').length < 60);

  let host = findHost();
  for (let i = 0; i < 10 && !host; i++) { await sleep(1000); host = findHost(); }
  if (!host) return JSON.stringify({ ok: false, err: 'ไม่พบแถบ retention — หน้ายังโหลดไม่เสร็จ' });

  const v = host.querySelector('video');
  if (!v || !v.duration) return JSON.stringify({ ok: false, err: 'ไม่พบ video หรือยังไม่รู้ความยาว' });

  // ── ค่า 5 วินาทีแรก ─────────────────────────────────────────────
  v.currentTime = 5;
  await sleep(2000);
  const host2 = findHost();
  const k5 = (host2.innerText.match(/\((\d+)%\)/) || [])[1];

  // ── ตัวเลขหัวโพสต์: วิว / ถูกใจ / คอมเมนต์ / แชร์ / บันทึก ──────
  const after = (T0.match(/โพสต์เมื่อ\s*[\d\/]+\s*([\s\S]{0,60})/) || [])[1] || '';
  const head = after.split('\n').map(s => s.trim()).filter(Boolean).slice(0, 5);
  // "232K" / "1.2M" -> เลขเต็ม (ปัดจากแพลตฟอร์ม ไม่ใช่เลขจริง)
  const num = s => {
    const t = String(s).replace(/,/g, '').trim();
    const m = t.match(/^([\d.]+)([KMB])$/i);
    if (m) return Math.round(parseFloat(m[1]) * { K: 1e3, M: 1e6, B: 1e9 }[m[2].toUpperCase()]);
    return parseFloat(t);
  };
  const approx = head.some(s => /[KMB]$/i.test(String(s).trim()));

  const grab = (re) => { const m = T0.match(re); return m ? m[1] : null; };
  const capLine = (T0.split('\n').find(s => /#/.test(s)) || '').trim();

  return JSON.stringify({
    ok: k5 != null && head.length === 5,
    video_id: (location.pathname.match(/analytics\/(\d+)/) || [])[1],
    posted: grab(/โพสต์เมื่อ\s*([\d\/]+)/),         // d/m/yyyy ค.ศ.
    len_sec: Math.round(v.duration),                  // -> คอลัมน์ O
    ret5: k5 ? k5 + '%' : null,                       // -> คอลัมน์ K
    avg_watch: grab(/เวลาที่ดูโดยเฉลี่ย\s*([\d.]+)s/), // -> คอลัมน์ N
    views: num(head[0]), likes: num(head[1]), comments: num(head[2]),
    shares: num(head[3]), saves: num(head[4]),        // -> P Q R S T
    views_approx: approx,                             // true = เลขถูกย่อมาจากหน้าเว็บ
    caption: capLine.split('#')[0].trim(),            // -> คอลัมน์ D (เฉพาะแถวใหม่)
    hashtags: ('#' + capLine.split('#').slice(1).join('#')).trim() // -> คอลัมน์ H
  });
})();
