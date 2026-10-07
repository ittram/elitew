# -*- coding: utf-8 -*-
"""Draft 2.4.9: the price section rebuilt on 2.4.8 (which keeps the real class
photos). Run build/v248.py first; this reads its output, then run
build/pricelist.py.

What changed, 7 October 2026:
- Personal training is quoted per customer: the calculator shows where it
  starts and asks what the person needs (general training, rehab, training
  with nutrition), then the plan becomes a WhatsApp message for a quote.
  Assessments are not sold on the site.
- "Day / week passes" is "Passes".
- Product boxes and option boxes on one structure: border and padding add up
  to 24px (desktop product), 16px (option) and 12px (phone); every type size
  sits on a 4px line height; the name area of the product boxes is reserved for
  two lines so descriptions and from prices line up across the row.
- The plan is always there, in the same black card: before a choice it shows
  the receipt with empty lines, so people see where the price will appear; it
  fills in as they choose. Both columns start with a label at the same height,
  and the plan no longer scrolls on its own (no sticky)."""
import io, re

s = io.open('elite-wellness-landing_2-4-8.html', encoding='utf-8').read()

CSS = r'''<style>
/* ---------- 2.4.9 prices: options on columns 1 to 7, the plan on 9 to 12 ---------- */
.pc{display:grid;grid-template-columns:repeat(12,1fr);column-gap:24px;align-items:start}
.pc-opts{grid-column:1 / span 7;min-width:0}
.pc-plan{grid-column:9 / span 4;min-width:0}
.pc-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.pc-set{border:0;padding:0;margin:0 0 40px;min-width:0}
.pc-set:last-child{margin-bottom:0}
/* the two column labels: same type, same height, so both columns start on one line */
.pc-leg{float:left;width:100%;padding:0;margin:0 0 16px;font-weight:800;font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey);transition:color .2s}
.pc-leg+*{clear:both}
.pc-set.next>.pc-leg{color:var(--black)}
.pc-hint{clear:both;font-size:14px;line-height:20px;color:#5A5A5A;margin:0 0 16px;max-width:56ch}
.pc-opts input[type=radio]{position:absolute;opacity:0;pointer-events:none}

/* product boxes: 2px border + 22px padding = 24px; the name keeps room for two lines */
.pk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.pk-i{position:relative;display:flex;flex-direction:column;min-height:208px;padding:22px;background:var(--white);border:2px solid var(--light-grey);cursor:pointer;transition:border-color .15s,background .15s,color .15s}
.pk-n{display:block;min-height:56px;font-family:var(--font-display);font-size:28px;line-height:28px;text-transform:uppercase}
.pk-d{display:block;margin-top:8px;font-size:14px;line-height:20px;color:#4A4A4A}
.pk-f{display:block;margin-top:auto;padding-top:16px;font-weight:800;font-size:11px;line-height:16px;letter-spacing:.1em;text-transform:uppercase;color:var(--royal-blue)}
@media (hover:hover){ .pk-i:hover{border-color:var(--black)} }
.pk-i:has(input:checked){background:var(--royal-blue);border-color:var(--royal-blue);color:var(--white)}
.pk-i:has(input:checked) .pk-d{color:rgba(255,255,255,.8)}
.pk-i:has(input:checked) .pk-f{color:var(--white)}
.pk-i:has(input:focus-visible){outline:2px solid var(--royal-blue);outline-offset:2px}

/* option boxes: 2px border + 14px padding = 16px */
.op-row{display:grid;gap:8px}
.op-row.c2{grid-template-columns:repeat(2,minmax(0,1fr))}
.op-row.c3{grid-template-columns:repeat(3,minmax(0,1fr))}
.op-row.c5{grid-template-columns:repeat(5,minmax(0,1fr))}
.op-row.has-tag{padding-top:8px}
.op{position:relative;display:flex;flex-direction:column;justify-content:center;min-height:80px;padding:14px;background:var(--white);border:2px solid var(--light-grey);cursor:pointer;transition:border-color .15s,background .15s,color .15s}
.op-n{display:block;font-size:16px;line-height:24px;font-weight:700}
.op-p{display:block;font-size:14px;line-height:20px;color:#3A3A3A}
.op-s{display:block;font-size:12px;line-height:16px;color:#6A6A6A}
.op .tag{display:inline-block;background:var(--accent);color:var(--black);font-weight:800;font-size:9px;line-height:16px;letter-spacing:.08em;text-transform:uppercase;padding:0 4px;white-space:nowrap}
.op-badge{position:absolute;top:-10px;left:12px}
.op-chip{margin-left:8px;vertical-align:2px}
@media (hover:hover){ .op:hover{border-color:var(--black)} }
.op:has(input:checked){background:var(--royal-blue);border-color:var(--royal-blue);color:var(--white)}
.op:has(input:checked) .op-p,.op:has(input:checked) .op-s{color:rgba(255,255,255,.8)}
.op:has(input:focus-visible){outline:2px solid var(--royal-blue);outline-offset:2px}

/* the plan: the same black card from the start; empty lines until there is a choice */
.pc-card{background:var(--black);color:var(--white);padding:32px}
.pc-n{font-size:20px;line-height:28px;font-weight:700}
.pc-card.is-todo .pc-n{color:rgba(255,255,255,.6)}
.pc-lines{margin-top:16px}
.pc-line{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:12px 0;box-shadow:inset 0 -1px 0 rgba(255,255,255,.16);font-size:14px;line-height:20px}
.pc-line b{font-weight:700;white-space:nowrap}
.pc-line.todo span{color:rgba(255,255,255,.48)}
.pc-dash{display:inline-block;width:24px;height:2px;background:rgba(255,255,255,.32);vertical-align:middle}
.pc-ins{display:flex;align-items:center;gap:16px;margin-top:16px;cursor:pointer;font-size:12px;line-height:16px;color:rgba(255,255,255,.8)}
.pc-ins input{appearance:none;flex:0 0 40px;width:40px;height:24px;border-radius:12px;background:rgba(255,255,255,.24);position:relative;cursor:pointer;margin:0;transition:background .15s}
.pc-ins input::after{content:"";position:absolute;top:4px;left:4px;width:16px;height:16px;border-radius:50%;background:var(--white);transition:transform .15s}
.pc-ins input:checked{background:var(--royal-blue)}
.pc-ins input:checked::after{transform:translateX(16px)}
.pc-ins input:focus-visible{outline:2px solid var(--white);outline-offset:2px}
.pc-total{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-top:24px;min-height:48px}
.pc-total span{font-size:12px;line-height:16px;color:rgba(255,255,255,.6)}
.pc-total b{font-family:var(--font-display);font-weight:400;font-size:48px;line-height:48px;color:var(--accent);white-space:nowrap}
.pc-total .pc-dash{width:48px;height:4px;margin-bottom:20px}
.pc-note{font-size:12px;line-height:16px;color:rgba(255,255,255,.6);margin-top:16px}
.pc-card .btn{width:100%;justify-content:center;margin-top:24px}
.pc-card .btn[aria-disabled=true]{background:rgba(255,255,255,.12);border-color:transparent;color:rgba(255,255,255,.48);cursor:not-allowed;box-shadow:none;transform:none}
@media (prefers-reduced-motion:reduce){ .pk-i,.op,.pc-leg{transition:none} }

.bar-price{display:none}
@media (max-width:1100px){
  .pc-plan{grid-column:8 / span 5}
  .pk-i{min-height:176px;padding:14px}
  .pk-n{min-height:48px;font-size:22px;line-height:24px}
  .pc-card{padding:24px}
  .op-row.c5{grid-template-columns:repeat(6,minmax(0,1fr))}
  .op-row.c5 .op{grid-column:span 2}
  .op-row.c5 .op:nth-child(n+4){grid-column:span 3}
}
@media (max-width:768px){
  .pc{display:block}
  .pc-plan{margin-top:40px}
  .pc-set{margin-bottom:32px}
  /* three product boxes side by side: the name and where it starts, nothing else */
  .pk{gap:8px}
  .pk-i{min-height:96px;padding:10px}
  .pk-n{min-height:40px;font-size:16px;line-height:20px}
  .pk-d{display:none}
  .pk-f{padding-top:12px;font-size:11px;letter-spacing:.06em;white-space:nowrap}
  .op{min-height:72px;padding:10px}
  .op-n{font-size:14px;line-height:20px}
  .op-p{font-size:14px;line-height:20px}
  .op-badge{left:8px}
  .op .tag{font-size:8px;letter-spacing:.06em}
  .op-chip{margin-left:4px}
  .pc-total b{font-size:40px;line-height:40px}
  /* the page bar carries the plan once it is complete, and steps aside for the plan's own button */
  html.in-prices.has-plan .action-bar>.bar-status,html.in-prices.has-plan .action-bar>.btn{display:none}
  html.in-prices.has-plan .action-bar .bar-price{display:flex}
  html.in-prices.card-visible .action-bar{transform:translateY(110%)}
  .bar-price{flex:1 1 auto;align-items:center;gap:16px;min-width:0}
  .bp-txt{flex:1 1 auto;min-width:0}
  .bp-txt>span{display:block;font-size:13px;line-height:16px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bp-txt small{display:block;font-weight:800;font-size:10px;line-height:16px;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.56)}
  .bar-price b{font-family:var(--font-display);font-weight:400;font-size:24px;line-height:24px;color:var(--accent);white-space:nowrap}
  .bar-price .btn{flex:0 0 auto;padding:16px;font-size:.85rem}
}
@media (max-width:374px){
  .pk-i{padding:10px 6px}
  .pk-n{font-size:15px}
  .pk-f{font-size:10px;letter-spacing:.02em}
  .op-n{font-size:13px}
}
</style>'''

JS = r'''<script>
/* 2.4.9: the price builder. Passes and membership are priced here; personal training is quoted per person. */
(function(){
  var E=window.EWPricing, opts=document.getElementById('pc-opts'), box=document.getElementById('pc-plan');
  if(!E||!opts||!box) return;
  var P=E.P, money=E.money, off=P.member.plans[0].desk-P.member.plans[0].dd;
  var WA='https://wa.me/351926565836?text=';
  function find(list,id){ return list.filter(function(x){return x.id===id})[0] }
  var ptFrom=Math.min.apply(null,P.pt.packs.map(function(k){return k.each}));
  var memFrom=Math.min.apply(null,P.member.plans.map(function(p){return p.dd}));
  var TODO_COACH='<span class="pr-todo" title="[PLACEHOLDER: confirm every coach who gives personal training is certified, and by whom]">todo</span>';
  var KINDS=[
    {id:'pass', name:'Passes',            desc:'No commitment. From 1 day to 4 weeks.',                 from:'From '+money(P.visitor[0].price)},
    {id:'mem',  name:'Membership',        desc:'Paid every 2 weeks. Best value if you train regularly.', from:'From '+money(memFrom)},
    {id:'pt',   name:'Personal training', desc:'One to one with a certified coach.'+TODO_COACH,          from:'From '+money(ptFrom)}
  ];
  var NEEDS=[
    {id:'gen',   name:'Training',  sub:'Strength and fitness',     msg:'general training'},
    {id:'rehab', name:'Rehab',     sub:'After an injury',          msg:'rehab after an injury'},
    {id:'food',  name:'Nutrition', sub:'Training and a food plan', msg:'training with a nutrition plan'}
  ];
  /* nothing is chosen until the visitor chooses; each product keeps its own choice */
  var st={kind:null,stay:null,plan:null,pay:null,need:null,insured:false}, cur=null;

  function radio(name,value,checked){ return '<input type="radio" name="'+name+'" value="'+value+'"'+(checked?' checked':'')+'>' }
  function set(legend,body,hint,id){ return '<fieldset class="pc-set"'+(id?' id="'+id+'"':'')+'><legend class="pc-leg">'+legend+'</legend>'+(hint?'<p class="pc-hint">'+hint+'</p>':'')+body+'</fieldset>' }
  function tile(name,i){
    return '<label class="op">'+radio(name,i.id,st[name]===i.id)+(i.tag?'<span class="tag op-badge">'+i.tag+'</span>':'')+
      '<span class="op-n">'+i.name+(i.chip?'<span class="tag op-chip">'+i.chip+'</span>':'')+'</span>'+
      (i.p?'<span class="op-p">'+i.p+'</span>':'')+(i.s?'<span class="op-s">'+i.s+'</span>':'')+'</label>';
  }
  function row(items,name){
    var tag=items.some(function(i){return i.tag});
    return '<div class="op-row c'+items.length+(tag?' has-tag':'')+'">'+items.map(function(i){ return tile(name,i) }).join('')+'</div>';
  }
  function products(){
    return '<div class="pk">'+KINDS.map(function(k){
      return '<label class="pk-i">'+radio('kind',k.id,st.kind===k.id)+'<span class="pk-n">'+k.name+'</span><span class="pk-d">'+k.desc+'</span><span class="pk-f">'+k.from+'</span></label>';
    }).join('')+'</div>';
  }
  function payRow(){
    var p=st.plan?E.memberPlan(st.plan):null;
    return row([
      {id:'dd',   name:'Direct debit', chip:money(off)+' off', p:p?money(p.dd)+' every 2 weeks':'',   s:'Paid automatically'},
      {id:'desk', name:'At reception',                         p:p?money(p.desk)+' every 2 weeks':'', s:'Standard price'}
    ],'pay');
  }
  function renderOpts(){
    var h=set('Choose a pass or membership',products());
    if(st.kind==='pass')
      h+=set('Choose a pass',row(P.visitor.map(function(v){ return {id:v.id,name:v.name,p:money(v.price)} }),'stay'));
    else if(st.kind==='mem')
      h+=set('How often will you train?',row(P.member.plans.map(function(p){ return {id:p.id,name:p.name,p:money(p.desk),s:'every 2 weeks',tag:p.best?'Recommended':''} }),'plan'))+
         set('How will you pay?',payRow(),'','pc-pay');
    else if(st.kind==='pt')
      h+=set('What do you need?',row(NEEDS.map(function(n){ return {id:n.id,name:n.name,s:n.sub} }),'need'),
             'Every plan is made for you. Tell us what you need and a coach sends you a personal quote.');
    opts.innerHTML=h;
  }

  /* the receipt, filled in as far as the choices go */
  function summary(){
    var s={title:'Nothing chosen yet', lines:[['Pass or membership',null],['Option',null]], totalLabel:'Total', price:null, notes:[], hint:'Choose a pass or membership to see your price.', ready:false};
    if(st.kind==='pass'){
      var v=st.stay?find(P.visitor,st.stay):null;
      s.title=v?(v.days===1?'Day pass':v.name+' pass'):'Pass'; s.totalLabel='To pay at reception';
      s.lines=[[v?(v.days===1?'Day pass':v.name+' pass'):'Pass', v?money(v.price):null],['Sports insurance','Included']];
      s.hint='Choose a pass.';
      if(v){
        s.ready=true; s.id=v.id; s.price=v.price;
        var n=Math.ceil(P.visitor[1].price/P.visitor[0].price), words=['','one','two','three','four','five','six','seven'];
        if(v.days<n) s.notes.push('Paid each time you come. From '+words[n]+' days on, the week pass costs less.');
        if(v.days>=28) s.notes.push('Four weeks of membership is '+money(E.fourWeeks().member)+' with the insurance, and it keeps going after four weeks.');
      }
    } else if(st.kind==='mem'){
      var p=st.plan?E.memberPlan(st.plan):null, dd=st.pay==='dd';
      s.title=p?p.name+' membership':'Membership'; s.totalLabel='To pay on your first visit';
      s.lines=[[p?p.name+', first 2 weeks':'Plan, first 2 weeks', p?money(p.desk):null]];
      if(!st.pay) s.lines.push(['Payment',null]);
      else if(dd) s.lines.push(['Direct debit discount', p?money(p.desk-p.dd)+' off':money(off)+' off']);
      else s.lines.push(['Payment','At reception']);
      s.lines.push(st.insured?['Sports insurance','Already paid']:['Sports insurance, once a year',money(P.insurance.year)]);
      s.hint=p?'Choose how you will pay.':'Choose how often you will train.';
      if(p&&st.pay){
        var rate=dd?p.dd:p.desk;
        s.ready=true; s.id=p.id; s.price=rate+(st.insured?0:P.insurance.year);
        s.notes.push(dd?'Then '+money(p.dd)+' every 2 weeks by direct debit. That saves you '+money(P.member.ddSavingYear)+' a year.'
                       :'Then '+money(p.desk)+' every 2 weeks. With direct debit it is '+money(p.dd)+', a saving of '+money(P.member.ddSavingYear)+' a year.');
      }
    } else if(st.kind==='pt'){
      var nd=st.need?find(NEEDS,st.need):null;
      s.title=nd?'Personal training, '+(nd.id==='gen'?'general':nd.name.toLowerCase()):'Personal training'; s.quote=true;
      s.lines=[['What you need',nd?nd.name:null],['Your price','Personal quote']];
      s.totalLabel='A session, from'; s.price=ptFrom; s.hint='Choose what you need.';
      if(nd){ s.ready=true; s.id='pt-'+nd.id; s.msg='Hi! I would like a personal training quote for '+nd.msg+'.';
              s.notes.push('Every plan is made for you. A coach replies on WhatsApp with a personal quote.'); }
    }
    return s;
  }

  var root=document.documentElement, co=null;
  function renderPlan(){
    var s=summary();
    var lines=s.lines.map(function(l){
      return '<div class="pc-line'+(l[1]==null?' todo':'')+'"><span>'+l[0]+'</span>'+(l[1]==null?'<b class="pc-dash" aria-label="not chosen yet"></b>':'<b>'+l[1]+'</b>')+'</div>';
    }).join('');
    var btn;
    if(s.quote) btn = s.ready
      ? '<a class="btn" id="pc-go" href="'+WA+encodeURIComponent(s.msg)+'" target="_blank" rel="noopener">Ask for a quote on WhatsApp</a>'
      : '<button class="btn" type="button" id="pc-go" aria-disabled="true">Ask for a quote on WhatsApp</button>';
    else btn='<button class="btn" type="button" id="pc-go"'+(s.ready?'':' aria-disabled="true"')+'>Get this plan</button>';
    var showTotal=s.ready||s.quote;
    box.innerHTML='<p class="pc-leg">Your plan</p>'+
      '<div class="pc-card'+(s.ready?'':' is-todo')+'">'+
        '<p class="pc-n">'+s.title+'</p>'+
        '<div class="pc-lines">'+lines+'</div>'+
        (st.kind==='mem'?'<label class="pc-ins"><input type="checkbox" id="pc-ins"'+(st.insured?' checked':'')+'><span>My sports insurance is already paid this year</span></label>':'')+
        '<div class="pc-total"><span>'+s.totalLabel+'</span>'+(showTotal?'<b>'+money(s.price)+'</b>':'<b class="pc-dash" aria-label="not chosen yet"></b>')+'</div>'+
        '<p class="pc-note">'+(s.ready?s.notes.join(' '):s.hint)+'</p>'+
        btn+
      '</div>';
    cur=s.ready&&!s.quote?{id:s.id,title:s.title,price:s.price,totalLabel:s.totalLabel,lines:s.lines,notes:s.notes}:null;
    document.getElementById('pc-live').textContent=s.ready?s.title+', '+(s.quote?'from '+money(s.price)+' a session':money(s.price))+'.':'';
    root.classList.toggle('has-plan',s.ready);
    if(s.ready){
      document.getElementById('bp-n').textContent=s.title;
      document.getElementById('bp-l').textContent=s.totalLabel;
      document.getElementById('bp-p').textContent=money(s.price);
      var bp=document.getElementById('bp-go'); bp.textContent=s.quote?'Ask':'Get this'; bp.dataset.wa=s.quote?WA+encodeURIComponent(s.msg):'';
    } else root.classList.remove('card-visible');
    if(co){ co.disconnect(); if(s.ready) co.observe(document.getElementById('pc-go')) }
  }
  function guide(){
    var done=false;
    [].forEach.call(opts.querySelectorAll('fieldset'),function(f){
      var next=!done&&!f.querySelector('input:checked'); f.classList.toggle('next',next); if(next) done=true;
    });
  }

  opts.addEventListener('change',function(e){
    var t=e.target; if(t.type!=='radio') return;
    if(t.name==='kind'){
      if(st.kind!==t.value) E.track('pricing_kind',{kind:t.value});
      st.kind=t.value; renderOpts();
      var back=opts.querySelector('input[name=kind]:checked'); if(back) back.focus();
    } else {
      st[t.name]=t.value;
      if(t.name==='plan'){ var f=document.getElementById('pc-pay'); if(f) f.outerHTML=set('How will you pay?',payRow(),'','pc-pay') }
    }
    renderPlan(); guide();
  });
  box.addEventListener('change',function(e){
    if(e.target.id!=='pc-ins') return;
    st.insured=e.target.checked; E.track('pricing_insured',{insured:st.insured});
    renderPlan(); document.getElementById('pc-ins').focus();
  });
  box.addEventListener('click',function(e){
    var go=e.target.closest('#pc-go'); if(!go) return;
    if(go.getAttribute('aria-disabled')==='true'){ e.preventDefault(); return }
    if(go.tagName==='A'){ E.track('pricing_quote',{need:st.need}); return }
    if(cur) E.review(cur);
  });
  document.getElementById('bp-go').addEventListener('click',function(){
    var wa=this.dataset.wa;
    if(wa){ E.track('pricing_quote',{need:st.need,from:'bar'}); window.open(wa,'_blank','noopener'); return }
    if(cur) E.review(cur);
  });

  /* on a phone the page bar carries a complete plan inside Prices, and steps aside for the plan's own button */
  var mq=window.matchMedia('(max-width:768px)'), sec=document.getElementById('prices'), inView=false;
  function mark(){ root.classList.toggle('in-prices', inView&&mq.matches) }
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){ inView=es[0].isIntersecting; mark() },{rootMargin:'-45% 0px -45% 0px'}).observe(sec);
    co=new IntersectionObserver(function(es){ root.classList.toggle('card-visible', es[0].isIntersecting&&root.classList.contains('has-plan')) },{threshold:0.5});
  }
  if(mq.addEventListener) mq.addEventListener('change',mark); else mq.addListener(mark);
  renderOpts(); renderPlan(); guide();
})();
</script>'''

i = s.find('2.4.6.x shared: layout'); a = s.rfind('<style>', 0, i); b = s.find('</style>', i) + len('</style>')
assert a > 0 and b > i
s = s[:a] + CSS + s[b:]
j = s.find("var E=window.EWPricing, opts=document.getElementById('pc-opts')"); c = s.rfind('<script>', 0, j); d = s.find('</script>', j) + len('</script>')
assert c > 0 and d > j
s = s[:c] + JS + s[d:]
io.open('elite-wellness-landing_2-4-9.html', 'w', encoding='utf-8').write(s)
print('2.4.9', len(s))
