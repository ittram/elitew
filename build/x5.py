# -*- coding: utf-8 -*-
"""2.4.5.1 to 2.4.5.3: the committed 2.4.5, plus one mobile-only change each.
Nothing in 2.4.5 is edited: each version appends CSS, a little markup and a
script that mirrors the receipt and presses its existing button. Desktop is
therefore identical to 2.4.5 by construction."""
import io

BASE = io.open('elite-wellness-landing_2-4-5.html', encoding='utf-8').read()
BAR_END = '<a class="btn on-dark ghost" href="https://maps.app.goo.gl/ks6o4URGCYT7rzHJ8" target="_blank" rel="noopener">Directions</a>\n</div>'
assert BASE.count(BAR_END) == 1
STRIP_END = '<span id="rc-sticky-n"></span><b id="rc-sticky-p"></b>\n    </button>'
assert BASE.count(STRIP_END) == 1

# knows when a phone is in the Prices section, and keeps copies of the plan in step
SYNC = '''
(function(){
  var mq=window.matchMedia('(max-width:768px)'), sec=document.getElementById('prices'), root=document.documentElement, inView=false;
  function set(){ var on=inView&&mq.matches; root.classList.toggle('in-prices',on); if(!on){ var b=document.getElementById('action-bar'); if(b) b.classList.remove('open') } }
  /* true while the section crosses the middle of the screen: one switch in, one out, no flicker */
  if(sec&&'IntersectionObserver' in window) new IntersectionObserver(function(es){ inView=es[0].isIntersecting; set() },{rootMargin:'-45% 0px -45% 0px'}).observe(sec);
  if(mq.addEventListener) mq.addEventListener('change',set); else mq.addListener(set);
  function put(id,v){ var e=document.getElementById(id); if(e&&e.textContent!==v) e.textContent=v }
  function putHTML(id,v){ var e=document.getElementById(id); if(e&&e.innerHTML!==v) e.innerHTML=v }
  function mirror(){
    var n=document.getElementById('rc-sticky-n').textContent, p=document.getElementById('rc-sticky-p').textContent,
        l=document.getElementById('rc-total-l').textContent;
    put('bp-n',n); put('bp-p',p); put('bp-l',l); put('rt-n',n); put('rt-p',p); put('rt-l',l);
    putHTML('bs-lines',document.getElementById('rc-lines').innerHTML);
    put('bs-note',document.getElementById('rc-note').textContent);
  }
  var mo=new MutationObserver(mirror), opt={subtree:true,childList:true,characterData:true};
  mo.observe(document.querySelector('.rc-sticky'),opt); mo.observe(document.querySelector('.rc-receipt'),opt);
  mirror();
  /* every copy of the button presses the receipt's own, so the flow and its tracking stay single */
  [].forEach.call(document.querySelectorAll('[data-rc-go]'),function(b){
    b.addEventListener('click',function(){ document.getElementById('rc-go').click() });
  });
  var tog=document.getElementById('bp-open');
  if(tog) tog.addEventListener('click',function(){
    var bar=document.getElementById('action-bar'), open=bar.classList.toggle('open');
    tog.setAttribute('aria-expanded',String(open));
    if(window.EWPricing) window.EWPricing.track(open?'pricing_sheet_open':'pricing_sheet_close',{});
  });
})();
'''

PRICE_ROW_CSS = '''
.bar-price{display:none}
@media (max-width:768px){
  .rc-sticky{display:none}
  html.in-prices .action-bar>.bar-status,html.in-prices .action-bar>.btn{display:none}
  html.in-prices .action-bar .bar-price{display:flex}
  .bar-price{flex:1 1 auto;align-items:center;gap:12px;min-width:0;animation:bpIn .25s ease both}
  .bp-txt{flex:1 1 auto;min-width:0;text-align:left}
  .bp-txt>span{display:block;font-size:13px;line-height:18px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bp-txt small{display:block;font-weight:800;font-size:10px;line-height:14px;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.55)}
  .bar-price b{font-family:var(--font-display);font-size:26px;line-height:1;color:var(--accent);white-space:nowrap}
  .bar-price .btn{flex:0 0 auto;padding:14px 18px;font-size:.85rem}
  @keyframes bpIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
}
@media (prefers-reduced-motion:reduce){.bar-price{animation:none}}
'''

def build(name, css, bar=None, strip=None, extra=''):
    s = BASE
    if bar:   s = s.replace(BAR_END, BAR_END[:-len('\n</div>')] + '\n' + bar + '\n</div>')
    if strip: s = s.replace(STRIP_END, STRIP_END + '\n' + strip)
    s = s.replace('</head>', '<style>\n/* ' + name + ': the only change from 2.4.5, phones only */' + css + '</style>\n</head>', 1)
    s = s.replace('</body>', '<script>' + SYNC + extra + '</script>\n</body>', 1)
    io.open('elite-wellness-landing_%s.html' % name.replace('.', '-'), 'w', encoding='utf-8').write(s)
    print(name, len(s))

# .1  the page's bar becomes the price row while you are in Prices
HANDOFF_CSS = '''
@media (max-width:768px){
  /* one price surface at a time: once the card and its button are on screen, the bar steps away */
  html.in-prices.card-visible .action-bar{transform:translateY(110%)}
}
'''
HANDOFF_JS = '''
(function(){
  var go=document.getElementById('rc-go'); if(!go||!('IntersectionObserver' in window)) return;
  new IntersectionObserver(function(es){
    document.documentElement.classList.toggle('card-visible', es[0].isIntersecting);
  },{threshold:0.5}).observe(go);
})();
'''
build('2.4.5.1', PRICE_ROW_CSS + HANDOFF_CSS, extra=HANDOFF_JS,
  bar='''  <div class="bar-price" aria-live="polite">
    <span class="bp-txt"><span id="bp-n"></span><small id="bp-l"></small></span>
    <b id="bp-p"></b>
    <button class="btn on-dark" type="button" data-rc-go>Get this</button>
  </div>''')

# .2  the same row, and it opens upward into the breakdown; the card below goes
build('2.4.5.2', PRICE_ROW_CSS + '''
.bar-sheet{display:none}
@media (max-width:768px){
  .rc-receipt{display:none}
  html.in-prices .action-bar{flex-wrap:wrap}
  html.in-prices .action-bar.open .bar-sheet{display:block}
  .bar-sheet{flex:1 0 100%;order:-1;padding:8px 0 4px;max-height:50dvh;overflow-y:auto}
  .bar-sheet .rc-line{display:flex;justify-content:space-between;gap:16px;padding:10px 0;box-shadow:inset 0 -1px 0 rgba(255,255,255,.18);font-size:14px;line-height:20px}
  .bar-sheet .rc-line.sub{color:rgba(255,255,255,.6);font-size:12px;box-shadow:none;padding-top:0}
  .bs-note{font-size:12px;line-height:18px;color:rgba(255,255,255,.6);margin:8px 0 4px}
  .bp-open{appearance:none;border:0;background:transparent;color:inherit;font-family:var(--font-body);display:flex;align-items:center;gap:12px;flex:1 1 auto;min-width:0;padding:0;cursor:pointer}
  .bp-open b{display:flex;align-items:center;gap:8px}
  .bp-open b::after{content:"";width:7px;height:7px;border-left:2px solid rgba(255,255,255,.6);border-top:2px solid rgba(255,255,255,.6);transform:rotate(45deg);margin-top:4px;transition:transform .2s}
  .action-bar.open .bp-open b::after{transform:rotate(225deg);margin-top:-4px}
}
''',
  bar='''  <div class="bar-sheet" id="bar-sheet"><div id="bs-lines"></div><p class="bs-note" id="bs-note"></p></div>
  <div class="bar-price" aria-live="polite">
    <button class="bp-open" type="button" id="bp-open" aria-expanded="false" aria-controls="bar-sheet">
      <span class="bp-txt"><span id="bp-n"></span><small id="bp-l"></small></span>
      <b id="bp-p"></b>
    </button>
    <button class="btn on-dark" type="button" data-rc-go>Get this</button>
  </div>''')

# .3  the strip at the top keeps its place and gets the button; the card below
#     and the page bar step aside, so the strip is the one surface
build('2.4.5.3', '''
.rc-top{display:none}
@media (max-width:768px){
  .rc-sticky,.rc-receipt{display:none}
  html.in-prices .action-bar{transform:translateY(110%)}
  .rc-top{display:flex;position:sticky;top:50px;z-index:40;width:calc(100% + 3rem);margin:0 -1.5rem 8px;align-items:center;gap:12px;background:var(--black);color:var(--white);padding:10px 1.5rem}
  .rt-txt{flex:1 1 auto;min-width:0}
  .rt-txt>span{display:block;font-size:13px;line-height:18px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .rt-txt small{display:block;font-weight:800;font-size:10px;line-height:14px;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.55)}
  .rc-top b{font-family:var(--font-display);font-size:26px;line-height:1;color:var(--accent);white-space:nowrap}
  .rc-top .btn{flex:0 0 auto;border:0;padding:12px 16px;font-size:.85rem;clip-path:polygon(5% 0%,100% 0%,95% 100%,0% 100%)}
}
''',
  strip='''    <div class="rc-top" aria-live="polite">
      <span class="rt-txt"><span id="rt-n"></span><small id="rt-l"></small></span>
      <b id="rt-p"></b>
      <button class="btn on-dark" type="button" data-rc-go>Get this</button>
    </div>''')
