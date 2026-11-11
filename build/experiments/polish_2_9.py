# -*- coding: utf-8 -*-
"""Writes draft 2.9 and 2.9.1 from draft 2.7: the parts of the five 2.8 polish
drafts that were kept (Martti, 11 November 2026), merged into one page.

    python3 build/experiments/polish_2_9.py
    python3 build/pricelist.py
    python3 build/check_prices.py

Kept:    the small fixes shared by the 2.8 drafts; blocks and notes appearing
         as you reach them (2.8.1); a class card showing its slots in the
         timetable, the line under the header, today in the opening hours, the
         counting total and the folding answers (2.8.3).
New:     no volt on any hover, primary buttons lean like WhatsApp in the bar,
         a flat edge above Good to know, grain on the photos, what each class
         is when you tap it, each review linking to itself on Google.
Dropped: the marker strokes (2.8.5), the hero entrance and drifting photos
         (2.8.1), the type changes (2.8.2), the menu underline (2.8.3) and the
         Open now tag in the hero (2.8.4).
2.9.1 is 2.9 with the two buttons under the headline, to judge side by side.

For the record only, like the other scripts here."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import polish_2_8 as P8

ROOT, sub1 = P8.ROOT, P8.sub1

GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E"
         "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='1.05' numOctaves='2' stitchTiles='stitch'/%3E"
         "%3CfeColorMatrix values='.33 .33 .33 0 0 .33 .33 .33 0 0 .33 .33 .33 0 0 0 0 0 0 1'/%3E"
         "%3CfeComponentTransfer%3E%3CfeFuncR type='linear' slope='1.8' intercept='-.4'/%3E%3CfeFuncG type='linear' slope='1.8' intercept='-.4'/%3E%3CfeFuncB type='linear' slope='1.8' intercept='-.4'/%3E%3C/feComponentTransfer%3E%3C/filter%3E"
         "%3Crect width='240' height='240' filter='url(%23n)'/%3E%3C/svg%3E\")")

CSS = r'''
/* ---------- 2.9: the polish that was kept ---------- */
/* one focus ring for the keyboard, white on the dark bands */
a:focus-visible,button:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--royal-blue);outline-offset:3px}
.classes-section :focus-visible,.find-block :focus-visible,.site-footer :focus-visible,.action-bar :focus-visible,.menu :focus-visible{outline-color:var(--white)}
/* the plus was a letter and came out tiny: now it is drawn, and turns into a cross */
.faq-item summary::after{content:'';flex:0 0 16px;width:16px;height:16px;margin-left:1rem;font-size:0;background:linear-gradient(var(--royal-blue),var(--royal-blue)) center/100% 2px no-repeat,linear-gradient(var(--royal-blue),var(--royal-blue)) center/2px 100% no-repeat;transition:transform .25s cubic-bezier(.2,.8,.2,1)}
/* phone timetable: room for the busiest day, not for a class that does not exist */
@media (max-width:768px){.tt-list{min-height:calc(var(--tt-rows,3) * 96px)}}

/* buttons. A primary button leans, like WhatsApp in the bar. No volt on hover anywhere:
   on white, blue turns black and the outline fills blue; on black or blue, white turns blue
   and the outline fills white; on the black plan card, blue turns white. */
.btn:not(.ghost){clip-path:polygon(6px 0%,100% 0%,calc(100% - 6px) 100%,0% 100%)}
.action-bar .btn:not(.ghost){clip-path:polygon(6px 0%,100% 0%,calc(100% - 6px) 100%,0% 100%)}
.btn{transition:background .2s,color .2s,border-color .2s,scale .12s}
.btn:hover,.btn:focus-visible{background:var(--black);border-color:var(--black);color:var(--white)}
.btn.on-dark:hover,.btn.on-dark:focus-visible{background:var(--royal-blue);border-color:var(--royal-blue);color:var(--white)}
.pc-card .btn:hover,.pc-card .btn:focus-visible{background:var(--white);border-color:var(--white);color:var(--royal-blue)}
.nav-cta{transition:background .2s,color .2s,scale .12s}
.nav-cta:hover,.nav-cta:focus-visible{transform:none;background:var(--black);color:var(--white);outline:none}
.btn-main:hover,.btn-main:focus-visible{background:var(--black);border-color:var(--black);color:var(--white)}
.ft-social a:hover svg{color:var(--white);opacity:1}
/* everything you press gives a little */
.pk-i,.op{transition:border-color .15s,background .15s,color .15s,scale .12s}
.menu-cta,.tt-tabs button,.pi-nav button,.lang-btn{transition:background .2s,color .2s,scale .12s}
.btn:active,.nav-cta:active,.pk-i:active,.op:active,.menu-cta:active,.tt-tabs button:active,.pi-nav button:active,.lang-btn:active{scale:.97}

/* a thin line under the header shows how far down the page you are */
header::after{content:'';position:absolute;left:0;bottom:-2px;width:100%;height:2px;background:var(--royal-blue);transform:scaleX(var(--read,0));transform-origin:left}

/* each block comes up once as you reach it, then is left alone; the notes are written in */
.mo .pz-up{opacity:0;transform:translateY(24px)}
.mo .pz-up.pz-in{opacity:1;transform:none;transition:opacity .8s cubic-bezier(.16,1,.3,1) var(--d,0s),transform .8s cubic-bezier(.16,1,.3,1) var(--d,0s)}
.mo .pz-wr{clip-path:inset(-40% 104% -40% -4%)}
.mo .pz-wr.pz-in{clip-path:inset(-40% -4% -40% -4%);transition:clip-path .9s cubic-bezier(.4,0,.2,1) .25s}

/* film grain on the photos, so they sit less clean: one tile of noise laid over each */
.hero-image-strip,.class-card,.is-pt .pc-bg{position:relative}
.hero-image-strip::after,.class-card::before,.is-pt .pc-bg::before{content:'';position:absolute;inset:0;pointer-events:none;background-image:GRAIN;background-size:240px 240px;mix-blend-mode:overlay;opacity:.55}
.class-card::before{background-position:60px 90px;z-index:1}   /* the photo has a filter, so it would paint over the grain */
.class-overlay{z-index:2}

/* a class card answers "what is it, and when is it on?" */
.class-card{cursor:pointer}
.class-img{transition:transform .7s cubic-bezier(.2,.8,.2,1)}
@media (hover:hover){.class-card:hover{transform:none}.class-card:hover .class-img{transform:scale(1.05)}}
.class-days{margin-top:.6rem;font-weight:700;font-size:.8rem;line-height:1rem;color:var(--white)}
.class-days i{font-style:normal;margin-left:.5em;opacity:.7}
.class-card.on{outline:3px solid var(--white);outline-offset:-3px}
.tt-pick{display:none;margin:20px auto 0;max-width:560px}
.tt.pick .tt-pick{display:block}
.tt.pick .tt-next{display:none}
.tt-pick-n{font-family:var(--font-display);font-size:28px;line-height:32px;text-transform:uppercase}
.tt-pick-d{margin-top:8px;font-size:16px;line-height:24px;color:rgba(255,255,255,.9);text-wrap:balance}
.tt-pick-s{margin-top:12px;font-weight:800;font-size:12px;line-height:16px;letter-spacing:.12em;text-transform:uppercase;color:var(--white)}
.tt-pick button{appearance:none;border:0;background:transparent;margin-left:16px;padding:0;font:inherit;letter-spacing:inherit;text-transform:inherit;color:rgba(255,255,255,.75);cursor:pointer;box-shadow:inset 0 -2px 0 rgba(255,255,255,.5)}
.tt-pick button:hover{color:var(--white);box-shadow:inset 0 -2px 0 var(--white)}
.tt-cell:not(:empty),.tt-list li{cursor:pointer}
.tt-cell>*,.tt-list li>*{transition:opacity .25s}
.tt.pick .tt-cell:not(.hit)>*,.tt.pick .tt-list li:not(.hit)>*{opacity:.3}
.tt.pick .tt-cell.hit:not(.is-next){background:rgba(255,255,255,.16);box-shadow:inset 0 0 0 2px var(--white)}
.tt-tabs button.has:not([aria-selected="true"]){box-shadow:inset 0 0 0 2px var(--white),inset 0 -6px 0 var(--white)}
@media (max-width:768px){.tt-pick{margin-top:16px}.tt-pick-d{font-size:15px}.tt-pick button{display:block;margin:12px auto 0}}

/* opening hours: today's line is marked */
.hours-row li.today .hr-d{color:var(--white)}
.hr-now{font-style:normal;margin-left:8px;padding:0 6px;background:var(--white);color:var(--royal-blue);font-size:10px;line-height:16px;display:inline-block}
@media (prefers-reduced-motion:reduce){.btn,.nav-cta,.pk-i,.op,.class-img{transition:none}}
'''.replace('GRAIN', GRAIN) + P8.FOLD_CSS

JS = r'''
(function(){
  var root=document.documentElement, head=document.querySelector('header'), mo=root.classList.contains('mo');

  /* how far down the page: the line under the header */
  var busy=false;
  function read(){ busy=false; var max=root.scrollHeight-innerHeight; head.style.setProperty('--read',max>0?Math.min(1,scrollY/max).toFixed(4):0) }
  addEventListener('scroll',function(){ if(!busy){ busy=true; requestAnimationFrame(read) } },{passive:true});
  addEventListener('resize',read); read();

  /* blocks come up once as you reach them; anything on the first screen is left as it is */
  if(mo&&'IntersectionObserver' in window){
    var phone=matchMedia('(max-width:768px)').matches;
    var host=new WeakMap();   /* a note that is clipped away never counts as on screen: its parent is watched for it */
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(!e.isIntersecting) return;
        var el=host.get(e.target)||e.target; io.unobserve(e.target); el.classList.add('pz-in');
        setTimeout(function(){ el.classList.remove('pz-up','pz-wr','pz-in'); el.style.removeProperty('--d') },2400);
      });
    },{rootMargin:'0px 0px -10% 0px',threshold:.06});
    var add=function(sel,cls,gap,base){
      [].forEach.call(document.querySelectorAll(sel),function(el,i){
        if(el.getBoundingClientRect().top<innerHeight) return;
        el.classList.add(cls||'pz-up');
        el.style.setProperty('--d',((base||0)+Math.min(i,6)*(gap||0))+'ms');
        if(cls==='pz-wr'){ host.set(el.parentElement,el); io.observe(el.parentElement) } else io.observe(el);
      });
    };
    add('.section-header'); add('.section-script','pz-wr');
    add('.gym-col','pz-up',90); add('.gym-map');
    add(phone?'.classes-grid':'.class-card','pz-up',70);
    add('.tt'); add('#pc-opts'); add('#pc-plan','pz-up',0,phone?0:120);
    add('.rv-rating'); add('.marquee'); add('.about-band p'); add('.family','pz-up',0,120);
    add('.find-a'); add('.find-b','pz-up',0,phone?0:100); add('.faq-item','pz-up',40);
  }

  /* today's line in the opening hours (Lisbon time) */
  var day=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Lisbon',weekday:'short'}).format(new Date());
  var li=document.querySelectorAll('.hours-row li')[day==='Sat'?1:day==='Sun'?2:0];
  if(li){ li.classList.add('today'); var hd=li.querySelector('.hr-d'), f=document.createElement('i'); f.className='hr-now'; f.textContent='Today'; hd.appendChild(f); }

  /* tap a class, on a card or in the timetable: what it is, when it is on, and only its slots lit */
  var S=window.ELITE_SCHEDULE, tt=document.getElementById('timetable'), list=document.getElementById('tt-list'), tabs=document.getElementById('tt-tabs');
  if(!S||!tt||!list) return;
  var ORDER=['mon','tue','wed','thu','fri','sat','sun'], SHORT={mon:'Mon',tue:'Tue',wed:'Wed',thu:'Thu',fri:'Fri',sat:'Sat',sun:'Sun'};
  var byName={}; Object.keys(S.classes).forEach(function(k){ byName[S.classes[k].name.toLowerCase()]=k });
  var cards=[].slice.call(document.querySelectorAll('.class-card')), picked=null;
  var box=document.createElement('div'); box.className='tt-pick'; box.setAttribute('aria-live','polite'); tt.querySelector('.tt-head').appendChild(box);
  function esc(t){ return String(t).replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c] }) }
  function slots(k){ return S.sessions.filter(function(x){ return x.class===k }).sort(function(a,b){ return ORDER.indexOf(a.day)-ORDER.indexOf(b.day)||a.time.localeCompare(b.time) }) }
  function keyOf(el){ var n=el.querySelector('.tt-name'); return n&&n.firstChild?byName[String(n.firstChild.nodeValue||'').trim().toLowerCase()]:null }
  function paint(){
    tt.classList.toggle('pick',!!picked);
    [].forEach.call(tt.querySelectorAll('.tt-cell,.tt-list li'),function(c){ c.classList.toggle('hit',!!picked&&keyOf(c)===picked) });
    cards.forEach(function(c){ var on=!!picked&&c.dataset.cls===picked; c.classList.toggle('on',on); c.setAttribute('aria-pressed',on?'true':'false') });
    [].forEach.call(tabs.children,function(b){ b.classList.toggle('has',!!picked&&S.sessions.some(function(x){ return x.day===b.dataset.day&&x.class===picked })) });
    if(!picked){ box.innerHTML=''; return }
    var c=S.classes[picked], mins=slots(picked).map(function(x){ return x.minutes }).filter(function(v,i,a){ return v&&a.indexOf(v)===i }).sort(function(a,b){ return a-b });
    box.innerHTML='<p class="tt-pick-n">'+esc(c.name)+'</p>'+(c.about?'<p class="tt-pick-d">'+esc(c.about)+'</p>':'')+
      '<p class="tt-pick-s">'+slots(picked).map(function(x){ return SHORT[x.day]+' '+x.time }).join(' · ')+(mins.length?' · '+mins.join(' or ')+' min':'')+'<button type="button">Show all classes</button></p>';
  }
  function pick(k,scroll){
    picked=picked===k?null:k; paint();
    if(!picked) return;
    /* on a phone open the first day it runs, from today on */
    var today=ORDER.indexOf(day.toLowerCase()), days=slots(picked).map(function(x){ return x.day });
    var first=days.filter(function(d){ return ORDER.indexOf(d)>=today })[0]||days[0];
    var now=tabs.querySelector('[aria-selected="true"]'), tab=first&&tabs.querySelector('[data-day="'+first+'"]');
    if(tab&&now&&days.indexOf(now.dataset.day)<0) tab.click();
    if(scroll) tt.scrollIntoView({behavior:mo?'smooth':'auto',block:'center'});
  }
  cards.forEach(function(c){
    var nm=(c.querySelector('.class-name').textContent||'').trim(), k=byName[nm.toLowerCase()]; if(!k) return;
    c.dataset.cls=k; c.tabIndex=0; c.setAttribute('role','button'); c.setAttribute('aria-pressed','false'); c.setAttribute('aria-label',nm+': what it is and when it is on');
    var days=ORDER.filter(function(d){ return S.sessions.some(function(x){ return x.day===d&&x.class===k }) }).map(function(d){ return SHORT[d] });
    var el=document.createElement('div'); el.className='class-days'; el.innerHTML=days.join(' · ')+'<i aria-hidden="true">&darr;</i>'; c.querySelector('.class-overlay').appendChild(el);
    c.addEventListener('click',function(){ pick(k,true) });
    c.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); pick(k,true) } });
  });
  tt.addEventListener('click',function(e){
    if(e.target.closest('.tt-pick button')){ if(picked) pick(picked); return }
    var c=e.target.closest('.tt-cell,.tt-list li'), k=c&&keyOf(c); if(k) pick(k,false);
  });
  if(window.MutationObserver) new MutationObserver(paint).observe(list,{childList:true});
})();
''' + P8.ROLL_JS


def base():
    s = P8.shared(io.open(os.path.join(ROOT, P8.SRC), encoding='utf-8').read())
    # the torn edge above Good to know showed white teeth between the blue band and the grey one: a flat edge there
    s = sub1(s, '<section class="faq-section torn-top" id="faq">', '<section class="faq-section" id="faq">')
    # a review opens itself on Google when reviews.js has its link; the gym's page until then
    s = sub1(s, """'<a class="rv-card" href="'+R.url+'" target""", """'<a class="rv-card" href="'+esc(r.url||R.url)+'" target""")
    return s


def inject(s, v, css, js):
    head = '%s<style id="polish-css">%s</style>\n' % (P8.HEAD_JS, css)
    body = '<script id="polish-js">%s\n/* %s */%s</script>\n' % (P8.FIX_JS, v, js)
    s = sub1(s, '<style id="price-list-css">', head + '<style id="price-list-css">')
    return sub1(s, '<script id="price-list-js">', body + '<script id="price-list-js">')


HERO_CSS = r'''
/* ---------- 2.9.1 only: two buttons under the headline ---------- */
.hero-acts{grid-column:1 / -1;display:flex;justify-content:center;gap:12px;margin-top:32px}
.hero-acts .btn{min-width:184px}
@media (min-width:769px){
  .hero{padding-top:64px}
  .hero-image-strip{margin-top:56px;height:clamp(300px,44vh,480px)}
}
@media (max-width:768px){
  .hero{padding-top:32px}
  .hero-sub{margin-top:24px}
  .hero-acts{margin-top:24px;gap:8px}
  .hero-acts .btn{flex:1 1 0;min-width:0;padding-left:8px;padding-right:8px}
  .hero-image-strip{height:240px;margin-top:40px}
  /* a person first on a phone */
  .hero-img:nth-child(2){order:-1}
}
'''


def with_buttons(s):
    return sub1(s, 'Weights, machines, classes and space to train outdoors.</p>\n  </div>',
                'Weights, machines, classes and space to train outdoors.</p>\n'
                '    <div class="hero-acts"><a class="btn" href="#prices">See prices</a><a class="btn ghost" href="https://maps.app.goo.gl/ks6o4URGCYT7rzHJ8" target="_blank" rel="noopener">Get directions</a></div>\n  </div>')


if __name__ == '__main__':
    b = base()
    for name, page in (('2-9', inject(b, '2.9', CSS, JS)), ('2-9-1', inject(with_buttons(b), '2.9.1', CSS + HERO_CSS, JS))):
        out = 'elite-wellness-landing_%s.html' % name
        io.open(os.path.join(ROOT, out), 'w', encoding='utf-8').write(page)
        print(out)
