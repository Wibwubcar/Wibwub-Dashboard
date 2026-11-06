#!/usr/bin/env python3
"""ด่านความเป็นส่วนตัวของข้อมูลโฆษณาเชิงลึก — แทนชื่อครีเอเตอร์ + สแกนชื่อคนก่อน commit

**รีโปนี้เป็น public + GitHub Pages ทุกไฟล์ที่ commit คือเผยแพร่** (ดู wibwub-repo-is-public-pages)
ชื่อแอดของ TikTok ตั้งตามชื่อเล่นครีเอเตอร์จริง รูปแบบ `<วันที่>/<ชื่อเล่น>`
ถ้าปล่อยขึ้น `ads_detail_tk.json` = เปิดเผยว่าใครรับงานให้ร้าน วันไหน ได้ยอดเท่าไร

สองหน้าที่:
  1. `mask()` แทนชื่อคนด้วย `<วันที่>/ครีเอเตอร์ #NN` — **เลขคงที่ คนเดิมได้เลขเดิมทุกรอบ**
     ตารางจับคู่อยู่ที่ `data Ads/TikTok/creator_map_private.json` ซึ่ง .gitignore ครอบไว้
     เจอชื่อใหม่ออกเลขถัดไปเองอัตโนมัติ ไม่ต้องถาม (ผู้ใช้สั่งไว้ 5 พ.ย. 69)
  2. `scan()` ด่านก่อน commit — เจอชื่อคนที่ยังไม่ถูกแทนใน JSON ใด ๆ = **ห้าม commit**

⚠️ ห้ามเอาตารางจับคู่ขึ้น git และห้ามพิมพ์ชื่อจริงลงรายงานท้ายรอบ
   (ชื่อ KOL 335 รายเคยหลุดมาแล้ว 8 วัน)

ใช้:  python3 scripts/ads/detail_privacy.py scan "data Ads/ads_detail_tk.json" ...
exit: 0 = สะอาด · 2 = เจอชื่อคน (ผู้เรียกต้องไม่ commit)
"""
import sys, json, re, argparse
from pathlib import Path


def _find_base():
    p = Path(__file__).resolve()
    for d in (p, *p.parents):
        if (d / 'sw.js').is_file() and (d / '.git').exists():
            return d
    raise SystemExit('หาโฟลเดอร์ All ไม่เจอ — ห้ามเดาพาธ')


BASE = _find_base()
MAP_FILE = BASE / 'data Ads' / 'TikTok' / 'creator_map_private.json'

# คำนำหน้าที่บ่งชี้ "คน" ในชื่อแอด — เก็บเป็น raw string ทั้งหมด ห้ามใส่ชื่อจริงลงไฟล์นี้
PERSON_HINT = re.compile(
    r'(คุณ|พ่อ|แม่|น้อง|พี่|นาย|นาง|นางสาว|ครีเอเตอร์(?!\s*#)|creator(?!\s*#))',
    re.IGNORECASE)
# ของที่ห้ามหลุดเสมอ ไม่ว่าจะอยู่ฟิลด์ไหน
HARD = [
    (re.compile(r'(?<!\w)@[A-Za-z0-9._]{3,}'), 'มี @handle'),
    (re.compile(r'(?<!\d)0\d{8,9}(?!\d)'), 'มีเบอร์โทร'),
]
# ชื่อกลุ่ม/แคมเปญที่มีคำว่า creator แต่ไม่ระบุตัวบุคคล — ผู้ใช้ยืนยันให้ปล่อยได้ 5 พ.ย. 69
ALLOW = re.compile(r'^(C-Ads\s+TOP\s+CREATOR|Top\s+[Cc]reator\s+สินค้า\s+WIBWUB)', re.IGNORECASE)
# รูปแบบที่ mask() สร้าง ต้องไม่ถูกจับเป็นชื่อคนซ้ำ
MASKED = re.compile(r'ครีเอเตอร์\s*#\d+')


def _load_map():
    """คืน (ตารางชื่อ->เลข, รายชื่อที่เคลียร์แล้วว่าไม่ใช่คน)

    คีย์ `_allow` เก็บชื่อที่ผู้ใช้ตรวจแล้วว่าเป็นชื่อแบรนด์/สินค้า ไม่ใช่ชื่อบุคคล
    เก็บไว้ในไฟล์นอก git เหมือนกัน **ห้ามย้ายชื่อพวกนี้มาเขียนไว้ในซอร์สโค้ด**
    ไม่งั้นก็เท่ากับเอาชื่อขึ้นรีโปสาธารณะอยู่ดี
    """
    try:
        d = json.loads(MAP_FILE.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}, []
    allow = d.pop('_allow', [])
    return d, list(allow)


def _save_map(m, allow):
    MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
    out = dict(m)
    if allow:
        out['_allow'] = allow
    tmp = MAP_FILE.with_suffix('.tmp')
    tmp.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    tmp.replace(MAP_FILE)


def is_person(name):
    """ชื่อนี้ระบุตัวบุคคลไหม (ยังไม่ถูกแทน)"""
    if not name:
        return False
    s = str(name)
    if MASKED.search(s) or ALLOW.match(s.strip()):
        return False
    return bool(PERSON_HINT.search(s)) or any(rx.search(s) for rx, _ in HARD)


class Masker:
    """แทนชื่อครีเอเตอร์ด้วยเลขคงที่ · เขียนตารางกลับไฟล์ครั้งเดียวตอน save()"""

    def __init__(self):
        self.map, self.allow = _load_map()
        self.new = 0

    def mask_ad(self, name):
        """แทน **ทุกชื่อแอดของ TikTok** ไม่ว่าจะเดาได้ว่าเป็นชื่อคนหรือไม่

        ทำไมต้องแทนหมด (พบ 5 พ.ย. 69): ร้านตั้งชื่อแอดเป็น `<วันที่>/<ชื่อครีเอเตอร์>`
        และชื่อครีเอเตอร์จำนวนมาก **ไม่มีคำนำหน้าให้จับ** (เป็นชื่อภาษาอังกฤษล้วน
        ชื่อช่อง หรือฉายาที่ไม่ขึ้นต้นด้วยคำบ่งชี้บุคคล) — ถ้าใช้ `mask()` ที่เดาจากคำนำหน้า
        ชื่อพวกนี้จะหลุด
        ขึ้นรีโปสาธารณะทั้งที่ระบุตัวบุคคลได้ชัดเจน · การแทนหมดเสียแค่ความหมายของชื่อ
        แต่ยังแยกแอดออกจากกันได้ด้วยเลขที่คงที่
        """
        if not name:
            return name
        s = str(name).strip()
        # ชื่อที่ตรวจแล้วว่าเป็นแบรนด์/สินค้า ปล่อยไว้ให้อ่านรู้เรื่อง ไม่ต้องแปลงเป็นเลข
        tail = s.split('/')[-1].strip()
        if s in self.allow or tail in self.allow:
            return s
        return self._assign(s)

    def mask(self, name):
        """ใช้กับชื่อแคมเปญ/ชุดโฆษณา — แทนเมื่อ **เคยออกเลขให้ชื่อนั้นแล้ว** หรือมีคำบ่งชี้บุคคล

        ข้อแรกสำคัญกว่าที่คิด (เจอจริง 6 พ.ย. 69 ตอนเติมข้อมูล ต.ค.):
        ร้านตั้ง **ชื่อแคมเปญและชื่อชุดโฆษณา** เป็น `<วันที่>/<ชื่อครีเอเตอร์>` เหมือนชื่อแอด
        ชื่อพวกนั้นถูก mask_ad() ออกเลขไปแล้วตอนอ่านชั้นแอด แต่ `mask()` เดิมดูแค่คำนำหน้า
        จึงปล่อยผ่านในฟิลด์ `c`/`g` -> ชื่อจริง 2 ชื่อหลุดลง ads_detail_tk.json 10 แถว
        (ด่าน scan() มองไม่เห็นเพราะมันเดาจากคำนำหน้าเหมือนกัน · ด่าน names() จับได้)

        กฎใหม่: **ชื่อที่เคยตัดสินว่าเป็นคนแล้ว ต้องถูกแทนทุกฟิลด์ที่มันโผล่**
        """
        if not name:
            return name
        s = str(name).strip()
        tail = s.split('/')[-1].strip()
        if s in self.allow or tail in self.allow:
            return s
        if tail in self.map or s in self.map:
            return self._assign(s)
        if not is_person(name):
            return name
        return self._assign(s)

    def _assign(self, s):
        # เก็บส่วนวันที่ข้างหน้าไว้ (`02.11.26/<ชื่อเล่น>` -> `02.11.26/ครีเอเตอร์ #7`)
        m = re.match(r'^\s*([\d./\-]{4,12})\s*/\s*(.+)$', s)
        head, who = (m.group(1), m.group(2).strip()) if m else ('', s)
        if who not in self.map:
            self.map[who] = max([0] + list(self.map.values())) + 1
            self.new += 1
        tag = 'ครีเอเตอร์ #%02d' % self.map[who]
        return f'{head}/{tag}' if head else tag

    def save(self):
        if self.new:
            _save_map(self.map, self.allow)
        return self.new


def _walk(obj, path=''):
    """ไล่ค่าทุกตัวที่เป็นสตริงใน JSON พร้อมพาธ"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk(v, f'{path}.{k}' if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk(v, f'{path}[{i}]')
    elif isinstance(obj, str):
        yield path, obj


def scan(paths):
    """คืนรายการ (ไฟล์, พาธในไฟล์, ค่า, เหตุผล) ที่ยังมีชื่อคน"""
    hits = []
    for p in paths:
        fp = Path(p) if Path(p).is_absolute() else BASE / p
        try:
            data = json.loads(fp.read_text(encoding='utf-8'))
        except OSError as e:
            hits.append((str(p), '-', '', f'อ่านไฟล์ไม่ได้: {e}'))
            continue
        except ValueError as e:
            hits.append((str(p), '-', '', f'JSON พัง: {e}'))
            continue
        for where, val in _walk(data):
            # `notes` เป็นข้อความที่เราเขียนเอง ไม่ได้มาจากแพลตฟอร์ม และต้องพูดถึงคำว่า
            # "ครีเอเตอร์" เพื่ออธิบายว่าชื่อถูกแทนแล้ว — ถ้าสแกนด้วยจะเตือนผิดทุกรอบ
            if where == 'notes' or where.startswith('notes['):
                continue
            for rx, why in HARD:
                if rx.search(val):
                    hits.append((fp.name, where, val[:60], why))
                    break
            else:
                if is_person(val):
                    hits.append((fp.name, where, val[:60], 'มีคำบ่งชี้ตัวบุคคล'))
    return hits


def names(paths):
    """ด่านที่สองของทุกไฟล์ที่จะขึ้นรีโป — เทียบกับ "ชื่อจริง" ทุกชื่อในตารางจับคู่

    ต่างจาก `scan()` ที่เดาจากคำนำหน้า: อันนี้รู้ชื่อจริงทั้งหมดอยู่แล้ว จึงจับได้ 100%
    และต้องใช้กับ **โค้ด คอมเมนต์ docstring และพรอมป์ .md ด้วย** ไม่ใช่แค่ JSON
    (5 พ.ย. 69: docstring ของไฟล์นี้เองเคยยกตัวอย่างชื่อเล่นจริงไว้ 6 ชื่อ
     ถ้า commit ไป ชื่อก็ขึ้นเว็บสาธารณะผ่านทางซอร์สโค้ดแทน — ผู้ใช้จับได้ก่อน)
    """
    m, allow = _load_map()
    real = sorted([n for n in m if n not in allow], key=len, reverse=True)
    hits = []
    for p in paths:
        fp = Path(p) if Path(p).is_absolute() else BASE / p
        try:
            txt = fp.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue                      # ไฟล์ไบนารีหรืออ่านไม่ได้ ข้ามไป
        for n in real:
            if len(n) >= 3 and n in txt:
                ln = txt[:txt.index(n)].count('\n') + 1
                hits.append((fp.name, 'บรรทัด %d' % ln, '(ชื่อจริง)', 'ตรงกับตารางจับคู่'))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['scan', 'names'])
    ap.add_argument('files', nargs='+')
    a = ap.parse_args()
    hits = names(a.files) if a.cmd == 'names' else scan(a.files)
    if not hits:
        print('✅ สะอาด — ไม่พบชื่อคนใน %d ไฟล์' % len(a.files))
        return 0
    print('⛔ พบชื่อคน %d จุด — ห้าม commit' % len(hits))
    for f, w, v, why in hits[:40]:
        print(f'  {f} | {w} | {v} <- {why}')
    if len(hits) > 40:
        print('  ... อีก %d จุด' % (len(hits) - 40))
    return 2


if __name__ == '__main__':
    sys.exit(main())
