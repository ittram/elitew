# -*- coding: utf-8 -*-
"""Draft 2.4.7: 2.4.6 with the product boxes of 2.4.5.4.2 and the lessons of
2.4.6.x. Three product boxes (name in the display face, one line on what it
is, the from price), then the options as boxes side by side. Nothing chosen
when the page opens; a chosen box is a faint tint with a blue edge, never a
blue fill; the plan is a quiet grey box until the choice is complete. Direct
debit carries the discount tag, reception is the standard price."""
import io, re

src = io.open('build/v2461.py', encoding='utf-8').read()
ns = {}
exec(src[:src.index("# =====")], ns)          # the core, shared layout and build() of 2.4.6.x
build = ns['build']

# each product keeps its own choice when you look at another and come back
core = ns['CORE_JS']
for old, new in [
    ("var st={kind:null,stay:null,plan:null,pay:null,pack:null,insured:false}, cur=null;",
     "var st={kind:null,stay:null,plan:null,pay:null,pack:null,insured:false}, cur=null, keepChoices=false;"),
    ("if(st.kind!==t.value){ st.stay=st.plan=st.pay=st.pack=null; E.track('pricing_kind',{kind:t.value}) }",
     "if(st.kind!==t.value){ if(!keepChoices) st.stay=st.plan=st.pay=st.pack=null; E.track('pricing_kind',{kind:t.value}) }")]:
    assert core.count(old) == 1, old[:50]
    core = core.replace(old, new)
ns['CORE_JS'] = core

TODO_COACH = '<span class="pr-todo" title="[PLACEHOLDER: confirm every coach who gives personal training is certified, and by whom]">todo</span>'

CSS = '''
/* ---------- 2.4.7: the product boxes ---------- */
.pk{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.pk-i{position:relative;display:flex;flex-direction:column;gap:8px;padding:24px;background:var(--white);border:2px solid var(--light-grey);cursor:pointer;transition:border-color .15s,background .15s}
.pk-i:hover{border-color:var(--black)}
.pk-i b{font-family:var(--font-display);font-weight:400;font-size:28px;line-height:28px;text-transform:uppercase;color:var(--black)}
.pk-i span{font-size:14px;line-height:20px;color:#4A4A4A}
.pk-i i{font-style:normal;font-weight:800;font-size:11px;line-height:16px;letter-spacing:.1em;text-transform:uppercase;color:var(--royal-blue);margin-top:auto;padding-top:8px}
.pk-i:has(input:checked){border-color:var(--sel-bd);background:var(--sel-bg)}
.pk-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:2px}

/* ---------- the options: boxes side by side ---------- */
.pc-row{display:grid;gap:8px}
.pc-row.c2{grid-template-columns:repeat(2,1fr)}
.pc-row.c3{grid-template-columns:repeat(3,1fr)}
.pc-row.c4{grid-template-columns:repeat(4,1fr)}
.pc-row.c5{grid-template-columns:repeat(5,1fr)}
.pc-tile{position:relative;display:flex;flex-direction:column;gap:4px;min-height:72px;padding:12px 16px;background:var(--white);border:2px solid var(--light-grey);cursor:pointer;transition:border-color .15s,background .15s}
.pc-tile:hover{border-color:var(--black)}
.pc-tile b{font-size:15px;line-height:20px;font-weight:700}
.pc-tile small{font-size:12px;line-height:16px;color:#5A5A5A}
.pc-tile .tag{align-self:flex-start;margin-top:4px}
.pc-tile:has(input:checked){border-color:var(--sel-bd);background:var(--sel-bg)}
.pc-tile:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:2px}

@media (max-width:1100px){
  .pk-i{padding:16px}
  .pk-i b{font-size:22px;line-height:24px}
  .pc-row.c5{grid-template-columns:repeat(3,1fr)}
}
@media (max-width:768px){
  /* three product boxes stay side by side on a phone */
  .pk{gap:4px}
  .pk-i{padding:12px 8px;gap:8px}
  .pk-i b{font-size:18px;line-height:18px}
  .pk-i span{font-size:12px;line-height:16px}
  .pk-i i{font-size:10px;letter-spacing:.06em;padding-top:4px}
  .pc-row.c3{grid-template-columns:repeat(3,1fr)}
  .pc-row.c4{grid-template-columns:repeat(2,1fr)}
  .pc-row.c5{grid-template-columns:repeat(6,1fr)}
  .pc-row.c5 .pc-tile{grid-column:span 2}
  .pc-row.c5 .pc-tile:nth-child(n+4){grid-column:span 3}
  .pc-tile{min-height:64px;padding:12px}
  .pc-tile b{font-size:14px;line-height:18px}
  .pc-row.c3 .pc-tile{padding:12px 8px;justify-content:center;align-items:center;text-align:center}
  .pc-row.c3 .pc-tile b,.pc-row.c3 .pc-tile small{text-wrap:balance}
  .pc-row.c3 .pc-tile .tag{align-self:center}
  .pc-row .tag{font-size:8px;letter-spacing:.06em}
}
@media (max-width:374px){
  .pk-i b{font-size:16px;line-height:16px}
  .pk-i span{font-size:11px;line-height:15px}
  .pc-row.c3 .pc-tile b{font-size:13px}
}
'''

JS = '''
  /* the three products, in the words of 29 September */
  KINDS[0].name='Day / week passes'; KINDS[0].desc='No commitment. From 1 day to 4 weeks.';
  KINDS[1].desc='Paid every 2 weeks. Best value if you train regularly.'; KINDS[1].from='From '+money(P.member.plans[0].dd)+', every 2 weeks';
  KINDS[2].desc='One to one with a certified coach.%(todo)s'; KINDS[2].from='From '+money(P.pt.packs[P.pt.packs.length-1].each)+' a session';
  keepChoices=true;

  function cards(){
    return '<div class="pk">'+KINDS.map(function(k){
      return '<label class="pk-i">'+radio('kind',k.id,st.kind===k.id)+'<b>'+k.name+'</b><span>'+k.desc+'</span><i>'+k.from+'</i></label>';
    }).join('')+'</div>';
  }
  function tile(name,i){
    return '<label class="pc-tile">'+radio(name,i.id,st[name]===i.id)+'<b>'+i.name+'</b>'+(i.small?'<small>'+i.small+'</small>':'')+(i.tag?'<span class="tag">'+i.tag+'</span>':'')+'</label>';
  }
  function row(items,name){ return '<div class="pc-row c'+items.length+'">'+items.map(function(i){ return tile(name,i) }).join('')+'</div>' }
  function payRow(){
    var p=st.plan?E.memberPlan(st.plan):null;
    return row([
      {id:'dd',  name:'Direct debit', small:(p?money(p.dd)+' every 2 weeks<br>':'')+'Paid automatically', tag:money(off)+' off'},
      {id:'desk',name:'At reception', small:(p?money(p.desk)+' every 2 weeks<br>':'')+'Standard price'}
    ],'pay');
  }
  function renderOpts(){
    var h=set('Choose a pass or membership',cards());
    if(st.kind==='pass')
      h+=set('Choose a pass',row(P.visitor.map(function(v){ return {id:v.id,name:v.name,small:money(v.price)} }),'stay'));
    else if(st.kind==='mem')
      h+=set('How often will you train?',row(P.member.plans.map(function(p){ return {id:p.id,name:p.name,small:money(p.desk)+'<br>every 2 weeks',tag:p.best?'Recommended':''} }),'plan'),HINT)+
         set('How will you pay?',payRow(),'','pc-pay');
    else if(st.kind==='pt')
      h+=set('How many sessions?',row(P.pt.packs.map(function(k){ return {id:k.id,name:k.sessions>1?k.name:'1 session',small:money(k.total)+(k.sessions>1?'<br>'+money(k.each)+' a session':'')} }),'pack'));
    opts.innerHTML=h;
  }
  function onPlan(){ var f=document.getElementById('pc-pay'); if(f) f.outerHTML=set('How will you pay?',payRow(),'','pc-pay') }
''' % {'todo': TODO_COACH.replace("'", "\\'")}

build('2.4.7', CSS, JS)
