# -*- coding: utf-8 -*-
"""2.4.5.4.1: the folding steps of 2.4.5.4 on every screen size, with the real
product names (Passes, Membership, Personal training) and a switch for members
whose sports insurance is already paid. Built on the committed 2.4.5: its
desktop receipt is hidden and one inline builder serves both widths."""
import io

BASE = io.open('elite-wellness-landing_2-4-5.html', encoding='utf-8').read()
def one(s, old, new):
    assert s.count(old) == 1, old[:60]
    return s.replace(old, new)

CSS = '''
/* 2.4.5.4.2: one inline builder for every width; the 2.4.5 receipt stands down */
#prices .rc{display:none}
#mp{max-width:760px;margin:0 auto}
.acc{list-style:none;margin:0;padding:0;box-shadow:inset 0 1px 0 var(--black)}
.acc-step{box-shadow:inset 0 -1px 0 var(--light-grey)}
.acc-head{appearance:none;border:0;background:transparent;width:100%;display:flex;align-items:center;gap:16px;padding:20px 0;cursor:pointer;font-family:var(--font-body);text-align:left;color:var(--black)}
.acc-i{flex:0 0 28px;height:28px;border-radius:50%;box-shadow:inset 0 0 0 2px var(--light-grey);font-weight:800;font-size:12px;display:flex;align-items:center;justify-content:center;color:var(--silver-grey)}
.acc-step.open .acc-i{background:var(--royal-blue);box-shadow:none;color:var(--white)}
.acc-step.done .acc-i{background:var(--black);box-shadow:none;color:var(--white)}
.acc-t{flex:1 1 auto;min-width:0}
.acc-t small{display:block;font-weight:800;font-size:10px;line-height:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--silver-grey)}
.acc-t b{display:block;font-size:17px;line-height:24px}
.acc-step.open .acc-t b{font-family:var(--font-display);font-weight:400;font-size:28px;line-height:1.1;text-transform:uppercase}
.acc-c{font-size:13px;color:var(--royal-blue);text-decoration:underline}
.acc-body{padding:0 0 24px 44px}
.acc-head:focus-visible,.st-opt:focus-visible{outline:2px solid var(--royal-blue);outline-offset:2px}

.st-grid{display:grid;gap:8px}
.st-grid.kind{grid-template-columns:repeat(3,1fr)}
.st-grid.stay{grid-template-columns:repeat(5,1fr)}
.st-grid.plan{grid-template-columns:repeat(3,1fr)}
.st-grid.pay{grid-template-columns:repeat(2,1fr)}
.st-grid.pack{grid-template-columns:repeat(4,1fr)}
.st-grid .rc-chip{min-height:64px}
.st-opt{appearance:none;border:2px solid var(--light-grey);background:var(--white);text-align:left;padding:20px;cursor:pointer;font-family:var(--font-body);color:var(--black);display:flex;flex-direction:column;gap:6px;transition:border-color .15s}
.st-opt:hover{border-color:var(--black)}
.st-opt b{font-family:var(--font-display);font-weight:400;font-size:24px;line-height:1;text-transform:uppercase}
.st-opt span{font-size:13px;line-height:19px;color:#4a4a4a}
.st-opt i{font-style:normal;font-weight:800;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--royal-blue);margin-top:auto;padding-top:6px}
.st-hint{font-size:13px;line-height:20px;color:var(--silver-grey);margin:0 0 12px}
.rc-chip .tag{display:inline-block;background:var(--accent);color:var(--black);font-weight:800;font-size:9px;letter-spacing:.1em;text-transform:uppercase;padding:2px 5px;margin-top:4px;opacity:1}
.rc-chip.on .tag{background:var(--white)}

.dc-card{background:var(--black);color:var(--white);padding:28px 28px 24px;margin-top:32px;scroll-margin-top:90px;scroll-margin-bottom:96px;animation:dcIn .22s ease both}
.dc-head{display:flex;justify-content:space-between;align-items:baseline;gap:16px}
.dc-n{font-size:18px;line-height:24px;font-weight:700;min-width:0}
.dc-p{font-family:var(--font-display);font-size:48px;line-height:1;color:var(--accent);white-space:nowrap}
.dc-l{font-size:12px;line-height:16px;color:rgba(255,255,255,.55);margin-top:4px}
.dc-lines{margin-top:16px}
.dc-line{display:flex;justify-content:space-between;gap:16px;padding:10px 0;box-shadow:inset 0 -1px 0 rgba(255,255,255,.18);font-size:14px;line-height:20px}
.dc-line b{font-weight:700;white-space:nowrap}
.dc-note{font-size:12px;line-height:18px;color:rgba(255,255,255,.6);margin-top:12px}
.ins{display:flex;align-items:center;gap:12px;margin-top:16px;cursor:pointer;font-size:13px;line-height:18px;color:rgba(255,255,255,.85)}
.ins input{appearance:none;flex:0 0 40px;width:40px;height:24px;border-radius:12px;background:rgba(255,255,255,.25);position:relative;cursor:pointer;margin:0;transition:background .15s}
.ins input::after{content:"";position:absolute;top:3px;left:3px;width:18px;height:18px;border-radius:50%;background:var(--white);transition:transform .15s}
.ins input:checked{background:var(--royal-blue)}
.ins input:checked::after{transform:translateX(16px)}
.ins input:focus-visible{outline:2px solid var(--white);outline-offset:2px}
.dc-card .btn.dc-go{width:100%;justify-content:center;margin-top:20px}
@keyframes dcIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){ .dc-card{animation:none} }

@media (max-width:768px){
  .acc-head{padding:16px 0;gap:12px}
  .acc-i{flex-basis:24px;height:24px;font-size:11px}
  .acc-t b{font-size:16px;line-height:22px}
  .acc-step.open .acc-t b{font-size:22px}
  .acc-body{padding:0 0 20px}
  .st-grid.kind{grid-template-columns:1fr}
  .st-grid.stay,.st-grid.plan,.st-grid.pack{grid-template-columns:repeat(2,1fr)}
  .st-grid .rc-chip.span{grid-column:1 / -1}
  .st-grid .rc-chip{min-height:56px}
  .st-opt{padding:16px}
  .st-opt b{font-size:20px}
  .dc-card{padding:24px 20px;margin-top:24px;scroll-margin-top:64px}
  .dc-p{font-size:40px}
}
'''

JS = '''
(function(){
  var E=window.EWPricing, root=document.getElementById('mp'); if(!E||!root) return;
  var P=E.P, money=E.money, reduce=window.matchMedia('(prefers-reduced-motion:reduce)');
  function find(list,id){ return list.filter(function(x){return x.id===id})[0] }

  /* the three products, named as the gym sells them */
  var KINDS=[
    {id:'pass', name:'Day and week passes', desc:'No commitment. From one day to four weeks.',            from:'From '+money(P.visitor[0].price)},
    {id:'mem',  name:'Membership',        desc:'Paid every 2 weeks. The best value if you train here often.', from:'From '+money(P.member.plans[0].dd)+' every 2 weeks with direct debit'},
    {id:'pt',   name:'Personal training', desc:'One to one with a coach.',                                 from:'From '+money(P.pt.packs[P.pt.packs.length-1].each)+' a session'}
  ];
  var ASK={kind:'Choose a pass or membership',stay:'Choose a pass',plan:'How often will you train?',pay:'How will you pay?',pack:'How many sessions?'};
  var SHORT={kind:'Option',stay:'Pass',plan:'Training',pay:'Payment',pack:'Sessions'};

  var st={kind:null,stay:null,plan:null,pay:null,pack:null,insured:false}, open='kind', cur=null;

  function seq(){ var a=['kind']; if(st.kind==='pass') a.push('stay'); if(st.kind==='mem') a.push('plan','pay'); if(st.kind==='pt') a.push('pack'); return a }
  function val(id){
    if(id==='kind') return st.kind?find(KINDS,st.kind).name:null;
    if(id==='stay') return st.stay?find(P.visitor,st.stay).name:null;
    if(id==='plan') return st.plan?E.memberPlan(st.plan).name:null;
    if(id==='pay')  return st.pay?(st.pay==='dd'?'Direct debit':'At reception'):null;
    if(id==='pack') return st.pack?find(P.pt.packs,st.pack).name:null;
  }

  function chip(k,v,name,small,on,span,tag){
    return '<button class="rc-chip'+(on?' on':'')+(span?' span':'')+'" type="button" data-k="'+k+'" data-v="'+v+'" aria-pressed="'+on+'">'+
      name+(small?'<small>'+small+'</small>':'')+(tag?'<span class="tag">'+tag+'</span>':'')+'</button>';
  }
  function options(id){
    if(id==='kind') return '<div class="st-grid kind">'+KINDS.map(function(k){
      return '<button class="st-opt" type="button" data-k="kind" data-v="'+k.id+'" aria-pressed="'+(st.kind===k.id)+'"><b>'+k.name+'</b><span>'+k.desc+'</span><i>'+k.from+'</i></button>';
    }).join('')+'</div>';
    if(id==='stay') return '<div class="st-grid stay">'+P.visitor.map(function(v,i){ return chip('stay',v.id,v.name,money(v.price),st.stay===v.id,i===P.visitor.length-1) }).join('')+'</div>';
    if(id==='plan') return '<p class="st-hint">Prices every 2 weeks. Direct debit takes '+money(P.member.plans[0].desk-P.member.plans[0].dd)+' off each payment.</p>'+
      '<div class="st-grid plan">'+P.member.plans.map(function(p,i){ return chip('plan',p.id,p.name,money(p.desk)+' / 2 wks',st.plan===p.id,i===P.member.plans.length-1,p.best?'Recommended':'') }).join('')+'</div>';
    if(id==='pay'){ var p=E.memberPlan(st.plan||'un'), off=money(p.desk-p.dd);
      return '<div class="st-grid pay">'+chip('pay','dd','Direct debit',money(p.dd)+' every 2 weeks, '+off+' off',st.pay==='dd')+chip('pay','desk','At reception',money(p.desk)+' every 2 weeks',st.pay==='desk')+'</div>' }
    if(id==='pack') return '<div class="st-grid pack">'+P.pt.packs.map(function(k){ return chip('pack',k.id,k.name,money(k.total)+(k.sessions>1?', '+money(k.each)+' each':''),st.pack===k.id) }).join('')+'</div>';
  }

  function plan(){
    var lines=[], notes=[], total, title, id, label;
    if(st.kind==='pass'){
      var v=find(P.visitor,st.stay);
      title=(v.days===1?'Day pass':v.name+' pass'); id=v.id; total=v.price; label='To pay at reception';
      lines=[[title,money(v.price)],['Sports insurance','Included']];
      if(v.days<4) notes.push('Paid each time you come. From four days on, the week pass costs less.');
      if(v.days>=28) notes.push('Four weeks of membership is '+money(E.fourWeeks().member)+' with the insurance, and it keeps going after four weeks.');
    } else if(st.kind==='mem'){
      var p=E.memberPlan(st.plan), dd=st.pay!=='desk', rate=dd?p.dd:p.desk;
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
      if(k.sessions>1) lines.push([money(k.each)+' a session, valid '+k.months+' months','']);
      notes.push('Bring someone with you and the second person is '+money(P.pt.second)+' a session.');
      if(k.sessions>1) notes.push(P.pt.note);
    }
    return {id:id,title:title,price:total,totalLabel:label,lines:lines.filter(function(l){return l[1]!==''}),detail:lines,notes:notes};
  }

  function card(p){
    return '<div class="dc-card">'+
      '<div class="dc-head"><span class="dc-n">'+p.title+'</span><b class="dc-p">'+money(p.price)+'</b></div>'+
      '<p class="dc-l">'+p.totalLabel+'</p>'+
      '<div class="dc-lines">'+p.detail.map(function(l){ return '<div class="dc-line"><span>'+l[0]+'</span><b>'+l[1]+'</b></div>' }).join('')+'</div>'+
      (st.kind==='mem'?'<label class="ins"><input type="checkbox" data-ins'+(st.insured?' checked':'')+'><span>My sports insurance is already paid this year</span></label>':'')+
      (p.notes.length?'<p class="dc-note">'+p.notes.join(' ')+'</p>':'')+
      '<button class="btn dc-go" type="button">Get this plan</button></div>';
  }

  function reveal(el){
    if(!el) return;
    var r=el.getBoundingClientRect(), top=window.innerWidth>768?80:56;
    if(r.top<top||r.bottom>window.innerHeight-88) el.scrollIntoView({block:'nearest',behavior:reduce.matches?'auto':'smooth'});
  }

  function render(focus){
    var html='<ol class="acc">';
    seq().forEach(function(id,i){
      var v=val(id), on=open===id;
      html+='<li class="acc-step'+(on?' open':'')+(v&&!on?' done':'')+'">'+
        '<button class="acc-head" type="button" data-open="'+id+'" aria-expanded="'+on+'"><span class="acc-i">'+(i+1)+'</span>'+
        '<span class="acc-t">'+(on||!v?'<b>'+ASK[id]+'</b>':'<small>'+SHORT[id]+'</small><b>'+v+'</b>')+'</span>'+
        (v&&!on?'<span class="acc-c">Change</span>':'')+'</button>'+
        (on?'<div class="acc-body">'+options(id)+'</div>':'')+'</li>';
    });
    html+='</ol>';
    cur=null;
    if(open===null&&seq().every(val)){ cur=plan(); html+=card(cur) }
    root.innerHTML=html;
    if(focus!==false) reveal(root.querySelector(open===null?'.dc-card':'.acc-step.open'));
  }

  root.addEventListener('click',function(e){
    if(e.target.closest('.dc-go')){ if(cur) E.review(cur); return }
    var h=e.target.closest('[data-open]'); if(h){ open=h.dataset.open===open?null:h.dataset.open; render(); return }
    var c=e.target.closest('[data-k]'); if(!c) return;
    var k=c.dataset.k, v=c.dataset.v;
    if(k==='kind'){ if(st.kind!==v){ st.stay=st.plan=st.pay=st.pack=null; E.track('pricing_kind',{kind:v}) } st.kind=v }
    else st[k]=v;
    open=null; seq().some(function(id){ if(!val(id)){ open=id; return true } });
    render();
  });
  root.addEventListener('change',function(e){
    if(!e.target.matches('[data-ins]')) return;
    st.insured=e.target.checked; E.track('pricing_insured',{insured:st.insured});
    render(false);
    var box=root.querySelector('[data-ins]'); if(box) box.focus();
  });
  render(false);
})();
'''

s = BASE
s = one(s, 'Walk in and pay at the desk.</p>', 'Walk in and pay at reception.</p>')
s = one(s, 'Free parking outside. Pay at the reception or by direct debit.', 'Free parking outside. Pay at reception or by direct debit.')
s = one(s, '<span class="section-script">build it and see</span>', '<span class="section-script">a few taps, one price</span>')
s = one(s, 'All prices include VAT. Member plans are paid every 2 weeks by direct debit or at the desk. Visitor passes include the sports insurance; member plans add it once a year at €24.',
           'All prices include VAT. Day and week passes include the sports insurance. Membership is paid every 2 weeks, by direct debit or at reception, and adds the €24 insurance once a year.')
s = one(s, '<p class="pr-legal">', '<div id="mp"></div>\n  <p class="pr-legal">')
s = s.replace('</head>', '<style>' + CSS + '</style>\n</head>', 1)
s = s.replace('</body>', '<script>' + JS + '</script>\n</body>', 1)
io.open('elite-wellness-landing_2-4-5-4-2.html', 'w', encoding='utf-8').write(s)
print('2.4.5.4.2', len(s))
