# -*- coding: utf-8 -*-
"""2.4.5.4 to 2.4.5.8: the committed 2.4.5 plus an inline, phone-only builder.
Nothing in 2.4.5 is edited: each draft appends a container, a stylesheet, the
shared pricing-disclose.js and its own script. Desktop is identical by
construction, and on a phone nothing floats until Get this plan is pressed."""
import io

BASE = io.open('elite-wellness-landing_2-4-5.html', encoding='utf-8').read()
LEGAL = '<p class="pr-legal">All prices include VAT.'
PJS = '<script src="pricing.js"></script>'
for a in (LEGAL, PJS): assert BASE.count(a) == 1, a

def build(name, css, js):
    s = BASE.replace(LEGAL, '<div class="m-price" id="mp"></div>\n  ' + LEGAL, 1)
    s = s.replace(PJS, PJS + '\n<script src="pricing-disclose.js"></script>', 1)
    s = s.replace('</head>', '<link rel="stylesheet" href="pricing-disclose.css">\n<style>\n/* ' + name + ', phones only */\n@media (max-width:768px){' + css + '}\n</style>\n</head>', 1)
    s = s.replace('</body>', '<script>\n(function(){\n  var D=window.EWD, root=document.getElementById("mp"); if(!D||!root) return; var E=D.E;\n' + js + '\n})();\n</script>\n</body>', 1)
    io.open('elite-wellness-landing_%s.html' % name.replace('.', '-'), 'w', encoding='utf-8').write(s)
    print(name, len(s))

# ------------------------------------------------------------ .4  the steps fold
# One question open at a time. Answer it and it folds to a single line with
# Change, the next opens under it, and the plan appears when the last is answered.
build('2.4.5.4', '''
  .acc{list-style:none;margin:0;padding:0;box-shadow:inset 0 1px 0 var(--black)}
  .acc-step{box-shadow:inset 0 -1px 0 var(--light-grey)}
  .acc-head{appearance:none;border:0;background:transparent;width:100%;display:flex;align-items:center;gap:12px;padding:16px 0;cursor:pointer;font-family:var(--font-body);text-align:left;color:var(--black)}
  .acc-i{flex:0 0 24px;height:24px;border-radius:50%;box-shadow:inset 0 0 0 2px var(--light-grey);font-weight:800;font-size:11px;display:flex;align-items:center;justify-content:center;color:var(--silver-grey)}
  .acc-step.open .acc-i{background:var(--royal-blue);box-shadow:none;color:var(--white)}
  .acc-step.done .acc-i{background:var(--black);box-shadow:none;color:var(--white)}
  .acc-t{flex:1 1 auto;min-width:0}
  .acc-t small{display:block;font-weight:800;font-size:10px;line-height:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--silver-grey)}
  .acc-t b{display:block;font-size:16px;line-height:22px}
  .acc-step.open .acc-t b{font-family:var(--font-display);font-weight:400;font-size:22px;line-height:1.1;text-transform:uppercase}
  .acc-c{font-size:12px;color:var(--royal-blue);text-decoration:underline}
  .acc-body{padding:0 0 20px}
  .m-price .dc-card{margin-top:24px}
''', '''
  var st={who:null,stay:null,plan:null,pack:null,pay:null}, open='who', cur=null;
  function seq(){ var a=['who']; if(st.who){ a.push(D.whoOf(st.who).key); if(st.who==='member') a.push('pay') } return a }
  function val(id){
    if(id==='who') return st.who?D.whoOf(st.who).name:null;
    if(id==='pay') return st.pay?(st.pay==='dd'?'Direct debit':'At the desk'):null;
    var o=D.opts(st.who).filter(function(x){return x.id===st[id]})[0]; return o?o.name:null;
  }
  function ask(id){ return id==='who'?'Who are you?':id==='pay'?'How will you pay?':D.whoOf(st.who).ask }
  function render(){
    var html='<ol class="acc">';
    seq().forEach(function(id,i){
      var v=val(id), on=open===id;
      html+='<li class="acc-step'+(on?' open':'')+(v&&!on?' done':'')+'">'+
        '<button class="acc-head" type="button" data-open="'+id+'" aria-expanded="'+on+'"><span class="acc-i">'+(i+1)+'</span>'+
        '<span class="acc-t">'+(on||!v?'<b>'+ask(id)+'</b>':'<small>'+ask(id).replace('?','')+'</small><b>'+v+'</b>')+'</span>'+
        (v&&!on?'<span class="acc-c">Change</span>':'')+'</button>'+
        (on?'<div class="acc-body">'+D.grid(id,st)+'</div>':'')+'</li>';
    });
    html+='</ol>';
    var done=seq().every(val);
    if(done&&open===null){ cur=D.plan(st); html+=D.card(cur,{lines:true}) } else cur=null;
    root.innerHTML=html;
    D.reveal(root.querySelector(open===null?'.dc-card':'.acc-step.open'));
  }
  root.addEventListener('click',function(e){
    if(e.target.closest('.dc-go')){ if(cur) E.review(cur); return }
    var h=e.target.closest('[data-open]'); if(h){ open=h.dataset.open===open?null:h.dataset.open; render(); return }
    var c=e.target.closest('.rc-chip'); if(!c) return;
    var k=c.dataset.k, v=c.dataset.v;
    if(k==='who'){ if(st.who!==v){ st.stay=st.plan=st.pack=st.pay=null; E.track('pricing_who',{who:v}) } st.who=v }
    else st[k]=v;
    open=null; seq().some(function(id){ if(!val(id)){ open=id; return true } });
    render();
  });
  render();
''')

# ---------------------------------------------------- .5  the answer opens under
# Pick who you are, then tap an option: the plan opens directly beneath the row
# you tapped, so the price is where your thumb already is. Tap it again to close.
build('2.4.5.5', '''
  .ut-leg{margin-top:24px}
''', '''
  var st={who:'visitor',stay:null,plan:null,pack:null,pay:'dd'}, cur=null;
  function render(){
    var w=D.whoOf(st.who), k=w.key, os=D.opts(st.who), idx=-1;
    os.forEach(function(o,i){ if(st[k]===o.id) idx=i });
    root.innerHTML='<p class="m-leg">Who are you</p>'+D.grid('who',st)+'<p class="m-leg ut-leg">'+w.ask+'</p>'+D.grid(k,st);
    cur=null;
    if(idx>-1){
      cur=D.plan(st);
      var g=root.querySelectorAll('.rc-chips')[1], els=g.children;
      var end=(os.length%2===1&&idx===os.length-1) ? idx : Math.min(os.length-1, Math.floor(idx/2)*2+1);
      els[end].insertAdjacentHTML('afterend', D.card(cur,{lines:true, extra: st.who==='member'?D.paySeg(st.pay):''}));
      D.reveal(g.querySelector('.dc-card'));
    }
  }
  root.addEventListener('click',function(e){
    if(e.target.closest('.dc-go')){ if(cur) E.review(cur); return }
    var p=e.target.closest('[data-pay]'); if(p){ st.pay=p.dataset.pay; render(); return }
    var c=e.target.closest('.rc-chip'); if(!c) return;
    var k=c.dataset.k, v=c.dataset.v;
    if(k==='who'){ if(st.who!==v){ st.who=v; st.stay=st.plan=st.pack=null; E.track('pricing_who',{who:v}) } }
    else st[k] = st[k]===v ? null : v;
    render();
  });
  render();
''')

# ------------------------------------------------------ .6  every row has a price
# Each option is a row with its real price on it. Tap one and it opens in place
# with the breakdown and the button. One open at a time.
build('2.4.5.6', '''
  .rw{list-style:none;margin:24px 0 0;padding:0;box-shadow:inset 0 1px 0 var(--black)}
  .rw-i{box-shadow:inset 0 -1px 0 var(--light-grey)}
  .rw-h{appearance:none;border:0;background:transparent;width:100%;display:grid;grid-template-columns:1fr auto 16px;gap:12px;align-items:center;padding:16px 0;cursor:pointer;font-family:var(--font-body);text-align:left;color:var(--black)}
  .rw-h b{display:block;font-size:16px;line-height:22px}
  .rw-h small{display:block;font-size:12px;line-height:16px;color:var(--silver-grey);margin-top:2px}
  .rw-h i{font-style:normal;font-family:var(--font-display);font-size:24px;line-height:1;text-align:right;white-space:nowrap}
  .rw-h i small{font-family:var(--font-body);font-size:10px;line-height:14px;margin-top:4px;text-transform:none}
  .rw-h::after{content:"";width:8px;height:8px;border-right:2px solid var(--silver-grey);border-bottom:2px solid var(--silver-grey);transform:rotate(45deg);margin-top:-4px;transition:transform .2s}
  .rw-i.on .rw-h::after{transform:rotate(225deg);margin-top:4px}
  .rw-i.on .rw-h i{color:var(--royal-blue)}
  .rw-b{padding:0 0 16px}
''', '''
  var st={who:'visitor',stay:null,plan:null,pack:null,pay:'dd'}, cur=null;
  function render(){
    var w=D.whoOf(st.who), k=w.key;
    var html=D.grid('who',st)+'<ul class="rw">';
    cur=null;
    D.opts(st.who).forEach(function(o){
      var s2={who:st.who,stay:st.stay,plan:st.plan,pack:st.pack,pay:st.pay}; s2[k]=o.id;
      var p=D.plan(s2), on=st[k]===o.id;
      if(on) cur=p;
      html+='<li class="rw-i'+(on?' on':'')+'"><button class="rw-h" type="button" data-row="'+o.id+'" aria-expanded="'+on+'">'+
        '<span><b>'+o.name+'</b><small>'+o.sub+'</small></span>'+
        '<i>'+D.money(p.unit)+(p.unitLabel?'<small>'+p.unitLabel+'</small>':'')+'</i></button>'+
        (on?'<div class="rw-b">'+D.card(p,{lines:true, extra: st.who==='member'?D.paySeg(st.pay):''})+'</div>':'')+'</li>';
    });
    root.innerHTML=html+'</ul>';
    if(cur) D.reveal(root.querySelector('.rw-i.on .dc-card'));
  }
  root.addEventListener('click',function(e){
    if(e.target.closest('.dc-go')){ if(cur) E.review(cur); return }
    var p=e.target.closest('[data-pay]'); if(p){ st.pay=p.dataset.pay; render(); return }
    var r=e.target.closest('[data-row]');
    if(r){ var k=D.whoOf(st.who).key; st[k] = st[k]===r.dataset.row ? null : r.dataset.row; render(); return }
    var c=e.target.closest('.rc-chip'); if(!c||c.dataset.k!=='who') return;
    if(st.who!==c.dataset.v){ st.who=c.dataset.v; st.stay=st.plan=st.pack=null; E.track('pricing_who',{who:st.who}) }
    render();
  });
  render();
''')

# -------------------------------------------------------- .7  the receipt is the form
# One card. Each line of it (who, pass, paying) is a folded row showing what is
# chosen; tap a line and it opens into its options, pick one and it folds back.
# The total sits in the same card, so it is always on screen with the choices.
build('2.4.5.7', '''
  .fm{background:var(--black);color:var(--white);padding:8px 20px 24px}
  .fm-row{box-shadow:inset 0 -1px 0 rgba(255,255,255,.18)}
  .fm-h{appearance:none;border:0;background:transparent;color:inherit;width:100%;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:16px 0;cursor:pointer;font-family:var(--font-body);text-align:left}
  .fm-h span{font-weight:800;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.55)}
  .fm-h b{font-size:16px;line-height:22px;display:flex;align-items:center;gap:10px}
  .fm-h b::after{content:"";width:7px;height:7px;border-right:2px solid rgba(255,255,255,.55);border-bottom:2px solid rgba(255,255,255,.55);transform:rotate(45deg);margin-top:-4px;transition:transform .2s}
  .fm-row.open .fm-h b::after{transform:rotate(225deg);margin-top:4px}
  .fm-b{padding:0 0 16px}
  .fm .rc-chip{background:transparent;color:var(--white);border-color:rgba(255,255,255,.25)}
  .fm .rc-chip.on{background:var(--white);color:var(--black);border-color:var(--white)}
  .fm .rc-chip small{opacity:.7}
  .fm-total{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding-top:20px}
  .fm-total span{font-size:12px;color:rgba(255,255,255,.6)}
  .fm-total b{font-family:var(--font-display);font-size:44px;line-height:1;color:var(--accent);white-space:nowrap}
  .fm .btn.dc-go{width:100%;justify-content:center;margin-top:20px}
''', '''
  var st={who:'visitor',stay:'s1',plan:'un',pack:'p8',pay:'dd'}, open=null, cur=null;
  function rows(){
    var w=D.whoOf(st.who), o=D.opts(st.who).filter(function(x){return x.id===st[w.key]})[0];
    var r=[{id:'who',label:'You are',value:w.name},{id:w.key,label:w.label,value:o.name}];
    if(st.who==='member') r.push({id:'pay',label:'Paying',value:st.pay==='dd'?'Direct debit':'At the desk'});
    return r;
  }
  function render(){
    cur=D.plan(st);
    var html='<div class="fm">';
    rows().forEach(function(r){
      var on=open===r.id;
      html+='<div class="fm-row'+(on?' open':'')+'"><button class="fm-h" type="button" data-open="'+r.id+'" aria-expanded="'+on+'"><span>'+r.label+'</span><b>'+r.value+'</b></button>'+
        (on?'<div class="fm-b">'+D.grid(r.id,st)+'</div>':'')+'</div>';
    });
    html+='<div class="fm-total"><span>'+cur.totalLabel+'</span><b>'+D.money(cur.price)+'</b></div>'+
      (cur.notes.length?'<p class="dc-note">'+cur.notes.join(' ')+'</p>':'')+
      '<button class="btn dc-go" type="button">Get this plan</button></div>';
    root.innerHTML=html;
  }
  root.addEventListener('click',function(e){
    if(e.target.closest('.dc-go')){ E.review(cur); return }
    var h=e.target.closest('[data-open]'); if(h){ open=open===h.dataset.open?null:h.dataset.open; render(); return }
    var c=e.target.closest('.rc-chip'); if(!c) return;
    var k=c.dataset.k, v=c.dataset.v;
    if(k==='who'&&st.who!==v) E.track('pricing_who',{who:v});
    st[k]=v; open=null; render();
  });
  render();
''')

# ------------------------------------------------- .8  one answer, more on request
# Pick who you are and one plan is shown, priced and ready. The other options
# stay folded under it until asked for, and choosing one swaps the answer above.
build('2.4.5.8', '''
  .m-price .dc-card{margin-top:24px}
  .mo-t{appearance:none;border:0;background:transparent;width:100%;display:flex;justify-content:space-between;align-items:center;padding:16px 0;margin-top:8px;box-shadow:inset 0 -1px 0 var(--light-grey);cursor:pointer;font-family:var(--font-body);font-weight:800;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--black)}
  .mo-t::after{content:"";width:8px;height:8px;border-right:2px solid var(--black);border-bottom:2px solid var(--black);transform:rotate(45deg);margin-top:-4px;transition:transform .2s}
  .mo-t[aria-expanded=true]::after{transform:rotate(225deg);margin-top:4px}
  .mo-b{padding:16px 0 0}
''', '''
  var FIRST={visitor:'s1',member:'un',pt:'p8'};
  var st={who:'visitor',stay:'s1',plan:'un',pack:'p8',pay:'dd'}, more=false, cur=null;
  function render(){
    var w=D.whoOf(st.who), k=w.key, n=D.opts(st.who).length-1;
    cur=D.plan(st);
    var kick = st.who==='member'&&st.plan==='un' ? 'Recommended' : w.name;
    root.innerHTML = D.grid('who',st) +
      D.card(cur,{kicker:kick, extra: st.who==='member'?D.paySeg(st.pay):''}) +
      '<button class="mo-t" type="button" aria-expanded="'+more+'">'+(more?'Fewer options':'Other '+w.plural+' ('+n+')')+'</button>' +
      (more?'<div class="mo-b">'+D.grid(k,st)+'</div>':'');
  }
  root.addEventListener('click',function(e){
    if(e.target.closest('.dc-go')){ E.review(cur); return }
    if(e.target.closest('.mo-t')){ more=!more; if(more) E.track('pricing_more',{who:st.who}); render(); return }
    var p=e.target.closest('[data-pay]'); if(p){ st.pay=p.dataset.pay; render(); return }
    var c=e.target.closest('.rc-chip'); if(!c) return;
    var k=c.dataset.k, v=c.dataset.v;
    if(k==='who'){ if(st.who!==v){ st.who=v; st[D.whoOf(v).key]=FIRST[v]; more=false; E.track('pricing_who',{who:v}) } }
    else st[k]=v;
    render();
    if(k!=='who') D.reveal(root.querySelector('.dc-card'));
  });
  render();
''')
