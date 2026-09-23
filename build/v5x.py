# -*- coding: utf-8 -*-
"""Five iterations on the receipt builder (2.4.5.1 to 2.4.5.5).
One question stays the same in all of them: where do the price and the button
live so that they are never a scroll away from the thing you just tapped."""

# ---- the option chips, identical in every variant except 4 ----
CHIPS = '''      <fieldset class="rc-set">
        <legend class="rc-leg">Who are you</legend>
        <div class="rc-chips" id="rc-who">
          <button class="rc-chip on" type="button" data-who="visitor">Visiting</button>
          <button class="rc-chip" type="button" data-who="member">Living here</button>
          <button class="rc-chip" type="button" data-who="pt">With a coach</button>
        </div>
      </fieldset>
      <fieldset class="rc-set" id="rc-set-stay">
        <legend class="rc-leg">How long</legend>
        <div class="rc-chips" id="rc-stay"></div>
      </fieldset>
      <fieldset class="rc-set" id="rc-set-plan" hidden>
        <legend class="rc-leg">How often</legend>
        <div class="rc-chips" id="rc-plan"></div>
      </fieldset>
      <fieldset class="rc-set" id="rc-set-pay" hidden>
        <legend class="rc-leg">How you pay</legend>
        <div class="rc-chips" id="rc-pay">
          <button class="rc-chip on" type="button" data-pay="dd">Direct debit</button>
          <button class="rc-chip" type="button" data-pay="desk">At the desk</button>
        </div>
      </fieldset>
      <fieldset class="rc-set" id="rc-set-pack" hidden>
        <legend class="rc-leg">Which pack</legend>
        <div class="rc-chips" id="rc-pack"></div>
      </fieldset>
'''

# the chip grid and the shared wiring, in every variant
CHIPCSS = '''
.rc-set{border:0;padding:0;margin:0 0 32px;min-width:0}
.rc-leg{font-weight:800;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey);padding:0;margin-bottom:12px}
.rc-chips{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.rc-chips[hidden]{display:none}
#rc-stay{grid-template-columns:repeat(3,1fr)}
#rc-pay{grid-template-columns:repeat(2,1fr)}
#rc-pack{grid-template-columns:repeat(2,1fr)}
.rc-chip{appearance:none;border:2px solid var(--light-grey);background:var(--white);font-family:var(--font-body);font-weight:700;font-size:14px;line-height:20px;padding:12px 10px;cursor:pointer;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;min-height:60px;transition:border-color .15s,background .15s,color .15s}
.rc-chip:hover{border-color:var(--black)}
.rc-chip.on{background:var(--royal-blue);border-color:var(--royal-blue);color:var(--white)}
.rc-chip small{display:block;font-weight:400;font-size:11px;line-height:16px;opacity:.75;margin-top:2px}
@media (max-width:768px){
  .rc-set{margin-bottom:24px}
  .rc-chips{grid-template-columns:repeat(2,1fr)}
  #rc-who{grid-template-columns:repeat(3,1fr)}
  #rc-stay{grid-template-columns:repeat(2,1fr)}
  #rc-stay .rc-chip:last-child{grid-column:1 / -1}
  .rc-chip{font-size:13px;padding:12px 8px;min-height:56px}
}
'''

# the wiring every variant shares: fill the chips, hold the state, call paint()
WIRE = '''
  var E=window.EWPricing, P=E.P;
  var st={who:'visitor',stay:'s1',plan:'un',pay:'dd',pack:'p8'}, cur=null;
  document.getElementById('rc-stay').innerHTML = P.visitor.map(function(v){
    return '<button class="rc-chip'+(v.id===st.stay?' on':'')+'" type="button" data-stay="'+v.id+'">'+v.name+'<small>'+E.money(v.price)+'</small></button>';
  }).join('');
  document.getElementById('rc-plan').innerHTML = P.member.plans.map(function(p){
    return '<button class="rc-chip'+(p.id===st.plan?' on':'')+'" type="button" data-plan="'+p.id+'">'+p.name+'<small>'+E.money(p.dd)+' / 2 wks</small></button>';
  }).join('');
  document.getElementById('rc-pack').innerHTML = P.pt.packs.map(function(k){
    return '<button class="rc-chip'+(k.id===st.pack?' on':'')+'" type="button" data-pack="'+k.id+'">'+k.name+'<small>'+E.money(k.total)+'</small></button>';
  }).join('');
  function pick(g,a,v){ [].forEach.call(document.getElementById(g).children,function(b){ b.classList.toggle('on', b.dataset[a]===v) }) }
  function sets(){
    document.getElementById('rc-set-stay').hidden = st.who!=='visitor';
    document.getElementById('rc-set-plan').hidden = st.who!=='member';
    document.getElementById('rc-set-pay').hidden  = st.who!=='member';
    document.getElementById('rc-set-pack').hidden = st.who!=='pt';
  }
  function wire(root, after){
    root.addEventListener('click',function(e){
      var b=e.target.closest('.rc-chip'); if(!b) return; var d=b.dataset;
      if(d.who!=null){ st.who=d.who; pick('rc-who','who',d.who); sets(); E.track('pricing_who',{who:d.who}) }
      else if(d.stay!=null){ st.stay=d.stay; pick('rc-stay','stay',d.stay) }
      else if(d.plan!=null){ st.plan=d.plan; pick('rc-plan','plan',d.plan) }
      else if(d.pay!=null){ st.pay=d.pay; pick('rc-pay','pay',d.pay) }
      else if(d.pack!=null){ st.pack=d.pack; pick('rc-pack','pack',d.pack) }
      paint(); if(after) after(b);
    });
  }
'''

# ===================================================== .1 one bar at the bottom
A_SEC = '''  <div class="rc rc-onebar">
    <div class="rc-build">
''' + CHIPS + '''    </div>
  </div>
  <div class="pbar" id="pbar" aria-live="polite">
    <div class="pbar-in">
      <div class="pbar-txt"><span id="pbar-n"></span><small id="pbar-l"></small></div>
      <b id="pbar-p"></b>
      <button class="btn" type="button" id="pbar-go">Get this</button>
    </div>
  </div>
'''
A_CSS = CHIPCSS + '''
.rc-onebar{max-width:720px;margin:0 auto}
.pbar{position:fixed;left:0;right:0;bottom:0;z-index:90;background:var(--black);color:var(--white);transform:translateY(110%);transition:transform .3s cubic-bezier(.2,.8,.2,1)}
html.pricing-bottom .pbar{transform:none}
.pbar-in{display:flex;align-items:center;gap:16px;padding:12px 1.5rem calc(12px + env(safe-area-inset-bottom));max-width:1440px;margin:0 auto}
.pbar-txt{flex:1 1 auto;min-width:0}
.pbar-txt span{display:block;font-size:14px;line-height:20px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pbar-txt small{display:block;font-size:11px;line-height:16px;color:rgba(255,255,255,.55)}
.pbar b{font-family:var(--font-display);font-size:30px;line-height:1;color:var(--accent);white-space:nowrap}
.pbar .btn{flex:0 0 auto;border:0;padding:14px 20px;clip-path:polygon(5% 0%,100% 0%,95% 100%,0% 100%)}
.pbar .btn:hover,.pbar .btn:focus-visible{background:var(--royal-blue);color:var(--white)}
@media (min-width:769px){ .pbar-in{padding-left:4rem;padding-right:4rem} }
@media (max-width:768px){ .pbar b{font-size:26px} .pbar .btn{padding:12px 14px;font-size:.8rem} .rc-build{padding-bottom:16px} }
@media (prefers-reduced-motion:reduce){ .pbar{transition:none} }
'''
A_JS = '''
(function(){
''' + WIRE + '''
  var n=document.getElementById('pbar-n'), l=document.getElementById('pbar-l'), pr=document.getElementById('pbar-p');
  function paint(){ cur=E.plan(st); n.textContent=cur.title; l.textContent=cur.totalLabel; pr.textContent=E.money(cur.price) }
  wire(document.querySelector('.rc'));
  document.getElementById('pbar-go').addEventListener('click',function(){ if(cur) E.review(cur) });
  sets(); paint(); E.ownBottom('prices');
})();
'''

# ================================================== .2 the card sticks at the top
B_SEC = '''  <div class="rc rc-topcard">
    <div class="tcard" id="tcard">
      <div class="tcard-in">
        <div class="tcard-txt"><span id="tc-n"></span><small id="tc-l"></small></div>
        <b id="tc-p"></b>
      </div>
      <button class="btn" type="button" id="tc-go">Get this plan</button>
      <p class="tcard-note" id="tc-note"></p>
    </div>
    <div class="rc-build">
''' + CHIPS + '''    </div>
  </div>
'''
B_CSS = CHIPCSS + '''
.rc-topcard{max-width:720px;margin:0 auto}
.tcard{position:sticky;top:74px;z-index:40;background:var(--black);color:var(--white);padding:20px 24px;margin-bottom:32px}
.tcard-in{display:flex;align-items:flex-end;justify-content:space-between;gap:16px}
.tcard-txt{min-width:0}
.tcard-txt span{display:block;font-size:15px;line-height:22px}
.tcard-txt small{display:block;font-size:11px;line-height:16px;color:rgba(255,255,255,.55)}
.tcard b{font-family:var(--font-display);font-size:40px;line-height:1;color:var(--accent);white-space:nowrap}
.tcard .btn{width:100%;justify-content:center;margin-top:16px}
.tcard-note{font-size:11px;line-height:16px;color:rgba(255,255,255,.55);margin-top:12px}
@media (max-width:768px){
  .tcard{top:50px;padding:16px;margin:0 -1.5rem 24px;width:calc(100% + 3rem)}
  .tcard b{font-size:34px}
  .tcard-note{display:none}
}
'''
B_JS = '''
(function(){
''' + WIRE + '''
  var n=document.getElementById('tc-n'), l=document.getElementById('tc-l'), pr=document.getElementById('tc-p'), nt=document.getElementById('tc-note');
  function paint(){ cur=E.plan(st); n.textContent=cur.title; l.textContent=cur.totalLabel; pr.textContent=E.money(cur.price); nt.textContent=cur.notes.join(' ') }
  wire(document.querySelector('.rc'));
  document.getElementById('tc-go').addEventListener('click',function(){ if(cur) E.review(cur) });
  sets(); paint();
})();
'''

# ============================================================ .3 one at a time
C_SEC = '''  <div class="rc rc-steps">
    <div class="wz" id="wz">
      <ol class="wz-dots" id="wz-dots" aria-hidden="true"></ol>
      <div class="wz-pane" data-pane="who">
        <p class="wz-ask">Who are you?</p>
        <div class="rc-chips" id="rc-who">
          <button class="rc-chip" type="button" data-who="visitor">Visiting</button>
          <button class="rc-chip" type="button" data-who="member">Living here</button>
          <button class="rc-chip" type="button" data-who="pt">With a coach</button>
        </div>
      </div>
      <div class="wz-pane" data-pane="what" hidden>
        <p class="wz-ask" id="wz-ask2"></p>
        <div class="rc-chips" id="rc-stay"></div>
        <div class="rc-chips" id="rc-plan" hidden></div>
        <div class="rc-chips" id="rc-pack" hidden></div>
      </div>
      <div class="wz-pane" data-pane="pay" hidden>
        <p class="wz-ask">How will you pay?</p>
        <div class="rc-chips" id="rc-pay">
          <button class="rc-chip on" type="button" data-pay="dd">Direct debit<small>saves €130 a year</small></button>
          <button class="rc-chip" type="button" data-pay="desk">At the desk<small>every 2 weeks</small></button>
        </div>
      </div>
      <div class="wz-pane wz-end" data-pane="end" hidden>
        <p class="wz-k" id="wz-l"></p>
        <p class="wz-price" id="wz-p"></p>
        <p class="wz-name" id="wz-n"></p>
        <p class="wz-note" id="wz-note"></p>
        <button class="btn" type="button" id="wz-go">Get this plan</button>
      </div>
      <button class="wz-back" type="button" id="wz-back" hidden>Back</button>
    </div>
  </div>
'''
C_CSS = CHIPCSS + '''
.rc-steps{max-width:560px;margin:0 auto;min-height:420px}
.wz-dots{display:flex;gap:6px;justify-content:center;list-style:none;margin:0 0 32px;padding:0}
.wz-dots li{width:24px;height:2px;background:var(--light-grey)}
.wz-dots li.on{background:var(--royal-blue)}
.wz-ask{font-family:var(--font-display);font-size:clamp(26px,4vw,38px);line-height:1.05;text-transform:uppercase;text-align:center;margin-bottom:24px}
.rc-steps .rc-chips{grid-template-columns:1fr;gap:8px}
.rc-steps .rc-chip{min-height:64px;font-size:16px}
.wz-end{text-align:center}
.wz-k{font-weight:800;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey)}
.wz-price{font-family:var(--font-display);font-size:clamp(72px,16vw,112px);line-height:.9;color:var(--royal-blue);margin:8px 0}
.wz-name{font-family:var(--font-display);font-size:26px;line-height:1;text-transform:uppercase;margin-bottom:12px}
.wz-note{font-size:13px;line-height:20px;color:var(--silver-grey);max-width:34ch;margin:0 auto 24px}
.wz-end .btn{justify-content:center}
.wz-back{display:block;margin:32px auto 0;appearance:none;border:0;background:transparent;font-family:var(--font-body);font-size:13px;color:var(--silver-grey);text-decoration:underline;cursor:pointer;padding:8px}
@media (prefers-reduced-motion:no-preference){ .wz-pane{animation:wzIn .22s ease both} @keyframes wzIn{from{opacity:0;transform:translateX(16px)}to{opacity:1;transform:none}} }
'''
C_JS = '''
(function(){
''' + WIRE + '''
  var order=['who','what','pay','end'], at=0;
  function steps(){ return st.who==='member' ? order : ['who','what','end'] }
  function show(i){
    var seq=steps(); at=Math.max(0,Math.min(seq.length-1,i));
    [].forEach.call(document.querySelectorAll('.wz-pane'),function(p){ p.hidden = p.dataset.pane!==seq[at] });
    document.getElementById('wz-dots').innerHTML = seq.map(function(_,k){ return '<li class="'+(k<=at?'on':'')+'"></li>' }).join('');
    document.getElementById('wz-back').hidden = at===0;
    if(seq[at]==='end') end();
  }
  function paint(){ cur=E.plan(st) }
  function end(){
    paint();
    document.getElementById('wz-l').textContent=cur.totalLabel;
    document.getElementById('wz-p').textContent=E.money(cur.price);
    document.getElementById('wz-n').textContent=cur.title;
    document.getElementById('wz-note').textContent=cur.notes.join(' ');
  }
  document.getElementById('rc-who').addEventListener('click',function(e){
    var b=e.target.closest('.rc-chip'); if(!b) return;
    st.who=b.dataset.who; pick('rc-who','who',st.who); E.track('pricing_who',{who:st.who});
    document.getElementById('wz-ask2').textContent = st.who==='visitor' ? 'How long are you here?' : st.who==='member' ? 'How often will you train?' : 'Which pack?';
    document.getElementById('rc-stay').hidden = st.who!=='visitor';
    document.getElementById('rc-plan').hidden = st.who!=='member';
    document.getElementById('rc-pack').hidden = st.who!=='pt';
    show(1);
  });
  document.querySelector('[data-pane="what"]').addEventListener('click',function(e){
    var b=e.target.closest('.rc-chip'); if(!b) return; var d=b.dataset;
    if(d.stay!=null){ st.stay=d.stay; pick('rc-stay','stay',d.stay) }
    if(d.plan!=null){ st.plan=d.plan; pick('rc-plan','plan',d.plan) }
    if(d.pack!=null){ st.pack=d.pack; pick('rc-pack','pack',d.pack) }
    show(2);
  });
  document.getElementById('rc-pay').addEventListener('click',function(e){
    var b=e.target.closest('.rc-chip'); if(!b) return;
    st.pay=b.dataset.pay; pick('rc-pay','pay',st.pay); show(3);
  });
  document.getElementById('wz-back').addEventListener('click',function(){ show(at-1) });
  document.getElementById('wz-go').addEventListener('click',function(){ if(cur) E.review(cur) });
  show(0);
})();
'''

# ================================================= .4 the price is on the option
D_SEC = '''  <div class="rc rc-inline">
    <div class="rc-build">
      <fieldset class="rc-set">
        <legend class="rc-leg">Who are you</legend>
        <div class="rc-chips" id="rc-who">
          <button class="rc-chip on" type="button" data-who="visitor">Visiting</button>
          <button class="rc-chip" type="button" data-who="member">Living here</button>
          <button class="rc-chip" type="button" data-who="pt">With a coach</button>
        </div>
      </fieldset>
      <fieldset class="rc-set" id="rc-set-pay" hidden>
        <legend class="rc-leg">How you pay</legend>
        <div class="rc-chips" id="rc-pay">
          <button class="rc-chip on" type="button" data-pay="dd">Direct debit</button>
          <button class="rc-chip" type="button" data-pay="desk">At the desk</button>
        </div>
      </fieldset>
      <ul class="op" id="op"></ul>
      <div class="rc-chips" id="rc-stay" hidden></div>
      <div class="rc-chips" id="rc-plan" hidden></div>
      <div class="rc-chips" id="rc-pack" hidden></div>
    </div>
  </div>
'''
D_CSS = CHIPCSS + '''
.rc-inline{max-width:720px;margin:0 auto}
.op{list-style:none;margin:32px 0 0;padding:0;box-shadow:inset 0 1px 0 var(--black)}
.op-row{appearance:none;width:100%;border:0;background:transparent;display:grid;grid-template-columns:1fr auto;align-items:baseline;gap:16px;padding:20px 0;box-shadow:inset 0 -1px 0 var(--light-grey);cursor:pointer;font-family:var(--font-body);text-align:left}
.op-row b{font-size:17px;line-height:24px;font-weight:700}
.op-row small{display:block;font-size:12px;line-height:18px;color:var(--silver-grey);margin-top:2px}
.op-row i{font-style:normal;font-family:var(--font-display);font-size:26px;line-height:1;white-space:nowrap}
.op li.on .op-row i{color:var(--royal-blue)}
.op li.on .op-row b::after{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--royal-blue);margin-left:8px;vertical-align:1px}
.op-panel{display:none;padding:0 0 24px;box-shadow:inset 0 -1px 0 var(--light-grey)}
.op li.on .op-panel{display:block}
.op-line{display:flex;justify-content:space-between;gap:16px;font-size:14px;line-height:22px;color:#3a3a3a;padding:2px 0}
.op-note{font-size:12px;line-height:18px;color:var(--silver-grey);margin:8px 0 16px}
.op-panel .btn{width:100%;justify-content:center}
@media (min-width:769px){ .op-panel .btn{width:auto} }
'''
D_JS = '''
(function(){
''' + WIRE + '''
  var list=document.getElementById('op');
  function rows(){
    if(st.who==='visitor') return P.visitor.map(function(v){ return {k:'stay',id:v.id,name:v.name,sub:'Insurance included'} });
    if(st.who==='member') return P.member.plans.map(function(p){ return {k:'plan',id:p.id,name:p.name,sub:'Every 2 weeks, plus '+E.money(P.insurance.year)+' insurance a year'} });
    return P.pt.packs.map(function(k){ return {k:'pack',id:k.id,name:k.name,sub:k.sessions>1?E.money(k.each)+' a session, valid '+k.months+' months':'One session with a coach'} });
  }
  function priceOf(r){
    var s={who:st.who,stay:st.stay,plan:st.plan,pay:st.pay,pack:st.pack};
    s[r.k==='stay'?'stay':r.k==='plan'?'plan':'pack']=r.id;
    return E.plan(s);
  }
  function selected(){ return st.who==='visitor'?st.stay:st.who==='member'?st.plan:st.pack }
  function paint(){
    cur=E.plan(st);
    list.innerHTML = rows().map(function(r){
      var p=priceOf(r), on=r.id===selected();
      return '<li class="'+(on?'on':'')+'" data-id="'+r.id+'" data-k="'+r.k+'">'+
        '<button class="op-row" type="button"><span><b>'+r.name+'</b><small>'+r.sub+'</small></span><i>'+E.money(p.price)+'</i></button>'+
        '<div class="op-panel">'+
          p.detail.map(function(l){ return '<div class="op-line"><span>'+l[0]+'</span><span>'+(l[1]||'')+'</span></div>' }).join('')+
          (p.notes.length?'<p class="op-note">'+p.notes.join(' ')+'</p>':'<p class="op-note">'+p.totalLabel+'</p>')+
          '<button class="btn" type="button" data-go="1">Get this plan</button>'+
        '</div></li>';
    }).join('');
  }
  list.addEventListener('click',function(e){
    if(e.target.closest('[data-go]')){ if(cur) E.review(cur); return }
    var li=e.target.closest('li'); if(!li) return;
    st[li.dataset.k==='stay'?'stay':li.dataset.k==='plan'?'plan':'pack']=li.dataset.id;
    paint();
  });
  document.getElementById('rc-who').addEventListener('click',function(e){
    var b=e.target.closest('.rc-chip'); if(!b) return;
    st.who=b.dataset.who; pick('rc-who','who',st.who);
    document.getElementById('rc-set-pay').hidden = st.who!=='member';
    E.track('pricing_who',{who:st.who}); paint();
  });
  document.getElementById('rc-pay').addEventListener('click',function(e){
    var b=e.target.closest('.rc-chip'); if(!b) return;
    st.pay=b.dataset.pay; pick('rc-pay','pay',st.pay); paint();
  });
  paint();
})();
'''

# ============================================================ .5 a bottom sheet
E_SEC = '''  <div class="rc rc-sheet">
    <div class="rc-build">
''' + CHIPS + '''    </div>
  </div>
  <div class="psheet" id="psheet">
    <button class="psheet-grab" type="button" id="psheet-grab" aria-expanded="false">
      <span class="psheet-bar" aria-hidden="true"></span>
      <span class="psheet-peek"><span id="ps-n"></span><b id="ps-p"></b></span>
    </button>
    <div class="psheet-body" id="psheet-body">
      <div id="ps-lines"></div>
      <p class="psheet-note" id="ps-note"></p>
    </div>
    <div class="psheet-act"><button class="btn" type="button" id="ps-go">Get this plan</button></div>
  </div>
'''
E_CSS = CHIPCSS + '''
.rc-sheet{max-width:720px;margin:0 auto}
.psheet{position:fixed;left:0;right:0;bottom:0;z-index:90;background:var(--black);color:var(--white);transform:translateY(110%);transition:transform .3s cubic-bezier(.2,.8,.2,1);max-height:80dvh;display:flex;flex-direction:column}
html.pricing-bottom .psheet{transform:none}
.psheet-grab{appearance:none;border:0;background:transparent;color:inherit;width:100%;padding:8px 1.5rem 12px;cursor:pointer;font-family:var(--font-body)}
.psheet-bar{display:block;width:36px;height:3px;border-radius:2px;background:rgba(255,255,255,.35);margin:0 auto 10px}
.psheet-peek{display:flex;align-items:baseline;justify-content:space-between;gap:16px}
.psheet-peek span{font-size:14px;line-height:20px;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.psheet-peek b{font-family:var(--font-display);font-size:30px;line-height:1;color:var(--accent);white-space:nowrap}
.psheet-body{display:none;overflow-y:auto;padding:8px 1.5rem 0}
.psheet.open .psheet-body{display:block}
.psheet-line{display:flex;justify-content:space-between;gap:16px;padding:10px 0;box-shadow:inset 0 -1px 0 rgba(255,255,255,.18);font-size:14px;line-height:20px}
.psheet-line.sub{color:rgba(255,255,255,.6);font-size:12px;box-shadow:none;padding-top:0}
.psheet-note{font-size:12px;line-height:18px;color:rgba(255,255,255,.6);margin:12px 0 0}
.psheet-act{padding:12px 1.5rem calc(12px + env(safe-area-inset-bottom))}
.psheet-act .btn{width:100%;justify-content:center}
@media (min-width:769px){ .psheet-grab,.psheet-body,.psheet-act{padding-left:4rem;padding-right:4rem} }
@media (prefers-reduced-motion:reduce){ .psheet{transition:none} }
'''
E_JS = '''
(function(){
''' + WIRE + '''
  var sheet=document.getElementById('psheet'), grab=document.getElementById('psheet-grab');
  var n=document.getElementById('ps-n'), pr=document.getElementById('ps-p');
  function paint(){
    cur=E.plan(st);
    n.textContent=cur.title; pr.textContent=E.money(cur.price);
    document.getElementById('ps-lines').innerHTML = cur.detail.map(function(l){
      return '<div class="psheet-line'+(l[2]?' sub':'')+'"><span>'+l[0]+'</span><b>'+(l[1]||'')+'</b></div>';
    }).join('') + '<div class="psheet-line"><span>'+cur.totalLabel+'</span><b>'+E.money(cur.price)+'</b></div>';
    document.getElementById('ps-note').textContent=cur.notes.join(' ');
  }
  wire(document.querySelector('.rc'));
  grab.addEventListener('click',function(){
    var open=sheet.classList.toggle('open');
    grab.setAttribute('aria-expanded',String(open));
    E.track(open?'pricing_sheet_open':'pricing_sheet_close',{plan:cur&&cur.id});
  });
  document.getElementById('ps-go').addEventListener('click',function(){ if(cur) E.review(cur) });
  sets(); paint(); E.ownBottom('prices');
})();
'''

VARIANTS_X = [
  ('2-4-5-1', 'one bar, at the bottom', A_SEC, A_CSS, A_JS),
  ('2-4-5-2', 'the card rides along', B_SEC, B_CSS, B_JS),
  ('2-4-5-3', 'one question at a time', C_SEC, C_CSS, C_JS),
  ('2-4-5-4', 'the price is on the option', D_SEC, D_CSS, D_JS),
  ('2-4-5-5', 'a sheet you can open', E_SEC, E_CSS, E_JS),
]
