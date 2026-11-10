# -*- coding: utf-8 -*-
"""Drafts 2.4.6.1 to 2.4.6.5: five layouts for the same price builder.
Shared by all five: nothing is chosen until the visitor chooses; a chosen
option is a subtle tone (thin blue edge, faint blue tint), never a blue fill;
the plan stays a quiet placeholder until a choice is complete; the page is
prepared exactly as 2.4.6 (words, grid, the phone bar)."""
import io, re

src = io.open('build/v246.py', encoding='utf-8').read()
ns = {}
exec(src[:src.index("CSS = '''")], ns)          # the page as 2.4.6 prepares it
BASE = ns['s']

SHARED_CSS = '''
/* ---------- 2.4.6.x shared: layout, calm selection, the plan ---------- */
:root{--sel-bd:var(--royal-blue);--sel-bg:rgba(43,62,170,.06);--line:#E5E5E5}
.pc{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;align-items:start}
.pc-opts{grid-column:1 / span 7;min-width:0}
.pc-plan{grid-column:9 / span 4;position:sticky;top:96px;min-width:0}
.pc-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.pc-set{border:0;padding:0;margin:0 0 40px;min-width:0}
.pc-set:last-child{margin-bottom:0}
.pc-leg{font-weight:800;font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey);padding:0;margin-bottom:16px}
.pc-hint{font-size:13px;line-height:20px;color:var(--silver-grey);margin:-8px 0 16px}
.pc-set.next>.pc-leg{color:var(--black)}
.pc-leg{transition:color .2s}
.pc-opts input[type=radio]{position:absolute;opacity:0;pointer-events:none}
.tag{display:inline-block;background:var(--accent);color:var(--black);font-weight:800;font-size:9px;line-height:16px;letter-spacing:.08em;text-transform:uppercase;padding:0 4px;vertical-align:1px}

/* list rows: a radio, the name, the price on the right */
.lr{box-shadow:inset 0 1px 0 var(--line)}
.lr-i{position:relative;display:grid;grid-template-columns:20px 1fr auto;align-items:center;column-gap:16px;min-height:56px;padding:12px 16px;box-shadow:inset 0 -1px 0 var(--line);cursor:pointer;transition:background .15s}
.lr-i:hover{background:#FAFAF8}
.lr-dot{width:20px;height:20px;border-radius:50%;box-shadow:inset 0 0 0 2px #BDBDBD;transition:box-shadow .15s}
.lr-n{font-size:15px;line-height:20px;font-weight:600}
.lr-n small{display:block;font-weight:400;font-size:12px;line-height:16px;color:var(--silver-grey);margin-top:2px}
.lr-p{font-size:15px;line-height:20px;font-weight:700;white-space:nowrap;text-align:right}
.lr-p small{display:block;font-weight:400;font-size:11px;line-height:16px;color:var(--silver-grey)}
.lr-i:has(input:checked){background:var(--sel-bg)}
.lr-i:has(input:checked) .lr-dot{box-shadow:inset 0 0 0 6px var(--sel-bd)}
.lr-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:-2px}

/* segmented control: one track, the chosen segment lifts to white */
.seg{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:4px;background:#F0F0EE;border-radius:12px}
.seg-i{position:relative;display:flex;align-items:center;justify-content:center;text-align:center;min-height:48px;padding:8px;border-radius:8px;cursor:pointer;font-size:14px;line-height:18px;font-weight:600;color:#5a5a5a;text-wrap:balance;transition:background .15s,color .15s,box-shadow .15s}
.seg-i:hover{color:var(--black)}
.seg-i:has(input:checked){background:var(--white);color:var(--black);box-shadow:0 1px 3px rgba(0,0,0,.12)}
.seg-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:2px}

/* the plan: quiet until a choice is complete */
.pc-empty{background:#F6F6F4;padding:32px;min-height:160px}
.pc-empty p{font-size:15px;line-height:24px;color:#6a6a6a}
.pc-empty .pc-k{font-size:11px;line-height:16px;color:var(--silver-grey)}
.pc-card{background:var(--black);color:var(--white);padding:32px;animation:pcIn .2s ease both}
@keyframes pcIn{from{opacity:0}to{opacity:1}}
.pc-k{font-weight:800;font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.55);margin-bottom:16px}
.pc-n{font-size:18px;line-height:24px;font-weight:700}
.pc-lines{margin-top:16px}
.pc-line{display:flex;justify-content:space-between;gap:16px;padding:8px 0;box-shadow:inset 0 -1px 0 rgba(255,255,255,.18);font-size:14px;line-height:24px}
.pc-line b{font-weight:700;white-space:nowrap}
.pc-ins{display:flex;align-items:center;gap:16px;margin-top:16px;cursor:pointer;font-size:13px;line-height:20px;color:rgba(255,255,255,.85)}
.pc-ins input{appearance:none;flex:0 0 40px;width:40px;height:24px;border-radius:12px;background:rgba(255,255,255,.25);position:relative;cursor:pointer;margin:0;transition:background .15s}
.pc-ins input::after{content:"";position:absolute;top:4px;left:4px;width:16px;height:16px;border-radius:50%;background:var(--white);transition:transform .15s}
.pc-ins input:checked{background:var(--royal-blue)}
.pc-ins input:checked::after{transform:translateX(16px)}
.pc-ins input:focus-visible{outline:2px solid var(--white);outline-offset:2px}
.pc-total{display:flex;justify-content:space-between;align-items:baseline;gap:16px;margin-top:24px}
.pc-total span{font-size:13px;line-height:16px;color:rgba(255,255,255,.6)}
.pc-total b{font-family:var(--font-display);font-size:48px;line-height:48px;color:var(--accent);white-space:nowrap}
.pc-note{font-size:12px;line-height:16px;color:rgba(255,255,255,.6);margin-top:16px}
.pc-card .btn{width:100%;justify-content:center;margin-top:24px}
@media (prefers-reduced-motion:reduce){ .pc-card{animation:none} }

.bar-price{display:none}
@media (max-width:1100px){ .pc-opts{grid-column:1 / span 7} .pc-plan{grid-column:8 / span 5} }
@media (max-width:768px){
  .pc{display:block}
  .pc-plan{position:static;margin-top:32px}
  .pc-set{margin-bottom:32px}
  .lr-i{padding:12px 8px;column-gap:12px}
  .pc-empty{padding:24px;min-height:0}
  .pc-card{padding:24px}
  .pc-total b{font-size:40px;line-height:40px}
  /* the page bar carries the plan only once there is one, and steps aside for the plan's own button */
  html.in-prices.has-plan .action-bar>.bar-status,html.in-prices.has-plan .action-bar>.btn{display:none}
  html.in-prices.has-plan .action-bar .bar-price{display:flex}
  html.in-prices.card-visible .action-bar{transform:translateY(110%)}
  .bar-price{flex:1 1 auto;align-items:center;gap:16px;min-width:0}
  .bp-txt{flex:1 1 auto;min-width:0}
  .bp-txt>span{display:block;font-size:13px;line-height:16px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bp-txt small{display:block;font-weight:800;font-size:10px;line-height:16px;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.55)}
  .bar-price b{font-family:var(--font-display);font-size:24px;line-height:24px;color:var(--accent);white-space:nowrap}
  .bar-price .btn{flex:0 0 auto;padding:16px;font-size:.85rem}
}
'''

CORE_JS = '''
(function(){
  var E=window.EWPricing, opts=document.getElementById('pc-opts'), box=document.getElementById('pc-plan');
  if(!E||!opts||!box) return;
  var P=E.P, money=E.money, off=P.member.plans[0].desk-P.member.plans[0].dd;
  function find(list,id){ return list.filter(function(x){return x.id===id})[0] }
  var KINDS=[
    {id:'pass', name:'Day and week passes', from:'From '+money(P.visitor[0].price), fromSub:''},
    {id:'mem',  name:'Membership',          from:'From '+money(P.member.plans[0].dd), fromSub:'every 2 weeks, direct debit'},
    {id:'pt',   name:'Personal training',   from:'From '+money(P.pt.packs[P.pt.packs.length-1].each), fromSub:'a session'}
  ];
  /* nothing is chosen until the visitor chooses */
  var st={kind:null,stay:null,plan:null,pay:null,pack:null,insured:false}, cur=null;

  function radio(name,value,checked){ return '<input type="radio" name="'+name+'" value="'+value+'"'+(checked?' checked':'')+'>' }
  function set(legend,body,hint,id){ return '<fieldset class="pc-set"'+(id?' id="'+id+'"':'')+'><legend class="pc-leg">'+legend+'</legend>'+(hint?'<p class="pc-hint">'+hint+'</p>':'')+body+'</fieldset>' }
  function rows(name,items){
    return '<div class="lr">'+items.map(function(i){
      return '<label class="lr-i">'+radio(name,i.id,st[name]===i.id)+'<span class="lr-dot" aria-hidden="true"></span>'+
        '<span class="lr-n">'+i.name+(i.tag?' <span class="tag">'+i.tag+'</span>':'')+(i.sub?'<small>'+i.sub+'</small>':'')+'</span>'+
        '<b class="lr-p">'+(i.price||'')+(i.psub?'<small>'+i.psub+'</small>':'')+'</b></label>';
    }).join('')+'</div>';
  }
  function seg(){ return '<div class="seg">'+KINDS.map(function(k){ return '<label class="seg-i">'+radio('kind',k.id,st.kind===k.id)+'<span>'+k.name+'</span></label>' }).join('')+'</div>' }
  var ITEMS={
    stay:function(){ return P.visitor.map(function(v){ return {id:v.id,name:v.name,price:money(v.price)} }) },
    plan:function(){ return P.member.plans.map(function(p){ return {id:p.id,name:p.name,price:money(p.desk),psub:'every 2 weeks',tag:p.best?'Recommended':''} }) },
    pay:function(){ var p=st.plan?E.memberPlan(st.plan):null;
      return [{id:'dd',name:'Direct debit',sub:money(off)+' off each payment',price:p?money(p.dd):'',psub:p?'every 2 weeks':''},
              {id:'desk',name:'At reception',sub:'Standard price',price:p?money(p.desk):'',psub:p?'every 2 weeks':''}] },
    pack:function(){ return P.pt.packs.map(function(k){ return {id:k.id,name:k.sessions>1?k.name:'Single session',sub:k.sessions>1?money(k.each)+' a session, valid '+k.months+' months':'',price:money(k.total)} }) }
  };
  var HINT='Prices every 2 weeks at reception. Direct debit takes '+money(off)+' off each payment.';
  function subSets(list){
    if(st.kind==='pass') return set('Choose a pass',list('stay',ITEMS.stay()));
    if(st.kind==='mem') return set('How often will you train?',list('plan',ITEMS.plan()),HINT)+set('How will you pay?',list('pay',ITEMS.pay()),'','pc-pay');
    if(st.kind==='pt') return set('How many sessions?',list('pack',ITEMS.pack()));
    return '';
  }
  function stdOpts(kindHtml,list){ return set('Choose a pass or membership',kindHtml)+subSets(list) }
  function payRefresh(list){ var f=document.getElementById('pc-pay'); if(f) f.outerHTML=set('How will you pay?',list('pay',ITEMS.pay()),'','pc-pay') }
  /* a subtle guide: the question still waiting for an answer has the darker heading */
  function guide(){
    var done=false;
    [].forEach.call(opts.querySelectorAll('fieldset'),function(f){
      var next=!done&&!f.querySelector('input:checked'); f.classList.toggle('next',next); if(next) done=true;
    });
  }

  function missing(){
    if(!st.kind) return 'Choose a pass or membership to see your price.';
    if(st.kind==='pass'&&!st.stay) return 'Choose a pass to see your price.';
    if(st.kind==='mem'&&!st.plan) return 'Choose how often you will train.';
    if(st.kind==='mem'&&!st.pay) return 'Choose how you will pay.';
    if(st.kind==='pt'&&!st.pack) return 'Choose how many sessions.';
    return null;
  }
%VARIANT%
  function plan(){
    var lines=[], notes=[], total, title, id, label;
    if(st.kind==='pass'){
      var v=find(P.visitor,st.stay);
      title=v.days===1?'Day pass':v.name+' pass'; id=v.id; total=v.price; label='To pay at reception';
      lines=[[title,money(v.price)],['Sports insurance','Included']];
      if(v.days<4) notes.push('Paid each time you come. From four days on, the week pass costs less.');
      if(v.days>=28) notes.push('Four weeks of membership is '+money(E.fourWeeks().member)+' with the insurance, and it keeps going after four weeks.');
    } else if(st.kind==='mem'){
      var p=E.memberPlan(st.plan), dd=st.pay==='dd', rate=dd?p.dd:p.desk;
      title=p.name+' membership'; id=p.id; label='To pay on your first visit';
      lines=[[p.name+', first 2 weeks',money(p.desk)]];
      if(dd) lines.push(['Direct debit discount',money(p.desk-p.dd)+' off']);
      if(st.insured){ lines.push(['Sports insurance','Already paid']); total=rate }
      else { lines.push(['Sports insurance, once a year',money(P.insurance.year)]); total=rate+P.insurance.year }
      notes.push(dd ? 'Then '+money(p.dd)+' every 2 weeks by direct debit. That saves you '+money(P.member.ddSavingYear)+' a year.'
                    : 'Then '+money(p.desk)+' every 2 weeks. With direct debit it is '+money(p.dd)+', a saving of '+money(P.member.ddSavingYear)+' a year.');
    } else {
      var k=find(P.pt.packs,st.pack);
      title=k.sessions>1?'Personal training, '+k.sessions+' sessions':'Personal training, one session'; id=k.id; total=k.total; label='To pay at reception';
      lines=[[title,money(k.total)]];
      if(k.sessions>1) lines.push([money(k.each)+' a session','valid '+k.months+' months']);
      notes.push('Bring someone with you and the second person is '+money(P.pt.second)+' a session.');
      if(k.sessions>1) notes.push(P.pt.note);
    }
    return {id:id,title:title,price:total,totalLabel:label,lines:lines,notes:notes};
  }

  var root=document.documentElement;
  function renderPlan(){
    var m=missing();
    if(m){
      cur=null; root.classList.remove('has-plan','card-visible');
      box.innerHTML='<div class="pc-empty"><p class="pc-k">Your plan</p><p>'+m+'</p></div>';
      document.getElementById('pc-live').textContent='';
      if(co) co.disconnect();
      return;
    }
    cur=plan();
    box.innerHTML='<div class="pc-card">'+
      '<p class="pc-k">Your plan</p><p class="pc-n">'+cur.title+'</p>'+
      '<div class="pc-lines">'+cur.lines.map(function(l){ return '<div class="pc-line"><span>'+l[0]+'</span><b>'+l[1]+'</b></div>' }).join('')+'</div>'+
      (st.kind==='mem'?'<label class="pc-ins"><input type="checkbox" id="pc-ins"'+(st.insured?' checked':'')+'><span>My sports insurance is already paid this year</span></label>':'')+
      '<div class="pc-total"><span>'+cur.totalLabel+'</span><b>'+money(cur.price)+'</b></div>'+
      (cur.notes.length?'<p class="pc-note">'+cur.notes.join(' ')+'</p>':'')+
      '<button class="btn" type="button" id="pc-go">Get this plan</button></div>';
    document.getElementById('pc-live').textContent=cur.title+', '+money(cur.price)+'.';
    document.getElementById('bp-n').textContent=cur.title;
    document.getElementById('bp-l').textContent=cur.totalLabel;
    document.getElementById('bp-p').textContent=money(cur.price);
    root.classList.add('has-plan');
    if(co){ co.disconnect(); co.observe(document.getElementById('pc-go')) }
  }

  opts.addEventListener('change',function(e){
    var t=e.target; if(t.type!=='radio') return;
    if(t.name==='kind'){
      if(st.kind!==t.value){ st.stay=st.plan=st.pay=st.pack=null; E.track('pricing_kind',{kind:t.value}) }
      st.kind=t.value; renderOpts();
      var back=opts.querySelector('input[name=kind]:checked'); if(back) back.focus();
    } else if(t.name==='cell'){ var v=t.value.split('|'); st.plan=v[0]; st.pay=v[1] }
    else { st[t.name]=t.value; if(t.name==='plan'&&typeof onPlan==='function') onPlan() }
    renderPlan(); guide();
  });
  box.addEventListener('change',function(e){
    if(e.target.id!=='pc-ins') return;
    st.insured=e.target.checked; E.track('pricing_insured',{insured:st.insured});
    renderPlan(); document.getElementById('pc-ins').focus();
  });
  box.addEventListener('click',function(e){ if(e.target.closest('#pc-go')) E.review(cur) });
  document.getElementById('bp-go').addEventListener('click',function(){ if(cur) E.review(cur) });

  var mq=window.matchMedia('(max-width:768px)'), sec=document.getElementById('prices'), inView=false, co=null;
  function mark(){ root.classList.toggle('in-prices', inView&&mq.matches) }
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){ inView=es[0].isIntersecting; mark() },{rootMargin:'-45% 0px -45% 0px'}).observe(sec);
    co=new IntersectionObserver(function(es){ root.classList.toggle('card-visible', es[0].isIntersecting) },{threshold:0.5});
  }
  if(mq.addEventListener) mq.addEventListener('change',mark); else mq.addListener(mark);
  renderOpts(); renderPlan(); guide();
})();
'''

def hover_only(css):
    return re.sub(r'(?m)^(\.[^\n{]*:hover[^\n{]*\{[^\n}]*\})$', r'@media (hover:hover){ \1 }', css)

def build(name, css, variant_js, script='a few taps, one price'):
    s = BASE
    css = hover_only(SHARED_CSS + css)
    if script != 'a few taps, one price':
        s = s.replace('<span class="section-script">a few taps, one price</span>', '<span class="section-script">%s</span>' % script, 1)
    s = s.replace('</head>', '<style>' + css + '</style>\n</head>', 1)
    s = s.replace('</body>', '<script>' + CORE_JS.replace('%VARIANT%', variant_js) + '</script>\n</body>', 1)
    f = 'elite-wellness-landing_%s.html' % name.replace('.', '-')
    io.open(f, 'w', encoding='utf-8').write(s)
    print(name, len(s))

# =====================================================================
# 2.4.6.1  Segmented control for the product, plain list rows below.
#          The iOS and Apple Store pattern: one track, the chosen segment
#          lifts to white; every option a row with its price on the right.
# =====================================================================
V1_CSS = '''
@media (max-width:374px){ .seg-i{font-size:13px;padding:8px 4px} }
'''
V1_JS = '''
  function renderOpts(){ opts.innerHTML=stdOpts(seg(),rows) }
  function onPlan(){ payRefresh(rows) }
'''

# =====================================================================
# 2.4.6.2  Underline tabs for the product, price first tiles below.
#          The Nike app pattern: tabs with a thin rule under the chosen one;
#          the price is the biggest thing on each tile, the name under it.
# =====================================================================
V2_CSS = '''
.tabs{display:grid;grid-template-columns:repeat(3,1fr);box-shadow:inset 0 -1px 0 var(--line)}
.tab{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;padding:8px 8px 16px;cursor:pointer;color:#707070;transition:color .15s}
.tab b{font-size:15px;line-height:20px;font-weight:700;text-wrap:balance}
.tab small{font-size:12px;line-height:16px;color:var(--silver-grey);text-wrap:balance}
.tab:hover{color:var(--black)}
.tab::after{content:"";position:absolute;left:8px;right:8px;bottom:0;height:2px;background:transparent;transition:background .15s}
.tab:has(input:checked){color:var(--black)}
.tab:has(input:checked)::after{background:var(--sel-bd)}
.tab:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:-2px}
.tl{display:grid;gap:8px}
.tl.n2{grid-template-columns:repeat(2,1fr)}
.tl.n3{grid-template-columns:repeat(3,1fr)}
.tl.n4{grid-template-columns:repeat(4,1fr)}
.tl.n5{grid-template-columns:repeat(5,1fr)}
.tl-i{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:4px;min-height:96px;padding:16px;background:var(--white);box-shadow:inset 0 0 0 1px var(--line);cursor:pointer;transition:box-shadow .15s,background .15s}
.tl-i:hover{box-shadow:inset 0 0 0 1px #9A9A9A}
.tl-p{font-family:var(--font-display);font-size:28px;line-height:32px;color:var(--black);white-space:nowrap}
.tl-n{font-size:13px;line-height:16px;font-weight:700}
.tl-s{font-size:12px;line-height:16px;color:var(--silver-grey)}
.tl-i .tag{margin-top:auto}
.tl-i:has(input:checked){background:var(--sel-bg);box-shadow:inset 0 0 0 2px var(--sel-bd)}
.tl-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:2px}
@media (max-width:1100px){
  .tl.n5{grid-template-columns:repeat(6,1fr)}
  .tl.n5 .tl-i{grid-column:span 2}
  .tl.n5 .tl-i:nth-child(n+4){grid-column:span 3}
}
@media (max-width:768px){
  .tab b{font-size:14px;line-height:18px}
  .tl.n4{grid-template-columns:repeat(2,1fr)}
  .tl-i{padding:12px;min-height:80px}
  .tl-p{font-size:24px;line-height:28px}
}
@media (max-width:374px){ .tl-p{font-size:20px;line-height:24px} .tl.n3 .tl-i{padding:12px 8px} .tab b{font-size:13px} }
'''
V2_JS = '''
  function tabs(){ return '<div class="tabs">'+KINDS.map(function(k){ return '<label class="tab">'+radio('kind',k.id,st.kind===k.id)+'<b>'+k.name+'</b><small>'+k.from+(k.fromSub?'<br>'+k.fromSub:'')+'</small></label>' }).join('')+'</div>' }
  function tl(name,items){
    return '<div class="tl n'+items.length+'">'+items.map(function(i){
      var sub=[i.psub,i.sub].filter(Boolean).join('<br>');
      return '<label class="tl-i">'+radio(name,i.id,st[name]===i.id)+(i.price?'<span class="tl-p">'+i.price+'</span>':'')+
        '<span class="tl-n">'+i.name+'</span>'+(sub?'<span class="tl-s">'+sub+'</span>':'')+(i.tag?'<span class="tag">'+i.tag+'</span>':'')+'</label>';
    }).join('')+'</div>';
  }
  function renderOpts(){ opts.innerHTML=stdOpts(tabs(),tl) }
  function onPlan(){ payRefresh(tl) }
'''

# =====================================================================
# 2.4.6.3  One grid of equal boxes, in black and white.
#          The Nike size picker: every choice the same box, a hairline
#          until chosen, then a black edge. No blue anywhere in the choice.
# =====================================================================
V3_CSS = '''
.sz{display:grid;gap:8px;grid-template-columns:repeat(3,1fr)}
.sz.n2{grid-template-columns:repeat(2,1fr)}
.sz.n4{grid-template-columns:repeat(4,1fr)}
.sz.n5{grid-template-columns:repeat(5,1fr)}
.sz-i{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:4px;min-height:72px;padding:12px 8px;border-radius:4px;background:var(--white);box-shadow:inset 0 0 0 1px #DADADA;cursor:pointer;transition:box-shadow .15s}
.sz-i:hover{box-shadow:inset 0 0 0 1px var(--black)}
.sz-n{font-size:14px;line-height:18px;font-weight:600;text-wrap:balance}
.sz-p{font-size:13px;line-height:16px;color:#4A4A4A}
.sz-s{font-size:11px;line-height:16px;color:var(--silver-grey);text-wrap:balance}
.sz-i:has(input:checked){box-shadow:inset 0 0 0 2px var(--black)}
.sz-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:2px}
@media (max-width:1100px){ .sz.n5{grid-template-columns:repeat(3,1fr)} }
@media (max-width:768px){ .sz.n4{grid-template-columns:repeat(2,1fr)} .sz.n5{grid-template-columns:repeat(3,1fr)} .sz-i{min-height:64px} }
@media (max-width:374px){ .sz-n{font-size:13px} }
'''
V3_JS = '''
  function sz(name,items){
    return '<div class="sz n'+items.length+'">'+items.map(function(i){
      var sub=i.sub||i.psub;
      return '<label class="sz-i">'+radio(name,i.id,st[name]===i.id)+'<span class="sz-n">'+i.name+'</span>'+
        (i.price?'<span class="sz-p">'+i.price+'</span>':'')+(sub?'<span class="sz-s">'+sub+'</span>':'')+(i.tag?'<span class="tag">'+i.tag+'</span>':'')+'</label>';
    }).join('')+'</div>';
  }
  function kinds(){ return sz('kind',KINDS.map(function(k){ return {id:k.id,name:k.name,price:k.from,sub:k.fromSub} })) }
  function renderOpts(){ opts.innerHTML=stdOpts(kinds(),sz) }
  function onPlan(){ payRefresh(sz) }
'''

# =====================================================================
# 2.4.6.4  The price table. Membership is a real table: plans across,
#          the two ways to pay down, and you tap the price you want.
#          Passes and coaching are one row of columns, a column per choice.
# =====================================================================
V4_CSS = '''
.tb{display:grid;grid-template-columns:minmax(96px,auto) repeat(3,minmax(0,1fr));box-shadow:inset 0 1px 0 var(--line)}
.tb-0,.tb-h,.tb-r,.tb-c{box-shadow:inset 0 -1px 0 var(--line)}
.tb-h{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:4px;padding:12px 8px;text-align:center;font-size:13px;line-height:16px;font-weight:700;text-wrap:balance}
.tb-r{display:flex;flex-direction:column;justify-content:center;padding:12px 8px 12px 0;font-size:13px;line-height:16px;font-weight:600}
.tb-r small{font-weight:400;font-size:11px;line-height:16px;color:var(--silver-grey)}
.tb-c{position:relative;display:flex;align-items:center;justify-content:center;min-height:56px;font-size:16px;line-height:20px;font-weight:700;cursor:pointer;transition:background .15s}
.tb-c:hover{background:#FAFAF8}
.tb-c:has(input:checked){background:var(--sel-bg);box-shadow:inset 0 0 0 2px var(--sel-bd)}
.tb-c:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:-2px}
.tc{display:grid;box-shadow:inset 0 1px 0 var(--line),inset 0 -1px 0 var(--line)}
.tc-i{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;min-height:88px;padding:16px 4px;text-align:center;cursor:pointer;transition:background .15s}
.tc-i+.tc-i{box-shadow:inset 1px 0 0 var(--line)}
.tc-i:hover{background:#FAFAF8}
.tc-n{font-size:12px;line-height:16px;font-weight:600;color:#5A5A5A;text-wrap:balance}
.tc-p{font-size:16px;line-height:20px;font-weight:700;white-space:nowrap}
.tc-s{font-size:11px;line-height:16px;color:var(--silver-grey);white-space:nowrap}
.tc-i:has(input:checked){background:var(--sel-bg);box-shadow:inset 0 0 0 2px var(--sel-bd)}
.tc-i:has(input:focus-visible){outline:2px solid var(--sel-bd);outline-offset:-2px}
@media (max-width:768px){
  .tb{grid-template-columns:88px repeat(3,minmax(0,1fr))}
  .tb-h{font-size:12px;padding:12px 4px}
  .tb-h .tag{font-size:8px;letter-spacing:.04em}
  .tb-c{font-size:15px}
  .tc-p{font-size:14px}
  .tc-i{padding:16px 2px}
}
@media (max-width:374px){ .tb{grid-template-columns:76px repeat(3,minmax(0,1fr))} .tb-c{font-size:14px} .tc-p{font-size:13px} .tc-n{font-size:11px} }
'''
V4_JS = '''
  function table(){
    var PAYS=[{id:'desk',name:'At reception',sub:'Standard price'},{id:'dd',name:'Direct debit',sub:money(off)+' off'}];
    var h='<div class="tb" role="radiogroup" aria-label="Plan and payment"><span class="tb-0"></span>'+
      P.member.plans.map(function(p){ return '<span class="tb-h">'+p.name+(p.best?'<span class="tag">Recommended</span>':'')+'</span>' }).join('');
    PAYS.forEach(function(y){
      h+='<span class="tb-r">'+y.name+'<small>'+y.sub+'</small></span>';
      P.member.plans.forEach(function(p){
        var price=y.id==='dd'?p.dd:p.desk;
        h+='<label class="tb-c">'+radio('cell',p.id+'|'+y.id,st.plan===p.id&&st.pay===y.id)+'<span class="pc-sr">'+p.name+', '+y.name.toLowerCase()+', </span>'+money(price)+'</label>';
      });
    });
    return h+'</div>';
  }
  function cols(name,items){
    return '<div class="tc" style="grid-template-columns:repeat('+items.length+',1fr)">'+items.map(function(i){
      return '<label class="tc-i">'+radio(name,i.id,st[name]===i.id)+'<span class="tc-n">'+i.name+'</span><span class="tc-p">'+i.price+'</span>'+(i.sub?'<span class="tc-s">'+i.sub+'</span>':'')+'</label>';
    }).join('')+'</div>';
  }
  function renderOpts(){
    var h=set('Choose a pass or membership',seg());
    if(st.kind==='pass') h+=set('Choose a pass',cols('stay',P.visitor.map(function(v){ return {id:v.id,name:v.name,price:money(v.price)} })),'Sports insurance included.');
    else if(st.kind==='mem') h+=set('Tap the price that suits you',table(),'Every 2 weeks, plus the '+money(P.insurance.year)+' sports insurance once a year.');
    else if(st.kind==='pt') h+=set('How many sessions?',cols('pack',P.pt.packs.map(function(k){ return {id:k.id,name:k.sessions>1?k.sessions+' sessions':'1 session',price:money(k.total),sub:k.sessions>1?money(k.each)+' each':''} })));
    opts.innerHTML=h;
  }
'''

# =====================================================================
# 2.4.6.5  One list, the chosen line opens. The checkout pattern: three
#          radio lines with their from price; choosing one opens its
#          options right under it, as chips. Only one open at a time.
# =====================================================================
V5_CSS = '''
.ac{box-shadow:inset 0 1px 0 var(--line)}
.ac-i{box-shadow:inset 0 -1px 0 var(--line);transition:background .15s}
.ac-i>.lr-i{box-shadow:none}
.ac-i.open{background:var(--sel-bg)}
.ac-i>.lr-i:has(input:checked){background:transparent}
.ac-b{padding:0 16px 24px 52px}
.ac-b .pc-set{margin-bottom:24px}
.ac-b .pc-set:last-child{margin-bottom:0}
.ac-b .pc-leg{margin-bottom:8px}
.ac-b .pc-hint{margin:0 0 8px}
.ac-b .lr{background:var(--white);box-shadow:inset 0 0 0 1px var(--line)}
.ac-b .lr-i{min-height:48px;padding:8px 16px;box-shadow:inset 0 -1px 0 var(--line)}
.ac-b .lr-i:last-child{box-shadow:none}
.ac-b .lr-i:has(input:checked){background:var(--sel-bg)}
@media (max-width:768px){ .ac-b{padding:0 8px 24px 40px} .ac-b .lr-i{padding:8px 12px;column-gap:12px} }
'''
V5_JS = '''
  var SUB={pass:'Insurance included',mem:'Paid every 2 weeks',pt:'One to one with a coach'};
  function renderOpts(){
    var h='<div class="ac">'+KINDS.map(function(k){
      var open=st.kind===k.id;
      return '<div class="ac-i'+(open?' open':'')+'"><label class="lr-i ac-h">'+radio('kind',k.id,open)+'<span class="lr-dot" aria-hidden="true"></span>'+
        '<span class="lr-n">'+k.name+'<small>'+SUB[k.id]+'</small></span><b class="lr-p">'+k.from+(k.fromSub?'<small>'+k.fromSub+'</small>':'')+'</b></label>'+
        (open?'<div class="ac-b">'+subSets(rows)+'</div>':'')+'</div>';
    }).join('')+'</div>';
    opts.innerHTML=set('Choose a pass or membership',h);
  }
  function onPlan(){ payRefresh(rows) }
'''

build('2.4.6.1', V1_CSS, V1_JS)
build('2.4.6.2', V2_CSS, V2_JS)
build('2.4.6.3', V3_CSS, V3_JS)
build('2.4.6.4', V4_CSS, V4_JS)
build('2.4.6.5', V5_CSS, V5_JS)
