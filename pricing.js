/*
  The pricing engine shared by every 2.4.x draft.
  It holds the arithmetic, the two step confirm flow and the tracking hook,
  so the five drafts only differ in how they ask the question.
*/
(function(){
  var P = window.ELITE_PRICES;
  if(!P) return;

  /* ---------- tracking ----------
     Every step of the flow calls this. It does nothing yet on purpose.
     To switch it on, point it at Plausible:
       window.EW_TRACK = function(name, props){ plausible(name, {props:props}) }
     Nothing else in the page changes. */
  function track(name, props){
    if(typeof window.EW_TRACK === 'function'){ try{ window.EW_TRACK(name, props||{}) }catch(e){} }
    if(window.EW_TRACK_DEBUG) console.log('[track]', name, props||{});
  }

  /* ---------- money ---------- */
  function money(n){
    if(n == null) return '';
    var s = (Math.round(n*100)/100).toFixed(2);
    return '€' + (s.slice(-3) === '.00' ? s.slice(0,-3) : s);
  }

  /* ---------- the one pass that covers a stay of n days ----------
     Always one row of the price list, never a multiple of one. Under four days
     there is no bundle worth buying, so the answer is the day pass and a line
     saying you pay it each time you come. */
  function visitorFor(days){
    days = Math.max(1, Math.round(days));
    var one = P.visitor[0];
    if(days < 4) return { item:one, total:one.price, perVisit:true };
    var fit = null;
    P.visitor.forEach(function(v){
      if(v.days >= days && (!fit || v.days < fit.days)) fit = v;
    });
    if(!fit) return null;                       /* longer than four weeks: a member plan */
    return { item:fit, total:fit.price, perVisit:false };
  }

  /* ---------- what a member pays ---------- */
  function memberPlan(id){ return P.member.plans.filter(function(p){ return p.id===id })[0] }
  function memberFirst(plan, dd){
    var rate = dd ? plan.dd : plan.desk;
    return { rate:rate, insurance:P.insurance.year, total:rate + P.insurance.year };
  }
  function memberYear(plan, dd){ return (dd ? plan.dd : plan.desk) * 26 + P.insurance.year }

  /* ---------- the one comparison that decides the sale ----------
     Four weeks as a visitor against four weeks as a member. */
  function fourWeeks(){
    var v = P.visitor[P.visitor.length-1];
    var m = memberPlan('un');
    return { visitor:v.price, member:m.dd*2 + P.insurance.year, plan:m };
  }

  /* ---------- the flow: review, then a plain confirmation ---------- */
  var root = null;
  function el(tag, cls, html){ var e=document.createElement(tag); if(cls) e.className=cls; if(html!=null) e.innerHTML=html; return e }

  function build(){
    if(root) return root;
    root = el('div','ewf');
    root.setAttribute('role','dialog');
    root.setAttribute('aria-modal','true');
    root.setAttribute('aria-label','Your plan');
    root.innerHTML = '<div class="ewf-sheet"><button class="ewf-x" type="button" aria-label="Close">×</button><div class="ewf-body"></div></div>';
    root.addEventListener('click', function(e){ if(e.target===root) close('backdrop') });
    root.querySelector('.ewf-x').addEventListener('click', function(){ close('button') });
    document.body.appendChild(root);
    return root;
  }
  function open(){
    build().classList.add('on');
    document.documentElement.style.overflow='hidden';
    document.addEventListener('keydown', esc);
  }
  function close(how){
    if(!root) return;
    root.classList.remove('on');
    document.documentElement.style.overflow='';
    document.removeEventListener('keydown', esc);
    track('pricing_close', { how:how||'', step:root.dataset.step||'' });
  }
  function esc(e){ if(e.key==='Escape') close('escape') }

  /* a choice looks like:
     { kind:'visitor'|'member'|'pt', title, price, lines:[[label, value]], notes:[], id } */
  function review(choice){
    var b = build().querySelector('.ewf-body');
    root.dataset.step='review';
    var lines = choice.lines.map(function(l){
      return '<div class="ewf-line"><span>'+l[0]+'</span><b>'+l[1]+'</b></div>';
    }).join('');
    var notes = (choice.notes||[]).map(function(n){ return '<p class="ewf-note">'+n+'</p>' }).join('');
    b.innerHTML =
      '<p class="ewf-kicker">Your plan</p>'+
      '<h3 class="ewf-title">'+choice.title+'</h3>'+
      '<div class="ewf-lines">'+lines+'</div>'+
      '<div class="ewf-total"><span>'+(choice.totalLabel||'To pay on your first visit')+'</span><b>'+money(choice.price)+'</b></div>'+
      notes+
      '<div class="ewf-inc"><p class="ewf-inc-h">Included</p><ul>'+P.includes.map(function(i){return '<li>'+i+'</li>'}).join('')+'</ul></div>'+
      '<button class="btn ewf-go" type="button">Get this plan</button>'+
      '<button class="ewf-back" type="button">Pick something else</button>';
    b.querySelector('.ewf-go').addEventListener('click', function(){ done(choice) });
    b.querySelector('.ewf-back').addEventListener('click', function(){ close('back') });
    open();
    track('pricing_review', { plan:choice.id, price:choice.price });
  }

  function done(choice){
    var b = root.querySelector('.ewf-body');
    root.dataset.step='done';
    b.innerHTML =
      '<p class="ewf-kicker">Almost there</p>'+
      '<h3 class="ewf-title">Come by and we will set it up</h3>'+
      '<p class="ewf-lede">We cannot take payment online yet, so the last step happens at the desk. It takes about five minutes.</p>'+
      '<div class="ewf-lines">'+
        '<div class="ewf-line"><span>What you chose</span><b>'+choice.title+'</b></div>'+
        '<div class="ewf-line"><span>To pay at the desk</span><b>'+money(choice.price)+'</b></div>'+
      '</div>'+
      '<p class="ewf-inc-h">Bring</p>'+
      '<ul class="ewf-bring"><li>Something to pay with</li><li>A towel and a water bottle</li><li>Photo ID if you are joining as a member</li></ul>'+
      '<div class="ewf-acts">'+
        '<a class="btn" href="https://maps.app.goo.gl/ks6o4URGCYT7rzHJ8" target="_blank" rel="noopener">Get directions</a>'+
        '<a class="btn ghost" href="https://wa.me/351926565836?text=Hi%21%20I%20have%20a%20question%20about%20'+encodeURIComponent(choice.title)+'." target="_blank" rel="noopener">Ask a question</a>'+
      '</div>'+
      '<p class="ewf-note" data-status="flow-status"></p>';
    if(window.EW_WRITE_STATUS) window.EW_WRITE_STATUS();
    track('pricing_confirm', { plan:choice.id, price:choice.price });
  }

  window.EWPricing = {
    P:P, money:money, track:track,
    visitorFor:visitorFor, memberPlan:memberPlan, memberFirst:memberFirst,
    memberYear:memberYear, fourWeeks:fourWeeks,
    review:review, close:close
  };
})();
