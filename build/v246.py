# -*- coding: utf-8 -*-
"""Draft 2.4.6: the 2.4.5.1 price builder, rebuilt clean on 2.3, with the
language of 2.4.5.4.2. Options always visible, the plan beside them on desktop
(12 column grid: options 1 to 7, plan 9 to 12) and below them on a phone, where
the page bar turns into the price row until the plan's own button is on screen.
All spacing on the 8px scale (4px for the tightest steps)."""
import io

s = io.open('elite-wellness-landing_2-3.html', encoding='utf-8').read()
def one(old, new):
    global s
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)

# ---- the words around the calculator, as 2.4.5.4.2 settled them ----
one('Day pass €10, week pass €35.90, monthly from €21.', 'Day pass €10, week pass €35.90, membership from €13 every 2 weeks with direct debit.')
one('"priceRange":"€10 to €35.90"', '"priceRange":"€10 to €600"')
one('<span class="ms">Day pass €10 · Monthly €21</span>', '<span class="ms">Day pass €10 · Membership from €13</span>')
one('<p class="find-note">Free parking outside. Cash only at the reception.</p>', '<p class="find-note">Free parking outside. Pay at reception or by direct debit.</p>')
one('<p>Yes. A day pass is €10 and a week pass is €35.90. Walk in and pay at the desk. Cash only.</p>',
    '<p>Yes. A day pass is €10 and a week pass is €35.90, sports insurance included. Walk in and pay at reception.</p>')
i = s.index("<p>Not for day or week passes. The monthly membership"); j = s.index('</p>', i) + 4
s = s[:i] + ('<p>Not for day or week passes. Membership is paid every 2 weeks, from €13 with direct debit, plus the €24 sports insurance once a year. '
             '<sup class="pr-todo" title="[PLACEHOLDER: confirm whether the direct debit price needs a minimum period, e.g. no minimum, cancel any time]">todo</sup> '
             '<a href="https://wa.me/351926565836?text=Hi!%20I%27d%20like%20to%20ask%20about%20membership." target="_blank" rel="noopener">Ask us on WhatsApp</a>.</p>') + s[j:]

# ---- shared pricing files ----
one('</head>', '<link rel="stylesheet" href="pricing.css">\n</head>')
one('<script src="reviews.js"></script>', '<script src="prices.js"></script>\n<script src="pricing.js"></script>\n<script src="reviews.js"></script>')

# ---- the section ----
SECTION = '''<!-- ============ PRICES ============ -->
<section class="section" id="prices">
  <div class="section-kicker">
    <h2 class="section-header">Prices</h2>
    <span class="section-script">a few taps, one price</span>
  </div>
  <div class="pc" id="pc">
    <form class="pc-opts" id="pc-opts" onsubmit="return false"></form>
    <aside class="pc-plan" id="pc-plan" aria-label="Your plan"></aside>
  </div>
  <p class="pc-sr" id="pc-live" aria-live="polite"></p>
  <p class="pr-legal">All prices include VAT. Day and week passes include the sports insurance. Membership is paid every 2 weeks, by direct debit or at reception, and adds the €24 insurance once a year.<span class="pr-todo" title="[PLACEHOLDER: confirm whether the direct debit price needs a minimum period, e.g. no minimum, cancel any time]">todo</span></p>
</section>
'''
i = s.index('<!-- ============ PRICES ============ -->'); j = s.index('\n<!-- ============ REVIEWS', i)
s = s[:i] + SECTION + s[j:]

# ---- the phone bar's price row, inside the page's own bar ----
BAR_END = '<a class="btn on-dark ghost" href="https://maps.app.goo.gl/ks6o4URGCYT7rzHJ8" target="_blank" rel="noopener">Directions</a>\n</div>'
one(BAR_END, BAR_END[:-len('\n</div>')] + '''
  <div class="bar-price">
    <span class="bp-txt"><span id="bp-n"></span><small id="bp-l"></small></span>
    <b id="bp-p"></b>
    <button class="btn on-dark" type="button" id="bp-go">Get this</button>
  </div>
</div>''')

CSS = '''<style>
/* ---------- 2.4.6 prices: options on columns 1 to 7, the plan on 9 to 12 ---------- */
.pc{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;align-items:start}
.pc-opts{grid-column:1 / span 7;min-width:0}
.pc-plan{grid-column:9 / span 4;position:sticky;top:96px;min-width:0}
.pc-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

.pc-set{border:0;padding:0;margin:0 0 40px;min-width:0}
.pc-set:last-child{margin-bottom:0}
.pc-leg{font-weight:800;font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey);padding:0;margin-bottom:16px}
.pc-hint{font-size:13px;line-height:20px;color:var(--silver-grey);margin:-8px 0 16px}
.pc-row{display:grid;gap:8px}
.pc-row.c2{grid-template-columns:repeat(2,1fr)}
.pc-row.c3{grid-template-columns:repeat(3,1fr)}
.pc-row.c4{grid-template-columns:repeat(4,1fr)}
.pc-row.c5{grid-template-columns:repeat(5,1fr)}

/* each choice is a real radio button, drawn as a tile */
.pc-tile{position:relative;display:flex;flex-direction:column;justify-content:center;gap:4px;min-height:64px;padding:12px 16px;border:2px solid var(--light-grey);background:var(--white);cursor:pointer;transition:border-color .15s,background .15s,color .15s}
.pc-tile:hover{border-color:var(--black)}
.pc-tile input{position:absolute;opacity:0;pointer-events:none}
.pc-tile b{font-size:15px;line-height:20px;font-weight:700}
.pc-tile small{font-size:12px;line-height:16px;color:#5a5a5a}
.pc-tile:has(input:checked){background:var(--royal-blue);border-color:var(--royal-blue);color:var(--white)}
.pc-tile:has(input:checked) small{color:rgba(255,255,255,.8)}
.pc-tile:has(input:focus-visible){outline:2px solid var(--royal-blue);outline-offset:2px}
.pc-tile .tag{align-self:flex-start;background:var(--accent);color:var(--black);font-weight:800;font-size:9px;line-height:16px;letter-spacing:.1em;text-transform:uppercase;padding:0 4px;margin-top:4px}
.pc-kind .pc-tile{min-height:88px;padding:16px}
.pc-kind .pc-tile b{font-family:var(--font-display);font-weight:400;font-size:22px;line-height:24px;text-transform:uppercase}
.pc-kind .pc-tile small{font-weight:800;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--royal-blue)}
.pc-kind .pc-tile:has(input:checked) small{color:rgba(255,255,255,.85)}

/* the plan */
.pc-card{background:var(--black);color:var(--white);padding:32px}
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

/* the phone bar's price row: hidden until a phone is in Prices */
.bar-price{display:none}

@media (max-width:1100px){
  .pc-opts{grid-column:1 / span 7}
  .pc-plan{grid-column:8 / span 5}
  .pc-row.c5{grid-template-columns:repeat(3,1fr)}
}
@media (max-width:768px){
  .pc{display:block}
  .pc-plan{position:static;margin-top:32px}
  .pc-set{margin-bottom:32px}
  .pc-row.c3,.pc-row.c4,.pc-row.c5{grid-template-columns:repeat(2,1fr)}
  .pc-row .pc-tile.span{grid-column:1 / -1}
  .pc-tile{min-height:56px;padding:8px 12px}
  .pc-tile b{font-size:14px}
  .pc-kind.pc-row{grid-template-columns:1fr}
  .pc-kind .pc-tile{min-height:64px;flex-direction:row;align-items:center;justify-content:space-between;gap:16px;padding:12px 16px}
  .pc-kind .pc-tile b{font-size:20px}
  .pc-kind .pc-tile small{text-align:right}
  .pc-card{padding:24px}
  .pc-total b{font-size:40px;line-height:40px}
  /* inside Prices the page bar carries the plan, until the plan's own button is on screen */
  html.in-prices .action-bar>.bar-status,html.in-prices .action-bar>.btn{display:none}
  html.in-prices .action-bar .bar-price{display:flex}
  html.in-prices.card-visible .action-bar{transform:translateY(110%)}
  .bar-price{flex:1 1 auto;align-items:center;gap:16px;min-width:0}
  .bp-txt{flex:1 1 auto;min-width:0}
  .bp-txt>span{display:block;font-size:13px;line-height:16px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bp-txt small{display:block;font-weight:800;font-size:10px;line-height:16px;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.55)}
  .bar-price b{font-family:var(--font-display);font-size:24px;line-height:24px;color:var(--accent);white-space:nowrap}
  .bar-price .btn{flex:0 0 auto;padding:16px;font-size:.85rem}
}
</style>
'''

JS = '''<script>
/* 2.4.6: the price builder. Every choice stays on screen; the plan follows it. */
(function(){
  var E=window.EWPricing, opts=document.getElementById('pc-opts'), box=document.getElementById('pc-plan');
  if(!E||!opts||!box) return;
  var P=E.P, money=E.money;
  function find(list,id){ return list.filter(function(x){return x.id===id})[0] }
  var off=P.member.plans[0].desk-P.member.plans[0].dd;

  var KINDS=[
    {id:'pass', name:'Day and week passes', from:'From '+money(P.visitor[0].price)},
    {id:'mem',  name:'Membership',          from:'From '+money(P.member.plans[0].dd)+' every 2 weeks with direct debit'},
    {id:'pt',   name:'Personal training',   from:'From '+money(P.pt.packs[P.pt.packs.length-1].each)+' a session'}
  ];
  var FIRST={pass:{stay:'s1'},mem:{plan:'un',pay:'dd'},pt:{pack:'p8'}};
  var st={kind:'pass',stay:'s1',plan:'un',pay:'dd',pack:'p8',insured:false}, cur=null;

  function tile(name,value,title,small,checked,cls,tag){
    return '<label class="pc-tile'+(cls?' '+cls:'')+'"><input type="radio" name="'+name+'" value="'+value+'"'+(checked?' checked':'')+'>'+
      '<b>'+title+'</b>'+(small?'<small>'+small+'</small>':'')+(tag?'<span class="tag">'+tag+'</span>':'')+'</label>';
  }
  function set(legend,body,hint){ return '<fieldset class="pc-set"><legend class="pc-leg">'+legend+'</legend>'+(hint?'<p class="pc-hint">'+hint+'</p>':'')+body+'</fieldset>' }
  function row(n,inner,cls){ return '<div class="pc-row c'+n+(cls?' '+cls:'')+'">'+inner+'</div>' }

  function payGroup(){
    var p=E.memberPlan(st.plan);
    return row(2, tile('pay','dd','Direct debit',money(p.dd)+' every 2 weeks<br>'+money(p.desk-p.dd)+' off each payment',st.pay==='dd')+
                  tile('pay','desk','At reception',money(p.desk)+' every 2 weeks<br>Standard price',st.pay==='desk'));
  }
  function renderOpts(){
    var h=set('Choose a pass or membership', row(3, KINDS.map(function(k){ return tile('kind',k.id,k.name,k.from,st.kind===k.id) }).join(''), 'pc-kind'));
    if(st.kind==='pass'){
      var n=P.visitor.length;
      h+=set('Choose a pass', row(5, P.visitor.map(function(v,i){ return tile('stay',v.id,v.days===1?'Day pass':v.name,money(v.price),st.stay===v.id,(n%2&&i===n-1)?'span':'') }).join('')));
    } else if(st.kind==='mem'){
      h+=set('How often will you train?', row(3, P.member.plans.map(function(p,i){ return tile('plan',p.id,p.name,money(p.desk)+' every 2 weeks',st.plan===p.id,i===P.member.plans.length-1?'span':'',p.best?'Recommended':'') }).join('')),
             'Prices every 2 weeks at reception. Direct debit takes '+money(off)+' off each payment.');
      h+='<fieldset class="pc-set" id="pc-pay"><legend class="pc-leg">How will you pay?</legend>'+payGroup()+'</fieldset>';
    } else {
      h+=set('How many sessions?', row(4, P.pt.packs.map(function(k){ return tile('pack',k.id,k.name,money(k.total)+(k.sessions>1?', '+money(k.each)+' each':''),st.pack===k.id) }).join('')));
    }
    opts.innerHTML=h;
  }

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

  function renderPlan(){
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
    watchCard();
  }

  opts.addEventListener('change',function(e){
    var t=e.target; if(t.type!=='radio') return;
    if(t.name==='kind'){
      st.kind=t.value; var f=FIRST[t.value]; for(var k in f) st[k]=f[k];
      E.track('pricing_kind',{kind:t.value});
      renderOpts();
      var back=opts.querySelector('input[name=kind]:checked'); if(back) back.focus();
    } else {
      st[t.name]=t.value;
      if(t.name==='plan'){ var pay=document.getElementById('pc-pay'); if(pay) pay.innerHTML='<legend class="pc-leg">How will you pay?</legend>'+payGroup() }
    }
    renderPlan();
  });
  box.addEventListener('change',function(e){
    if(e.target.id!=='pc-ins') return;
    st.insured=e.target.checked; E.track('pricing_insured',{insured:st.insured});
    renderPlan(); document.getElementById('pc-ins').focus();
  });
  box.addEventListener('click',function(e){ if(e.target.closest('#pc-go')) E.review(cur) });
  document.getElementById('bp-go').addEventListener('click',function(){ E.review(cur) });

  /* on a phone: the page bar carries the plan inside Prices, and steps aside
     once the plan's own button is on screen, so there is only ever one */
  var root=document.documentElement, mq=window.matchMedia('(max-width:768px)'), sec=document.getElementById('prices'), inView=false, co=null;
  function mark(){ root.classList.toggle('in-prices', inView&&mq.matches) }
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){ inView=es[0].isIntersecting; mark() },{rootMargin:'-45% 0px -45% 0px'}).observe(sec);
    co=new IntersectionObserver(function(es){ root.classList.toggle('card-visible', es[0].isIntersecting) },{threshold:0.5});
  }
  function watchCard(){ if(co){ co.disconnect(); co.observe(document.getElementById('pc-go')) } }
  if(mq.addEventListener) mq.addEventListener('change',mark); else mq.addListener(mark);

  renderOpts(); renderPlan();
})();
</script>
'''
one('</head>', CSS + '</head>')
one('</body>', JS + '</body>')
io.open('elite-wellness-landing_2-4-6.html', 'w', encoding='utf-8').write(s)
print('2.4.6', len(s))
