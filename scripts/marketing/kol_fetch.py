#!/usr/bin/env python3
"""ดึงยอดจ่าย KOL รายเดือนจากชีต Payment KOL Wibwub -> data Ads/kol_monthly.json

⚠️ ชีตต้นทางมีข้อมูลส่วนบุคคล: ชื่อ-นามสกุล เลขบัตรประชาชน เลขผู้เสียภาษี
   เลขบัญชีธนาคาร ที่อยู่ เบอร์โทร
   สคริปต์นี้อ่าน **เฉพาะ 5 คอลัมน์**: วันที่ทำจ่าย · จำนวนที่ต้องจ่าย · Status · Month
   · ชื่อช่อง KOL   ห้ามเพิ่มคอลัมน์อื่นเข้ามาในสคริปต์นี้เด็ดขาด

⛔ ไฟล์ขาออกมี 2 ไฟล์ และ **แยกกันเด็ดขาด**
   · `data Ads/kol_monthly.json`      = commit ได้ — ยอดรวมรายวัน/รายเดือน/รายระดับ
                                        ไม่มีชื่อบัญชี KOL ไม่มีชื่อแคมเปญ ไม่มีแถวรายคน
   · `data Ads/kol_rows_private.json` = **ห้าม commit** (.gitignore แล้ว) — แถวรายคน
   28 ต.ค. 69: ก่อนหน้านี้แถวรายคน 497 แถว (ชื่อบัญชี 335 ราย + ยอดจ่ายรายคน
   + ชื่อแคมเปญ) อยู่ใน kol_monthly.json ที่ commit **และถูกฝังลงหน้าเว็บทั้ง 2 หน้า**
   ตั้งแต่ commit d61dce1 (20 ต.ค. 15:48) ค้างอยู่ 8 วัน ทั้งที่หัวไฟล์เขียนว่า
   "aggregate only — no personal data" · repo Wibwubcar/Wibwub-Dashboard เป็น
   **public** และ GitHub Pages เสิร์ฟไฟล์สาธารณะ (ยืนยันแล้ว HTTP 200 แบบไม่ล็อกอิน)
   -> ห้ามเอา rows กลับเข้า kol_monthly.json หรือส่งขึ้นหน้าเว็บอีกเด็ดขาด

กฎการนับ (ตามที่ตกลงไว้):
  · นับเฉพาะแถวที่ Status = Done
  · เดือนมาจาก "วันที่ทำจ่าย" (ไม่ใช่คอลัมน์ Month ซึ่งเป็นเดือนของแคมเปญ)
  · ยอด = "จำนวนที่ต้องจ่าย"
  · แถวที่ยังไม่ Done เก็บเป็น pending แยก (ไม่รวมยอดหลัก)
  · แถว Done ที่ไม่มีวันที่ทำจ่าย -> undated ไม่ยัดเข้าเดือนไหน และรายงานให้เห็น

ไม่มีคอลัมน์ "ระดับ KOL" รายแถวในชีต (ระดับอยู่ในแท็บสรุป Total Spending เท่านั้น)
จึงแตกตามชื่อแคมเปญ = ชื่อแท็บ ซึ่งไม่มีข้อมูลส่วนบุคคล

ใช้:  python3 scripts/marketing/kol_fetch.py [--dry-run]
exit: 0 = เขียนแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ
"""
import sys, json, re, argparse, datetime as dt
from pathlib import Path

def _find_base():
    """ไล่ขึ้นจากตำแหน่งไฟล์นี้จนเจอโฟลเดอร์ All — ดูจาก marker sw.js + .git

    ห้ามฝังพาธ Mac ตายตัว: งานตั้งเวลาฝั่ง local รันในแซนด์บ็อกซ์ที่ mount โฟลเดอร์ All
    ไว้คนละที่ (/sessions/<ชื่อ>/mnt/All) และชื่อเซสชันเปลี่ยนทุกรอบ (24 ต.ค. 69)
    """
    p = Path(__file__).resolve()
    for d in (p, *p.parents):
        if (d / 'sw.js').is_file() and (d / '.git').exists():
            return d
    raise SystemExit(f'หาโฟลเดอร์ All ไม่เจอ — ไล่ขึ้นจาก {p} แล้วไม่เจอโฟลเดอร์ที่มีทั้ง '
                     'sw.js และ .git · ห้ามเดาพาธ ให้ตรวจว่าสคริปต์ยังอยู่ในโฟลเดอร์ All หรือไม่')


BASE = _find_base()
OUT = BASE / 'data Ads' / 'kol_monthly.json'        # commit ได้ — ยอดรวมเท่านั้น
PRIV = BASE / 'data Ads' / 'kol_rows_private.json'  # ห้าม commit — แถวรายคน
SHEET_ID = '1NEkm1bcHvXO0Ehs6cwaNDkBUUM1A9assALMp5V7S7lo'
SA = Path.home() / 'wibwub-service-account.json'
SKIP_TABS = {'Total Spending'}            # แท็บสรุป ไม่ใช่รายแคมเปญ

# คอลัมน์ที่อนุญาตให้อ่าน — ชื่อหัวตารางหลัง normalize ช่องว่าง
COL_DATE  = 'วันที่ทำจ่าย'
COL_AMT   = 'จำนวนที่ต้องจ่าย'
COL_STAT  = 'Status'
COL_MONTH = 'Month'
# คอลัมน์ชื่อ KOL ที่อนุญาต — เป็น "ชื่อช่อง/ชื่อเล่น" เท่านั้น (เช่น atpk.live)
# **ห้ามเพิ่ม 'ชื่อจริง' / 'นามสกุล' / 'Name' เข้ามาเด็ดขาด** — 'Name' ในแท็บปี 2025
# เป็นชื่อ-นามสกุลจริง จึงไม่อยู่ในรายการนี้ แถวพวกนั้นจะได้ kol = '' แต่ยอดยังนับปกติ
COL_KOL = ('KOLs', 'KOLs Name')
TIER_MAP = BASE / 'data Ads' / 'kol_campaign_tier.json'
ROWS_FROM = '2026-01'                     # แถวรายตัวเก็บเฉพาะช่วงที่หน้าเว็บใช้จริง
#            ^ ขยับจาก 2026-09 เป็น 2026-01 ตอนทำ backfill Ads ย้อนหลัง (20 ต.ค. 69)
EPOCH = dt.date(1899, 12, 30)             # serial 1 = 1899-12-31 ใน Google Sheets
MONTH_WORDS = {m: i + 1 for i, m in enumerate(
    ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])}


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def norm(s):
    return re.sub(r'\s+', ' ', str(s)).strip()


def to_date(v):
    """คืน 'YYYY-MM' หรือ None — รับได้ทั้ง serial number และข้อความ dd/mm/yyyy"""
    if v is None or v == '':
        return None
    if isinstance(v, (int, float)):
        if not (20000 < v < 60000):       # นอกช่วง ~1954-2064 ไม่ใช่วันที่แน่ ๆ
            return None
        return (EPOCH + dt.timedelta(days=int(v))).strftime('%Y-%m')
    s = norm(v)
    m = re.match(r'^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$', s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if y > 2400: y -= 543             # เผื่อกรอกเป็น พ.ศ.
        try: return dt.date(y, mo, d).strftime('%Y-%m')
        except ValueError: return None
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', s)
    if m: return s[:7]
    # แท็บเก่า (2025 - กลางปี 2026) เก็บเป็นข้อความ เช่น '28 Nov 2025' / '21 April 2026'
    m = re.match(r'^(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})$', s)
    if m:
        mo = MONTH_WORDS.get(m.group(2)[:3].lower())
        if mo:
            y = int(m.group(3))
            if y > 2400: y -= 543
            return f'{y}-{mo:02d}'
    return None


def to_day(v):
    """คืน 'YYYY-MM-DD' (ใช้ตรรกะเดียวกับ to_date แต่เก็บวันด้วย)"""
    if v is None or v == '': return None
    if isinstance(v, (int, float)):
        if not (20000 < v < 60000): return None
        return (EPOCH + dt.timedelta(days=int(v))).isoformat()
    s = norm(v)
    m = re.match(r'^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$', s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if y > 2400: y -= 543
        try: return dt.date(y, mo, d).isoformat()
        except ValueError: return None
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', s)
    if m: return s
    m = re.match(r'^(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})$', s)
    if m:
        mm = MONTH_WORDS.get(m.group(2)[:3].lower())
        if mm:
            y = int(m.group(3));  y -= 543 if y > 2400 else 0
            try: return dt.date(y, mm, int(m.group(1))).isoformat()
            except ValueError: return None
    return None


def to_amt(v):
    if v is None or v == '': return None
    if isinstance(v, (int, float)): return float(v)
    s = norm(v).replace(',', '')
    if s in ('-', '', 'N/A'): return None
    try: return float(s)
    except ValueError: return None


def git_ignored(path):
    """(ถูก ignore จริงไหม, ถูก track อยู่ใน git ไหม, เหตุผลถ้าตรวจไม่ได้)

    ไม่ใช้ gitw.py เพราะต้องใช้ ls-files/check-ignore ซึ่งไม่อยู่ในรายการอนุญาตของ gitw
    (อ่านอย่างเดียว ไม่เปลี่ยนสถานะ repo)
    """
    import subprocess
    rel = str(path.relative_to(BASE))
    try:
        ig = subprocess.run(['git', '-C', str(BASE), 'check-ignore', '-q', rel],
                            capture_output=True)
        tr = subprocess.run(['git', '-C', str(BASE), 'ls-files', '--error-unmatch', rel],
                            capture_output=True)
    except (FileNotFoundError, OSError) as e:
        return False, False, f'เรียก git ไม่ได้: {type(e).__name__}'
    return ig.returncode == 0, tr.returncode == 0, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if not SA.exists(): die('ไม่พบ service account', str(SA))

    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except Exception as e:
        die('import gspread/google-auth ไม่สำเร็จ', f'{type(e).__name__}: {e}')

    cred = Credentials.from_service_account_file(
        str(SA), scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    sh = gspread.authorize(cred).open_by_key(SHEET_ID)

    months, pend, undated, camps, skipped = {}, {}, {'done': 0.0, 'n': 0}, {}, []
    rows_seen, rows_out = 0, []
    # ยอดรวมรายวัน: นี่คือสิ่งเดียวที่หน้าเว็บต้องใช้ (คอลัมน์ kol ของตารางรายวัน)
    days_done, days_pend, tier_days = {}, {}, {}
    tiers = json.loads(TIER_MAP.read_text(encoding='utf-8')).get('campaign_tier', {}) \
        if TIER_MAP.exists() else {}
    for ws in sh.worksheets():
        if ws.title in SKIP_TABS: continue
        grid = ws.get('A1:BC1200', value_render_option='UNFORMATTED_VALUE')
        hi = next((i for i, r in enumerate(grid[:5]) if any(COL_DATE in norm(x) for x in r)), None)
        if hi is None:
            skipped.append(ws.title); continue
        hdr = [norm(x) for x in grid[hi]]
        try:
            ci = {k: hdr.index(k) for k in (COL_DATE, COL_AMT, COL_STAT)}
        except ValueError:
            skipped.append(ws.title); continue
        ci[COL_MONTH] = hdr.index(COL_MONTH) if COL_MONTH in hdr else None
        ci['kol'] = next((hdr.index(x) for x in COL_KOL if x in hdr), None)

        for r in grid[hi + 1:]:
            if len(r) <= ci[COL_STAT]: continue          # แถวโน้ต/แถวว่าง
            amt = to_amt(r[ci[COL_AMT]] if len(r) > ci[COL_AMT] else None)
            if amt is None or amt <= 0: continue
            rows_seen += 1
            st = norm(r[ci[COL_STAT]]).lower()
            mo = to_date(r[ci[COL_DATE]] if len(r) > ci[COL_DATE] else None)
            kol = norm(r[ci['kol']]) if ci['kol'] is not None and len(r) > ci['kol'] else ''
            if mo and mo >= ROWS_FROM:
                day = to_day(r[ci[COL_DATE]])
                tier = tiers.get(ws.title)
                rows_out.append({'d': day, 'camp': ws.title, 'tier': tier, 'kol': kol,
                                 'amt': round(amt, 2),
                                 'st': 'done' if st == 'done' else 'pending'})
                if day:
                    if st == 'done':
                        days_done[day] = round(days_done.get(day, 0.0) + amt, 2)
                        k = tier or 'ยังไม่ระบุระดับ'
                        td = tier_days.setdefault(day, {})
                        td[k] = round(td.get(k, 0.0) + amt, 2)
                    else:
                        days_pend[day] = round(days_pend.get(day, 0.0) + amt, 2)
            if st != 'done':
                key = mo or 'undated'
                p = pend.setdefault(key, {'amount': 0.0, 'n': 0})
                p['amount'] += amt; p['n'] += 1
                continue
            if not mo:
                undated['done'] += amt; undated['n'] += 1; continue
            m = months.setdefault(mo, {'amount': 0.0, 'n': 0})
            m['amount'] += amt; m['n'] += 1
            c = camps.setdefault(mo, {}).setdefault(ws.title, 0.0)
            camps[mo][ws.title] = c + amt

    if rows_seen < 50: die('อ่านได้น้อยผิดปกติ — ชีตอาจเปลี่ยนโครงสร้าง', rows_seen)
    for k in months: months[k]['amount'] = round(months[k]['amount'], 2)
    for k in pend:   pend[k]['amount']   = round(pend[k]['amount'], 2)
    camps = {m: {k: round(v, 2) for k, v in sorted(d.items(), key=lambda x: -x[1])}
             for m, d in camps.items()}

    unmapped = sorted({r['camp'] for r in rows_out if not r['tier']})
    # ⛔ ไฟล์นี้ commit ลง repo ที่เป็น public — ใส่ได้แค่ยอดรวม
    #    ห้ามใส่: rows (แถวรายคน) · kol (ชื่อบัญชี) · camp/tabs_skipped/tiers_unmapped
    #    (ชื่อแท็บ = ชื่อแคมเปญ ซึ่งบางชื่อมีชื่อเล่น KOL ปนอยู่) -> เก็บเป็น "จำนวน"
    out = {'source': 'Payment KOL Wibwub (ยอดรวมเท่านั้น — ไม่มีแถวรายคน '
                     'ไม่มีชื่อบัญชี KOL ไม่มีชื่อแคมเปญ)',
           'privacy': 'รายละเอียดรายแถวอยู่ที่ data Ads/kol_rows_private.json '
                      'ซึ่ง .gitignore ไว้ — ห้าม commit และห้ามส่งขึ้นหน้าเว็บ',
           'rule': 'Status=Done · เดือนจากวันที่ทำจ่าย · ยอดจากจำนวนที่ต้องจ่าย',
           'fetched_at': dt.datetime.now().strftime('%Y-%m-%d %H:%M'),
           'months': dict(sorted(months.items())),
           'pending': dict(sorted(pend.items())),
           'undated_done': {'amount': round(undated['done'], 2), 'n': undated['n']},
           'rows_from': ROWS_FROM,
           'days': dict(sorted(days_done.items())),
           'days_pending': dict(sorted(days_pend.items())),
           'tier_days': {d: tier_days[d] for d in sorted(tier_days)},
           'tiers_unmapped_n': len(unmapped),
           'tabs_skipped_n': len(skipped), 'rows_scanned': rows_seen}

    # ด่าน: ถ้าคีย์ต้องห้ามหลุดเข้ามา ให้ตายก่อนเขียนไฟล์
    leak = [k for k in ('rows', 'tiers_unmapped', 'tabs_skipped', 'by_campaign') if k in out]
    if leak:
        die('มีคีย์ที่มีข้อมูลรายคน/ชื่อแคมเปญหลุดเข้า kol_monthly.json — ไม่เขียนไฟล์', leak)
    blob = json.dumps(out, ensure_ascii=False)
    hit = [r['kol'] for r in rows_out if r['kol'] and r['kol'] in blob]
    if hit:
        die('พบชื่อบัญชี KOL ในไฟล์ที่จะ commit — ไม่เขียนไฟล์', len(hit))

    # by_campaign = ชื่อแคมเปญ (บางชื่อมีชื่อเล่น KOL อยู่) -> ดูได้ตอน dry-run เท่านั้น
    # ไม่เขียนลงไฟล์ที่ commit ตามกฎ "เก็บเฉพาะยอดเงิน + วันที่ + ผลรวมรายเดือน"
    ignored, tracked, why = git_ignored(PRIV)
    priv = {'warning': '⛔ ข้อมูลส่วนบุคคล — ห้าม commit ห้ามส่งขึ้นหน้าเว็บ '
                       'ห้ามวางในรายงาน (repo เป็น public + GitHub Pages สาธารณะ)',
            'fetched_at': out['fetched_at'], 'rows_from': ROWS_FROM,
            'rows': sorted(rows_out, key=lambda r: (r['d'] or '', -r['amt'])),
            'tiers_unmapped': unmapped, 'tabs_skipped': skipped,
            'by_campaign': camps}

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **out,
                          'private_rows': len(rows_out),
                          'private_file': {'path': str(PRIV.relative_to(BASE)),
                                           'gitignored': ignored, 'tracked': tracked,
                                           'why': why}},
                         ensure_ascii=False)); return 0

    prev = json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {}
    same = {k: v for k, v in prev.items() if k != 'fetched_at'} == \
           {k: v for k, v in out.items() if k != 'fetched_at'}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')

    # ไฟล์ private เขียน "ต่อเมื่อ" git ยืนยันว่า ignore แล้วจริง
    # ตรวจไม่ได้ = ไม่เขียน (ยอมเสียรายละเอียด ดีกว่าเสี่ยงหลุด) แต่ยอดรวมยังอัปเดตปกติ
    if tracked:
        die('kol_rows_private.json ถูก track อยู่ใน git — ข้อมูลส่วนบุคคลจะถูก commit '
            'ให้เอาออกจาก index ก่อน (git rm --cached) แล้วเช็กว่า .gitignore ครอบถูก',
            str(PRIV.relative_to(BASE)))
    if ignored:
        PRIV.write_text(json.dumps(priv, ensure_ascii=False, indent=1), encoding='utf-8')
        priv_note = f'เขียนแล้ว {len(rows_out)} แถว (gitignored)'
    else:
        priv_note = ('ไม่ได้เขียน — git ยังไม่ยืนยันว่าไฟล์นี้ถูก ignore '
                     + (why or 'ไม่พบใน .gitignore'))
    print(json.dumps({'status': 'NO_CHANGE' if same else 'UPDATED',
                      'months': {k: v['amount'] for k, v in out['months'].items()},
                      'days_with_amount': len(out['days']),
                      'private_file': priv_note},
                     ensure_ascii=False))
    return 10 if same else 0


if __name__ == '__main__':
    sys.exit(main())
