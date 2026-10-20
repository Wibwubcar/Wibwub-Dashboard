#!/usr/bin/env python3
"""ดึงยอดจ่าย KOL รายเดือนจากชีต Payment KOL Wibwub -> data Ads/kol_monthly.json

⚠️ ชีตต้นทางมีข้อมูลส่วนบุคคล: ชื่อ-นามสกุล เลขบัตรประชาชน เลขผู้เสียภาษี
   เลขบัญชีธนาคาร ที่อยู่ เบอร์โทร
   สคริปต์นี้อ่าน **เฉพาะ 4 คอลัมน์**: วันที่ทำจ่าย · จำนวนที่ต้องจ่าย · Status · Month
   และเขียนออกเป็น **ผลรวมรายเดือนเท่านั้น** ไม่มีแถวรายบุคคลหลุดออกมา
   ห้ามเพิ่มคอลัมน์อื่นเข้ามาในสคริปต์นี้เด็ดขาด

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

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
OUT = BASE / 'data Ads' / 'kol_monthly.json'
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
                rows_out.append({'d': to_day(r[ci[COL_DATE]]), 'camp': ws.title,
                                 'tier': tiers.get(ws.title), 'kol': kol,
                                 'amt': round(amt, 2), 'st': 'done' if st == 'done' else 'pending'})
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

    out = {'source': 'Payment KOL Wibwub (aggregate only — no personal data)',
           'rule': 'Status=Done · เดือนจากวันที่ทำจ่าย · ยอดจากจำนวนที่ต้องจ่าย',
           'fetched_at': dt.datetime.now().strftime('%Y-%m-%d %H:%M'),
           'months': dict(sorted(months.items())),
           'pending': dict(sorted(pend.items())),
           'undated_done': {'amount': round(undated['done'], 2), 'n': undated['n']},
           'rows_from': ROWS_FROM, 'rows': sorted(rows_out, key=lambda r: (r['d'] or '', -r['amt'])),
           'tiers_unmapped': sorted({r['camp'] for r in rows_out if not r['tier']}),
           'tabs_skipped': skipped, 'rows_scanned': rows_seen}

    # by_campaign = ชื่อแคมเปญ (บางชื่อมีชื่อเล่น KOL อยู่) -> ดูได้ตอน dry-run เท่านั้น
    # ไม่เขียนลงไฟล์ที่ commit ตามกฎ "เก็บเฉพาะยอดเงิน + วันที่ + ผลรวมรายเดือน"
    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **out, 'by_campaign': camps},
                         ensure_ascii=False)); return 0
    prev = json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {}
    same = {k: v for k, v in prev.items() if k != 'fetched_at'} == \
           {k: v for k, v in out.items() if k != 'fetched_at'}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'status': 'NO_CHANGE' if same else 'UPDATED',
                      'months': {k: v['amount'] for k, v in out['months'].items()}},
                     ensure_ascii=False))
    return 10 if same else 0


if __name__ == '__main__':
    sys.exit(main())
