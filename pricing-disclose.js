/*
  Shared by 2.4.5.4 to 2.4.5.8: phone versions of the price builder that keep
  everything inline, revealing a little at a time. No bar, strip or sheet until
  someone presses Get this plan. The arithmetic lives here once; each draft only
  decides how much to show and when.
*/
(function(){
  var E=window.EWPricing; if(!E) return;
  var P=E.P, money=E.money;
  var reduce=window.matchMedia('(prefers-reduced-motion:reduce)');

  var WHO=[
    {id:'visitor', name:'Visiting',     ask:'How long are you here?',   key:'stay', label:'Pass', plural:'passes'},
    {id:'member',  name:'Living here',  ask:'How often will you train?', key:'plan', label:'Plan', plural:'plans'},
    {id:'pt',      name:'With a coach', ask:'Which pack?',               key:'pack', label:'Pack', plural:'packs'}
  ];
  function whoOf(id){ return WHO.filter(function(w){return w.id===id})[0] }

  function opts(who){
    if(who==='visitor') return P.visitor.map(function(v){ return {id:v.id,name:v.name,price:money(v.price),sub:'Insurance included'} });
    if(who==='member')  return P.member.plans.map(function(p){ return {id:p.id,name:p.name,price:money(p.dd),sub:'Plus '+money(P.insurance.year)+' insurance once a year'} });
    return P.pt.packs.map(function(k){ return {id:k.id,name:k.name,price:money(k.total),sub:k.sessions>1?money(k.each)+' a session, valid '+k.months+' months':'One session with a coach'} });
  }

  /* one plan from one state; the same numbers as the desktop receipt */
  function plan(st){
    var lines=[], notes=[], total=0, unit, unitLabel='', title, id, label;
    if(st.who==='visitor'){
      var v=P.visitor.filter(function(x){return x.id===st.stay})[0];
      lines=[[v.name+' visitor pass',money(v.price)],['Sports insurance','Included']];
      total=unit=v.price; title=v.name+' visitor pass'; id=v.id; label='To pay at the desk';
      if(v.days<4) notes.push('Paid each time you come. From four days on, the week pass costs less.');
      if(v.days>=28) notes.push('Four weeks as a member is '+money(E.fourWeeks().member)+' and it does not stop after four weeks.');
    } else if(st.who==='member'){
      var p=E.memberPlan(st.plan), dd=st.pay!=='desk', rate=dd?p.dd:p.desk;
      lines=[[p.name+', first 2 weeks',money(rate)],['Sports insurance, once a year',money(P.insurance.year)]];
      total=rate+P.insurance.year; unit=rate; unitLabel='every 2 weeks'; title=p.name+' member plan'; id=p.id; label='To pay on your first visit';
      notes.push('Then '+money(rate)+' every 2 weeks. '+(dd ? 'Direct debit saves you '+money(P.member.ddSavingYear)+' a year against paying at the desk.'
                                                          : 'Direct debit would save you '+money(P.member.ddSavingYear)+' a year.'));
    } else {
      var k=P.pt.packs.filter(function(x){return x.id===st.pack})[0];
      lines=[[k.name+' with a coach',money(k.total)]];
      total=unit=k.total; title=k.name+' with a coach'; id=k.id; label='To pay at the desk';
      notes.push('Bring someone with you and the second person is '+money(P.pt.second)+' a session.');
      if(k.sessions>1) notes.push(P.pt.note);
    }
    return {id:id,title:title,price:total,unit:unit,unitLabel:unitLabel,totalLabel:label,lines:lines,notes:notes};
  }

  function chip(k,v,name,small,on,span){
    return '<button class="rc-chip'+(on?' on':'')+(span?' span':'')+'" type="button" data-k="'+k+'" data-v="'+v+'" aria-pressed="'+(on?'true':'false')+'">'+
           name+(small?'<small>'+small+'</small>':'')+'</button>';
  }
  /* the options for one question, as an even grid */
  function grid(k, st){
    if(k==='who') return '<div class="rc-chips g3">'+WHO.map(function(w){ return chip('who',w.id,w.name,'',st.who===w.id) }).join('')+'</div>';
    if(k==='pay'){
      var p=E.memberPlan(st.plan||'un');
      return '<div class="rc-chips">'+chip('pay','dd','Direct debit','saves '+money(P.member.ddSavingYear)+' a year',st.pay!=='desk')+
                                      chip('pay','desk','At the desk',money(p.desk-p.dd)+' more every 2 weeks',st.pay==='desk')+'</div>';
    }
    var os=opts(st.who), odd=os.length%2===1;
    return '<div class="rc-chips">'+os.map(function(o,i){
      return chip(k,o.id,o.name,o.price+(st.who==='member'?' / 2 wks':''),st[k]===o.id,odd&&i===os.length-1);
    }).join('')+'</div>';
  }
  function paySeg(pay){
    return '<div class="dc-seg" role="group" aria-label="How you pay">'+
      '<button type="button" data-pay="dd" class="'+(pay!=='desk'?'on':'')+'">Direct debit</button>'+
      '<button type="button" data-pay="desk" class="'+(pay==='desk'?'on':'')+'">At the desk</button></div>';
  }
  function card(p, o){
    o=o||{};
    return '<div class="dc-card">'+
      (o.kicker?'<p class="dc-k">'+o.kicker+'</p>':'')+
      '<div class="dc-head"><span class="dc-n">'+p.title+'</span><b class="dc-p">'+money(p.price)+'</b></div>'+
      '<p class="dc-l">'+p.totalLabel+'</p>'+
      (o.extra||'')+
      (o.lines?'<div class="dc-lines">'+p.lines.map(function(l){ return '<div class="dc-line"><span>'+l[0]+'</span><b>'+l[1]+'</b></div>' }).join('')+'</div>':'')+
      (p.notes.length?'<p class="dc-note">'+p.notes.join(' ')+'</p>':'')+
      '<button class="btn dc-go" type="button">Get this plan</button></div>';
  }
  /* bring something into view only if it is not already, and never under the bar */
  function reveal(el){
    if(!el) return;
    var r=el.getBoundingClientRect();
    if(r.top<56 || r.bottom>window.innerHeight-88) el.scrollIntoView({block:'nearest',behavior:reduce.matches?'auto':'smooth'});
  }

  window.EWD={E:E,P:P,money:money,WHO:WHO,whoOf:whoOf,opts:opts,plan:plan,chip:chip,grid:grid,paySeg:paySeg,card:card,reveal:reveal};
})();
