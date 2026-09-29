# -*- coding: utf-8 -*-
"""Drafts 2.4.6.2.1 to 2.4.6.2.5: tabs for the product, boxes side by side for
the options, after 2.4.6.2 came closest. Five ways to make the tabs clear on a
phone, and a few ways to lay the boxes left to right.

Shared by all five, on top of 2.4.6.x: the tabs are navigation, so one tab is
open (the first) but no option is chosen; each tab remembers its own choice
when you switch away and back; the tab bar is not redrawn on a switch, only the
panel under it."""
import io, re

src = io.open('build/v2461.py', encoding='utf-8').read()
ns = {}
exec(src[:src.index("build('2.4.6.1'")], ns)       # core, shared CSS, the 2.4.6.2 tiles, build()
build, V2_CSS = ns['build'], ns['V2_CSS']
v2 = ns['V2_JS']
TL_JS = v2[v2.index('  function tl('):v2.index('  function renderOpts')]   # the 2.4.6.2 price first tiles

# the core, with two switches the tab drafts need
core = ns['CORE_JS']
def patch(old, new):
    global core
    assert core.count(old) == 1, old[:60]
    core = core.replace(old, new)
patch("var st={kind:null,stay:null,plan:null,pay:null,pack:null,insured:false}, cur=null;",
      "var st={kind:null,stay:null,plan:null,pay:null,pack:null,insured:false}, cur=null, keepChoices=false, PLANHINT=null;")
patch("set('How often will you train?',list('plan',ITEMS.plan()),HINT)",
      "set('How often will you train?',list('plan',ITEMS.plan()),PLANHINT===null?HINT:PLANHINT)")
patch("if(st.kind!==t.value){ st.stay=st.plan=st.pay=st.pack=null; E.track('pricing_kind',{kind:t.value}) }",
      "if(st.kind!==t.value){ if(!keepChoices) st.stay=st.plan=st.pay=st.pack=null; E.track('pricing_kind',{kind:t.value}) }")
ns['CORE_JS'] = core
build.__globals__['CORE_JS'] = core

TAB_CSS = V2_CSS + '''
/* ---------- 2.4.6.2.x shared: tab bar, then a panel of boxes ---------- */
.pc-tabset{margin:0}
.tp{margin-top:24px}
.tp-lead{font-size:14px;line-height:20px;color:#4A4A4A;margin:0 0 24px;max-width:56ch}
.tp .pc-set{margin-bottom:32px}
.tp .pc-set:last-child{margin-bottom:0}
@media (max-width:768px){ .tp .pc-set{margin-bottom:24px} .tp .tl.n3 .tl-i{padding:12px 8px} }
'''

TAB_JS = TL_JS + '''
  st.kind='pass'; keepChoices=true; PLANHINT='';
  var LEAD={
    pass:'No commitment. Sports insurance, the gym and every class included.',
    mem:'Paid every 2 weeks, plus the '+money(P.insurance.year)+' sports insurance once a year. Prices at reception; direct debit takes '+money(off)+' off each payment.',
    pt:'One to one with a coach. Bring someone with you and the second person is '+money(P.pt.second)+' a session.'
  };
  /* the panel's first line already says every 2 weeks, so the boxes do not repeat it */
  var planItems=ITEMS.plan, payItems=ITEMS.pay;
  ITEMS.plan=function(){ return planItems().map(function(i){ i.psub=''; return i }) };
  ITEMS.pay=function(){ return payItems().map(function(i){ i.psub=''; return i }) };
  ITEMS.pack=function(){ return P.pt.packs.map(function(k){ return {id:k.id,name:k.sessions>1?k.name:'1 session',sub:k.sessions>1?money(k.each)+' a session':'',price:money(k.total)} }) };
  function kindIndex(){ for(var i=0;i<KINDS.length;i++) if(KINDS[i].id===st.kind) return i; return 0 }
  function panel(list){ return '<p class="tp-lead">'+LEAD[st.kind]+'</p>'+subSets(list) }
  /* the tab bar is drawn once; a switch only redraws the panel */
  function tabRender(bar,list,cls){
    var p=document.getElementById('tp');
    if(p){ p.innerHTML=panel(list); opts.querySelector('.pc-tabset').style.setProperty('--i',kindIndex()); return }
    opts.innerHTML='<fieldset class="pc-set pc-tabset" style="--i:'+kindIndex()+'"><legend class="pc-sr">Choose a pass or membership</legend>'+bar()+'</fieldset>'+
      '<div class="tp'+(cls?' '+cls:'')+'" id="tp">'+panel(list)+'</div>';
  }
  function tabBar(cls,inner){ return '<div class="'+cls+'">'+KINDS.map(function(k){ return '<label class="'+cls+'-i">'+radio('kind',k.id,st.kind===k.id)+inner(k)+'</label>' }).join('')+'</div>' }
  function onPlan(){ payRefresh(tl) }
'''

# =====================================================================
# 2.4.6.2.1  Folder tabs. The open tab joins the panel under it, with a
#            black rule on top; the closed ones sit back in grey.
# =====================================================================
C1 = '''
.fd{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;position:relative;z-index:1}
.fd-i{position:relative;display:flex;align-items:center;justify-content:center;text-align:center;min-height:56px;padding:8px 12px;background:#EFEFED;border:1px solid transparent;border-bottom:0;border-radius:8px 8px 0 0;cursor:pointer;font-size:15px;line-height:20px;font-weight:700;color:#6A6A6A;text-wrap:balance;transition:color .15s,background .15s}
.fd-i:hover{color:var(--black)}
.fd-i:has(input:checked){background:var(--white);border-color:var(--line);color:var(--black);box-shadow:inset 0 3px 0 var(--black)}
.fd-i:has(input:checked)::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--white)}
.fd-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:2px}
.tp.fold{margin-top:0;border:1px solid var(--line);border-radius:0 0 8px 8px;padding:24px}
@media (max-width:768px){ .fd-i{font-size:14px;line-height:18px;padding:8px} .tp.fold{padding:16px} }
@media (max-width:374px){ .fd-i{font-size:13px} .tp.fold{padding:12px} }
'''
J1 = TAB_JS + '''
  function renderOpts(){ tabRender(function(){ return tabBar('fd',function(k){ return '<span>'+k.name+'</span>' }) },tl,'fold') }
'''

# =====================================================================
# 2.4.6.2.2  Pill tabs. Three pills, the open one black with white words;
#            the boxes under them centred, name above a big price.
# =====================================================================
C2 = '''
.pill{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.pill-i{display:flex;align-items:center;justify-content:center;text-align:center;min-height:56px;padding:8px 16px;border-radius:28px;background:var(--white);box-shadow:inset 0 0 0 1px #CFCFCF;cursor:pointer;font-size:15px;line-height:18px;font-weight:700;text-wrap:balance;transition:background .15s,color .15s,box-shadow .15s}
.pill-i:hover{box-shadow:inset 0 0 0 1px var(--black)}
.pill-i:has(input:checked){background:var(--black);color:var(--white);box-shadow:none}
.pill-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:2px}
.tp.center .tl-i{align-items:center;text-align:center}
.tp.center .tl-n{order:-1;font-weight:600;color:#4A4A4A}
.tp.center .tl-i .tag{margin-top:4px}
@media (max-width:768px){ .pill{gap:4px} .pill-i{font-size:14px;padding:8px 10px} }
@media (max-width:374px){ .pill-i{font-size:13px;padding:8px 6px} }
'''
J2 = TAB_JS + '''
  function renderOpts(){ tabRender(function(){ return tabBar('pill',function(k){ return '<span>'+k.name+'</span>' }) },tl,'center') }
'''

# =====================================================================
# 2.4.6.2.3  Big type tabs. The product names in the display face, the open
#            one black with a heavy rule under it, like the Nike app.
# =====================================================================
C3 = '''
.nk{display:grid;grid-template-columns:repeat(3,1fr);box-shadow:inset 0 -1px 0 #CFCFCF}
.nk-i{position:relative;display:flex;align-items:flex-end;justify-content:center;text-align:center;padding:8px 8px 16px;cursor:pointer;font-family:var(--font-display);font-size:26px;line-height:26px;text-transform:uppercase;color:#A3A3A3;text-wrap:balance;transition:color .15s}
.nk-i::after{content:"";position:absolute;left:0;right:0;bottom:0;height:4px;background:transparent;transition:background .15s}
.nk-i:hover{color:var(--black)}
.nk-i:has(input:checked){color:var(--black)}
.nk-i:has(input:checked)::after{background:var(--black)}
.nk-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:-2px}
@media (max-width:768px){ .nk-i{font-size:20px;line-height:20px;padding:8px 4px 16px} }
@media (max-width:374px){ .nk-i{font-size:18px;line-height:18px} }
'''
J3 = TAB_JS + '''
  function renderOpts(){ tabRender(function(){ return tabBar('nk',function(k){ return '<span>'+k.name+'</span>' }) },tl) }
'''

# =====================================================================
# 2.4.6.2.4  Card tabs with the from price. The open card turns black and
#            points down at its panel; every question is one row of boxes.
# =====================================================================
C4 = '''
.ct{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.ct-i{position:relative;display:flex;flex-direction:column;gap:8px;min-height:104px;padding:16px;background:#F2F2F0;cursor:pointer;transition:background .15s,color .15s}
.ct-i b{font-size:16px;line-height:20px;font-weight:700;text-wrap:balance}
.ct-i small{margin-top:auto;font-size:12px;line-height:16px;color:#5A5A5A;text-wrap:balance}
.ct-i small strong{display:block;font-size:15px;line-height:20px;color:var(--black)}
.ct-i:hover{background:#E8E8E6}
.ct-i:has(input:checked){background:var(--black);color:var(--white)}
.ct-i:has(input:checked) small{color:rgba(255,255,255,.7)}
.ct-i:has(input:checked) small strong{color:var(--accent)}
.ct-i:has(input:checked)::after{content:"";position:absolute;left:50%;bottom:-8px;margin-left:-8px;border:8px solid transparent;border-top-color:var(--black);border-bottom:0}
.ct-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:2px}
.tp.row1 .tl{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);grid-template-columns:none;gap:8px}
.tp.row1 .tl .tl-i{grid-column:auto}
@media (max-width:768px){
  .ct{gap:4px}
  .ct-i{padding:12px;min-height:96px}
  .ct-i b{font-size:14px;line-height:18px}
  .tp.row1 .tl{gap:4px}
  .tp.row1 .tl-i{padding:12px 8px;min-height:72px}
  .tp.row1 .tl.n4 .tl-i,.tp.row1 .tl.n5 .tl-i{padding:12px 4px;align-items:center;text-align:center}
  .tp.row1 .tl.n5 .tl-p{font-size:18px;line-height:24px}
  .tp.row1 .tl.n4 .tl-p{font-size:20px;line-height:24px}
  .tp.row1 .tl-n,.tp.row1 .tl-s{font-size:11px}
}
@media (max-width:374px){ .ct-i{padding:12px 8px} .ct-i b{font-size:13px} .tp.row1 .tl.n5 .tl-p{font-size:16px} }
'''
J4 = TAB_JS + '''
  function renderOpts(){ tabRender(function(){ return tabBar('ct',function(k){ return '<b>'+k.name+'</b><small><strong>'+k.from+'</strong>'+k.fromSub+'</small>' }) },tl,'row1') }
'''

# =====================================================================
# 2.4.6.2.5  A sliding tab bar and boxes you swipe. The black marker slides
#            to the open tab; on a phone, a question with more than three
#            answers becomes a row you swipe left to right.
# =====================================================================
C5 = '''
.sl{position:relative;display:grid;grid-template-columns:repeat(3,1fr);padding:4px;background:#EDEDEB;border-radius:12px}
.sl::before{content:"";position:absolute;top:4px;bottom:4px;left:4px;width:calc((100% - 8px) / 3);border-radius:8px;background:var(--black);transform:translateX(calc(var(--i,0) * 100%));transition:transform .25s ease}
.sl-i{position:relative;z-index:1;display:flex;align-items:center;justify-content:center;text-align:center;min-height:52px;padding:8px;cursor:pointer;font-size:15px;line-height:18px;font-weight:700;color:#5A5A5A;text-wrap:balance;transition:color .2s}
.sl-i:hover{color:var(--black)}
.sl-i:has(input:checked){color:var(--white)}
.sl-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:-2px;border-radius:8px}
@media (prefers-reduced-motion:reduce){ .sl::before{transition:none} }
@media (max-width:768px){
  .sl-i{font-size:14px}
  .tp.strip .tl.n4,.tp.strip .tl.n5{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;margin:0 -24px;padding:0 24px 4px;scroll-padding:0 24px}
  .tp.strip .tl.n4::-webkit-scrollbar,.tp.strip .tl.n5::-webkit-scrollbar{display:none}
  .tp.strip .tl.n4 .tl-i,.tp.strip .tl.n5 .tl-i{flex:0 0 36%;scroll-snap-align:start}
  .tp.strip .swipe{display:block}
}
.swipe{display:none;font-size:12px;line-height:16px;color:var(--silver-grey);margin-top:8px}
@media (max-width:374px){ .sl-i{font-size:13px;padding:8px 4px} }
'''
J5 = TAB_JS + '''
  function tlSwipe(name,items){ return tl(name,items)+(items.length>3?'<p class="swipe" aria-hidden="true">Swipe for more</p>':'') }
  function renderOpts(){ tabRender(function(){ return tabBar('sl',function(k){ return '<span>'+k.name+'</span>' }) },tlSwipe,'strip') }
  function onPlan(){ payRefresh(tlSwipe) }
'''

build('2.4.6.2.1', C1 := TAB_CSS + C1, J1)
build('2.4.6.2.2', TAB_CSS + C2, J2)
build('2.4.6.2.3', TAB_CSS + C3, J3)
build('2.4.6.2.4', TAB_CSS + C4, J4)
build('2.4.6.2.5', TAB_CSS + C5, J5)
