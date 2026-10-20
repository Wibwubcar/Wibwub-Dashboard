#!/usr/bin/env python3
"""ฝัง CSS/JS ของเมนู "การตลาด vs ยอดขาย" เข้าทั้ง 2 หน้า

ตัวจริงอยู่ที่ `scripts/marketing/mks_ui.css` และ `mks_ui.js` — **แก้ที่นั่น** แล้วรันไฟล์นี้
เพื่อฝังทับของเดิมในหน้าเว็บ (หน้าเว็บ minified/ยาวมาก แก้มือพลาดง่าย)

บล็อกข้อมูล `/* MKT_SPEND:AUTO-START */ ... END */` จะถูกเก็บไว้เหมือนเดิมเสมอ
(ข้อมูลเป็นของ marketing_update.py ไม่ใช่ของไฟล์นี้)

ใช้:  python3 scripts/marketing/marketing_ui.py [--dry-run]
"""
import sys, re, json, argparse, subprocess, tempfile
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
SRC = Path(__file__).resolve().parent
PAGES = {'WIBWUB_Dashboard.html': ('mks-css', 'mks-js'),
         'WIBWUB_Mobile.html': ('mks-css-m', 'mks-js-m')}
START = '/* MKT_SPEND:AUTO-START */'
END = '/* MKT_SPEND:AUTO-END */'


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    css = (SRC / 'mks_ui.css').read_text(encoding='utf-8')
    js = (SRC / 'mks_ui.js').read_text(encoding='utf-8')
    rep = {}

    for page, (cid, jid) in PAGES.items():
        fp = BASE / page
        t0 = t = fp.read_text(encoding='utf-8')

        mc = re.search(r'<style id="' + cid + r'">[\s\S]*?</style>', t)
        mj = re.search(r'<script id="' + jid + r'">[\s\S]*?</script>', t)
        if not mc or not mj: die('ไม่พบบล็อก style/script ของเมนูนี้ใน ' + page)

        # เก็บบล็อกข้อมูลเดิมไว้ (อยู่ใน <script>) — ห้ามหายไปกับการฝัง JS ใหม่
        md = re.search(re.escape(START) + r'[\s\S]*?' + re.escape(END), mj.group(0))
        data = md.group(0) if md else (START + '\nconst MKT_SPEND = {"days":{}};\n' + END)

        t = t[:mc.start()] + f'<style id="{cid}">\n{css}\n</style>' + t[mc.end():]
        mj = re.search(r'<script id="' + jid + r'">[\s\S]*?</script>', t)
        t = t[:mj.start()] + f'<script id="{jid}">\n{js}\n{data}\n</script>' + t[mj.end():]

        # เรนเดอร์ใหม่เมื่อหมุนจอ/ย่อขยาย (กราฟคำนวณความกว้างตอน render)
        if 'mksResize' not in t:
            t = t.replace('</body>', '<script>window.addEventListener("resize",function(){'
                          'clearTimeout(window.mksResize);window.mksResize=setTimeout(function(){'
                          'try{mksRender();}catch(e){}},250);});</script>\n</body>', 1)

        # ตรวจ JS ทั้งหน้าก่อนเขียน
        tmp = Path(tempfile.gettempdir()) / f'mksui_{page}.js'
        tmp.write_text('\n;\n'.join(
            re.findall(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', t)), encoding='utf-8')
        r = subprocess.run(['node', '--check', str(tmp)], capture_output=True, text=True)
        if r.returncode: die(f'node --check ไม่ผ่าน ({page})', r.stderr[:400])

        rep[page] = {'changed': t != t0, 'kept_data_bytes': len(data)}
        if not a.dry_run and t != t0: fp.write_text(t, encoding='utf-8')

    if not a.dry_run and any(v['changed'] for v in rep.values()):
        r = subprocess.run([sys.executable, str(BASE / 'scripts' / 'bump_sw.py')],
                           capture_output=True, text=True)
        rep['sw'] = r.stdout.strip() or r.stderr.strip()[:80]
    print(json.dumps({'status': 'DRY_RUN' if a.dry_run else 'OK', **rep}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
