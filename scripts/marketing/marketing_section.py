#!/usr/bin/env python3
"""แทรกเมนู "การตลาด vs ยอดขาย" เข้า WIBWUB_Dashboard.html + WIBWUB_Mobile.html

รันครั้งเดียวเพื่อวาง "โครง" (เมนู + section + ฟังก์ชัน render + บล็อกข้อมูลเปล่า)
หลังจากนั้นตัวเลขทั้งหมดดูแลโดย `marketing_update.py` ซึ่งเขียนทับเฉพาะในบล็อก
`/* MKT_SPEND:AUTO-START */ ... /* MKT_SPEND:AUTO-END */`

สคริปต์นี้ **idempotent**: ถ้าเจอของเดิมอยู่แล้วจะไม่แทรกซ้ำ
ใช้:  python3 scripts/marketing/marketing_section.py [--dry-run]
"""
import sys, re, json, argparse, subprocess, tempfile
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
DASH, MOB = BASE / 'WIBWUB_Dashboard.html', BASE / 'WIBWUB_Mobile.html'
START = '/* MKT_SPEND:AUTO-START */'
END = '/* MKT_SPEND:AUTO-END */'

EMPTY_BLOCK = START + '\nconst MKT_SPEND = {"asof":"","months":[]};\n' + END

# ── CSS ที่ใช้ร่วมกันทั้ง 2 หน้า ───────────────────────────────────────────────
CSS = """
<style id="mks-css">
.mks-wrap{font-size:13px}
.mks-tbl{width:100%;border-collapse:collapse;font-size:12.5px;white-space:nowrap}
.mks-tbl th,.mks-tbl td{padding:7px 9px;border-bottom:1px solid var(--border);text-align:right}
.mks-tbl th{font-size:11px;color:var(--muted);font-weight:600;text-align:right;
  background:rgba(0,0,0,.02);position:sticky;top:0}
.mks-tbl th:first-child,.mks-tbl td:first-child{text-align:left;font-weight:600}
.mks-tbl tr:last-child td{border-bottom:none}
.mks-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.mks-na{color:var(--muted);font-weight:500;font-style:italic}
.mks-tot{font-weight:700}
.mks-note{margin-top:10px;font-size:11.5px;color:var(--muted);line-height:1.8}
.mks-note b{color:#b45309}
.mks-legend{display:flex;flex-wrap:wrap;gap:12px;margin:2px 0 14px;font-size:11.5px;color:var(--muted)}
.mks-lg{display:flex;align-items:center;gap:5px}
.mks-sw{width:11px;height:11px;border-radius:3px;display:inline-block}
.mks-chart{display:flex;gap:26px;align-items:flex-end;padding:8px 2px 0;overflow-x:auto}
.mks-mo{display:flex;flex-direction:column;align-items:center;gap:7px;min-width:96px}
.mks-cols{display:flex;gap:9px;align-items:flex-end;height:188px}
.mks-col{width:34px;display:flex;flex-direction:column;justify-content:flex-end;
  border-radius:4px 4px 0 0;overflow:hidden}
.mks-seg{width:100%}
.mks-cap{font-size:10.5px;color:var(--muted);text-align:center;line-height:1.5}
.mks-mol{font-size:12px;font-weight:600}
</style>
"""

# ── ฟังก์ชัน render ที่ใช้ร่วมกัน ─────────────────────────────────────────────
JS = """
<script id="mks-js">
/* เมนู "การตลาด vs ยอดขาย" — อ่านจาก MKT_SPEND ที่ marketing_update.py เขียนไว้
   ยอดขายอ่านจาก TOTAL_REV ในหน้า (แหล่งเดียวกับกราฟอื่น) ถ้าไม่มีจึงใช้ค่าที่ฝังมา */
const MKS_CAT = [
  {k:'sh',    n:'Ads Shopee',  c:'#ee4d2d'},
  {k:'tk',    n:'Ads TikTok',  c:'#111111'},
  {k:'lz',    n:'Ads Lazada',  c:'#1b04a1'},
  {k:'fb',    n:'Ads Facebook',c:'#1877f2'},
  {k:'kol',   n:'KOL',         c:'#8b5cf6'},
  {k:'event', n:'Event',       c:'#f59e0b'}
];
const MKS_REVC = '#22c55e';
function mksNum(v){return v==null?null:Math.round(v).toLocaleString('en-US');}
function mksRev(r){
  try{ if(typeof TOTAL_REV!=='undefined' && TOTAL_REV[r.i]!=null) return TOTAL_REV[r.i]; }catch(e){}
  return r.rev;
}
function renderMktSpend(elId){
  const el=document.getElementById(elId); if(!el) return;
  const D=(typeof MKT_SPEND!=='undefined')?MKT_SPEND:null;
  if(!D||!D.months||!D.months.length){el.innerHTML='<div class="mks-note">ยังไม่มีข้อมูล</div>';return;}
  const rows=D.months;
  const miss=MKS_CAT.filter(c=>rows.every(r=>r[c.k]==null));

  let h='<div class="mks-wrap">';
  h+='<div class="mks-legend"><span class="mks-lg"><i class="mks-sw" style="background:'+MKS_REVC+'"></i>ยอดขายรวม</span>';
  MKS_CAT.forEach(c=>{h+='<span class="mks-lg"><i class="mks-sw" style="background:'+c.c+
    (miss.includes(c)?';opacity:.25':'')+'"></i>'+c.n+(miss.includes(c)?' (รอข้อมูล)':'')+'</span>';});
  h+='</div>';

  /* ── ตาราง ─────────────────────────────────────────────── */
  h+='<div class="mks-scroll"><table class="mks-tbl"><thead><tr><th>เดือน</th><th>ยอดขายรวม</th>';
  MKS_CAT.forEach(c=>{h+='<th>'+c.n+'</th>';});
  h+='<th>ค่าการตลาดรวม</th><th>% ต่อยอดขาย</th><th>ยอดขาย/ค่าการตลาด</th></tr></thead><tbody>';
  rows.forEach(r=>{
    const rev=mksRev(r);
    h+='<tr><td>'+r.label+'</td><td>'+mksNum(rev)+'</td>';
    MKS_CAT.forEach(c=>{
      h+= r[c.k]==null ? '<td class="mks-na">รอข้อมูล</td>' : '<td>'+mksNum(r[c.k])+'</td>';
    });
    const spend=MKS_CAT.reduce((s,c)=>s+(r[c.k]||0),0);
    h+='<td class="mks-tot">'+mksNum(spend)+'</td>';
    h+='<td class="mks-tot">'+(rev?(spend/rev*100).toFixed(2)+'%':'-')+'</td>';
    h+='<td class="mks-tot">'+(spend?(rev/spend).toFixed(2)+'x':'-')+'</td></tr>';
  });
  h+='</tbody></table></div>';

  /* ── กราฟแท่ง: ยอดขาย เทียบ ค่าการตลาด (ซ้อนสีตามประเภท) ── */
  const mx=Math.max(...rows.map(r=>mksRev(r)));
  h+='<div class="mks-chart">';
  rows.forEach(r=>{
    const rev=mksRev(r), spend=MKS_CAT.reduce((s,c)=>s+(r[c.k]||0),0);
    h+='<div class="mks-mo"><div class="mks-cols">';
    h+='<div class="mks-col" title="ยอดขาย '+mksNum(rev)+'" style="height:'+(rev/mx*100)+'%;background:'+MKS_REVC+'"></div>';
    h+='<div class="mks-col" title="ค่าการตลาด '+mksNum(spend)+'" style="height:'+(spend/mx*100)+'%">';
    MKS_CAT.forEach(c=>{ const v=r[c.k]||0; if(v>0)
      h+='<div class="mks-seg" title="'+c.n+' '+mksNum(v)+'" style="height:'+(v/spend*100)+'%;background:'+c.c+'"></div>';});
    h+='</div></div>';
    h+='<div class="mks-mol">'+r.label+'</div>';
    h+='<div class="mks-cap">'+mksNum(rev)+'<br>vs '+mksNum(spend)+'<br>'+(rev?(spend/rev*100).toFixed(1)+'%':'')+'</div>';
    h+='</div>';
  });
  h+='</div>';

  /* ── หมายเหตุ ───────────────────────────────────────────── */
  h+='<div class="mks-note">';
  if(miss.length) h+='<b>⚠️ % ต่อยอดขายยังไม่รวม '+miss.map(c=>c.n).join(' และ ')+
    '</b> — ยังไม่มีข้อมูล จึงเว้นไว้ ไม่ได้นับเป็น 0<br>';
  const pend=rows.filter(r=>r.kol_pending>0);
  if(pend.length) h+='KOL รอจ่าย (ยังไม่นับในยอดหลัก): '+
    pend.map(r=>r.label+' '+mksNum(r.kol_pending)+' บาท'+(r.kol_pending_n?' ('+r.kol_pending_n+' ราย)':'')).join(' · ')+'<br>';
  h+='KOL นับเฉพาะ Status = Done ตามวันที่ทำจ่าย · ข้อมูลครอบถึง '+
    rows.map(r=>r.label+' ถึง '+r.cov).join(' · ')+'<br>';
  h+='ตัดข้อมูลที่ '+(D.asof||'-')+' ให้ตรงกับฝั่งยอดขาย (SALES_ASOF)';
  h+='</div></div>';
  el.innerHTML=h;
}
</script>
"""

DASH_SECTION = """
    <!-- ═══ การตลาด vs ยอดขาย ═══ -->
    <section id="mktspend" class="section">
      <div class="card" style="background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:18px;box-shadow:var(--shadow)">
        <div id="mks-dash"></div>
      </div>
    </section>
"""

MOB_VIEW = """
  <div class="sv" id="m-sv-4">
    <div class="card"><div class="sec-title">การตลาด vs ยอดขาย</div><div id="mks-mob"></div></div>
  </div>
"""


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def once(t, anchor, add, where='after'):
    """แทรก add รอบ anchor ครั้งเดียว — ถ้ามี add อยู่แล้วคืนค่าเดิม"""
    if add.strip() and add.strip()[:60] in t: return t, False
    i = t.find(anchor)
    if i < 0: die('ไม่พบจุดแทรก', anchor[:80])
    return (t[:i + len(anchor)] + add + t[i + len(anchor):] if where == 'after'
            else t[:i] + add + t[i:]), True


def node_check(text, tag):
    js = Path(tempfile.gettempdir()) / f'mks_{tag}.js'
    js.write_text('\n;\n'.join(re.findall(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', text)),
                  encoding='utf-8')
    r = subprocess.run(['node', '--check', str(js)], capture_output=True, text=True)
    if r.returncode: die(f'node --check ไม่ผ่าน ({tag})', r.stderr[:400])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    rep = {}

    # ── Dashboard ───────────────────────────────────────────────────────────
    t = DASH.read_text(encoding='utf-8'); hits = []
    t, c = once(t, '<div class="nav-item" data-sec="affiliate" onclick="go(\'affiliate\',this)">'
                   '<span class="nav-icon">🤝</span><span>Affiliate</span></div>',
                '\n    <div class="nav-item" data-sec="mktspend" onclick="go(\'mktspend\',this)">'
                '<span class="nav-icon">📊</span><span>การตลาด vs ยอดขาย</span></div>'); hits.append(('nav', c))
    t, c = once(t, '    <!-- ═══ SOCIAL ═══ -->', DASH_SECTION, where='before'); hits.append(('section', c))
    if "mktspend:'📊" not in t:
        t = t.replace("const TITLES = {overview:", "const TITLES = {mktspend:'📊 การตลาด vs ยอดขาย',overview:", 1)
        hits.append(('title', True))
    for role in ('admin', 'head_marketing'):
        m = re.search(role + r":\s*(\[[^\]]*\])", t)
        if m and "'mktspend'" not in m.group(1):
            t = t[:m.start(1)] + m.group(1)[:-1] + ",'mktspend']" + t[m.end(1):]
            hits.append((f'role:{role}', True))
    if START not in t:
        t = t.replace('</body>', CSS + JS.replace('</script>', EMPTY_BLOCK + '\n</script>') +
                      '\n<script>document.addEventListener("DOMContentLoaded",function(){'
                      'try{renderMktSpend("mks-dash");}catch(e){console.error(e);}});</script>\n</body>', 1)
        hits.append(('block', True))
    node_check(t, 'dash')
    rep['WIBWUB_Dashboard.html'] = dict(hits)
    if not a.dry_run and any(v for _, v in hits): DASH.write_text(t, encoding='utf-8')

    # ── Mobile ──────────────────────────────────────────────────────────────
    t = MOB.read_text(encoding='utf-8'); hits = []
    t, c = once(t, '<div class="stab" onclick="mTab(3,this)">Social Media</div>',
                '\n    <div class="stab" onclick="mTab(4,this)">การตลาด vs ยอดขาย</div>'); hits.append(('tab', c))
    t, c = once(t, '    <div id="tt-clips"></div>\n  </div>\n', MOB_VIEW); hits.append(('view', c))
    if START not in t:
        t = t.replace('</body>', CSS.replace('mks-css', 'mks-css-m') +
                      JS.replace('mks-js', 'mks-js-m').replace('</script>', EMPTY_BLOCK + '\n</script>') +
                      '\n<script>document.addEventListener("DOMContentLoaded",function(){'
                      'try{renderMktSpend("mks-mob");}catch(e){console.error(e);}});</script>\n</body>', 1)
        hits.append(('block', True))
    node_check(t, 'mob')
    rep['WIBWUB_Mobile.html'] = dict(hits)
    if not a.dry_run and any(v for _, v in hits): MOB.write_text(t, encoding='utf-8')

    print(json.dumps({'status': 'DRY_RUN' if a.dry_run else 'OK', 'inserted': rep},
                     ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
