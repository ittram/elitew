# -*- coding: utf-8 -*-
"""Writes the five final polish drafts, 2.8.1 to 2.8.5, from draft 2.7.

    python3 build/experiments/polish_2_8.py
    python3 build/pricelist.py          # puts the price list back in its place
    python3 build/check_prices.py

Every draft gets the same fixes (shared() below: wording, the empty slot in the
phone timetable, reviews that showed twice on one screen, focus rings, the menu
button's hover). Then each one pushes one kind of polish:

    2.8.1  Motion         things arrive once and settle
    2.8.2  Type           one type scale, one rhythm, finer rules
    2.8.3  Feedback       everything you touch answers
    2.8.4  First screen   status and two buttons in the hero
    2.8.5  Marker         hand drawn marks that draw themselves

For the record only, like the other scripts here. Layout, prices and contact
details are not touched."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = 'elite-wellness-landing_2-7.html'


def sub1(s, old, new, n=1):
    assert s.count(old) == n, '%d x %r' % (s.count(old), old[:70])
    return s.replace(old, new)


# ---------------------------------------------------------------- shared fixes
FIX_CSS = r'''
/* ---------- 2.8, in every polish draft: small fixes ---------- */
/* the header button answers like every other button: volt, no skew */
.nav-cta{transition:background .2s,color .2s}
.nav-cta:hover,.nav-cta:focus-visible{transform:none;background:var(--accent);color:var(--accent-ink);outline:none}
/* one focus ring for the keyboard, white on the dark bands */
a:focus-visible,button:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--royal-blue);outline-offset:3px}
.classes-section :focus-visible,.find-block :focus-visible,.site-footer :focus-visible,.action-bar :focus-visible,.menu :focus-visible{outline-color:var(--white)}
/* the plus was a letter and came out tiny: now it is drawn, and turns into a cross */
.faq-item summary::after{content:'';flex:0 0 16px;width:16px;height:16px;margin-left:1rem;font-size:0;background:linear-gradient(var(--royal-blue),var(--royal-blue)) center/100% 2px no-repeat,linear-gradient(var(--royal-blue),var(--royal-blue)) center/2px 100% no-repeat;transition:transform .25s cubic-bezier(.2,.8,.2,1)}
/* phone timetable: room for the busiest day, not for a class that does not exist */
@media (max-width:768px){.tt-list{min-height:calc(var(--tt-rows,3) * 96px)}}
'''

FIX_JS = r'''
/* 2.8: the phone timetable keeps the height of its busiest day */
(function(){
  var S=window.ELITE_SCHEDULE, l=document.getElementById('tt-list'); if(!S||!l) return;
  var n={}; S.sessions.forEach(function(x){ n[x.day]=(n[x.day]||0)+1 });
  l.style.setProperty('--tt-rows', Math.max.apply(null, Object.keys(n).map(function(k){ return n[k] })));
})();
'''

HEAD_JS = "<script>/* 2.8: motion only where it is wanted */document.documentElement.classList.add('js');if(!matchMedia('(prefers-reduced-motion:reduce)').matches)document.documentElement.classList.add('mo')</script>\n"


def shared(s):
    s = sub1(s, '<title>Draft 2.2 (footer: full width, text only) | Gym in Lagos, Algarve | Elite Wellness by Santos | Day Passes &amp; Memberships</title>',
             '<title>Gym in Lagos, Algarve | Elite Wellness by Santos | Day passes and membership</title>')
    # one name for the family, one for the deck
    s = sub1(s, 'A family owned gym in Lagos.', 'A family run gym in Lagos.')
    s = sub1(s, 'keep it bright with the air moving.', 'keep it bright and the air moving.')
    s = sub1(s, "An outdoor training area right outside the doors. When the weather's good, classes often move outdoors. That's how this gym started, and it never stopped.",
             "An outdoor deck right outside the doors. When the weather's good, classes often move out there. That's how this gym started, and we never stopped.")
    s = sub1(s, '<span class="gl-t">Outdoor area</span>', '<span class="gl-t">Outdoor deck</span>')
    # classes come with membership too, not only with a pass
    s = sub1(s, '<span class="section-script">included in every pass</span>', '<span class="section-script">included in the price</span>')
    s = sub1(s, '<span>No booking. Come during opening hours and join in.</span>', '<span>No booking. Just turn up and join in.</span>')
    s = sub1(s, '<p class="find-label">Open hours</p>', '<p class="find-label">Opening hours</p>')
    # how to pay belongs to Prices, not under the address
    s = sub1(s, '<p class="find-note">Free parking outside. Pay at reception or by direct debit.</p>', '<p class="find-note">Free parking outside.</p>')
    # the price section says the price is agreed with the coach; the answer here now says the same
    s = sub1(s, '<p>Yes, one to one with a qualified coach. <a href="https://wa.me/351926565836?text=Hi!%20I%27d%20like%20to%20ask%20about%20personal%20training." target="_blank" rel="noopener">Ask us on WhatsApp</a> for prices.</p>',
             '<p>Yes, one to one with a qualified coach. The price is agreed with your coach. <a href="https://wa.me/351926565836?text=Hi!%20I%20would%20like%20to%20book%20a%20time%20to%20talk%20to%20a%20coach%20about%20personal%20training." target="_blank" rel="noopener">Book a time on WhatsApp</a>.</p>')
    # five reviews in two rows showed the same card twice on one screen
    s = sub1(s, '  if(!sets[1].length) sets[1]=sets[0].slice();\n',
             '  /* 2.8: with few reviews two rows show the same card twice on one screen. One row until there are eight. */\n'
             '  if(R.reviews.length<8){ sets=[R.reviews.slice()]; rows[1].style.display=\'none\'; rows=[rows[0]]; }\n')
    return s


def inject(s, v, label, css, js):
    head = '%s<style id="polish-css">%s\n/* ---------- %s: %s ---------- */%s</style>\n' % (HEAD_JS, FIX_CSS, v, label, css)
    body = '<script id="polish-js">%s\n/* %s: %s */%s</script>\n' % (FIX_JS, v, label, js)
    s = sub1(s, '<style id="price-list-css">', head + '<style id="price-list-css">')
    s = sub1(s, '<script id="price-list-js">', body + '<script id="price-list-js">')
    return s


# the answers fold open instead of jumping (where the browser can; elsewhere they open at once)
FOLD_CSS = r'''
@supports (interpolate-size:allow-keywords){
  :root{interpolate-size:allow-keywords}
  .faq-item::details-content,.pl::details-content{block-size:0;overflow:clip;transition:block-size .4s cubic-bezier(.2,.8,.2,1),content-visibility .4s allow-discrete}
  .faq-item[open]::details-content,.pl[open]::details-content{block-size:auto}
}
@media (prefers-reduced-motion:reduce){.faq-item::details-content,.pl::details-content{transition:none}}
'''

# the total counts to its new value when a choice changes it
ROLL_JS = r'''
(function(){
  var plan=document.getElementById('pc-plan'), last=null;
  if(!plan||!document.documentElement.classList.contains('mo')||!window.MutationObserver) return;
  function roll(){
    var b=plan.querySelector('.pc-total b'); if(!b){ last=null; return }
    var txt=b.textContent, to=parseFloat(txt.replace(/[^\d.]/g,''));
    if(last===null||last===to||isNaN(to)){ last=to; return }
    var from=last, pre=txt.replace(/[\d.]+.*$/,''), t0=performance.now(); last=to;
    (function step(t){
      var k=Math.min(1,(t-t0)/420), e=1-Math.pow(1-k,3);
      if(!b.isConnected) return;
      b.textContent=k<1?pre+Math.round(from+(to-from)*e):txt;
      if(k<1) requestAnimationFrame(step);
    })(t0);
  }
  new MutationObserver(roll).observe(plan,{childList:true}); roll();
})();
'''


# ---------------------------------------------------------------- 2.8.1 Motion
def t1(s):
    s = sub1(s, '<h1 class="hero-title">Train<br>In Lagos</h1>',
             '<h1 class="hero-title"><span class="ln"><span>Train</span></span> <span class="ln"><span>In Lagos</span></span></h1>')
    css = r'''
/* the first screen arrives: the title rises out of its own line, the photos settle */
.hero-title .ln{display:block;clip-path:inset(-.12em -2em -.03em -2em)}
.hero-title .ln>span{display:block}
.mo .hero-title .ln>span{animation:pz-rise 1s cubic-bezier(.16,1,.3,1) backwards}
.mo .hero-title .ln:nth-child(2)>span{animation-delay:.09s}
.mo .hero-rating{animation:pz-up .8s cubic-bezier(.16,1,.3,1) .4s backwards}
.mo .hero-sub{animation:pz-up .8s cubic-bezier(.16,1,.3,1) .5s backwards}
.mo .hero-img{scale:1.14;translate:0 var(--py,0px);animation:pz-photo 1.5s cubic-bezier(.16,1,.3,1) .25s backwards}
.mo .hero-img:nth-child(2){animation-delay:.35s}
.mo .hero-img:nth-child(3){animation-delay:.45s}
@keyframes pz-rise{from{transform:translateY(104%)}}
@keyframes pz-up{from{opacity:0;transform:translateY(16px)}}
@keyframes pz-photo{from{opacity:0;scale:1.28}}
/* each block comes up once as you reach it, then is left alone */
.mo .pz-up{opacity:0;transform:translateY(28px)}
.mo .pz-up.pz-in{opacity:1;transform:none;transition:opacity .8s cubic-bezier(.16,1,.3,1) var(--d,0s),transform .8s cubic-bezier(.16,1,.3,1) var(--d,0s)}
/* the handwritten notes are written in, left to right */
.mo .pz-wr{clip-path:inset(-40% 104% -40% -4%)}
.mo .pz-wr.pz-in{clip-path:inset(-40% -4% -40% -4%);transition:clip-path .9s cubic-bezier(.4,0,.2,1) .25s}
''' + FOLD_CSS
    js = r'''
(function(){
  var root=document.documentElement;
  if(!root.classList.contains('mo')||!('IntersectionObserver' in window)) return;
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
    [].forEach.call(document.querySelectorAll(sel),function(el,i){
      if(el.getBoundingClientRect().top<innerHeight) return;   /* already on the first screen: leave it */
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
  add('.find-a'); add('.find-b','pz-up',0,phone?0:100); add('.faq-item','pz-up',40);

  /* the hero photos drift a little slower than the page, each at its own pace */
  var strip=document.querySelector('.hero-image-strip'), imgs=strip?strip.querySelectorAll('.hero-img'):[], busy=false;
  function drift(){
    busy=false;
    var r=strip.getBoundingClientRect(), vh=innerHeight;
    if(r.bottom<0||r.top>vh) return;
    var p=(vh-r.top)/(vh+r.height)-.5, amp=r.height*.085;
    [].forEach.call(imgs,function(im,i){ im.style.setProperty('--py',(-p*amp*(1+i*.25)).toFixed(1)+'px') });
  }
  if(strip){ addEventListener('scroll',function(){ if(!busy){ busy=true; requestAnimationFrame(drift) } },{passive:true}); drift(); }
})();
''' + ROLL_JS
    return inject(s, '2.8.1', 'motion', css, js)


# ---------------------------------------------------------------- 2.8.2 Type
def curl(s):
    """Typographic apostrophes in the words people read (not in tags, scripts or styles)."""
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>)', s, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", u'’', parts[i])
    return ''.join(parts)


def t2(s):
    head, body = s.split('<body>', 1)
    s = head + '<body>' + curl(body)
    css = r'''
/* one small label everywhere: 11 on 16, wide, heavy */
.hero-rating,.tt-next,.rv-rating,.family-names,.find-status,.hr-d,.find-label,.ft-h,.tt-updated,.menu-status,.class-tag,.tt-desc,.rv-meta{font-size:11px;line-height:16px;letter-spacing:.14em;font-weight:800}
nav .nav-link{font-size:12px;letter-spacing:.14em}
/* numbers line up under each other */
.tt-time,.hr-t,.pc-card,.pk-f,.op-p,.pl-t,.bx-sheet,.bar-price,.tt-next,.find-status,.bar-status,.rv-rating,.hero-rating{font-variant-numeric:tabular-nums}
body{text-rendering:optimizeLegibility;font-kerning:normal}
h1,h2,h3,summary{text-wrap:balance}
p{text-wrap:pretty}
/* headings: one fluid scale, set tighter, with the note tucked under */
.section-header{font-size:clamp(2.75rem,6.4vw,5.75rem);line-height:.94}
.find-block .section-header{font-size:clamp(2.5rem,4vw,4rem);line-height:1}
.section-script{font-size:clamp(1.3rem,1.9vw,1.75rem)}
.section-kicker{margin-bottom:clamp(2.5rem,5vw,4.5rem)}
.tt-title{font-size:clamp(2.5rem,4vw,3.75rem);line-height:1}
/* one rhythm between the bands */
.section,.classes-section,.reviews-section,.faq-section,.about-band{padding-top:clamp(4.5rem,9vw,8.5rem);padding-bottom:clamp(4.5rem,9vw,8.5rem)}
/* two sizes of running text: a lead and a body */
.gym-col p,.faq-item p{font-size:17px;line-height:28px}
.about-band p{font-size:clamp(1.15rem,1.75vw,1.5rem);line-height:1.6;max-width:31em}
@media (min-width:769px){.hero-sub{font-size:clamp(18px,1.45vw,21px);line-height:1.5}}
/* the gym: each column hangs from a rule, like the price list */
.gym-col{border-top:2px solid var(--black);padding-top:20px}
.gym-col h3{font-size:1.75rem;line-height:1;margin-bottom:.75rem}
/* good to know: hairlines instead of heavy bars, a longer measure for the question */
.faq-grid{border-top:2px solid var(--black)}
.faq-item{border-bottom:1px solid rgba(0,0,0,.28)}
.faq-item summary{font-size:clamp(1.2rem,1.6vw,1.5rem);line-height:1.15;padding:1.5rem 0;letter-spacing:.01em}
.faq-item p{max-width:62ch;padding-bottom:1.75rem}
/* small things */
.class-name{font-size:clamp(1.9rem,2.5vw,2.6rem)}
.equipment-ticker{padding:.85rem 0}
.ticker-content{font-size:1.1rem;letter-spacing:.12em}
.ft-body,.ft-list a,.ft-soon{font-size:14px}
.rv-text{text-wrap:pretty}
@media (max-width:768px){
  .about-band p{font-size:1.125rem;line-height:1.65}
  .gym-col p,.faq-item p{font-size:16px;line-height:26px}
}
'''
    return inject(s, '2.8.2', 'type and spacing', css, '\n')


# ---------------------------------------------------------------- 2.8.3 Feedback
def t3(s):
    css = r'''
/* everything you press gives a little */
.btn{transition:background .2s,color .2s,border-color .2s,scale .12s}
.nav-cta{transition:background .2s,color .2s,scale .12s}
.pk-i,.op{transition:border-color .15s,background .15s,color .15s,scale .12s}
.menu-cta,.tt-tabs button,.pi-nav button,.lang-btn{transition:background .2s,color .2s,scale .12s}
.btn:active,.nav-cta:active,.pk-i:active,.op:active,.menu-cta:active,.tt-tabs button:active,.pi-nav button:active,.lang-btn:active{scale:.97}
/* the menu knows where you are, and the line under the header shows how far */
nav .nav-link{position:relative;padding:6px 0}
nav .nav-link::after{content:'';position:absolute;left:0;right:0;bottom:0;height:2px;background:var(--royal-blue);transform:scaleX(0);transform-origin:left;transition:transform .3s cubic-bezier(.2,.8,.2,1)}
nav .nav-link:hover::after,nav .nav-link.here::after{transform:scaleX(1)}
nav .nav-link.here{color:var(--royal-blue)}
header::after{content:'';position:absolute;left:0;bottom:-2px;width:100%;height:2px;background:var(--royal-blue);transform:scaleX(var(--read,0));transform-origin:left}
/* a class card answers "when is it on?" */
.class-card{cursor:pointer}
.class-img{transition:transform .7s cubic-bezier(.2,.8,.2,1)}
@media (hover:hover){.class-card:hover{transform:none}.class-card:hover .class-img{transform:scale(1.05)}}
.class-days{margin-top:.6rem;font-weight:700;font-size:.8rem;line-height:1rem;color:var(--white)}
.class-card.on{box-shadow:inset 0 0 0 0 transparent;outline:3px solid var(--white);outline-offset:-3px}
.tt-pick{display:none;margin-top:16px;font-size:14px;line-height:24px;color:rgba(255,255,255,.85)}
.tt.pick .tt-pick{display:block}
.tt-pick b{color:var(--white)}
.tt-pick button{appearance:none;border:0;background:transparent;margin-left:12px;padding:0;font:inherit;font-weight:800;color:var(--white);cursor:pointer;box-shadow:inset 0 -2px 0 rgba(255,255,255,.5)}
.tt.pick .tt-next{display:none}
.tt-cell>*,.tt-list li>*{transition:opacity .25s}
.tt.pick .tt-cell:not(.hit)>*,.tt.pick .tt-list li:not(.hit)>*{opacity:.3}
.tt.pick .tt-cell.hit:not(.is-next){background:rgba(255,255,255,.16);box-shadow:inset 0 0 0 2px var(--white)}
.tt-tabs button.has:not([aria-selected="true"]){box-shadow:inset 0 0 0 2px var(--white),inset 0 -6px 0 var(--white)}
/* opening hours: today's line is marked */
.hours-row li.today .hr-d{color:var(--white)}
.hr-now{font-style:normal;margin-left:8px;padding:0 6px;background:var(--white);color:var(--royal-blue);font-size:10px;line-height:16px;display:inline-block}
@media (prefers-reduced-motion:reduce){.btn,.nav-cta,.pk-i,.op,.class-img,nav .nav-link::after{transition:none}}
''' + FOLD_CSS
    js = r'''
(function(){
  var root=document.documentElement, head=document.querySelector('header');
  /* where you are: the menu word of the section on screen, and how far down the page */
  var links=[].slice.call(document.querySelectorAll('nav .nav-link')).map(function(a){ return {a:a,el:document.querySelector(a.getAttribute('href'))} }).filter(function(x){ return x.el });
  var busy=false;
  function where(){
    busy=false;
    var max=root.scrollHeight-innerHeight, line=head.offsetHeight+innerHeight*.35;
    head.style.setProperty('--read', max>0?Math.min(1,scrollY/max).toFixed(4):0);
    links.forEach(function(x){ var r=x.el.getBoundingClientRect(); x.a.classList.toggle('here', r.top<=line&&r.bottom>line) });
  }
  addEventListener('scroll',function(){ if(!busy){ busy=true; requestAnimationFrame(where) } },{passive:true});
  addEventListener('resize',where); where();

  /* today's line in the opening hours (Lisbon time) */
  var day=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Lisbon',weekday:'short'}).format(new Date());
  var li=document.querySelectorAll('.hours-row li')[day==='Sat'?1:day==='Sun'?2:0];
  if(li){ li.classList.add('today'); var d=li.querySelector('.hr-d'), f=document.createElement('i'); f.className='hr-now'; f.textContent='Today'; d.appendChild(f); }

  /* tap a class: its days are on the card, and the timetable shows only its slots */
  var S=window.ELITE_SCHEDULE, tt=document.getElementById('timetable'), list=document.getElementById('tt-list'), tabs=document.getElementById('tt-tabs');
  if(!S||!tt||!list) return;
  var ORDER=['mon','tue','wed','thu','fri','sat','sun'], SHORT={mon:'Mon',tue:'Tue',wed:'Wed',thu:'Thu',fri:'Fri',sat:'Sat',sun:'Sun'};
  var byName={}; Object.keys(S.classes).forEach(function(k){ byName[S.classes[k].name.toLowerCase()]=k });
  var cards=[].slice.call(document.querySelectorAll('.class-card')), picked=null;
  var chip=document.createElement('p'); chip.className='tt-pick'; chip.setAttribute('aria-live','polite'); tt.querySelector('.tt-head').appendChild(chip);
  function slots(k){ return S.sessions.filter(function(x){ return x.class===k }).sort(function(a,b){ return ORDER.indexOf(a.day)-ORDER.indexOf(b.day)||a.time.localeCompare(b.time) }) }
  function nameOf(el){ var n=el.querySelector('.tt-name'); return n&&n.firstChild?String(n.firstChild.nodeValue||'').trim().toLowerCase():'' }
  function paint(){
    var nm=picked?S.classes[picked].name.toLowerCase():'';
    tt.classList.toggle('pick',!!picked);
    [].forEach.call(tt.querySelectorAll('.tt-cell,.tt-list li'),function(c){ c.classList.toggle('hit',!!picked&&nameOf(c)===nm) });
    cards.forEach(function(c){ var on=!!picked&&c.dataset.cls===picked; c.classList.toggle('on',on); c.setAttribute('aria-pressed',on?'true':'false') });
    [].forEach.call(tabs.children,function(b){ b.classList.toggle('has',!!picked&&S.sessions.some(function(x){ return x.day===b.dataset.day&&x.class===picked })) });
    chip.innerHTML=picked?'<b>'+S.classes[picked].name+'</b> '+slots(picked).map(function(x){ return SHORT[x.day]+' '+x.time }).join(' · ')+'<button type="button">Show all</button>':'';
  }
  function pick(k){
    picked=picked===k?null:k; paint();
    if(!picked) return;
    /* on a phone open the first day it runs, from today on */
    var today=ORDER.indexOf(day.toLowerCase()), days=slots(picked).map(function(x){ return x.day });
    var first=days.filter(function(d){ return ORDER.indexOf(d)>=today })[0]||days[0];
    var tab=first&&tabs.querySelector('[data-day="'+first+'"]'); if(tab&&tab.getAttribute('aria-selected')!=='true') tab.click();
    tt.scrollIntoView({behavior:root.classList.contains('mo')?'smooth':'auto',block:'center'});
  }
  cards.forEach(function(c){
    var nm=(c.querySelector('.class-name').textContent||'').trim(), k=byName[nm.toLowerCase()]; if(!k) return;
    c.dataset.cls=k; c.tabIndex=0; c.setAttribute('role','button'); c.setAttribute('aria-pressed','false'); c.setAttribute('aria-label',nm+': show when it is on');
    var days=ORDER.filter(function(d){ return S.sessions.some(function(x){ return x.day===d&&x.class===k }) }).map(function(d){ return SHORT[d] });
    var el=document.createElement('div'); el.className='class-days'; el.textContent=days.join(' · '); c.querySelector('.class-overlay').appendChild(el);
    c.addEventListener('click',function(){ pick(k) });
    c.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); pick(k) } });
  });
  chip.addEventListener('click',function(e){ if(e.target.closest('button')&&picked) pick(picked) });
  if(window.MutationObserver) new MutationObserver(paint).observe(list,{childList:true});
})();
''' + ROLL_JS
    return inject(s, '2.8.3', 'feedback', css, js)


# ---------------------------------------------------------------- 2.8.4 First screen
def t4(s):
    s = sub1(s, '4.8 · 153 Google reviews</a></p>\n    <h1 class="hero-title">',
             '4.8 · 153 Google reviews</a><span class="hero-open" data-status="hero-open"></span></p>\n    <h1 class="hero-title">')
    s = sub1(s, 'Weights, machines, classes and space to train outdoors.</p>\n  </div>',
             'Weights, machines, classes and space to train outdoors.</p>\n'
             '    <div class="hero-acts"><a class="btn" href="#prices">See prices</a><a class="btn ghost" href="https://maps.app.goo.gl/ks6o4URGCYT7rzHJ8" target="_blank" rel="noopener">Get directions</a></div>\n  </div>')
    css = r'''
/* the first screen answers three things at once: is it good, is it open, what do I do next */
.hero-rating{display:flex;justify-content:center;align-items:center;flex-wrap:wrap;gap:12px 16px}
.hero-open{display:inline-flex;align-items:center;gap:8px;padding:4px 10px;background:var(--black);color:rgba(255,255,255,.75);white-space:nowrap}
.hero-open:empty{display:none}
.hero-open b{color:var(--white)}
.hero-open .dot{width:8px;height:8px;border-radius:50%;background:var(--accent)}
.hero-open.closed .dot{background:rgba(255,255,255,.45)}
.hero-acts{grid-column:1 / -1;display:flex;justify-content:center;gap:12px;margin-top:32px}
.hero-acts .btn{min-width:184px}
/* less air above, more photo below: the people are on the first screen */
@media (min-width:769px){
  .hero{padding-top:64px}
  .hero-image-strip{margin-top:56px;height:clamp(300px,44vh,480px)}
}
@media (max-width:768px){
  .hero{padding-top:32px}
  .hero-sub{margin-top:24px}
  .hero-acts{margin-top:24px;gap:8px}
  .hero-acts .btn{flex:1 1 0;min-width:0;padding-left:8px;padding-right:8px}
  /* a person first, and the strip can be swiped to see all three */
  .hero-image-strip{height:260px;margin-top:40px;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none;overscroll-behavior-x:contain}
  .hero-image-strip::-webkit-scrollbar{display:none}
  .hero-img{flex:0 0 78%;scroll-snap-align:start}
  .hero-img:nth-child(2){order:-1}
}
'''
    return inject(s, '2.8.4', 'first screen', css, '\n')


# ---------------------------------------------------------------- 2.8.5 Marker
def t5(s):
    s = sub1(s, '<h1 class="hero-title">Train<br>In Lagos</h1>', '<h1 class="hero-title">Train<br><span class="mk-word" data-mk="swipe">In Lagos</span></h1>')
    s = sub1(s, '<span class="section-script">since 2020</span>', '<span class="section-script" data-mk="under2">since 2020</span>')
    s = sub1(s, '<p class="ft-motto">Juntos Somos Elite</p>', '<p class="ft-motto"><span data-mk="under">Juntos Somos Elite</span></p>')
    css = r'''
/* the coach's marker: a few hand drawn strokes that draw themselves once, like the route on the plan */
[data-mk],.mk-host{position:relative}
.mk-word{display:inline-block}
.mk-svg{position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible;pointer-events:none;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round}
.mk-svg path{stroke-dasharray:var(--len);stroke-dashoffset:var(--len)}
.section-script[data-mk].pz-wr{clip-path:inset(-40% 104% -70% -4%)}
.section-script[data-mk].pz-wr.pz-in{clip-path:inset(-40% -4% -70% -4%)}
.mk-svg.go path{stroke-dashoffset:0;transition:stroke-dashoffset .8s cubic-bezier(.45,0,.2,1) var(--wait,0s)}
html:not(.mo) .mk-svg path{stroke-dashoffset:0;transition:none}
/* under the title the stroke is the volt highlighter, behind the letters */
.hero-title .mk-svg{color:var(--accent);z-index:-1}
.hero-title{position:relative;z-index:0}
.tt-next b{display:inline-block}
.tt-next .mk-svg{color:var(--white)}
.pc-total b{position:relative}
.pc-total .mk-svg{color:var(--white)}
.rv-rating .mk-n{position:relative;display:inline-block;margin:0 6px 0 4px;color:var(--royal-blue)}
/* the handwritten notes are written in, left to right */
.mo .pz-wr{clip-path:inset(-40% 104% -40% -4%)}
.mo .pz-wr.pz-in{clip-path:inset(-40% -4% -40% -4%);transition:clip-path .9s cubic-bezier(.4,0,.2,1) .25s}
'''
    js = r'''
(function(){
  var NS='http://www.w3.org/2000/svg', root=document.documentElement, mo=root.classList.contains('mo');
  function n(v){ return (Math.round(v*10)/10) }
  /* each stroke is drawn in the pixels of the thing it marks, so the line keeps one weight */
  var DRAW={
    /* one fast swipe of a wide marker, low across the word */
    swipe:function(w,h){ var y=h*.84; return {d:'M'+n(-w*.03)+' '+n(y+h*.03)+' C'+n(w*.22)+' '+n(y-h*.05)+','+n(w*.6)+' '+n(y+h*.05)+','+n(w*1.03)+' '+n(y-h*.03), sw:Math.max(8,h*.2), cap:'butt'} },
    under:function(w,h){ var y=h+3; return {d:'M0 '+n(y+1)+' C'+n(w*.25)+' '+n(y-3)+','+n(w*.55)+' '+n(y+4)+','+n(w)+' '+n(y-1), sw:2} },
    under2:function(w,h){ var y=h+2; return {d:'M'+n(w*.02)+' '+n(y)+' C'+n(w*.3)+' '+n(y-4)+','+n(w*.6)+' '+n(y+3)+','+n(w*.98)+' '+n(y-2)+' M'+n(w*.22)+' '+n(y+7)+' C'+n(w*.45)+' '+n(y+4)+','+n(w*.7)+' '+n(y+9)+','+n(w*.9)+' '+n(y+5), sw:2} },
    /* a loop that starts at the top, goes round and overshoots its own start */
    ring:function(w,h){ var px=Math.max(7,w*.14), py=Math.max(8,h*.22), x0=-px, x1=w+px, y0=-py, y1=h+py, cx=w/2, cy=h/2;
      return {d:'M'+n(cx-w*.12)+' '+n(y0+3)+
        ' C'+n(x0+w*.1)+' '+n(y0-3)+','+n(x0-5)+' '+n(cy-h*.3)+','+n(x0)+' '+n(cy+3)+
        ' C'+n(x0+4)+' '+n(y1+5)+','+n(cx-w*.2)+' '+n(y1+5)+','+n(cx+w*.12)+' '+n(y1+1)+
        ' C'+n(x1+8)+' '+n(y1-3)+','+n(x1+7)+' '+n(cy+h*.1)+','+n(x1)+' '+n(cy-h*.2)+
        ' C'+n(x1-6)+' '+n(y0-7)+','+n(cx+w*.15)+' '+n(y0-5)+','+n(cx-w*.3)+' '+n(y0+6), sw:2} }
  };
  var host=new WeakMap();   /* a note that is clipped away never counts as on screen: its parent is watched for it */
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ io.unobserve(e.target); go(host.get(e.target)||e.target) } }) },{rootMargin:'0px 0px -18% 0px',threshold:0}):null;
  function watch(el){ var w=el.classList.contains('section-script')?el.parentElement:el; host.set(w,el); io.observe(w) }
  function go(el){ var s=el.querySelector(':scope > .mk-svg'); if(s) s.classList.add('go'); el.classList.add('pz-in') }
  function mark(el,kind,wait,now){
    var old=el.querySelector(':scope > .mk-svg'), was=old&&old.classList.contains('go'); if(old) old.remove();
    var w=el.offsetWidth, h=el.offsetHeight; if(!w||!h||!DRAW[kind]) return;
    var p=DRAW[kind](w,h), svg=document.createElementNS(NS,'svg'), path=document.createElementNS(NS,'path');
    svg.setAttribute('class','mk-svg'); svg.setAttribute('viewBox','0 0 '+w+' '+h); svg.setAttribute('aria-hidden','true');
    path.setAttribute('d',p.d); path.setAttribute('stroke-width',n(p.sw)); if(p.cap) path.setAttribute('stroke-linecap',p.cap);
    svg.appendChild(path); el.appendChild(svg);
    svg.style.setProperty('--len',Math.ceil(path.getTotalLength())+1);
    if(wait) svg.style.setProperty('--wait',wait+'s');
    el.dataset.mk=kind;
    if(was){ svg.style.transition='none'; path.style.transition='none'; svg.classList.add('go') }
    else if(now||!io||!mo){ void svg.getBoundingClientRect(); svg.classList.add('go') }
    else watch(el);
  }
  function all(){ [].forEach.call(document.querySelectorAll('[data-mk]'),function(el){ mark(el,el.dataset.mk,el.closest('.hero-title')?.7:0) }) }

  /* the next class gets a line under it, the rating a ring round the score */
  var nx=document.querySelector('#tt-next b'); if(nx) nx.dataset.mk='under';
  var sc=document.getElementById('rv-score');
  if(sc){ var m=sc.textContent.match(/^([\d.]+)(.*)$/); if(m){ sc.textContent=''; var b=document.createElement('span'); b.className='mk-n'; b.textContent=m[1]; b.dataset.mk='ring'; sc.appendChild(b); sc.appendChild(document.createTextNode(m[2])) } }
  /* the notes under the headings are written in */
  [].forEach.call(document.querySelectorAll('.section-script'),function(el){ if(mo&&io&&el.getBoundingClientRect().top>innerHeight*.9){ el.classList.add('pz-wr'); watch(el) } });

  function start(){ all(); ringTotal(true) }
  /* what you pay is ringed, and the ring is drawn again each time the price changes */
  var plan=document.getElementById('pc-plan');
  function ringTotal(first){ var t=plan&&plan.querySelector('.pc-total b'); if(t){ var o=t.querySelector('.mk-svg'); if(o) o.remove(); mark(t,'ring',first?.2:.15,!first) } }
  if(plan&&window.MutationObserver) new MutationObserver(function(){ ringTotal(false) }).observe(plan,{childList:true});
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(start); else start();
  var t; addEventListener('resize',function(){ clearTimeout(t); t=setTimeout(function(){ all(); var b=plan&&plan.querySelector('.pc-total b'); if(b) mark(b,'ring',0,true) },250) });
})();
'''
    return inject(s, '2.8.5', 'marker', css, js)


TAKES = [('2-8-1', t1), ('2-8-2', t2), ('2-8-3', t3), ('2-8-4', t4), ('2-8-5', t5)]

if __name__ == '__main__':
    base = shared(io.open(os.path.join(ROOT, SRC), encoding='utf-8').read())
    for name, take in TAKES:
        out = 'elite-wellness-landing_%s.html' % name
        io.open(os.path.join(ROOT, out), 'w', encoding='utf-8').write(take(base))
        print(out)
