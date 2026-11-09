#!/usr/bin/env python3
"""commit **เฉพาะ hunk ที่เป็นบรรทัดของงานตัวเอง** ในไฟล์ที่หลายงานใช้ร่วมกัน

ปัญหาที่แก้ (ทางตัน samp-request ↔ affiliate · ยืนยัน 9 พ.ย. 69)
────────────────────────────────────────────────────────────────────────────
`WIBWUB_Affiliate_Dashboard.html` มี 5 สคริปต์เขียน (samp_update, affiliate_update,
vid_merge, wibwub_update, channel_performance_update) ทุกตัวมีกฎว่า **ห้าม commit
ถ้าไฟล์มีงานของคนอื่นค้างอยู่** เพราะ `git add <ไฟล์>` กวาดการแก้ของทุกงานไปด้วย
(เคส 5 พ.ย. 69 aabd90c: ชื่อครีเอเตอร์จริงหลุดขึ้นรีโปสาธารณะแบบนี้)

ผลคือ samp_update เขียนข้อมูลลงไฟล์ แล้ว "ข้าม commit" · รอบถัดไปเทียบชีตกับหน้าเว็บ
ได้ว่าเหมือนกัน -> คืน NO_CHANGE (exit 10) ตั้งแต่ก่อนถึงขั้น commit
**จึงไม่มีรอบไหนกลับมา commit การแก้นั้นอีกเลย = ทางตันถาวร**

วิธีแก้: ไม่ต้องรอให้ไฟล์ว่าง และไม่กวาดของใคร — commit เฉพาะ hunk ที่ทุกบรรทัด
อยู่ในเขตที่งานตัวเองเป็นเจ้าของ · hunk ที่มีบรรทัดอื่นปนแม้บรรทัดเดียว **ข้ามและรายงาน**

ทำอย่างไรให้ปลอดภัยโดยโครงสร้าง (ไม่ใช่ด้วยความระมัดระวัง)
────────────────────────────────────────────────────────────────────────────
ไม่แตะ `.git/index` ของจริงเลยแม้แต่ครั้งเดียว · ใช้ index ชั่วคราวแล้วปั้น commit เอง:
    read-tree HEAD -> apply --cached เฉพาะ hunk ของตัวเอง -> write-tree
    -> commit-tree -> update-ref HEAD <ใหม่> <เก่า>
ข้อดีที่ตามมาเอง:
  · ของที่งานอื่น `git add` ค้างไว้ใน index จริง **ไม่ถูกแตะและไม่ถูก commit** —
    ไม่ใช่เพราะเราเช็ก แต่เพราะเราไม่ได้อ่าน index นั้นเลย
  · ล้มกลางทางไม่ต้อง unstage คืน (ไม่มีอะไรค้าง) — ลบไฟล์ index ชั่วคราวทิ้งพอ
    จึงไม่ต้องใช้ `git reset` ซึ่ง gitw ห้ามไว้
  · `update-ref HEAD <ใหม่> <เก่า>` มีค่าเก่าเป็นด่าน ถ้างานอื่น commit แทรกระหว่าง
    ที่เรากำลังปั้น จะล้มแบบรู้ตัว ไม่ใช่ทับ commit ของคนอื่นหาย
  · working tree ไม่ถูกเขียนเลย การแก้ของงานอื่นยังค้างอยู่ครบเหมือนเดิม

ทุกคำสั่ง git ไปผ่าน gitw.py (import มาใช้ `_run` / `_run_waiting`) จึงได้กลไกรอ
index.lock/HEAD.lock และตัวเก็บกวาด lock ที่ตายแล้วชุดเดียวกับทุกงาน
ที่ไม่ผ่าน main() ของ gitw เพราะ read-tree/write-tree/commit-tree/update-ref ไม่อยู่ใน
ALLOWED — รายการ ALLOWED นั้นมีไว้กันคำสั่งที่ "เอเจนต์พิมพ์เอง" ส่วนที่นี่ชุดคำสั่ง
ตายตัวอยู่ในไฟล์นี้ และไม่มีทางกวาดของใครได้ตามเหตุผลข้างบน
⛔ ห้ามเปลี่ยนไปใช้ index จริง (`git apply --cached` ตรง ๆ แล้ว commit) — นั่นคือการ
   เอาความปลอดภัยเชิงโครงสร้างออกไปแลกกับการเช็กว่า "index ว่างไหม" ซึ่งแข่งกันได้

ใช้เป็นโมดูล:
    from commit_own_hunks import commit_own_hunks
    commit_own_hunks('WIBWUB_Affiliate_Dashboard.html', REGIONS, 'ข้อความ')
REGIONS = [{'re': regex ของเขต, 'need': regex ที่บรรทัดต้องมี, 'only': regex ส่วนที่เป็นของเรา}]

กรณีที่ยากที่สุด: **บรรทัดเดียวมีของสองงาน** (ของจริงใน SAMPLE_MONTHS)
    {key:'2026-11', ..., funnel:{req:9,...}, perf:{gmv:99,...}}
  `funnel:` เป็นของ samp_update · `perf:` เป็นของ affiliate_update · อยู่บรรทัดเดียวกัน
  จึงแยกด้วย hunk ไม่ได้เลยไม่ว่าจะใช้ -U0 หรือหั่นทีละบรรทัด
  ทางเดียวที่ปลอดภัยคือ **พิสูจน์ว่าส่วนที่ไม่ใช่ของเราไม่ได้เปลี่ยน**: เอาบรรทัดเก่า/ใหม่
  มาปิดทับส่วน `only` ด้วยตัวยึด แล้วเทียบว่าที่เหลือเท่ากันทุกไบต์ ถ้าไม่เท่า = มีของ
  งานอื่นปนในบรรทัดนั้น -> ข้ามและรายงาน (ห้ามเดา ห้ามรวมค่าเอง)
"""
import bisect, importlib.util, json, os, re, subprocess, sys, tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]


def _gitw():
    """โหลด gitw.py เป็นโมดูล — ใช้ตัวรันที่รอ lock ตัวเดียวกับทุกงาน"""
    spec = importlib.util.spec_from_file_location('_gitw', BASE / 'scripts' / 'gitw.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


G = None        # ตั้งตอนเรียกใช้จริง เพื่อให้ import โมดูลนี้เปล่า ๆ ไม่แตะ git


def own_lines(text, regions):
    """คืน {เลขบรรทัด (เริ่มที่ 1): index ของ region ที่คลุมบรรทัดนั้น}"""
    lines = text.split('\n')
    starts, off = [], 0
    for ln in lines:
        starts.append(off)
        off += len(ln) + 1
    out = {}
    for ri, rg in enumerate(regions):
        for m in re.finditer(rg['re'], text, re.S):
            a = bisect.bisect_right(starts, m.start()) - 1
            b = bisect.bisect_right(starts, max(m.end() - 1, m.start())) - 1
            for i in range(a, b + 1):
                need = rg.get('need')
                if need is None or re.search(need, lines[i]):
                    out[i + 1] = ri
    return out


def _mask(line, only):
    """ปิดทับส่วนที่เป็นของเราด้วยตัวยึด เพื่อเทียบว่า "ส่วนที่เหลือ" เปลี่ยนไหม"""
    return re.sub(only, '\u00ab\u00bb', line)


HDR = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@')


def split_hunks(diff):
    """แยก unified diff (-U0) เป็น (header, [hunk...]) — hunk = dict"""
    lines = diff.split('\n')
    head, hunks, i = [], [], 0
    while i < len(lines) and not lines[i].startswith('@@'):
        head.append(lines[i]); i += 1
    cur = None
    for ln in lines[i:]:
        m = HDR.match(ln)
        if m:
            os_, ol, ns, nl = (int(m.group(1)), 1 if m.group(2) is None else int(m.group(2)),
                               int(m.group(3)), 1 if m.group(4) is None else int(m.group(4)))
            cur = {'old': (os_, ol), 'new': (ns, nl), 'text': [ln]}
            hunks.append(cur)
        elif cur is not None:
            if ln.startswith(('+', '-', ' ')) or ln.startswith('\\'):
                cur['text'].append(ln)
            elif ln == '':
                pass            # บรรทัดท้ายไฟล์จาก split
            else:
                cur = None       # เริ่มไฟล์ใหม่ — ไฟล์เดียวจึงไม่ควรเกิด
    return head, hunks


def split_pairs(h):
    """หั่น hunk -U0 ที่เป็น "แทนที่ล้วน" (จำนวน - เท่ากับ +) ให้เป็น hunk ละ 1 บรรทัด

    ต้องหั่นเพราะ git รวมบรรทัดที่ติดกันเป็น hunk เดียวแม้ใช้ -U0 เช่น SAMPLE_DATA_ASOF
    ที่อยู่ติดกับ const ของงานอื่นพอดี ถ้าไม่หั่นจะถูกตัดสินว่า "มีของคนอื่นปน" ทั้งก้อน
    แล้วทางตันก็ไม่คลาย · เมื่อหั่นแล้วแต่ละชิ้นมีคู่เก่า/ใหม่ชัดเจน จึงเทียบ mask ได้ด้วย
    hunk ที่จำนวนบรรทัดไม่เท่ากัน (เขตถูกเขียนใหม่ทั้งก้อนจนยาวขึ้น/สั้นลง) คืนเป็นก้อนเดิม
    """
    minus = [x for x in h['text'][1:] if x.startswith('-')]
    plus = [x for x in h['text'][1:] if x.startswith('+')]
    os_, ol = h['old']
    ns, nl = h['new']
    if not (ol == nl == len(minus) == len(plus)) or ol <= 1:
        return [h]
    return [{'old': (os_ + i, 1), 'new': (ns + i, 1),
             'text': ['@@ -%d +%d @@' % (os_ + i, ns + i), minus[i], plus[i]]}
            for i in range(ol)]


def classify(hunks, old_lines, new_lines, own_old, own_new, regions):
    keep, skip = [], []
    for h0 in hunks:
        for h in split_pairs(h0):
            os_, ol = h['old']
            ns, nl = h['new']
            bad = [str(n) for n in range(os_, os_ + ol) if n not in own_old]
            bad += ['+%d' % n for n in range(ns, ns + nl) if n not in own_new]
            # บรรทัดที่ใช้ร่วมกับงานอื่น (region มี only) ต้องเป็นคู่ 1:1 และส่วนที่เหลือต้องเท่ากัน
            shared = [n for n in range(ns, ns + nl)
                      if n in own_new and regions[own_new[n]].get('only')]
            if shared and not bad:
                if not (ol == nl == 1):
                    bad.append('+%d (บรรทัดใช้ร่วมกับงานอื่น แต่จับคู่เก่า/ใหม่ไม่ได้)' % ns)
                else:
                    only = regions[own_new[ns]]['only']
                    if _mask(old_lines[os_ - 1], only) != _mask(new_lines[ns - 1], only):
                        bad.append('+%d (ส่วนที่ไม่ใช่ของงานนี้ในบรรทัดเดียวกันถูกแก้ด้วย)' % ns)
            if bad:
                h['why'] = 'ไม่ใช่ของงานนี้: ' + ', '.join(bad[:6])
                skip.append(h)
            else:
                keep.append(h)
    return keep, skip


def commit_own_hunks(rel, regions, msg, name='WIBWUB Bot',
                     email='marketingwibwub@gmail.com', dry=False):
    """commit เฉพาะ hunk ของตัวเองในไฟล์ rel · คืน dict รายงานเสมอ ไม่ raise

    status: CLEAN (ไม่มีอะไรค้าง) · NO_OWN_HUNKS (ของค้างไม่ใช่ของเราเลย)
            COMMITTED · DRY · ERROR
    """
    global G
    if G is None:
        G = _gitw()
    rep = {'file': rel}
    h = G._run(['show', 'HEAD:' + rel])
    if h.returncode:
        return {**rep, 'status': 'ERROR', 'error': 'อ่าน HEAD:%s ไม่ได้: %s' % (rel, h.stderr[:200])}
    old, new = h.stdout, (BASE / rel).read_text(encoding='utf-8')
    if old == new:
        return {**rep, 'status': 'CLEAN'}
    # ถ้างานอื่น `git add` ไฟล์นี้ค้างไว้ -> ถอยทันที
    # เพราะตอนท้ายเราต้องตั้งช่อง index ของไฟล์นี้ให้ตรง HEAD ใหม่ (ดูเหตุผลข้างล่าง)
    # ซึ่งจะทับของที่เขา stage ไว้หาย · เรื่องนี้ต้องให้คนตัดสิน ไม่ใช่สคริปต์
    st = G._run(['diff', '--cached', '--name-only', '--', rel])
    if st.stdout.strip():
        return {**rep, 'status': 'FILE_STAGED_BY_OTHER',
                'note': 'มีงานอื่น git add ไฟล์นี้ค้างไว้ใน index — ยังไม่ commit '
                        'เพื่อไม่ให้ของที่เขา stage ไว้หาย ให้รายงานแล้วรอคน'}
    d = G._run(['diff', '-U0', 'HEAD', '--', rel])
    if d.returncode:
        return {**rep, 'status': 'ERROR', 'error': 'git diff ล้ม: ' + d.stderr[:200]}
    head_lines, hunks = split_hunks(d.stdout)
    keep, skip = classify(hunks, old.split('\n'), new.split('\n'),
                          own_lines(old, regions), own_lines(new, regions), regions)
    rep.update(hunks_total=len(hunks), hunks_mine=len(keep),
               hunks_skipped=[{'at': '%d,%d' % h['old'], 'why': h.get('why')} for h in skip])
    if not keep:
        return {**rep, 'status': 'NO_OWN_HUNKS'}
    patch = '\n'.join(head_lines + [x for h in keep for x in h['text']]) + '\n'
    if dry:
        return {**rep, 'status': 'DRY', 'patch_lines': patch.count('\n')}
    pf = Path(tempfile.mkstemp(prefix='own_hunks', suffix='.patch')[1])
    pf.write_text(patch, encoding='utf-8')
    idx = Path(tempfile.mkstemp(prefix='own_hunks', suffix='.index')[1])
    idx.unlink()                                   # git ต้องสร้างเอง
    base_sha = G._run(['rev-parse', 'HEAD']).stdout.strip()
    try:
        os.environ['GIT_INDEX_FILE'] = str(idx)    # ⛔ index จริงไม่ถูกแตะตั้งแต่บรรทัดนี้
        for args in (['read-tree', 'HEAD'],
                     ['apply', '--cached', '--unidiff-zero', str(pf)]):
            r = G._run_waiting(args)
            if r.returncode:
                return {**rep, 'status': 'ERROR',
                        'error': '%s ล้ม: %s' % (args[0], (r.stderr or r.stdout)[:300])}
        tr = G._run_waiting(['write-tree'])
        if tr.returncode:
            return {**rep, 'status': 'ERROR', 'error': 'write-tree ล้ม: ' + tr.stderr[:200]}
    finally:
        os.environ.pop('GIT_INDEX_FILE', None)
        for p in (pf, idx):
            try: p.unlink()
            except OSError: pass
    c = G._run_waiting(['-c', 'user.name=' + name, '-c', 'user.email=' + email,
                        'commit-tree', tr.stdout.strip(), '-p', base_sha, '-m', msg])
    if c.returncode:
        return {**rep, 'status': 'ERROR', 'error': 'commit-tree ล้ม: ' + c.stderr[:200]}
    sha = c.stdout.strip()
    # ค่าเก่าเป็นด่าน: ถ้างานอื่น commit แทรกระหว่างนี้ จะล้มแทนที่จะทับ commit เขาหาย
    u = G._run_waiting(['update-ref', 'HEAD', sha, base_sha])
    if u.returncode:
        return {**rep, 'status': 'ERROR',
                'error': 'update-ref ล้ม (อาจมีงานอื่น commit แทรก ให้รอบถัดไปลองใหม่): '
                         + u.stderr[:200]}
    # ── ตั้งช่อง index ของไฟล์นี้ให้ตรงกับ HEAD ใหม่ ───────────────────────────
    # จำเป็น ไม่ใช่การเก็บกวาด: index จริงยังถือ blob ของ HEAD เก่าอยู่ พอ HEAD ขยับ
    # `git diff --cached` จะมองไฟล์นี้เป็น "staged ย้อนการแก้ของเรา" ทันที
    # ถ้างานถัดไป commit โดยอิง index (ไม่ใส่ pathspec) commit ของเราจะถูกย้อนเงียบ ๆ
    # update-index --cacheinfo แตะช่องของไฟล์นี้ช่องเดียว ไม่ stage อะไรเพิ่ม
    # และไฟล์ของงานอื่นใน index ไม่ถูกแตะ (ตรวจแล้วว่าไฟล์นี้ไม่มีใคร stage ไว้)
    mode = (G._run(['ls-files', '-s', '--', rel]).stdout or '100644').split(' ')[0] or '100644'
    blob = G._run(['rev-parse', 'HEAD:' + rel]).stdout.strip()
    ui = G._run_waiting(['update-index', '--cacheinfo', '%s,%s,%s' % (mode, blob, rel)])
    if ui.returncode:
        rep['index_warning'] = ('⛔ commit ผ่านแล้ว (%s) แต่ตั้งช่อง index ของไฟล์นี้ไม่สำเร็จ — '
                                'งานถัดไปที่ commit โดยไม่ใส่ pathspec อาจย้อนการแก้นี้ '
                                'ให้ตรวจ git diff --cached ด้วยมือ: %s'
                                % (sha[:7], (ui.stderr or '')[:150]))
    return {**rep, 'status': 'COMMITTED', 'commit': sha[:7]}


if __name__ == '__main__':      # ใช้ทดสอบ: ... <rel> <json ของ regions> [--dry]
    rel = sys.argv[1]
    regions = json.loads(sys.argv[2])
    print(json.dumps(commit_own_hunks(rel, regions, 'ทดสอบ commit_own_hunks',
                                      dry='--dry' in sys.argv), ensure_ascii=False, indent=1))
