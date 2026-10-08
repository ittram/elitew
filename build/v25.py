# -*- coding: utf-8 -*-
"""Drafts 2.5.1 to 2.5.5: five answers to the empty price screen, on 2.4.9.7.

What 2.4.9.7 got wrong (8 October 2026): before anything is chosen the plan is
an empty black box with dashes, the product boxes do not say what comes next,
nothing helps the eye tell the three apart, and Personal training throws the
plan away for a banner, so the three products feel like two different pages.

Shared by all five:
- an icon on each product box (a ticket, a calendar that repeats, two people),
  a ring that fills when it is chosen, a line saying what you choose next, and
  the from price with its condition (membership: with direct debit);
- Personal training keeps the plan column: the same black card says one to
  one, made for you, price agreed with your coach, from the lowest price a
  session, and holds the Book a time on WhatsApp button. On the left, the
  session photo and how it works in three steps.

The five empty states:
  2.5.1  the plan explains itself: three steps to your price
  2.5.2  a photo of the gym until there is a plan
  2.5.3  no plan yet: three full width cards show what is inside each
  2.5.4  the best value is already chosen, so there is never an empty plan
  2.5.5  the plan is a full width strip under the options, with progress

Run from the repo root: python3 build/v25.py, then build/pricelist.py."""
import io, re

BASE = 'elite-wellness-landing_2-4-9-7.html'
VARIANTS = {
    1: 'Empty plan, three steps',
    2: 'Empty plan, a photo',
    3: 'Cards first, no plan yet',
    4: 'Best value chosen',
    5: 'The plan as a strip',
}

MARKUP = '''<div class="pc v%(v)d" id="pc">
    <form class="pc-opts" id="pc-opts" onsubmit="return false"><div class="pc-k" id="pc-k"></div><div class="pc-q" id="pc-q"></div></form>
    <aside class="pc-plan" id="pc-plan" aria-label="Your plan"></aside>
  </div>'''

JS = r'''<script>
/* 2.5.%(v)d: the price builder (%(label)s). Passes and membership are priced here; personal training
   keeps the same plan card and books a first talk with a coach on WhatsApp. */
(function(){
  var V=%(v)d; /* 1 three steps, 2 a photo, 3 cards first, 4 best value chosen, 5 the plan as a strip */
  var E=window.EWPricing, opts=document.getElementById('pc-opts'), kEl=document.getElementById('pc-k'), qEl=document.getElementById('pc-q'), box=document.getElementById('pc-plan'), pc=document.getElementById('pc');
  if(!E||!opts||!box) return;
  var P=E.P, money=E.money, off=P.member.plans[0].desk-P.member.plans[0].dd;
  var WA='https://wa.me/351926565836?text=';
  var BOOK_MSG='Hi! I would like to book a time to talk to a coach about personal training.';
  function find(list,id){ return list.filter(function(x){return x.id===id})[0] }
  var ptFrom=Math.min.apply(null,P.pt.packs.map(function(k){return k.each}));
  var memFrom=Math.min.apply(null,P.member.plans.map(function(p){return p.dd}));
  var first=P.visitor[0], last=P.visitor[P.visitor.length-1];
  var INCL=P.includes[0].charAt(0).toLowerCase()+P.includes[0].slice(1);

  /* one line icons on a 32 grid, 2px, square ends: what each product is at a glance */
  var IC={
    pass:'<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M3 9h26v4.6a2.4 2.4 0 0 0 0 4.8V23H3v-4.6a2.4 2.4 0 0 0 0-4.8z"/><path class="ic-cut" d="M21 11v10"/><path d="M8 14h8M8 18h5"/></svg>',
    mem:'<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M4 7h24v21H4zM4 12h24M10 4v5M22 4v5"/><path d="M20.4 21.6a4.6 4.6 0 1 1-1-4.9"/><path d="M20.2 14.6v3h-3"/></svg>',
    pt:'<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="11" cy="9" r="4"/><path d="M3 28v-3a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v3"/><circle cx="22.5" cy="10.5" r="3"/><path d="M21.5 18.5h1.5a6 6 0 0 1 6 6V28"/></svg>'
  };
  var PT_FACTS=[['Sessions','One to one'],['Plan','Made for you'],['Price','Agreed with your coach']];
  var KINDS=[
    {id:'pass', name:'Passes', desc:'No commitment. Come for a day or up to 4 weeks.', next:'Then pick '+first.name+' to '+last.name,
      from:money(first.price), per:'for a day', go:'See the passes', foot:'Sports insurance included',
      list:P.visitor.map(function(v){ return [v.name,money(v.price)] })},
    {id:'mem', name:'Membership', desc:'Paid every 2 weeks. Best value if you train regularly.', next:'Then pick how often, and how to pay',
      from:money(memFrom), per:'every 2 weeks with direct debit', go:'See the plans', foot:'Every 2 weeks with direct debit, '+money(off)+' off the reception price',
      list:P.member.plans.map(function(p){ return [p.name,money(p.dd)] })},
    {id:'pt', name:'Personal training', desc:'One to one with a coach, planned around you.', next:'Then book a first talk with a coach',
      from:money(ptFrom), per:'a session', go:'How it works', foot:'From '+money(ptFrom)+' a session',
      list:PT_FACTS}
  ];

  /* nothing is chosen until the visitor chooses (2.5.4: the best value is chosen for them) */
  var st=V===4?{kind:'mem',stay:null,plan:'un',pay:'dd',insured:false}:{kind:null,stay:null,plan:null,pay:null,insured:false}, cur=null;

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
      var inside=V===3
        ?'<span class="pk-l">'+k.list.map(function(r){ return '<span><i>'+r[0]+'</i><b>'+r[1]+'</b></span>' }).join('')+'<em>'+k.foot+'</em></span><span class="pk-go">'+k.go+'</span>'
        :'';
      return '<label class="pk-i">'+radio('kind',k.id,st.kind===k.id)+
        '<span class="pk-ic">'+IC[k.id]+'</span>'+
        '<span class="pk-n">'+k.name+'</span><span class="pk-d">'+k.desc+'</span>'+
        '<span class="pk-x">'+k.next+'</span>'+inside+
        '<span class="pk-f"><small>From</small><b>'+k.from+'</b><small>'+k.per+'</small></span></label>';
    }).join('')+'</div>';
  }
  function payRow(){
    var p=st.plan?E.memberPlan(st.plan):null;
    return row([
      {id:'dd',   name:'Direct debit', chip:money(off)+' off', p:p?money(p.dd)+' every 2 weeks':'',   s:'Paid automatically'},
      {id:'desk', name:'At reception',                         p:p?money(p.desk)+' every 2 weeks':'', s:'Standard price'}
    ],'pay');
  }
  /* personal training on the left: the session photo, what it is, how it starts */
  var STEPS=[['Message us','Say what you want to work on.'],['Meet your coach','A first talk at the gym, to see where you are and set the goal.'],['Train','One to one, with a plan and a price agreed together.']];
  function ptHow(){
    var ph=V===2?'':'<div class="ptx-ph"><img src="assets/pt-session.webp" srcset="assets/pt-session-800.webp 800w, assets/pt-session.webp 1600w" sizes="(max-width:768px) 100vw, 25vw" width="1600" height="1200" loading="lazy" alt="A coach guiding a member through a lunge in a personal training session at Elite Wellness"></div>';
    return '<div class="ptx'+(ph?'':' no-ph')+'">'+ph+'<div class="ptx-t"><p class="ptx-h">Made around you</p>'+
      '<p class="ptx-p">Everyone starts from a different place: an injury to come back from, pain that holds you back, a goal you keep missing, or not knowing where to begin. Your coach sets the goal with you and builds every session around it.</p>'+
      '<ol class="ptx-s">'+STEPS.map(function(s,i){ return '<li><i>'+(i+1)+'</i><span><b>'+s[0]+'</b>'+s[1]+'</span></li>' }).join('')+'</ol></div></div>';
  }
  function renderOpts(){
    kEl.innerHTML=set('Choose how you want to train',products());
    var h='';
    if(st.kind==='pass')
      h=set('Choose a pass',row(P.visitor.map(function(v){ return {id:v.id,name:v.name,p:money(v.price)} }),'stay'));
    else if(st.kind==='mem')
      h=set('How often will you train?',row(P.member.plans.map(function(p){ return {id:p.id,name:p.name,p:money(p.desk),s:'every 2 weeks',tag:p.best?'Recommended':''} }),'plan'))+
        set('How will you pay?',payRow(),'','pc-pay');
    else if(st.kind==='pt')
      h=set('How personal training works',ptHow());
    qEl.innerHTML=h;
    pc.classList.toggle('empty',!st.kind);
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
    }
    return s;
  }

  /* 2.5.5: where you are, on top of the strip */
  function progress(ready){
    var opt=st.kind==='pass'?!!st.stay:st.kind==='mem'?!!(st.plan&&st.pay):st.kind==='pt';
    var done=[!!st.kind,opt,ready||st.kind==='pt'], on=done.indexOf(false);
    return '<ol class="g-prog">'+['What','Option','Your price'].map(function(x,i){
      return '<li class="'+(done[i]?'done':i===on?'on':'')+'"><i>'+(i+1)+'</i>'+x+'</li>' }).join('')+'</ol>';
  }
  var LEG='<p class="pc-leg">Your plan</p>';

  /* before anything is chosen: each draft answers the empty plan differently */
  function renderEmpty(){
    if(V===1){
      var g=[['Choose how you want to train','A pass, a membership or personal training.'],['Pick your option','How long you stay, or how often you come.'],['See your price','Then pay at reception on your first visit.']];
      box.innerHTML=LEG+'<div class="pc-card is-guide"><p class="pc-n">Your price in three taps</p>'+
        '<ol class="g-steps">'+g.map(function(s,i){ return '<li'+(i?'':' class="on"')+'><i>'+(i+1)+'</i><span><b>'+s[0]+'</b>'+s[1]+'</span></li>' }).join('')+'</ol>'+
        '<p class="pc-note">Every pass and membership includes '+INCL+'.</p></div>';
    } else if(V===2){
      box.innerHTML=LEG+'<div class="pc-card is-photo"><img class="pp-img" src="assets/class-trx.webp" srcset="assets/class-trx-600.webp 600w, assets/class-trx.webp 900w" sizes="(max-width:768px) 100vw, 30vw" width="900" height="1200" loading="lazy" alt="A member training on the TRX straps at Elite Wellness">'+
        '<div class="pp-t"><p class="pp-k">In every pass and membership</p><p class="pp-h">The gym and every class</p><p class="pc-note">Choose how you want to train and your price shows here.</p></div></div>';
    } else if(V===5){
      box.innerHTML=LEG+'<div class="pc-card is-strip0">'+progress(false)+'<p class="pc-note">Choose how you want to train and your price shows here.</p></div>';
    } else box.innerHTML='';
  }

  var root=document.documentElement, co=null;
  function off_(){ cur=null; root.classList.remove('has-plan','card-visible'); if(co) co.disconnect(); document.getElementById('pc-live').textContent='' }

  /* personal training: the same plan card, with a first talk instead of a total */
  function renderContact(){
    var href=WA+encodeURIComponent(BOOK_MSG);
    var ph=V===2?'<div class="pc-ph"><img src="assets/pt-session-800.webp" srcset="assets/pt-session-800.webp 800w, assets/pt-session.webp 1600w" sizes="(max-width:768px) 100vw, 30vw" width="1600" height="1200" loading="lazy" alt="A coach guiding a member through a lunge in a personal training session at Elite Wellness"></div>':'';
    box.innerHTML=LEG+'<div class="pc-card is-pt">'+ph+(V===5?progress(true):'')+
      '<p class="pc-n">Personal training</p>'+
      '<div class="pc-lines">'+PT_FACTS.map(function(l){ return '<div class="pc-line"><span>'+l[0]+'</span><b>'+l[1]+'</b></div>' }).join('')+'</div>'+
      '<div class="pc-total"><span>Sessions from</span><b>'+money(ptFrom)+'</b></div>'+
      '<p class="pc-note">For general fitness, rehab after an injury, nutrition or a mix. Your coach agrees the plan and its price with you.</p>'+
      '<a class="btn" id="pt-wa" href="'+href+'" target="_blank" rel="noopener">Book a time on WhatsApp</a>'+
      '<p class="pc-alt">Prefer to talk? Call <a href="tel:+351926565836">+351 926 565 836</a></p>'+
    '</div>';
    off_();
    document.getElementById('pc-live').textContent='Personal training: book a time on WhatsApp to talk to a coach.';
  }
  function renderPlan(){
    if(st.kind==='pt') return renderContact();
    if(!st.kind){ renderEmpty(); return off_() }
    var s=summary();
    var lines=s.lines.map(function(l){
      return '<div class="pc-line'+(l[1]==null?' todo':'')+'"><span>'+l[0]+'</span>'+(l[1]==null?'<b class="pc-dash" aria-label="not chosen yet"></b>':'<b>'+l[1]+'</b>')+'</div>';
    }).join('');
    var btn=s.ready?'<button class="btn" type="button" id="pc-go">Get this plan</button>':'';
    box.innerHTML=LEG+
      '<div class="pc-card'+(s.ready?'':' is-todo')+'">'+(V===5?progress(s.ready):'')+
        '<p class="pc-n">'+s.title+'</p>'+
        '<div class="pc-lines">'+lines+'</div>'+
        (st.kind==='mem'?'<label class="pc-ins"><input type="checkbox" id="pc-ins"'+(st.insured?' checked':'')+'><span>My sports insurance is already paid this year</span></label>':'')+
        '<div class="pc-total"><span>'+s.totalLabel+'</span>'+(s.ready?'<b>'+money(s.price)+'</b>':'<b class="pc-dash" aria-label="not chosen yet"></b>')+'</div>'+
        '<p class="pc-note">'+(s.ready?s.notes.join(' '):s.hint)+'</p>'+
        btn+
      '</div>';
    cur=s.ready?{id:s.id,title:s.title,price:s.price,totalLabel:s.totalLabel,lines:s.lines,notes:s.notes}:null;
    document.getElementById('pc-live').textContent=s.ready?s.title+', '+money(s.price)+'.':'';
    root.classList.toggle('has-plan',s.ready);
    if(s.ready){
      document.getElementById('bp-n').textContent=s.title;
      document.getElementById('bp-l').textContent=s.totalLabel;
      document.getElementById('bp-p').textContent=money(s.price);
      document.getElementById('bp-go').textContent='Get this';
    } else root.classList.remove('card-visible');
    if(co){ co.disconnect(); if(s.ready) co.observe(document.getElementById('pc-go')) }
  }
  function guide(){
    var done=false;
    [].forEach.call(opts.querySelectorAll('fieldset'),function(f){
      var next=!done&&!!f.querySelector('input[type=radio]')&&!f.querySelector('input:checked'); f.classList.toggle('next',next); if(next) done=true;
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
  document.addEventListener('click',function(e){ if(e.target.closest('#pt-wa')) E.track('pricing_pt_whatsapp',{}) });
  box.addEventListener('click',function(e){
    var go=e.target.closest('#pc-go'); if(!go) return;
    if(cur) E.review(cur);
  });
  document.getElementById('bp-go').addEventListener('click',function(){
    if(cur) E.review(cur);
  });

  /* on a phone the page bar carries a complete plan inside Prices, and steps aside for the plan's own button */
  var mq=window.matchMedia('(max-width:768px)'), sec=document.getElementById('prices'), inView=false;
  function mark(){ root.classList.toggle('in-prices', inView&&mq.matches) }
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){ inView=es[0].isIntersecting; mark() },{rootMargin:'-45%% 0px -45%% 0px'}).observe(sec);
    co=new IntersectionObserver(function(es){ root.classList.toggle('card-visible', es[0].isIntersecting&&root.classList.contains('has-plan')) },{threshold:0.5});
  }
  if(mq.addEventListener) mq.addEventListener('change',mark); else mq.addListener(mark);
  renderOpts(); renderPlan(); guide();
})();
</script>'''

CSS = r'''<style id="v25-css">
/* ---------- 2.5: the empty price screen. Shared: product boxes ---------- */
.pc-k .pc-set{margin-bottom:40px}
.pc-q:empty{display:none}
.pk-i{min-height:0;padding:24px}
.pk-ic{display:block;width:32px;height:32px;margin-bottom:24px;color:var(--royal-blue);transition:color .15s}
.pk-ic svg{display:block;width:100%;height:100%;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:square;stroke-linejoin:miter}
.pk-ic .ic-cut{stroke-linecap:butt;stroke-dasharray:2 2}
/* a ring that fills when the box is chosen: it reads as a choice, not as a link */
.pk-i::after{content:"";position:absolute;top:24px;right:24px;width:20px;height:20px;border-radius:50%;box-shadow:inset 0 0 0 2px var(--light-grey);transition:box-shadow .15s,background .15s}
@media (hover:hover){ .pk-i:hover::after{box-shadow:inset 0 0 0 2px var(--black)} }
.pk-i:has(input:checked)::after{background:var(--white);box-shadow:inset 0 0 0 2px var(--white),inset 0 0 0 6px var(--royal-blue)}
.pk-n{padding-right:24px}
.pk-x{display:block;margin-top:16px;padding-top:12px;box-shadow:inset 0 1px 0 var(--light-grey);font-size:13px;line-height:20px;font-weight:600;color:var(--black)}
.pk-x::after{content:"";display:inline-block;width:6px;height:6px;margin-left:8px;border-top:2px solid currentColor;border-right:2px solid currentColor;transform:rotate(45deg);vertical-align:1px}
.pk-f{display:block;margin-top:auto;padding-top:24px;text-transform:none;letter-spacing:0;font-weight:400;color:var(--black)}
.pk-f small{display:block;font-weight:800;font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey)}
.pk-f b{display:block;font-family:var(--font-display);font-weight:400;font-size:40px;line-height:44px;color:var(--royal-blue)}
.pk-f b+small{font-weight:400;font-size:12px;letter-spacing:0;text-transform:none;color:#5A5A5A}
.pk-i:has(input:checked) .pk-ic,.pk-i:has(input:checked) .pk-f b,.pk-i:has(input:checked) .pk-x{color:var(--white)}
.pk-i:has(input:checked) .pk-x{box-shadow:inset 0 1px 0 rgba(255,255,255,.24)}
.pk-i:has(input:checked) .pk-f small{color:rgba(255,255,255,.72)}
.pk-l,.pk-go{display:none}

/* the plan card: shared extras */
.pc-alt{margin-top:16px;text-align:center;font-size:12px;line-height:16px;color:rgba(255,255,255,.64)}
.pc-alt a{color:var(--white);font-weight:700;text-decoration:none;white-space:nowrap}
@media (hover:hover){ .pc-alt a:hover{text-decoration:underline;text-underline-offset:4px} }
.pc-card.is-pt .pc-total b{font-size:40px;line-height:44px}

/* personal training on the left */
.ptx{clear:both;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);column-gap:32px;align-items:start}
.ptx.no-ph{display:block}
.ptx-ph{aspect-ratio:4/5;overflow:hidden;background:#222}
.ptx-ph img{width:100%;height:100%;object-fit:cover;object-position:50% 0}
.ptx-h{font-family:var(--font-display);font-size:40px;line-height:44px;text-transform:uppercase}
.ptx-p{margin-top:12px;font-size:15px;line-height:24px;color:#3A3A3A;max-width:56ch}
.ptx-s{list-style:none;margin:24px 0 0;padding:0;box-shadow:inset 0 1px 0 var(--light-grey)}
.ptx-s li{display:grid;grid-template-columns:32px 1fr;column-gap:16px;padding:12px 0;box-shadow:inset 0 -1px 0 var(--light-grey)}
.ptx-s i{font-style:normal;font-family:var(--font-display);font-size:24px;line-height:24px;color:var(--royal-blue)}
.ptx-s b{display:block;font-size:15px;line-height:24px}
.ptx-s span{font-size:14px;line-height:20px;color:#4A4A4A}

/* ---------- 2.5.1: the plan explains itself ---------- */
.g-steps{list-style:none;margin:24px 0 0;padding:0;box-shadow:inset 0 1px 0 rgba(255,255,255,.16)}
.g-steps li{display:grid;grid-template-columns:32px 1fr;column-gap:16px;align-items:start;padding:16px 0;box-shadow:inset 0 -1px 0 rgba(255,255,255,.16)}
.g-steps i{font-style:normal;display:grid;place-items:center;width:32px;height:32px;border-radius:50%;box-shadow:inset 0 0 0 2px rgba(255,255,255,.32);font-weight:800;font-size:13px;color:rgba(255,255,255,.72)}
.g-steps li.on i{background:var(--accent);color:var(--accent-ink);box-shadow:none}
.g-steps b{display:block;font-size:15px;line-height:20px}
.g-steps span{display:block;font-size:13px;line-height:20px;color:rgba(255,255,255,.6)}
.g-steps li:not(.on) b{color:rgba(255,255,255,.72)}
.is-guide .pc-note{margin-top:24px}

/* ---------- 2.5.2: a photo until there is a plan ---------- */
.pc-card.is-photo{position:relative;display:flex;flex-direction:column;justify-content:flex-end;min-height:480px;padding:0;overflow:hidden}
.pp-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 30%}
.is-photo::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 30%,rgba(0,0,0,.88) 100%)}
.pp-t{position:relative;z-index:1;padding:32px}
.pp-k{font-weight:800;font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.72)}
.pp-h{margin-top:8px;font-family:var(--font-display);font-size:40px;line-height:44px;text-transform:uppercase}
.pc-ph{margin:-32px -32px 24px;aspect-ratio:4/3;overflow:hidden;background:#222}
.pc-ph img{width:100%;height:100%;object-fit:cover;object-position:50% 0}

/* ---------- 2.5.3: cards first, the plan comes when there is one ---------- */
.v3 .pc-opts{display:contents}
.v3 .pc-k{grid-column:1 / -1}
.v3 .pc-q{grid-column:1 / span 7;min-width:0}
.v3 .pc-plan{grid-column:9 / span 4}
.v3.empty .pc-plan{display:none}
.v3.empty .pk-l{display:block;margin-top:24px;box-shadow:inset 0 1px 0 var(--black)}
.v3.empty .pk-l>span{display:flex;justify-content:space-between;gap:16px;padding:10px 0;box-shadow:inset 0 -1px 0 var(--light-grey);font-size:15px;line-height:20px}
.v3.empty .pk-l i{font-style:normal}
.v3.empty .pk-l b{white-space:nowrap}
.v3.empty .pk-l em{display:block;margin-top:12px;font-style:normal;font-size:12px;line-height:16px;color:#5A5A5A}
.v3.empty .pk-go{display:flex;justify-content:center;margin-top:auto;padding:14px 16px;border:2px solid var(--royal-blue);font-family:var(--font-display);font-size:1rem;line-height:1;text-transform:uppercase;color:var(--royal-blue);transition:background .15s,color .15s}
.v3.empty .pk-l+.pk-go{margin-top:24px}
@media (hover:hover){ .v3.empty .pk-i:hover .pk-go{background:var(--royal-blue);color:var(--white)} }
.v3.empty .pk-f,.v3.empty .pk-x{display:none}
.v3.empty .pk-i{padding:32px}
.v3.empty .pk-i::after{top:32px;right:32px}
.v3.empty .pk-d{min-height:40px}

/* ---------- 2.5.5: the plan is a strip under the options ---------- */
.pc.v5{display:block}
.v5 .pc-plan{margin-top:48px}
.v5 .ptx{grid-template-columns:minmax(0,5fr) minmax(0,7fr);column-gap:48px}
.v5 .ptx-ph{aspect-ratio:3/2}
.v5 .pc-card{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,5fr) minmax(0,4fr);column-gap:48px;align-items:start;padding:32px 40px}
.v5 .pc-card>*{grid-column:1}
.v5 .g-prog{grid-column:1 / -1}
.v5 .pc-lines{grid-column:2;grid-row:2 / span 4;margin-top:-12px}
.v5 .pc-total{grid-column:3;grid-row:2;margin-top:0;min-height:0}
.v5 .pc-card .btn{grid-column:3;grid-row:3;margin-top:16px}
.v5 .pc-alt{grid-column:3;grid-row:4}
.v5 .pc-note{margin-top:8px}
.g-prog{display:flex;flex-wrap:wrap;gap:8px 32px;list-style:none;margin:0 0 24px;padding:0 0 20px;box-shadow:inset 0 -1px 0 rgba(255,255,255,.16)}
.g-prog li{display:flex;align-items:center;gap:8px;font-weight:800;font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.48)}
.g-prog i{display:grid;place-items:center;width:24px;height:24px;border-radius:50%;box-shadow:inset 0 0 0 2px rgba(255,255,255,.32);font-style:normal;letter-spacing:0}
.g-prog li.on,.g-prog li.done{color:var(--white)}
.g-prog li.on i{box-shadow:inset 0 0 0 2px var(--white)}
.g-prog li.done i{background:var(--white);color:var(--black);box-shadow:none}
.v5 .is-strip0{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px 48px}
.v5 .is-strip0 .g-prog{margin:0;padding:0;box-shadow:none}
.v5 .is-strip0 .pc-note{margin:0;font-size:14px;line-height:20px}

@media (max-width:1100px){
  .pk-i{padding:16px}
  .pk-i::after{top:16px;right:16px}
  .pk-f b{font-size:32px;line-height:36px}
  .ptx{display:block}
  .ptx-ph{aspect-ratio:16/9;margin-bottom:24px}
  .v3 .pc-q{grid-column:1 / span 7}
  .v3 .pc-plan{grid-column:8 / span 5}
  .v3.empty .pk-i{padding:24px}
  .v3.empty .pk-i::after{top:24px;right:24px}
  .v5 .pc-card{grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:32px}
  .v5 .pc-lines{grid-row:2 / span 2}
  .v5 .pc-total{grid-column:2;grid-row:4;margin-top:24px}
  .v5 .pc-card .btn{grid-column:2;grid-row:5}
  .v5 .pc-alt{grid-column:2;grid-row:6}
}
@media (max-width:768px){
  .pk-i{padding:12px 10px}
  .pk-i::after{top:12px;right:10px;width:16px;height:16px}
  .pk-ic{width:24px;height:24px;margin-bottom:12px}
  .pk-n{padding-right:0}
  .pk-x{display:none}
  .pk-f{padding-top:12px;white-space:normal}
  .pk-f small{font-size:9px;letter-spacing:.1em}
  .pk-f b{font-size:24px;line-height:28px}
  .pk-f b+small{font-size:11px;line-height:14px;letter-spacing:0}
  .ptx-h{font-size:32px;line-height:36px}
  .pc-card.is-photo{min-height:360px}
  .pp-t{padding:24px}
  .pp-h{font-size:32px;line-height:36px}
  .pc-ph{margin:-24px -24px 24px}
  .v3.empty .pk{grid-template-columns:1fr;gap:16px}
  .v3.empty .pk-i{padding:24px}
  .v3.empty .pk-n{min-height:0;font-size:28px;line-height:32px}
  .v3.empty .pk-d{display:block;min-height:0}
  .v3.empty .pk-ic{width:32px;height:32px;margin-bottom:16px}
  .v3.empty .pk-i::after{top:24px;right:24px;width:20px;height:20px}
  .v5 .pc-plan{margin-top:32px}
  .g-prog{gap:8px 16px}
  .g-prog li{letter-spacing:.08em}
  .v5 .pc-card{display:block;padding:24px}
  .v5 .pc-lines{margin-top:16px}
  .v5 .pc-total{margin-top:24px}
}
@media (prefers-reduced-motion:reduce){ .pk-i::after,.pk-ic,.pk-go{transition:none} }
</style>
'''


def make(v, label):
    s = io.open(BASE, encoding='utf-8').read()
    a = s.index('<div class="pc" id="pc">')
    b = s.index('<div class="pt-band" id="pt-band"></div>') + len('<div class="pt-band" id="pt-band"></div>')
    s = s[:a] + MARKUP % {'v': v} + s[b:]
    a = s.index('<script>\n/* 2.4.9: the price builder')
    b = s.index('</script>', a) + len('</script>')
    s = s[:a] + JS % {'v': v, 'label': label} + s[b:]
    a = s.index('<style id="price-list-css">')
    s = s[:a] + CSS + s[a:]
    out = 'elite-wellness-landing_2-5-%d.html' % v
    io.open(out, 'w', encoding='utf-8').write(s)
    print(out)


if __name__ == '__main__':
    for v, label in VARIANTS.items():
        make(v, label)
