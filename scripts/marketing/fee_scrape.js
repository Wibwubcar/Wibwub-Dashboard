// WIBWUB — อ่านยอดในแผง "รายงานธุรกิจ" ของ TikTok Seller Center
// หน้า: https://seller-th.tiktok.com/finance/transactions (การเงิน > ธุรกรรม)
//       แล้วกด "เพิ่มเติม" ใต้การ์ด "ค่าธรรมเนียมทั้งหมด" ให้แผงด้านขวาเปิดขึ้นมา
//       จากนั้นเลือกช่วงวันที่ให้เป็น "ทั้งเดือน" ที่ต้องการ
//
// ใช้: วางไฟล์นี้ใน javascript_tool แล้วอ่านค่าที่คืนมา (เป็น JSON บรรทัดเดียว)
//
// ทำไมอ่านจาก DOM ไม่ยิง API: endpoint /pay/statement/stat/info ที่หน้าเว็บใช้
// คืน data ว่างเมื่อ replay ด้วยช่วงวันที่อื่น (ทดสอบแล้ว 21 ต.ค. 69) ตัวเลขในแผง
// มาจาก request แบบ batch ที่ประกอบยาก — อ่าน DOM เสถียรกว่าและตรวจสอบด้วยตาได้
//
// กับดัก: ตัวเลขมีเครื่องหมาย ฿ และ , และค่าธรรมเนียมเป็นค่าติดลบ (-)
//         ต้องใช้ค่าสัมบูรณ์ ไม่งั้นอัตราจะติดลบ
(() => {
  const NEED = {
    revenue:     'รายได้ทั้งหมด',
    fee:         'ค่าธรรมเนียมทั้งหมด',
    aff:         'ค่าคอมมิชชั่นแอฟฟิลิเอต',
    aff_ads:     'ค่าคอมมิชชั่นแอฟฟิลิเอตสำหรับโฆษณาร้านค้า',
    commission:  'ค่าคอมมิชชั่น TikTok Shop',
    order_fee:   'ค่าธรรมเนียมคำสั่งซื้อ'
  };
  const num = s => {
    const m = String(s || '').replace(/[฿,\s]/g, '').match(/-?\d+(\.\d+)?/);
    return m ? Math.abs(parseFloat(m[0])) : null;
  };
  // แต่ละบรรทัดคือ element ที่มีข้อความ label และมีตัวเลขอยู่ใน element พี่น้อง
  const rows = [...document.querySelectorAll('div,li,tr')].filter(e => {
    const t = (e.innerText || '').trim();
    return t && t.length < 160 && /฿/.test(t) && e.children.length <= 6;
  });
  const pick = label => {
    // เอาแถวที่ "ขึ้นต้นด้วย" label พอดี (กัน 'ค่าคอมมิชชั่นแอฟฟิลิเอต' ไปจับตัวที่ยาวกว่า)
    const cand = rows.filter(e => {
      const t = (e.innerText || '').replace(/\n/g, ' ').trim();
      return t.startsWith(label);
    });
    if (!cand.length) return null;
    // ตัวที่สั้นที่สุด = แถวนั้นจริง ๆ ไม่ใช่กล่องที่ครอบหลายแถว
    cand.sort((a, b) => (a.innerText || '').length - (b.innerText || '').length);
    const t = (cand[0].innerText || '').replace(/\n/g, ' ');
    return num(t.slice(label.length));
  };
  const out = {};
  for (const [k, label] of Object.entries(NEED)) out[k] = pick(label);
  // ช่วงวันที่ที่แผงกำลังแสดง (ไว้ตรวจว่าเลือกเดือนถูก)
  const head = [...document.querySelectorAll('div')]
    .map(e => (e.innerText || '').trim())
    .find(t => /^\d{1,2} [ก-๙]+ \d{4} - \d{1,2} [ก-๙]+ \d{4}$/.test(t));
  out.range = head || null;
  out.ok = out.revenue != null && out.fee != null;
  if (out.ok) {
    out.fee_pct = +(out.fee / out.revenue * 100).toFixed(3);
    const aff = (out.aff || 0) + (out.aff_ads || 0);
    out.aff_total = aff;
    out.aff_pct = +(aff / out.revenue * 100).toFixed(3);
    out.fee_excl_aff_pct = +((out.fee - aff) / out.revenue * 100).toFixed(3);
  }
  return JSON.stringify(out);
})();
