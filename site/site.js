/*
  ELITE WELLNESS: everything the page does. Both pages load this one file:
  index.html (Portuguese) and en/index.html (English).

  The page says which language it is with <html lang="pt-PT"> or <html lang="en">.
  Every word a script writes is in WORDS below, once in English and once in
  Portuguese. To change such a word, change it in both. Words that are written
  in the page itself are changed in both pages (build/check_pages.py compares them).

  Prices come from prices.js, the timetable from schedule.js, reviews from
  reviews.js. No price is ever typed into this file.
*/
(function(){
'use strict';

var root=document.documentElement;
var LANG=(root.lang||'en').slice(0,2).toLowerCase()==='pt'?'pt':'en';
var BASE=((document.currentScript&&document.currentScript.src)||'').replace(/site\.js.*$/,'');   /* where the shared files are, from either page */
var mo=root.classList.contains('mo');   /* motion is wanted (set in the page head) */
var PHONE='https://wa.me/351926565836?text=', MAPS='https://maps.app.goo.gl/ks6o4URGCYT7rzHJ8';
var DAYS=['mon','tue','wed','thu','fri','sat','sun'];

/* ---------- the words ---------- */
var WORDS={
  en:{
    locale:'en-GB',
    dayShort:{mon:'Mon',tue:'Tue',wed:'Wed',thu:'Thu',fri:'Fri',sat:'Sat',sun:'Sun'},
    dayLong:{mon:'Monday',tue:'Tuesday',wed:'Wednesday',thu:'Thursday',fri:'Friday',sat:'Saturday',sun:'Sunday'},
    today:'Today', tomorrow:'Tomorrow',
    /* open now */
    openNow:'Open now', until:function(t){ return 'until '+t }, opens:'Opens',
    opensWhen:function(day,t){ return (day||'today')+' '+t },
    /* menu */
    openMenu:'Open menu', closeMenu:'Close menu',
    /* reviews */
    thisMonth:'This month', monthAgo:'A month ago', monthsAgo:function(n){ return n+' months ago' },
    yearAgo:'A year ago', yearsAgo:function(n){ return n+' years ago' },
    gReview:'Google review', more:'More', stars:function(n){ return n+' out of 5 stars' },
    score:function(r,c){ return r+' · '+c+' Google reviews' },
    /* timetable */
    nextClass:'Next class:', next:'Next', isNew:'new!', time:'Time', min:'min', or:' or ',
    updated:function(d){ return 'Updated '+d },
    showClass:function(n){ return 'Show '+n },
    classCard:function(n){ return n+': what it is and when it is on' },
    showAll:'Show all classes',
    /* floor plan */
    planTitle:"What's where", planHint:'Tap any area on the plan',
    /* prices */
    qKind:'How do you want to train?', from:'From',
    kinds:{
      pass:{name:'Passes',            desc:'No commitment',       per:'for a day'},
      mem: {name:'Membership',        desc:'Best value',          per:'every 2 weeks with direct debit'},
      pt:  {name:'Personal training', desc:'With your own coach', per:'a session'}
    },
    qStay:'How long?', qPlan:'How often?', paidEvery:'Paid every 2 weeks', qPay:'How will you pay?',
    dd:'Direct debit', desk:'At reception', off:function(m){ return m+' off' }, recommended:'Recommended',
    howItWorks:'How it works',
    steps:[['Message us','Say what you want to work on.'],['Meet your coach','A first talk at the gym.'],['Train','One to one, to a plan made for you.']],
    passTitle:function(v,name){ return v.days===1?'Day pass':name+' pass' },
    planTitle2:function(name){ return name+' membership' },
    getPass:'Get this pass', getPlan:'Get this plan',
    gymAndClasses:'Gym and every class', included:'Included', insurance:'Sports insurance', insuranceYear:'Sports insurance, 1 year',
    first2:'First 2 weeks', total:'Total', firstPayment:'First payment',
    then:function(m,dd){ return 'Then '+m+' every 2 weeks'+(dd?' by direct debit.':' at reception.') },
    bringId:'Photo ID', bringIban:'Your IBAN, for the direct debit',
    yourPlan:'Your plan',
    pt:'Personal training', ptKicker:'Made around you', ptText:'Your coach sets the goal with you and builds every session around it.',
    ptFrom:function(m){ return 'From '+m+' a session. The price is agreed with your coach.' },
    ptBook:'Book a time on WhatsApp', ptCall:'Prefer to talk? Call',
    ptAlt:'A coach guiding a member through a lunge in a personal training session at Elite Wellness',
    ptLive:'Personal training: book a time on WhatsApp to talk to a coach.',
    bookMsg:'Hi! I would like to book a time to talk to a coach about personal training.',
    askMsg:function(title){ return 'Hi! I have a question about the '+title+'.' },
    close:'Close', buyNow:'Buy now', change:'Change',
    oneStep:'One step left', finish:'Finish at reception', finishText:'We set up every plan in person. Nothing has been charged.',
    payAtDesk:'To pay at reception', bring:'Bring', directions:'Directions'
  },
  pt:{
    locale:'pt-PT',
    dayShort:{mon:'Seg',tue:'Ter',wed:'Qua',thu:'Qui',fri:'Sex',sat:'Sáb',sun:'Dom'},
    dayLong:{mon:'Segunda',tue:'Terça',wed:'Quarta',thu:'Quinta',fri:'Sexta',sat:'Sábado',sun:'Domingo'},
    today:'Hoje', tomorrow:'Amanhã',
    openNow:'Aberto', until:function(t){ return 'até às '+t }, opens:'Abre',
    opensWhen:function(day,t){ return (day?day.toLowerCase():'hoje')+' às '+t },
    openMenu:'Abrir menu', closeMenu:'Fechar menu',
    thisMonth:'Este mês', monthAgo:'Há um mês', monthsAgo:function(n){ return 'Há '+n+' meses' },
    yearAgo:'Há um ano', yearsAgo:function(n){ return 'Há '+n+' anos' },
    gReview:'Avaliação no Google', more:'Mais', stars:function(n){ return n+' de 5 estrelas' },
    score:function(r,c){ return String(r).replace('.',',')+' · '+c+' avaliações no Google' },
    nextClass:'Próxima aula:', next:'A seguir', isNew:'nova!', time:'Hora', min:'min', or:' ou ',
    updated:function(d){ return 'Atualizado a '+d },
    showClass:function(n){ return 'Mostrar '+n },
    classCard:function(n){ return n+': o que é e quando há' },
    showAll:'Mostrar todas as aulas',
    planTitle:'O que há onde', planHint:'Toca numa zona da planta',
    qKind:'Como queres treinar?', from:'Desde',
    kinds:{
      pass:{name:'Passes',               desc:'Sem compromisso',     per:'por um dia'},
      mem: {name:'Adesão',               desc:'Melhor preço',        per:'a cada 2 semanas por débito direto'},
      pt:  {name:'Treino personalizado', desc:'Com o teu treinador', per:'por sessão'}
    },
    qStay:'Quanto tempo?', qPlan:'Quantas vezes?', paidEvery:'Pago a cada 2 semanas', qPay:'Como queres pagar?',
    dd:'Débito direto', desk:'Na receção', off:function(m){ return 'menos '+m }, recommended:'Recomendado',
    howItWorks:'Como funciona',
    steps:[['Escreve-nos','Diz-nos o que queres trabalhar.'],['Conhece o teu treinador','Uma primeira conversa no ginásio.'],['Treina','Individual, com um plano feito para ti.']],
    passTitle:function(v,name){ return v.days===1?'Passe diário':'Passe de '+name },
    planTitle2:function(name){ return 'Adesão '+name },
    getPass:'Quero este passe', getPlan:'Quero este plano',
    gymAndClasses:'Ginásio e todas as aulas', included:'Incluído', insurance:'Seguro desportivo', insuranceYear:'Seguro desportivo, 1 ano',
    first2:'Primeiras 2 semanas', total:'Total', firstPayment:'Primeiro pagamento',
    then:function(m,dd){ return 'Depois, '+m+' a cada 2 semanas'+(dd?' por débito direto.':' na receção.') },
    bringId:'Documento de identificação com fotografia', bringIban:'O teu IBAN, para o débito direto',
    yourPlan:'O teu plano',
    pt:'Treino personalizado', ptKicker:'Feito à tua medida', ptText:'O teu treinador define o objetivo contigo e constrói cada sessão à volta dele.',
    ptFrom:function(m){ return 'Desde '+m+' por sessão. O preço é combinado com o teu treinador.' },
    ptBook:'Marca pelo WhatsApp', ptCall:'Preferes falar? Liga',
    ptAlt:'Um treinador a acompanhar uma sócia num lunge, numa sessão de treino personalizado no Elite Wellness',
    ptLive:'Treino personalizado: marca pelo WhatsApp uma conversa com um treinador.',
    bookMsg:'Olá! Gostava de marcar uma conversa com um treinador sobre treino personalizado.',
    askMsg:function(title){ return 'Olá! Tenho uma pergunta sobre: '+title+'.' },
    close:'Fechar', buyNow:'Comprar agora', change:'Alterar',
    oneStep:'Falta um passo', finish:'Termina na receção', finishText:'Ativamos todos os planos presencialmente. Não foi cobrado nada.',
    payAtDesk:'A pagar na receção', bring:'Traz', directions:'Como chegar'
  }
};
var T=WORDS[LANG];

/* ---------- small helpers ---------- */
function esc(t){ return String(t).replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c] }) }
function $(id){ return document.getElementById(id) }
function all(sel,el){ return [].slice.call((el||document).querySelectorAll(sel)) }
/* the name of a price or a class in this page's language */
function nm(x){ return (LANG==='pt'&&x.namePt)||x.name }
/* a price as each language writes it: the euro sign in front in English; behind, after a space and with a comma for the cents, in Portuguese */
function money(n){
  if(n==null) return '';
  var s=(Math.round(n*100)/100).toFixed(2); if(s.slice(-3)==='.00') s=s.slice(0,-3);
  return LANG==='pt'?s.replace('.',',')+' €':'€'+s;
}
/* the day and time in Lisbon, wherever the visitor is */
function lisbon(){
  var p={}; new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Lisbon',weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date()).forEach(function(x){ p[x.type]=x.value });
  return {day:(p.weekday||'').toLowerCase().slice(0,3), hm:(p.hour==='24'?'00':p.hour)+':'+p.minute};
}
/* counting visitors: does nothing until a counting tool is connected, e.g.
   window.EW_TRACK = function(name, props){ plausible(name, {props:props}) } */
function track(name,props){
  if(typeof window.EW_TRACK==='function'){ try{ window.EW_TRACK(name,props||{}) }catch(e){} }
  if(window.EW_TRACK_DEBUG) console.log('[track]',name,props||{});
}

/* ---------- the language button keeps you in the same section ---------- */
(function(){
  var a=$('lang-btn'); if(!a) return;
  a.addEventListener('click',function(){ if(location.hash) a.href=a.getAttribute('href').replace(/#.*$/,'')+location.hash });
})();

/* ---------- the action bar follows you; the map fades in instead of flashing white ---------- */
(function(){
  var bar=$('action-bar');
  if(bar){
    var upd=function(){ bar.classList.toggle('on',window.scrollY>window.innerHeight*.9) };
    upd(); window.addEventListener('scroll',upd,{passive:true}); window.addEventListener('resize',upd);
  }
  var wrap=$('find-map'), frame=$('map-frame');
  if(wrap&&frame){
    var ready=function(){ wrap.classList.add('ready') };
    frame.addEventListener('load',ready); setTimeout(ready,4000);
  }
})();

/* ---------- the design grid, shown with ?grid=1 ---------- */
(function(){
  if(new URLSearchParams(location.search).get('grid')!=='1') return;
  document.body.classList.add('show-grid');
  var b=document.createElement('div'); b.className='grid-badge';
  b.textContent=innerWidth>768?'12 col / 24px gutters / 4px baseline':'4 col / 16px gutters / 4px baseline';
  document.body.appendChild(b);
})();

/* ---------- open now (Mon to Fri 07:00 to 21:00, Sat 09:00 to 13:00) and the phone menu ---------- */
var HOURS={mon:['07:00','21:00'],tue:['07:00','21:00'],wed:['07:00','21:00'],thu:['07:00','21:00'],fri:['07:00','21:00'],sat:['09:00','13:00']};
function status(){
  var now=lisbon(), i=DAYS.indexOf(now.day), els=all('[data-status]'), h=HOURS[now.day];
  /* the bar on a phone gets a short two line version, everything else gets the full line */
  function put(cls,head,tail){
    els.forEach(function(el){
      var key=el.getAttribute('data-status'); el.className=key+cls;
      el.innerHTML=key==='bar-status'
        ? '<span class="dot"></span><span class="bs-txt"><b>'+head+'</b><span>'+tail+'</span></span>'
        : '<span class="dot"></span>'+head+' · <b>'+tail+'</b>';
    });
  }
  if(h&&now.hm>=h[0]&&now.hm<h[1]){ put('',T.openNow,T.until(h[1])); return }
  for(var k=0;k<8;k++){
    var d=DAYS[(i+k)%7], hh=HOURS[d]; if(!hh) continue;
    if(k===0&&now.hm>=hh[0]) continue;
    put(' closed',T.opens,T.opensWhen(k===0?'':T.dayShort[d],hh[0])); return;
  }
}
(function(){
  var btn=$('menu-btn'), menu=$('menu');
  if(btn&&menu){
    var setOpen=function(open){
      root.classList.toggle('menu-open',open);
      root.style.overflow=open?'hidden':'';
      btn.setAttribute('aria-expanded',open?'true':'false');
      btn.setAttribute('aria-label',open?T.closeMenu:T.openMenu);
      menu.setAttribute('aria-hidden',open?'false':'true');
      if(open) status();
    };
    btn.addEventListener('click',function(){ setOpen(!root.classList.contains('menu-open')) });
    menu.addEventListener('click',function(e){
      var a=e.target.closest('a[href^="#"]'); if(!a) return;
      e.preventDefault(); setOpen(false);
      var t=document.querySelector(a.getAttribute('href'));
      if(t){ var y=t.getBoundingClientRect().top+window.scrollY-document.querySelector('header').offsetHeight; window.scrollTo({top:y,behavior:'smooth'}) }
    });
    document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&root.classList.contains('menu-open')){ setOpen(false); btn.focus() } });
    window.addEventListener('resize',function(){ if(window.innerWidth>768&&root.classList.contains('menu-open')) setOpen(false) });
  }
  status(); setInterval(status,60000);
  /* today's line in the opening hours */
  var day=lisbon().day, li=all('.hours-row li')[day==='sat'?1:day==='sun'?2:0];
  if(li){ li.classList.add('today'); var f=document.createElement('i'); f.className='hr-now'; f.textContent=T.today; li.querySelector('.hr-d').appendChild(f) }
})();

/* ---------- a thin line under the header shows how far down the page you are ---------- */
(function(){
  var head=document.querySelector('header'), busy=false; if(!head) return;
  function read(){ busy=false; var max=root.scrollHeight-innerHeight; head.style.setProperty('--read',max>0?Math.min(1,scrollY/max).toFixed(4):0) }
  addEventListener('scroll',function(){ if(!busy){ busy=true; requestAnimationFrame(read) } },{passive:true});
  addEventListener('resize',read); read();
})();

/* ---------- reviews: built from reviews.js. One row until there are eight, then two rows ---------- */
(function(){
  var R=window.ELITE_REVIEWS, marquee=document.querySelector('.marquee'); if(!R||!marquee) return;
  var rows=[$('rv-row-1'),$('rv-row-2')], SPEED=32;   /* pixels a second */
  function ago(ym){
    if(!ym) return '';
    var p=ym.split('-'), now=new Date(), m=(now.getFullYear()-(+p[0]))*12+(now.getMonth()+1-(+p[1]));
    if(m<=0) return T.thisMonth; if(m===1) return T.monthAgo; if(m<12) return T.monthsAgo(m);
    var y=Math.floor(m/12); return y===1?T.yearAgo:T.yearsAgo(y);
  }
  function card(r,hidden){
    var n=Math.max(1,Math.min(5,Math.round(r.stars||5))), note=(LANG==='pt'&&r.notePt)||r.note;
    /* a review opens itself on Google when it has its own link; the gym's page until then */
    return '<a class="rv-card" href="'+esc(r.url||R.url)+'" target="_blank" rel="noopener"'+(hidden?' aria-hidden="true" tabindex="-1"':'')+'>'+
      '<div class="rv-top"><span class="rv-avatar" aria-hidden="true">'+esc(r.name.charAt(0))+'</span>'+
      '<span class="rv-who"><span class="rv-name">'+esc(r.name)+'</span><span class="rv-meta">'+esc(note||T.gReview)+'</span></span></div>'+
      '<div class="rv-line"><span class="rv-stars" aria-label="'+T.stars(n)+'">'+'★★★★★'.slice(0,n)+'</span>'+(r.date?'<span>'+ago(r.date)+'</span>':'')+'</div>'+
      '<div class="rv-body"><p class="rv-text" lang="en">'+esc(r.text)+'</p><span class="rv-more">'+T.more+'</span></div></a>';
  }
  var sm=$('rv-summary'); if(sm){ sm.href=R.url; $('rv-score').textContent=T.score(R.rating,R.count) }
  var sets=[[],[]]; R.reviews.forEach(function(r,i){ sets[i%2].push(r) });
  /* with few reviews two rows show the same card twice on one screen */
  if(R.reviews.length<8){ sets=[R.reviews.slice()]; rows[1].style.display='none'; rows=[rows[0]] }
  var anims=[], builtFor=0;
  function build(){
    anims.forEach(function(a){ a.cancel() }); anims=[];
    var view=Math.max(marquee.clientWidth,window.innerWidth);
    rows.forEach(function(row,k){
      var list=sets[k];
      row.innerHTML=list.map(function(r){ return card(r,false) }).join('');
      var cards=row.children, step=cards[cards.length-1].offsetLeft+cards[cards.length-1].offsetWidth+parseFloat(getComputedStyle(cards[0]).marginRight)-cards[0].offsetLeft;
      var copies=Math.max(1,Math.ceil((view+step)/step)), html='';
      for(var c=0;c<copies*2;c++) html+=list.map(function(r){ return card(r,c>0) }).join('');
      row.innerHTML=html;
      var dist=step*copies;   /* the exact length of one copy, in pixels */
      row.style.width=(dist*2)+'px';
      all('.rv-text',row).forEach(function(t){ if(t.scrollHeight>t.clientHeight+1) t.closest('.rv-card').classList.add('is-clamped') });
      if(window.matchMedia('(prefers-reduced-motion: reduce)').matches||!row.animate) return;
      var from='translate3d(0,0,0)', to='translate3d('+(-dist)+'px,0,0)';
      anims.push(row.animate(k===0?[{transform:from},{transform:to}]:[{transform:to},{transform:from}],{duration:dist/SPEED*1000,iterations:Infinity,easing:'linear'}));
    });
    builtFor=view;
  }
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(build); else build();
  marquee.addEventListener('mouseenter',function(){ anims.forEach(function(a){ a.pause() }) });
  marquee.addEventListener('mouseleave',function(){ anims.forEach(function(a){ a.play() }) });
  var t; window.addEventListener('resize',function(){ clearTimeout(t); t=setTimeout(function(){ if(Math.abs(Math.max(marquee.clientWidth,window.innerWidth)-builtFor)>40) build() },200) });
})();

/* ---------- classes and the timetable: built from schedule.js ---------- */
(function(){
  var S=window.ELITE_SCHEDULE, tt=$('timetable'); if(!S||!tt) return;
  var sessions=S.sessions.slice().sort(function(a,b){ return DAYS.indexOf(a.day)-DAYS.indexOf(b.day)||a.time.localeCompare(b.time) });
  var days=DAYS.filter(function(d){ return sessions.some(function(x){ return x.day===d }) });
  var times=Array.from(new Set(sessions.map(function(x){ return x.time }))).sort();
  function info(x){ return S.classes[x.class]||{name:x.class,en:''} }
  function tag(c){ return (LANG==='pt'&&c.pt)||c.en||'' }
  function about(c){ return (LANG==='pt'&&c.aboutPt)||c.about||'' }
  var now=lisbon(), today=now.day, ti=DAYS.indexOf(today), next=null;

  /* the next class from now, wrapping to next week */
  for(var k=0;k<8&&!next;k++){
    var d=DAYS[(ti+k)%7];
    next=sessions.find(function(x){ return x.day===d&&(k>0||x.time>now.hm) })||null;
  }
  function when(x){ return x.day===today?T.today:DAYS[(ti+1)%7]===x.day?T.tomorrow:T.dayLong[x.day] }
  if(next) $('tt-next').innerHTML=T.nextClass+' <b>'+when(next)+' '+next.time+' · '+esc(info(next).name)+'</b>';

  function cellHTML(x,flag){
    var c=info(x);
    return '<div class="tt-name">'+esc(c.name)+(flag?'<span class="tt-flag">'+T.next+'</span>':'')+(x.isNew?'<span class="tt-new">'+T.isNew+'</span>':'')+'</div>'+
      '<div class="tt-desc">'+esc(tag(c))+'</div>';
  }
  function dur(t){ var x=sessions.find(function(s){ return s.time===t }); return x&&x.minutes?x.minutes+' '+T.min:'' }

  /* the week as a table, on a desktop */
  var h='<thead><tr><th class="tt-time" scope="col"><span class="sr-only">'+T.time+'</span></th>';
  days.forEach(function(d){ h+='<th scope="col"'+(d===today?' class="is-today"':'')+'>'+T.dayLong[d]+(d===today?'<small>'+T.today+'</small>':'')+'</th>' });
  h+='</tr></thead><tbody>';
  times.forEach(function(t){
    h+='<tr><th class="tt-time" scope="row"><b>'+t+'</b><span>'+dur(t)+'</span></th>';
    days.forEach(function(d){
      var x=sessions.find(function(s){ return s.day===d&&s.time===t }), isNext=x&&next&&x===next;
      h+='<td class="tt-cell'+(d===today?' is-today':'')+(isNext?' is-next':'')+'"'+(x?' data-cls="'+esc(x.class)+'"':'')+'>'+(x?cellHTML(x,isNext):'')+'</td>';
    });
    h+='</tr>';
  });
  $('tt-table').innerHTML=h+'</tbody>';

  /* a day at a time, on a phone: tabs, and a swipe left or right */
  var tabs=$('tt-tabs'), list=$('tt-list'), cur=0, calm=window.matchMedia('(prefers-reduced-motion:reduce)');
  var busiest={}; sessions.forEach(function(x){ busiest[x.day]=(busiest[x.day]||0)+1 });
  list.style.setProperty('--tt-rows',Math.max.apply(null,days.map(function(d){ return busiest[d] })));   /* the list keeps the height of its busiest day */
  function showDay(d){
    cur=Math.max(0,days.indexOf(d));
    all('button',tabs).forEach(function(b){ b.setAttribute('aria-selected',b.dataset.day===d?'true':'false') });
    list.innerHTML=sessions.filter(function(x){ return x.day===d }).map(function(x){
      var isNext=next&&x===next;
      return '<li class="'+(isNext?'is-next':'')+'" data-cls="'+esc(x.class)+'"><div class="tt-time"><b>'+x.time+'</b><span>'+(x.minutes?x.minutes+' '+T.min:'')+'</span></div><div>'+cellHTML(x,isNext)+'</div></li>';
    }).join('');
    paint();
  }
  tabs.innerHTML=days.map(function(d){ return '<button type="button" role="tab" data-day="'+d+'">'+T.dayShort[d]+'</button>' }).join('');
  tabs.addEventListener('click',function(e){ var b=e.target.closest('button'); if(b) showDay(b.dataset.day) });
  function step(n){
    var i=Math.min(days.length-1,Math.max(0,cur+n)); if(i===cur) return;
    showDay(days[i]);
    if(calm.matches) return;
    list.classList.remove('in-l','in-r'); void list.offsetWidth; list.classList.add(n<0?'in-l':'in-r');
  }
  var x0=null, y0=null;
  list.addEventListener('touchstart',function(e){ var t=e.changedTouches[0]; x0=t.clientX; y0=t.clientY },{passive:true});
  list.addEventListener('touchend',function(e){
    if(x0===null) return;
    var t=e.changedTouches[0], dx=t.clientX-x0, dy=t.clientY-y0; x0=null;
    if(Math.abs(dx)>48&&Math.abs(dx)>Math.abs(dy)*1.5) step(dx<0?1:-1);
  },{passive:true});

  /* tap a class, on a card or in the timetable: what it is, when it is on, and only its slots lit */
  var cards=all('.class-card'), picked=null;
  var box=document.createElement('div'); box.className='tt-pick'; box.setAttribute('aria-live','polite'); tt.querySelector('.tt-head').appendChild(box);
  function slots(key){ return sessions.filter(function(x){ return x.class===key }) }
  function paint(){
    tt.classList.toggle('pick',!!picked);
    all('.tt-cell,.tt-list li',tt).forEach(function(c){ c.classList.toggle('hit',!!picked&&c.dataset.cls===picked) });
    cards.forEach(function(c){ var on=!!picked&&c.dataset.cls===picked; c.classList.toggle('on',on); if(c.dataset.cls) c.setAttribute('aria-pressed',on?'true':'false') });
    all('button',tabs).forEach(function(b){ b.classList.toggle('has',!!picked&&sessions.some(function(x){ return x.day===b.dataset.day&&x.class===picked })) });
    if(!picked){ box.innerHTML=''; return }
    var c=S.classes[picked], mins=slots(picked).map(function(x){ return x.minutes }).filter(function(v,i,a){ return v&&a.indexOf(v)===i }).sort(function(a,b){ return a-b });
    box.innerHTML='<p class="tt-pick-n">'+esc(c.name)+'</p>'+(about(c)?'<p class="tt-pick-d">'+esc(about(c))+'</p>':'')+
      '<p class="tt-pick-s">'+slots(picked).map(function(x){ return T.dayShort[x.day]+' '+x.time }).join(' · ')+(mins.length?' · '+mins.join(T.or)+' '+T.min:'')+'<button type="button">'+T.showAll+'</button></p>';
  }
  function pick(key,scroll){
    picked=picked===key?null:key; paint();
    if(!picked) return;
    /* on a phone open the first day it runs, from today on, unless the open day already has it */
    var ds=slots(picked).map(function(x){ return x.day }), first=ds.filter(function(d){ return DAYS.indexOf(d)>=ti })[0]||ds[0];
    if(ds.indexOf(days[cur])<0&&first) showDay(first);
    if(scroll) tt.scrollIntoView({behavior:mo?'smooth':'auto',block:'center'});
  }
  var byName={}; Object.keys(S.classes).forEach(function(key){ byName[S.classes[key].name.toLowerCase()]=key });
  cards.forEach(function(c){
    var name=(c.querySelector('.class-name').textContent||'').trim(), key=byName[name.toLowerCase()]; if(!key) return;
    c.dataset.cls=key; c.tabIndex=0; c.setAttribute('role','button'); c.setAttribute('aria-pressed','false'); c.setAttribute('aria-label',T.classCard(name));
    var on=DAYS.filter(function(d){ return sessions.some(function(x){ return x.day===d&&x.class===key }) }).map(function(d){ return T.dayShort[d] });
    var el=document.createElement('div'); el.className='class-days'; el.innerHTML=on.join(' · ')+'<i aria-hidden="true">&darr;</i>'; c.querySelector('.class-overlay').appendChild(el);
    c.addEventListener('click',function(){ pick(key,true) });
    c.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); pick(key,true) } });
  });
  tt.addEventListener('click',function(e){
    if(e.target.closest('.tt-pick button')){ if(picked) pick(picked); return }
    var c=e.target.closest('.tt-cell[data-cls],.tt-list li[data-cls]'); if(c) pick(c.dataset.cls,false);
  });

  showDay(days.indexOf(today)>-1?today:(next?next.day:days[0]));
  if(S.updated){ var u=new Date(S.updated+'T12:00:00'); $('tt-updated').textContent=T.updated(u.toLocaleDateString(T.locale,{day:'numeric',month:'long',year:'numeric'})) }

  /* on a phone the class cards are a strip you swipe; the dots follow it */
  var grid=document.querySelector('.classes-grid'), dots=$('classes-dots');
  if(grid&&dots){
    dots.innerHTML=cards.map(function(c,i){
      var name=(c.querySelector('.class-name')||{}).textContent||String(i+1);
      return '<button type="button" role="tab" aria-label="'+esc(T.showClass(name))+'" aria-selected="'+(i?'false':'true')+'"></button>';
    }).join('');
    var btns=all('button',dots), tick;
    btns.forEach(function(b,i){ b.addEventListener('click',function(){ grid.scrollTo({left:cards[i].offsetLeft-cards[0].offsetLeft,behavior:'smooth'}) }) });
    grid.addEventListener('scroll',function(){
      clearTimeout(tick);
      tick=setTimeout(function(){
        var x=grid.scrollLeft, best=0, far=Infinity;
        cards.forEach(function(c,i){ var v=Math.abs((c.offsetLeft-cards[0].offsetLeft)-x); if(v<far){ far=v; best=i } });
        btns.forEach(function(b,i){ b.setAttribute('aria-selected',i===best?'true':'false') });
      },60);
    },{passive:true});
  }
})();

/* ---------- the floor plan: highlight from the list or the markers, swipe and tap on a phone ---------- */
(function(){
  var map=document.querySelector('.gym-map'); if(!map) return;
  var scroller=map.querySelector('.gym-plan'), info=map.querySelector('.plan-info'), hint=map.querySelector('.plan-hint');
  var mob=window.matchMedia('(max-width:768px)'), cur=null, data={};
  all('.gym-legend li',map).forEach(function(li){
    data[li.getAttribute('data-z')]={n:li.querySelector('.gl-n').textContent,t:li.querySelector('.gl-t').textContent,s:li.querySelector('.gl-s').textContent};
  });
  var count=Object.keys(data).length;
  function svg(){ return map.querySelector('svg[data-style="'+map.getAttribute('data-style')+'"]') }
  function centre(z,smooth){
    if(!mob.matches) return;
    var mk=svg().querySelector('.mk[data-z="'+z+'"] .mk-c')||svg().querySelector('.z[data-z="'+z+'"] .zf'); if(!mk) return;
    var r=mk.getBoundingClientRect(), s=scroller.getBoundingClientRect();
    scroller.scrollTo({left:scroller.scrollLeft+(r.left+r.width/2)-(s.left+s.width/2),behavior:smooth?'smooth':'auto'});
  }
  function set(z,scroll){
    cur=z;
    map.classList.toggle('hl',!!z);
    all('[data-z]',map).forEach(function(e){ e.classList.toggle('on',!!z&&e.getAttribute('data-z')===z) });
    var d=z&&data[z];
    info.classList.toggle('idle',!d);
    info.querySelector('.pi-n').textContent=d?d.n:'00';
    info.querySelector('.pi-t').textContent=d?d.t:T.planTitle;
    info.querySelector('.pi-s').textContent=d?d.s:T.planHint;
    if(z&&scroll) centre(z,true);
  }
  all('.gym-legend li',map).forEach(function(li){
    li.addEventListener('mouseenter',function(){ set(li.getAttribute('data-z')) });
    li.addEventListener('click',function(){ set(li.classList.contains('on')?null:li.getAttribute('data-z')) });
  });
  map.querySelector('.gym-legend').addEventListener('mouseleave',function(){ set(null) });
  all('.plan .mk,.plan .tap',map).forEach(function(mk){
    var z=mk.getAttribute('data-z');
    mk.addEventListener('mouseenter',function(){ if(!mob.matches) set(z) });
    mk.addEventListener('mouseleave',function(){ if(!mob.matches) set(null) });
    mk.addEventListener('click',function(){ set(cur===z&&!mob.matches?null:z,true) });
    mk.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); set(z,true) } });
  });
  all('[data-step]',info).forEach(function(b){
    b.addEventListener('click',function(){
      var n=(cur?+cur:0)+(+b.getAttribute('data-step')); if(n<1) n=count; if(n>count) n=1;
      set(String(n),true);
    });
  });
  /* the route draws itself the first time the plan comes into view */
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ map.classList.remove('draw'); void map.offsetWidth; map.classList.add('draw'); io.disconnect() } },{threshold:.35});
    io.observe(scroller);
  }
  /* on a phone the plan opens on the entrance, where the route starts; the hint goes once people swipe */
  function start(){
    if(!mob.matches) return;
    var el=scroller.querySelector('.plan circle.acc:not(.pulse)');
    if(!el){ scroller.scrollLeft=(scroller.scrollWidth-scroller.clientWidth)/2; return }
    scroller.scrollLeft=0;
    var r=el.getBoundingClientRect(), b=scroller.getBoundingClientRect();
    scroller.scrollLeft=(r.left+r.width/2)-(b.left+b.width/2)+40;
  }
  start(); window.addEventListener('load',start);
  var s0=null;
  scroller.addEventListener('scroll',function(){ if(s0===null){ s0=scroller.scrollLeft; return } if(Math.abs(scroller.scrollLeft-s0)>12) hint.classList.add('gone') },{passive:true});
  setTimeout(function(){ hint.classList.add('gone') },6000);
})();

/* ---------- prices. Every price comes from prices.js. Something is always chosen, so the plan
   always shows a real price: Membership, the recommended plan and direct debit when the page
   opens, the day pass when you tap Passes. Personal training has no price to add up, so it
   books a first talk on WhatsApp instead.
   Get this plan opens a sheet: check the plan, Buy now, then Finish at reception. We do not take
   payment online; the two steps count how many people would buy online (pricing_review, then
   pricing_confirm), which says whether paying online is worth building. ---------- */
(function(){
  var P=window.ELITE_PRICES, opts=$('pc-opts'), kEl=$('pc-k'), qEl=$('pc-q'), box=$('pc-plan'), pc=$('pc'), live=$('pc-live');
  if(!P||!opts||!box) return;
  var off=P.member.plans[0].desk-P.member.plans[0].dd;
  function find(list,id){ return list.filter(function(x){ return x.id===id })[0] }
  var ptFrom=Math.min.apply(null,P.pt.packs.map(function(k){ return k.each }));
  var memFrom=Math.min.apply(null,P.member.plans.map(function(p){ return p.dd }));
  var first=P.visitor[0], best=P.member.plans.filter(function(p){ return p.best })[0]||P.member.plans[P.member.plans.length-1];

  /* one line icons on a 32 grid, 2px, square ends: what each product is at a glance */
  var IC={
    pass:'<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M3 9h26v4.6a2.4 2.4 0 0 0 0 4.8V23H3v-4.6a2.4 2.4 0 0 0 0-4.8z"/><path class="ic-cut" d="M21 11v10"/><path d="M8 14h8M8 18h5"/></svg>',
    mem:'<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M4 7h24v21H4zM4 12h24M10 4v5M22 4v5"/><path d="M20.4 21.6a4.6 4.6 0 1 1-1-4.9"/><path d="M20.2 14.6v3h-3"/></svg>',
    pt:'<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="11" cy="9" r="4"/><path d="M3 28v-3a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v3"/><circle cx="22.5" cy="10.5" r="3"/><path d="M21.5 18.5h1.5a6 6 0 0 1 6 6V28"/></svg>'
  };
  var KINDS=[{id:'pass',from:money(first.price)},{id:'mem',from:money(memFrom)},{id:'pt',from:money(ptFrom)}];
  var PT_IMG='<img src="'+BASE+'assets/pt-session-800.webp" srcset="'+BASE+'assets/pt-session-800.webp 800w, '+BASE+'assets/pt-session.webp 1600w" sizes="(max-width:768px) 100vw, 30vw" width="1600" height="1200" loading="lazy" alt="'+esc(T.ptAlt)+'">';

  /* each product remembers its own choice when you look at another */
  var st={kind:'mem',stay:first.id,plan:best.id,pay:'dd'}, cur=null;

  function radio(name,value,checked){ return '<input type="radio" name="'+name+'" value="'+value+'"'+(checked?' checked':'')+'>' }
  function set(legend,body,aside){ return '<fieldset class="pc-set"><legend class="pc-leg">'+legend+(aside?'<small>'+aside+'</small>':'')+'</legend>'+body+'</fieldset>' }
  function tile(name,i){
    return '<label class="op">'+radio(name,i.id,st[name]===i.id)+(i.tag?'<span class="tag op-badge">'+i.tag+'</span>':'')+
      '<span class="op-n">'+i.name+(i.chip?'<span class="tag op-chip">'+i.chip+'</span>':'')+'</span><span class="op-p">'+i.p+'</span></label>';
  }
  function row(items,name){ return '<div class="op-row c'+items.length+'">'+items.map(function(i){ return tile(name,i) }).join('')+'</div>' }
  function products(){
    return '<div class="pk">'+KINDS.map(function(k){
      var w=T.kinds[k.id];
      return '<label class="pk-i">'+radio('kind',k.id,st.kind===k.id)+'<span class="pk-ic">'+IC[k.id]+'</span>'+
        '<span class="pk-n">'+w.name+'</span><span class="pk-d">'+w.desc+'</span>'+
        '<span class="pk-f"><small>'+T.from+'</small><b>'+k.from+'</b><small>'+w.per+'</small></span></label>';
    }).join('')+'</div>';
  }
  function renderOpts(){
    var dd=st.pay==='dd', plan=find(P.member.plans,st.plan), h='';
    kEl.innerHTML=set(T.qKind,products());
    if(st.kind==='pass')
      h=set(T.qStay,row(P.visitor.map(function(v){ return {id:v.id,name:nm(v),p:money(v.price)} }),'stay'));
    else if(st.kind==='mem')
      /* the plans show the price for the way to pay that is chosen, so the number on the box is the number you pay */
      h=set(T.qPlan,row(P.member.plans.map(function(p){ return {id:p.id,name:nm(p),p:money(dd?p.dd:p.desk),tag:p.best?T.recommended:''} }),'plan'),T.paidEvery)+
        set(T.qPay,row([
          {id:'dd',  name:T.dd,   chip:T.off(money(off)), p:money(plan.dd)},
          {id:'desk',name:T.desk, p:money(plan.desk)}
        ],'pay'));
    else
      h=set(T.howItWorks,'<ol class="pt-s">'+T.steps.map(function(s,i){ return '<li><i>'+(i+1)+'</i><span><b>'+s[0]+'</b>'+s[1]+'</span></li>' }).join('')+'</ol>');
    qEl.innerHTML=h;
    pc.classList.toggle('pt-on',st.kind==='pt');
  }

  /* what is chosen, as a receipt: the same lines on the card and on the check screen */
  function summary(){
    var incl=[[T.gymAndClasses,T.included]];
    if(st.kind==='pass'){
      var v=find(P.visitor,st.stay);
      return {id:v.id,title:T.passTitle(v,nm(v)),go:T.getPass,lines:incl.concat([[T.insurance,T.included]]),totalLabel:T.total,price:v.price,note:'',bring:[]};
    }
    var p=find(P.member.plans,st.plan), dd=st.pay==='dd', rate=dd?p.dd:p.desk;
    return {id:p.id+'-'+st.pay,title:T.planTitle2(nm(p)),go:T.getPlan,
      lines:[[T.first2,money(rate)],[T.insuranceYear,money(P.insurance.year)]].concat(incl),
      totalLabel:T.firstPayment,price:rate+P.insurance.year,note:T.then(money(rate),dd),
      bring:[T.bringId].concat(dd?[T.bringIban]:[])};
  }
  function lines(c,cls){ return c.lines.map(function(l){ return '<div class="'+cls+'"><span>'+l[0]+'</span><b>'+l[1]+'</b></div>' }).join('') }

  var LEG='<p class="pc-leg">'+T.yourPlan+'</p>', co=null, last=null;
  function renderPlan(){
    if(co) co.disconnect();
    if(st.kind==='pt'){
      cur=null; last=null; root.classList.remove('has-plan','card-visible');
      box.innerHTML=LEG+'<div class="pc-card is-pt">'+
        '<div class="pc-hd"><p class="pc-n">'+T.pt+'</p></div>'+
        '<div class="pc-bg">'+PT_IMG+'</div>'+
        '<div class="pc-bd"><p class="pc-k">'+T.ptKicker+'</p><p class="pc-p">'+T.ptText+'</p>'+
          '<p class="pc-note">'+T.ptFrom(money(ptFrom))+'</p>'+
          '<a class="btn" id="pt-wa" href="'+PHONE+encodeURIComponent(T.bookMsg)+'" target="_blank" rel="noopener">'+T.ptBook+'</a>'+
          '<p class="pc-alt">'+T.ptCall+' <a href="tel:+351926565836">+351 926 565 836</a></p></div>'+
      '</div>';
      live.textContent=T.ptLive;
      return;
    }
    var s=cur=summary();
    box.innerHTML=LEG+'<div class="pc-card">'+
      '<p class="pc-n">'+s.title+'</p>'+
      '<div class="pc-lines">'+lines(s,'pc-line')+'</div>'+
      '<div class="pc-total"><span>'+s.totalLabel+'</span><b>'+money(s.price)+'</b></div>'+
      (s.note?'<p class="pc-note">'+s.note+'</p>':'')+
      '<button class="btn" type="button" id="pc-go">'+s.go+'</button>'+
    '</div>';
    live.textContent=s.title+', '+money(s.price)+'.';
    root.classList.add('has-plan');
    $('bp-n').textContent=s.title; $('bp-l').textContent=s.totalLabel; $('bp-p').textContent=money(s.price);
    if(co) co.observe($('pc-go'));
    roll(s.price);
  }
  /* the total counts to its new value when a choice changes it */
  function roll(to){
    var b=box.querySelector('.pc-total b'), from=last; last=to;
    if(!mo||!b||from===null||from===to) return;
    var t0=performance.now();
    (function step(t){
      var k=Math.min(1,(t-t0)/420), e=1-Math.pow(1-k,3);
      if(!b.isConnected) return;
      b.textContent=money(k<1?Math.round(from+(to-from)*e):to);
      if(k<1) requestAnimationFrame(step);
    })(t0);
  }

  opts.addEventListener('change',function(e){
    var t=e.target; if(t.type!=='radio') return;
    if(t.name==='kind'&&st.kind!==t.value) track('pricing_kind',{kind:t.value});
    st[t.name]=t.value;
    renderOpts(); renderPlan();
    var back=opts.querySelector('input[name="'+t.name+'"]:checked'); if(back) back.focus();
  });
  document.addEventListener('click',function(e){
    if(e.target.closest('#pt-wa')) track('pricing_pt_whatsapp',{});
    if(e.target.closest('#pc-go, #bp-go')&&cur) review(cur);
  });

  /* ---------- check and buy ---------- */
  var bx=null, body=null, opener=null;
  function build(){
    if(bx) return;
    bx=document.createElement('div'); bx.className='bx';
    bx.setAttribute('role','dialog'); bx.setAttribute('aria-modal','true'); bx.setAttribute('aria-labelledby','bx-h');
    bx.innerHTML='<div class="bx-sheet"><button class="bx-x" type="button" aria-label="'+T.close+'">×</button><div id="bx-body"></div></div>';
    document.body.appendChild(bx); body=bx.querySelector('#bx-body');
    bx.addEventListener('click',function(e){ if(e.target===bx) close('backdrop') });
    bx.querySelector('.bx-x').addEventListener('click',function(){ close('button') });
    bx.addEventListener('keydown',function(e){
      if(e.key==='Escape') return close('escape');
      if(e.key!=='Tab') return;   /* the sheet keeps the keyboard until it closes */
      var f=bx.querySelectorAll('button,a[href]'), a=f[0], z=f[f.length-1];
      if(e.shiftKey&&document.activeElement===a){ e.preventDefault(); z.focus() }
      else if(!e.shiftKey&&document.activeElement===z){ e.preventDefault(); a.focus() }
    });
  }
  function show(step){
    bx.dataset.step=step; bx.classList.add('on'); root.style.overflow='hidden';
    bx.querySelector('.bx-sheet').scrollTop=0;
    var f=body.querySelector('.btn'); if(f) f.focus();
  }
  function close(how){
    bx.classList.remove('on'); root.style.overflow='';
    track('pricing_close',{how:how,step:bx.dataset.step||''});
    if(opener&&opener.isConnected) opener.focus();
  }
  /* step 1: the plan once more, and Buy now */
  function review(c){
    build(); opener=document.activeElement;
    body.innerHTML='<p class="bx-k">'+T.yourPlan+'</p><h3 class="bx-h" id="bx-h">'+c.title+'</h3>'+
      '<div class="bx-lines">'+lines(c,'bx-line')+'</div>'+
      '<div class="bx-total"><span>'+c.totalLabel+'</span><b>'+money(c.price)+'</b></div>'+
      (c.note?'<p class="bx-note">'+c.note+'</p>':'')+
      '<button class="btn bx-go" type="button">'+T.buyNow+'</button>'+
      '<button class="bx-back" type="button">'+T.change+'</button>';
    body.querySelector('.bx-go').addEventListener('click',function(){ done(c) });
    body.querySelector('.bx-back').addEventListener('click',function(){ close('back') });
    show('review');
    track('pricing_review',{plan:c.id,price:c.price});
  }
  /* step 2: we do not take payment online, so the plan is finished at reception. Said plainly:
     nobody should think they have paid */
  function done(c){
    body.innerHTML='<p class="bx-k">'+T.oneStep+'</p><h3 class="bx-h" id="bx-h">'+T.finish+'</h3>'+
      '<p class="bx-p">'+T.finishText+'</p>'+
      '<div class="bx-lines">'+
        '<div class="bx-line"><span>'+T.yourPlan+'</span><b>'+c.title+'</b></div>'+
        '<div class="bx-line"><span>'+T.payAtDesk+'</span><b>'+money(c.price)+'</b></div>'+
        (c.bring.length?'<div class="bx-line"><span>'+T.bring+'</span><b>'+c.bring.join('<br>')+'</b></div>':'')+
      '</div>'+
      '<div class="bx-acts">'+
        '<a class="btn" href="'+MAPS+'" target="_blank" rel="noopener">'+T.directions+'</a>'+
        '<a class="btn ghost" href="'+PHONE+encodeURIComponent(T.askMsg(c.title))+'" target="_blank" rel="noopener">WhatsApp</a>'+
      '</div>';
    show('done');
    track('pricing_confirm',{plan:c.id,price:c.price});
  }

  /* on a phone the page bar carries the plan inside Prices, and steps aside for the plan's own button */
  var mq=window.matchMedia('(max-width:768px)'), sec=$('prices'), inView=false;
  function mark(){ root.classList.toggle('in-prices',inView&&mq.matches) }
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){ inView=es[0].isIntersecting; mark() },{rootMargin:'-45% 0px -45% 0px'}).observe(sec);
    co=new IntersectionObserver(function(es){ root.classList.toggle('card-visible',es[0].isIntersecting&&root.classList.contains('has-plan')) },{threshold:0.5});
  }
  if(mq.addEventListener) mq.addEventListener('change',mark); else mq.addListener(mark);
  renderOpts(); renderPlan();

  /* the full price list opens when someone arrives at #price-list; we count who prefers the table */
  var d=$('price-list');
  if(d){
    var hash=function(){ if(location.hash==='#price-list') d.open=true };
    hash(); window.addEventListener('hashchange',hash);
    d.addEventListener('toggle',function(){ track(d.open?'pricing_list_open':'pricing_list_close',{}) });
  }
})();

/* ---------- blocks come up once as you reach them, the handwritten notes are written in.
   Anything on the first screen is left as it is. Runs last, so it sees the page as built. ---------- */
(function(){
  if(!mo||!('IntersectionObserver' in window)) return;
  var phone=matchMedia('(max-width:768px)').matches;
  var host=new WeakMap();   /* a note that is clipped away never counts as on screen: its parent is watched for it */
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting) return;
      var el=host.get(e.target)||e.target; io.unobserve(e.target); el.classList.add('pz-in');
      /* afterwards the block is exactly as it was: its own hover and transitions come back */
      setTimeout(function(){ el.classList.remove('pz-up','pz-wr','pz-in'); el.style.removeProperty('--d') },2400);
    });
  },{rootMargin:'0px 0px -10% 0px',threshold:.06});
  function add(sel,cls,gap,base){
    all(sel).forEach(function(el,i){
      if(el.getBoundingClientRect().top<innerHeight) return;
      el.classList.add(cls||'pz-up');
      el.style.setProperty('--d',((base||0)+Math.min(i,6)*(gap||0))+'ms');
      if(cls==='pz-wr'){ host.set(el.parentElement,el); io.observe(el.parentElement) } else io.observe(el);
    });
  }
  add('.section-header'); add('.section-script','pz-wr');
  add('.gym-col','pz-up',90); add('.gym-map');
  add(phone?'.classes-grid':'.class-card','pz-up',70);
  add('.tt'); add('#pc-opts'); add('#pc-plan','pz-up',0,phone?0:120);
  add('.rv-rating'); add('.marquee'); add('.about-band p'); add('.family','pz-up',0,120);
  add('.find-a'); add('.find-b','pz-up',0,phone?0:100);
  add('.faq-grid');   /* the questions come up together, once */
})();

})();
