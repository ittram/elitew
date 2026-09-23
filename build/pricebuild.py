# -*- coding: utf-8 -*-
"""Builds drafts 2.4.1 to 2.4.5 from 2.3, swapping the Prices section for five
different pricing treatments. Everything else on the page stays identical."""
import io, re, sys, os

SRC = 'elite-wellness-landing_2-3.html'
s0 = io.open(SRC, encoding='utf-8').read()

# ---------------------------------------------------------------- shared fixes
def shared(s):
    def one(old, new):
        assert s_count(old) == 1, 'not unique: ' + old[:70]
        return old, new
    def s_count(x): return s.count(x)

    reps = [
        # the page said monthly, the list is per two weeks, and there is no cash only rule
        ('Day pass €10, week pass €35.90, monthly from €21.',
         'Day pass €10, week pass €35.90, member plans from €13 a fortnight.'),
        ('"priceRange":"€10 to €35.90"', '"priceRange":"€10 to €69"'),
        ('<span class="ms">Day pass €10 · Monthly €21</span>',
         '<span class="ms">Day pass €10 · Members from €13</span>'),
        ('<p class="find-note">Free parking outside. Cash only at the reception.</p>',
         '<p class="find-note">Free parking outside. Pay at the reception or by direct debit.</p>'),
        ('<p>Yes. A day pass is €10 and a week pass is €35.90. Walk in and pay at the desk. Cash only.</p>',
         '<p>Yes. A day pass is €10 and a week pass is €35.90, insurance included. Walk in and pay at the desk.</p>'),
        ("<p>Not for day or week passes. The monthly membership (€21 a month) has a 3 month minimum, and there's a yearly insurance of €24, billed separately. <a href=\"https://wa.me/351926565836?text=Hi!%20I%27d%20like%20to%20ask%20about%20a%20monthly%20membership.\" target=\"_blank\" rel=\"noopener\">Ask us on WhatsApp</a>.</p>",
         "<p>Not for visitor passes. Member plans are paid every 2 weeks, from €13, plus the €24 sports insurance once a year. <sup class=\"pr-todo\" title=\"[PLACEHOLDER: confirm whether the direct debit price needs a minimum period, e.g. 'no minimum, cancel any time']\">todo</sup> <a href=\"https://wa.me/351926565836?text=Hi!%20I%27d%20like%20to%20ask%20about%20a%20member%20plan.\" target=\"_blank\" rel=\"noopener\">Ask us on WhatsApp</a>.</p>"),
    ]
    for old, new in reps:
        assert s.count(old) == 1, 'shared fix not unique: ' + old[:60]
        s = s.replace(old, new)

    # the pricing engine
    s = s.replace('</head>',
        '<link rel="stylesheet" href="pricing.css">\n</head>', 1)
    s = s.replace('<script src="reviews.js"></script>',
        '<script src="prices.js"></script>\n<script src="pricing.js"></script>\n<script src="reviews.js"></script>', 1)
    return s

# ------------------------------------------------------------- section surgery
START = '<!-- ============ PRICES ============ -->'
END   = '\n<!-- ============ REVIEWS'
def swap(s, section, css, js):
    i = s.index(START); j = s.index(END, i)
    s = s[:i] + section.strip() + '\n' + s[j:]
    s = s.replace('</head>', '<style>\n' + css.strip() + '\n</style>\n</head>', 1)
    s = s.replace('</body>', '<script>\n' + js.strip() + '\n</script>\n</body>', 1)
    return s

KICKER = '''<!-- ============ PRICES ============ -->
<section class="section" id="prices">
  <div class="section-kicker">
    <h2 class="section-header">Prices</h2>
    <span class="section-script">%s</span>
  </div>
'''

LEGAL = '''  <p class="pr-legal">All prices include VAT. Member plans are paid every 2 weeks by direct debit or at the desk. Visitor passes include the sports insurance; member plans add it once a year at €24.<span class="pr-todo" title="[PLACEHOLDER: confirm whether the direct debit price needs a minimum period, e.g. 'no minimum, cancel any time']">todo</span></p>
</section>'''

INCLUDED = '''  <div class="pr-inc">
    <div><p><b>Included</b>The gym floor, every group class and the outdoor deck. Your first visit comes with a fitness assessment.</p></div>
    <div><p><b>Paying</b>No booking. Pay at the desk, or set up direct debit for a member plan and save €130 a year.</p></div>
    <div><p><b>Bring</b>Your own towel, water and trainers. Towels and locks are for sale at reception.</p></div>
  </div>
'''

# The whole list as plain HTML. It is in the source of every draft, so the
# prices are readable without JavaScript and search engines can see them.
ALLPRICES = '''  <div class="pr-all" id="pr-all">
    <div class="pr-block">
      <h3 class="pr-h">Visiting</h3>
      <p class="pr-sub">Insurance, the gym and every class included.</p>
      <table class="pr-table">
        <tr><th scope="row">1 day</th><td>€10</td></tr>
        <tr><th scope="row">1 week</th><td>€35.90</td></tr>
        <tr><th scope="row">2 weeks</th><td>€45.90</td></tr>
        <tr><th scope="row">3 weeks</th><td>€51.90</td></tr>
        <tr><th scope="row">4 weeks</th><td>€61.90<span class="pr-todo" title="[PLACEHOLDER: the price list review proposes €69.90 so that four weeks as a member is cheaper. Current price shown until the family decides]">todo</span></td></tr>
      </table>
    </div>
    <div class="pr-block">
      <h3 class="pr-h">Living here</h3>
      <p class="pr-sub">Paid every 2 weeks. Insurance €24 once a year.</p>
      <table class="pr-table pr-two">
        <tr><td></td><th scope="col">Direct debit</th><th scope="col">At the desk</th></tr>
        <tr><th scope="row">Once a week</th><td>€13</td><td class="dim">€18</td></tr>
        <tr><th scope="row">Three a week</th><td>€19.50</td><td class="dim">€24.50</td></tr>
        <tr><th scope="row">Unlimited</th><td>€21</td><td class="dim">€26</td></tr>
      </table>
    </div>
    <div class="pr-block">
      <h3 class="pr-h">With a coach</h3>
      <p class="pr-sub">One to one, or two of you together for €15 more a session.</p>
      <table class="pr-table pr-two">
        <tr><td></td><th scope="col">Each</th><th scope="col">Total</th></tr>
        <tr><th scope="row">Single session</th><td class="dim">€50</td><td>€50</td></tr>
        <tr><th scope="row">8 sessions</th><td class="dim">€45</td><td>€360</td></tr>
        <tr><th scope="row">12 sessions</th><td class="dim">€40</td><td>€480</td></tr>
        <tr><th scope="row">20 sessions</th><td class="dim">€30</td><td>€600</td></tr>
      </table>
    </div>
  </div>
'''

ALLCSS = '''
.pr-all{display:grid;grid-template-columns:repeat(3,1fr);gap:64px;margin-top:64px}
.pr-h{font-family:var(--font-display);font-size:24px;line-height:1;text-transform:uppercase;margin-bottom:4px}
.pr-sub{font-size:13px;line-height:20px;color:var(--silver-grey);margin-bottom:16px}
.pr-table{width:100%;border-collapse:collapse;font-size:15px;line-height:24px}
.pr-table th,.pr-table td{padding:8px 0;text-align:right;box-shadow:inset 0 -1px 0 var(--light-grey);font-weight:700}
.pr-table th[scope=row]{text-align:left;font-weight:400}
.pr-table th[scope=col]{font-weight:800;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--silver-grey)}
.pr-table .dim{color:var(--silver-grey);font-weight:400}
.pr-toggle{appearance:none;border:0;background:transparent;font-family:var(--font-body);font-weight:800;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--black);cursor:pointer;padding:16px 0;margin-top:32px;box-shadow:inset 0 1px 0 var(--light-grey);width:100%;text-align:left}
.pr-toggle::after{content:" +";color:var(--royal-blue)}
.pr-toggle[aria-expanded=true]::after{content:" \\2212";color:var(--royal-blue)}
.js .pr-all[hidden]{display:none}
@media (max-width:768px){ .pr-all{grid-template-columns:1fr;gap:48px;margin-top:48px} }
'''

# ============================================================ 2.4.1 two questions
V1_SEC = (KICKER % 'two questions, one answer') + '''  <div class="q" id="q">
    <div class="q-step" data-step="1">
      <p class="q-ask">Are you visiting, or do you live here?</p>
      <div class="q-opts">
        <button class="q-opt" type="button" data-who="visitor"><b>Visiting</b><span>A few days or a few weeks in Lagos</span></button>
        <button class="q-opt" type="button" data-who="member"><b>Living here</b><span>Staying for a season or for good</span></button>
      </div>
    </div>
    <div class="q-step" data-step="2" hidden>
      <p class="q-ask" id="q-ask2"></p>
      <div class="q-opts" id="q-opts2"></div>
      <button class="q-restart" type="button">Start again</button>
    </div>
    <div class="q-step" data-step="3" hidden>
      <div class="q-answer" id="q-answer"></div>
      <button class="q-restart" type="button">Start again</button>
    </div>
  </div>
  <button class="pr-toggle" type="button" id="pr-toggle" aria-expanded="false" aria-controls="pr-all">See every price</button>
''' + ALLPRICES + LEGAL

V1_CSS = ALLCSS + '''
.q{max-width:720px;margin:0 auto}
.q-ask{font-family:var(--font-display);font-size:clamp(28px,4vw,44px);line-height:1.05;text-transform:uppercase;text-align:center;margin-bottom:32px}
.q-opts{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.q-opts.many{grid-template-columns:repeat(3,1fr)}
.q-opt{appearance:none;border:2px solid var(--light-grey);background:var(--white);text-align:left;padding:24px;cursor:pointer;font-family:var(--font-body);transition:border-color .2s,transform .2s}
.q-opt:hover,.q-opt:focus-visible{border-color:var(--royal-blue);transform:translateY(-4px)}
.q-opt b{display:block;font-family:var(--font-display);font-size:22px;line-height:1;text-transform:uppercase;margin-bottom:8px}
.q-opt span{display:block;font-size:13px;line-height:20px;color:var(--silver-grey)}
.q-restart{display:block;margin:32px auto 0;appearance:none;border:0;background:transparent;font-family:var(--font-body);font-size:13px;color:var(--silver-grey);text-decoration:underline;cursor:pointer}
.q-answer{border:2px solid var(--royal-blue);padding:40px 32px;text-align:center}
.q-answer .qa-k{font-weight:800;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey);margin-bottom:8px}
.q-answer .qa-n{font-family:var(--font-display);font-size:34px;line-height:1;text-transform:uppercase}
.q-answer .qa-p{font-family:var(--font-display);font-size:72px;line-height:1;color:var(--royal-blue);margin:16px 0 8px}
.q-answer .qa-s{font-size:15px;line-height:24px;color:#3a3a3a;max-width:34ch;margin:0 auto 24px}
.q-answer .btn{justify-content:center}
.q-alt{font-size:13px;line-height:20px;color:var(--silver-grey);margin-top:24px}
@media (max-width:768px){ .q-opts,.q-opts.many{grid-template-columns:1fr} .q-opt{padding:16px} }
'''

V1_JS = '''
(function(){
  var E=window.EWPricing; if(!E) return; var P=E.P;
  var q=document.getElementById('q'); if(!q) return;
  document.documentElement.classList.add('js');
  var all=document.getElementById('pr-all'), tog=document.getElementById('pr-toggle');
  all.hidden=true;
  tog.addEventListener('click',function(){
    var open=tog.getAttribute('aria-expanded')==='true';
    tog.setAttribute('aria-expanded',String(!open)); all.hidden=open;
    tog.textContent = open ? 'See every price' : 'Hide the full list';
    if(!open) E.track('pricing_see_all',{});
  });
  function step(n){ [].forEach.call(q.querySelectorAll('.q-step'),function(s){ s.hidden = s.dataset.step!==String(n) }) }
  [].forEach.call(q.querySelectorAll('.q-restart'),function(b){ b.addEventListener('click',function(){ step(1); E.track('pricing_restart',{}) }) });

  q.querySelector('[data-who="visitor"]').addEventListener('click',function(){ askVisitor() });
  q.querySelector('[data-who="member"]').addEventListener('click',function(){ askMember() });

  function opts(html){ document.getElementById('q-opts2').innerHTML=html; }
  function askVisitor(){
    E.track('pricing_who',{who:'visitor'});
    document.getElementById('q-ask2').textContent='How long are you here?';
    opts(P.visitor.map(function(v){
      return '<button class="q-opt" type="button" data-days="'+(v.days<4?1:v.days)+'"><b>'+v.name+'</b><span>'+E.money(v.price)+'</span></button>';
    }).join('') + '<button class="q-opt" type="button" data-days="60"><b>Longer than that</b><span>A member plan costs less</span></button>');
    document.getElementById('q-opts2').className='q-opts many';
    step(2);
    [].forEach.call(document.querySelectorAll('[data-days]'),function(b){
      b.addEventListener('click',function(){ visitorAnswer(+b.dataset.days) });
    });
  }
  function askMember(){
    E.track('pricing_who',{who:'member'});
    document.getElementById('q-ask2').textContent='How often will you train?';
    opts(P.member.plans.map(function(p){
      return '<button class="q-opt" type="button" data-plan="'+p.id+'"><b>'+p.name+'</b><span>'+E.money(p.dd)+' every 2 weeks by direct debit</span></button>';
    }).join(''));
    document.getElementById('q-opts2').className='q-opts many';
    step(2);
    [].forEach.call(document.querySelectorAll('[data-plan]'),function(b){
      b.addEventListener('click',function(){ memberAnswer(b.dataset.plan) });
    });
  }
  function show(k,n,p,s,choice,alt){
    document.getElementById('q-answer').innerHTML =
      '<p class="qa-k">'+k+'</p><p class="qa-n">'+n+'</p><p class="qa-p">'+p+'</p><p class="qa-s">'+s+'</p>'+
      '<button class="btn" type="button" id="qa-go">Get this plan</button>'+(alt?'<p class="q-alt">'+alt+'</p>':'');
    step(3);
    document.getElementById('qa-go').addEventListener('click',function(){ E.review(choice) });
  }
  function visitorAnswer(days){
    var f=E.fourWeeks();
    if(days>28){
      var m=E.memberPlan('un');
      return show('Staying a while','Unlimited, as a member',E.money(m.dd),
        'Paid every 2 weeks by direct debit, plus '+E.money(P.insurance.year)+' insurance once a year. Past four weeks this beats any visitor pass.',
        {id:'un',title:'Unlimited member plan',price:m.dd+P.insurance.year,totalLabel:'To pay on your first visit',
         lines:[['First 2 weeks',E.money(m.dd)],['Sports insurance, once a year',E.money(P.insurance.year)]],
         notes:['Then '+E.money(m.dd)+' every 2 weeks by direct debit. Paying at the desk instead is '+E.money(m.desk)+'.']},
        'Four weeks as a visitor is '+E.money(f.visitor)+'. Four weeks as a member is '+E.money(f.member)+', and it keeps going.');
    }
    var b=E.visitorFor(days), title=b.item.name+' pass';
    show('Visiting',title,E.money(b.total),
      b.perVisit ? 'Pay it each time you come. From four days on, the week pass costs less.'
                 : 'One payment covers the whole stay. Insurance, the gym and every class included.',
      {id:b.item.id,title:title,price:b.total,totalLabel:'To pay at the desk',
       lines:[[b.item.name+' pass',E.money(b.item.price)],['Sports insurance','Included']]},
      b.item.days>=28 ? 'Four weeks as a member is '+E.money(f.member)+' with the insurance, and it does not stop after four weeks.' : '');
  }
  function memberAnswer(id){
    var p=E.memberPlan(id), first=E.memberFirst(p,true);
    show('Living here',p.name,E.money(p.dd),
      'Every 2 weeks by direct debit. Paying at the desk instead is '+E.money(p.desk)+', so direct debit saves you '+E.money(P.member.ddSavingYear)+' a year.',
      {id:p.id,title:p.name+' member plan',price:first.total,totalLabel:'To pay on your first visit',
       lines:[['First 2 weeks',E.money(first.rate)],['Sports insurance, once a year',E.money(first.insurance)]],
       notes:['Then '+E.money(p.dd)+' every 2 weeks.']},
      id==='w3' ? 'Unlimited is only '+E.money(P.member.plans[2].dd-p.dd)+' more every 2 weeks, and you can come any day.' : '');
  }
})();
'''

# ================================================================= 2.4.2 the dial
V2_SEC = (KICKER % 'move the dial') + '''  <div class="dial">
    <p class="dial-ask">I am in Lagos for <b id="dial-n">7 days</b></p>
    <input class="dial-range" id="dial" type="range" min="1" max="40" value="7" step="1" aria-label="How many days you are in Lagos">
    <div class="dial-scale"><span>1 day</span><span>2 weeks</span><span>40 days</span></div>
    <div class="dial-out" id="dial-out"></div>
  </div>
  <button class="pr-toggle" type="button" id="pr-toggle" aria-expanded="false" aria-controls="pr-all">See every price</button>
''' + ALLPRICES + LEGAL

V2_CSS = ALLCSS + '''
.dial{max-width:720px;margin:0 auto}
.dial-ask{font-family:var(--font-display);font-size:clamp(26px,3.6vw,40px);line-height:1.1;text-transform:uppercase;text-align:center;margin-bottom:32px}
.dial-ask b{color:var(--royal-blue)}
.dial-range{-webkit-appearance:none;appearance:none;width:100%;height:2px;background:var(--light-grey);outline:0}
.dial-range::-webkit-slider-thumb{-webkit-appearance:none;width:32px;height:32px;border-radius:50%;background:var(--royal-blue);cursor:grab;border:0}
.dial-range::-moz-range-thumb{width:32px;height:32px;border-radius:50%;background:var(--royal-blue);cursor:grab;border:0}
.dial-range:active::-webkit-slider-thumb{cursor:grabbing}
.dial-scale{display:flex;justify-content:space-between;font-weight:800;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--silver-grey);margin-top:16px}
.dial-out{margin-top:48px;text-align:center;min-height:280px}
.dial-k{font-weight:800;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey);margin-bottom:8px}
.dial-name{font-family:var(--font-display);font-size:34px;line-height:1;text-transform:uppercase}
.dial-price{font-family:var(--font-display);font-size:clamp(72px,12vw,120px);line-height:.9;color:var(--royal-blue);margin:8px 0}
.dial-note{font-size:15px;line-height:24px;color:#3a3a3a;max-width:36ch;margin:0 auto 24px}
.dial-switch{display:inline-block;background:var(--accent);color:var(--black);font-weight:800;font-size:11px;letter-spacing:.12em;text-transform:uppercase;padding:6px 12px;margin-bottom:16px}
@media (max-width:768px){ .dial-out{min-height:300px} }
'''

V2_JS = '''
(function(){
  var E=window.EWPricing; if(!E) return; var P=E.P;
  var d=document.getElementById('dial'); if(!d) return;
  document.documentElement.classList.add('js');
  var all=document.getElementById('pr-all'), tog=document.getElementById('pr-toggle');
  all.hidden=true;
  tog.addEventListener('click',function(){
    var open=tog.getAttribute('aria-expanded')==='true';
    tog.setAttribute('aria-expanded',String(!open)); all.hidden=open;
    tog.textContent = open ? 'See every price' : 'Hide the full list';
    if(!open) E.track('pricing_see_all',{});
  });
  var out=document.getElementById('dial-out'), lab=document.getElementById('dial-n'), last=null, t;
  function render(){
    var days=+d.value;
    lab.textContent = days===1 ? '1 day' : days+' days';
    /* a member plan only once no visitor pass covers the stay: today the four
       week pass at 61.90 is still cheaper than four weeks as a member */
    var f=E.fourWeeks(), longest=P.visitor[P.visitor.length-1].days, member = days>longest, choice, html;
    if(member){
      var m=E.memberPlan('un');
      choice={id:'un',title:'Unlimited member plan',price:m.dd+P.insurance.year,totalLabel:'To pay on your first visit',
        lines:[['First 2 weeks',E.money(m.dd)],['Sports insurance, once a year',E.money(P.insurance.year)]],
        notes:['Then '+E.money(m.dd)+' every 2 weeks by direct debit.']};
      html='<p class="dial-switch">Past four weeks, join instead</p>'+
        '<p class="dial-k">Living here</p><p class="dial-name">Unlimited</p>'+
        '<p class="dial-price">'+E.money(m.dd)+'</p>'+
        '<p class="dial-note">Every 2 weeks, train any day. Four weeks costs '+E.money(f.member)+' with the insurance, against '+E.money(f.visitor)+' as a visitor, and it does not stop after four weeks.</p>';
    } else {
      var b=E.visitorFor(days), title=b.item.name+' pass';
      choice={id:b.item.id,title:title,price:b.total,totalLabel:'To pay at the desk',
        lines:[[b.item.name+' pass',E.money(b.item.price)],['Sports insurance','Included']]};
      html='<p class="dial-k">Visiting</p><p class="dial-name">'+title+'</p>'+
        '<p class="dial-price">'+E.money(b.total)+'</p>'+
        '<p class="dial-note">'+(b.perVisit
          ? 'Pay it each time you come. From four days on, the week pass costs less.'
          : 'One payment for the whole stay. Insurance, the gym and every class included.')+'</p>';
    }
    out.innerHTML = html + '<button class="btn" type="button" id="dial-go">Get this plan</button>';
    document.getElementById('dial-go').addEventListener('click',function(){ E.review(choice) });
    clearTimeout(t); t=setTimeout(function(){
      if(last!==choice.id){ last=choice.id; E.track('pricing_dial',{days:days,plan:choice.id}) }
    },600);
  }
  d.addEventListener('input',render); render();
})();
'''

# ================================================================ 2.4.3 two doors
V3_SEC = (KICKER % 'pick your door') + '''  <div class="doors">
    <div class="door">
      <p class="door-k">Visiting Lagos</p>
      <h3 class="door-h">Pay for the days you are here</h3>
      <p class="door-s">Insurance, the gym floor and every class are in the price. No booking, no sign up.</p>
      <ul class="door-list">
        <li><span>1 day</span><b>€10</b></li>
        <li><span>1 week</span><b>€35.90</b></li>
        <li><span>2 weeks</span><b>€45.90</b></li>
        <li><span>3 weeks</span><b>€51.90</b></li>
        <li><span>4 weeks</span><b>€61.90<span class="pr-todo" title="[PLACEHOLDER: the price list review proposes €69.90 so four weeks as a member is cheaper. Current price shown until the family decides]">todo</span></b></li>
      </ul>
      <p class="door-tip">Four days or more? The week pass costs less than four day passes.</p>
      <button class="btn" type="button" data-door="visitor">Choose a visitor pass</button>
    </div>
    <div class="door door-b">
      <p class="door-k">Living in Lagos</p>
      <h3 class="door-h">Join, and pay every 2 weeks</h3>
      <p class="door-s">Prices are per 2 weeks, not per month. Direct debit saves you €130 a year against paying at the desk.</p>
      <ul class="door-list">
        <li><span>Once a week</span><b>€13</b></li>
        <li><span>Three a week</span><b>€19.50</b></li>
        <li class="door-best"><span>Unlimited <i>best value</i></span><b>€21</b></li>
      </ul>
      <p class="door-tip">Unlimited is €1.50 more than three a week, and you can come any day. Add €24 once a year for the sports insurance.</p>
      <button class="btn on-dark" type="button" data-door="member">Choose a member plan</button>
    </div>
  </div>
  <div class="pt-band">
    <div>
      <p class="door-k">With a coach</p>
      <h3 class="door-h">Personal training</h3>
      <p class="door-s">One to one with a qualified coach. Bring someone with you for €15 more a session.</p>
    </div>
    <ul class="pt-list">
      <li><span>Single session</span><b>€50</b></li>
      <li><span>8 sessions, 2 months</span><b>€360</b><i>€45 each</i></li>
      <li><span>12 sessions, 2 months</span><b>€480</b><i>€40 each</i></li>
      <li><span>20 sessions, 3 months</span><b>€600</b><i>€30 each</i></li>
    </ul>
  </div>
  <p class="pr-legal pt-note">Packs of two sessions a week or fewer do not include the gym on the other days. To train on the other days, add a member plan.</p>
''' + LEGAL

V3_CSS = ALLCSS + '''
.doors{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.door{border:2px solid var(--light-grey);padding:40px 32px;display:flex;flex-direction:column}
.door-b{background:var(--royal-blue);border-color:var(--royal-blue);color:var(--white)}
.door-k{font-weight:800;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey);margin-bottom:8px}
.door-b .door-k{color:rgba(255,255,255,.7)}
.door-h{font-family:var(--font-display);font-size:34px;line-height:1.05;text-transform:uppercase;margin-bottom:8px}
.door-s{font-size:15px;line-height:24px;color:#3a3a3a;margin-bottom:32px}
.door-b .door-s{color:rgba(255,255,255,.85)}
.door-list{list-style:none;margin:0 0 24px;padding:0}
.door-list li{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:12px 0;box-shadow:inset 0 -1px 0 var(--light-grey);font-size:16px;line-height:24px}
.door-b .door-list li{box-shadow:inset 0 -1px 0 rgba(255,255,255,.25)}
.door-list b{font-family:var(--font-display);font-size:24px;line-height:1}
.door-best i{display:inline-block;font-style:normal;background:var(--accent);color:var(--black);font-weight:800;font-size:9px;letter-spacing:.1em;text-transform:uppercase;padding:2px 6px;margin-left:8px;vertical-align:2px}
.door-tip{font-size:13px;line-height:20px;color:var(--silver-grey);margin-bottom:24px}
.door-b .door-tip{color:rgba(255,255,255,.7)}
.door .btn{margin-top:auto;justify-content:center}
.pt-band{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start;margin-top:24px;background:var(--off-white,#F4F4F2);padding:40px 32px}
.pt-list{list-style:none;margin:0;padding:0}
.pt-list li{display:grid;grid-template-columns:1fr auto auto;gap:16px;align-items:baseline;padding:12px 0;box-shadow:inset 0 -1px 0 var(--light-grey);font-size:16px}
.pt-list b{font-family:var(--font-display);font-size:24px;line-height:1}
.pt-list i{font-style:normal;font-size:12px;color:var(--silver-grey);min-width:56px;text-align:right}
.pt-note{margin-top:16px}
@media (max-width:768px){ .doors,.pt-band{grid-template-columns:1fr} .door{padding:32px 24px} .pt-band{padding:32px 24px;gap:32px} }
'''

V3_JS = '''
(function(){
  var E=window.EWPricing; if(!E) return; var P=E.P;
  var doors=document.querySelectorAll('[data-door]'); if(!doors.length) return;
  [].forEach.call(doors,function(b){
    b.addEventListener('click',function(){
      var who=b.dataset.door;
      E.track('pricing_door',{who:who});
      if(who==='member'){
        var m=E.memberPlan('un'), f=E.memberFirst(m,true);
        E.review({id:'un',title:'Unlimited member plan',price:f.total,totalLabel:'To pay on your first visit',
          lines:[['First 2 weeks',E.money(f.rate)],['Sports insurance, once a year',E.money(f.insurance)]],
          notes:['Then '+E.money(m.dd)+' every 2 weeks by direct debit. At the desk it is '+E.money(m.desk)+'.',
                 'Training once or three times a week costs less. Ask at the desk and we will set up whichever fits.']});
      } else {
        var v=P.visitor[1];
        E.review({id:v.id,title:v.name+' pass',price:v.price,totalLabel:'To pay at the desk',
          lines:[[v.name+' pass',E.money(v.price)],['Sports insurance','Included']],
          notes:['Here for fewer than four days? Day passes at '+E.money(P.visitor[0].price)+' work out cheaper. Longer? Two, three and four week passes are on the list above.']});
      }
    });
  });
})();
'''

# ========================================================== 2.4.4 the honest table
V4_SEC = (KICKER % 'the whole list, and the maths') + '''  <p class="ht-lede">Most gyms in Lagos will not tell you what they cost until you walk in. Here is everything, with the arithmetic already done.</p>
  <table class="ht">
    <caption class="ht-cap">Visiting</caption>
    <thead><tr><th scope="col">Pass</th><th scope="col">Price</th><th scope="col">Works out at</th><th scope="col"></th></tr></thead>
    <tbody>
      <tr><th scope="row">1 day</th><td class="n">€10</td><td class="d">€10 a day</td><td class="a"><button class="ht-go" type="button" data-v="d1">Choose</button></td></tr>
      <tr><th scope="row">1 week</th><td class="n">€35.90</td><td class="d">€5.13 a day</td><td class="a"><button class="ht-go" type="button" data-v="s1">Choose</button></td></tr>
      <tr><th scope="row">2 weeks</th><td class="n">€45.90</td><td class="d">€3.28 a day</td><td class="a"><button class="ht-go" type="button" data-v="s2">Choose</button></td></tr>
      <tr><th scope="row">3 weeks</th><td class="n">€51.90</td><td class="d">€2.47 a day</td><td class="a"><button class="ht-go" type="button" data-v="s3">Choose</button></td></tr>
      <tr><th scope="row">4 weeks</th><td class="n">€61.90<span class="pr-todo" title="[PLACEHOLDER: the price list review proposes €69.90 so four weeks as a member is cheaper. Current price shown until the family decides]">todo</span></td><td class="d">€2.21 a day</td><td class="a"><button class="ht-go" type="button" data-v="s4">Choose</button></td></tr>
    </tbody>
  </table>
  <p class="ht-read">Day passes are cheaper until the fourth day. From four days on, the week pass wins. Every visitor pass has the sports insurance in it.</p>

  <table class="ht">
    <caption class="ht-cap">Living here <em>paid every 2 weeks, not monthly</em></caption>
    <thead><tr><th scope="col">Plan</th><th scope="col">Direct debit</th><th scope="col">At the desk</th><th scope="col">A year, all in</th><th scope="col"></th></tr></thead>
    <tbody>
      <tr><th scope="row">Once a week</th><td class="n">€13</td><td class="d">€18</td><td class="d">€362</td><td class="a"><button class="ht-go" type="button" data-m="w1">Choose</button></td></tr>
      <tr><th scope="row">Three a week</th><td class="n">€19.50</td><td class="d">€24.50</td><td class="d">€531</td><td class="a"><button class="ht-go" type="button" data-m="w3">Choose</button></td></tr>
      <tr class="ht-best"><th scope="row">Unlimited <i>best value</i></th><td class="n">€21</td><td class="d">€26</td><td class="d">€570</td><td class="a"><button class="ht-go" type="button" data-m="un">Choose</button></td></tr>
    </tbody>
  </table>
  <p class="ht-read">The year column includes the €24 sports insurance and 26 payments. Direct debit saves €130 a year. Unlimited costs €1.50 more than three a week and lets you come any day.</p>

  <table class="ht">
    <caption class="ht-cap">With a coach</caption>
    <thead><tr><th scope="col">Personal training</th><th scope="col">Each</th><th scope="col">Total</th><th scope="col">You save</th></tr></thead>
    <tbody>
      <tr><th scope="row">Single session</th><td class="d">€50</td><td class="n">€50</td><td class="d"></td></tr>
      <tr><th scope="row">8 sessions, valid 2 months</th><td class="d">€45</td><td class="n">€360</td><td class="d">€40</td></tr>
      <tr><th scope="row">12 sessions, valid 2 months</th><td class="d">€40</td><td class="n">€480</td><td class="d">€120</td></tr>
      <tr><th scope="row">20 sessions, valid 3 months</th><td class="d">€30</td><td class="n">€600</td><td class="d">€400</td></tr>
    </tbody>
  </table>
  <p class="ht-read">Bring someone and the second person is €15 a session. Packs of two sessions a week or fewer do not include the gym on the other days, so add a member plan if you want to train around them.</p>
''' + LEGAL

V4_CSS = ALLCSS + '''
.ht-lede{font-size:clamp(16px,2vw,20px);line-height:1.5;max-width:44ch;margin:0 auto 64px;text-align:center;color:#3a3a3a}
.ht{width:100%;border-collapse:collapse;margin-top:48px}
.ht-cap{caption-side:top;text-align:left;font-family:var(--font-display);font-size:24px;line-height:1;text-transform:uppercase;padding-bottom:16px}
.ht-cap em{font-style:normal;font-family:var(--font-body);font-weight:400;font-size:13px;text-transform:none;color:var(--silver-grey);margin-left:8px}
.ht th[scope=col]{font-weight:800;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--silver-grey);text-align:right;padding:0 0 8px;box-shadow:inset 0 -1px 0 var(--black)}
.ht th[scope=col]:first-child{text-align:left}
.ht th[scope=row]{text-align:left;font-weight:400;font-size:16px;line-height:24px;padding:16px 0}
.ht td{text-align:right;padding:16px 0;box-shadow:inset 0 -1px 0 var(--light-grey);font-size:16px}
.ht th[scope=row]{box-shadow:inset 0 -1px 0 var(--light-grey)}
.ht td.n{font-family:var(--font-display);font-size:24px;line-height:1}
.ht td.d{color:var(--silver-grey)}
.ht td.a{width:1%;white-space:nowrap}
.ht-best th[scope=row],.ht-best td{background:var(--off-white,#F4F4F2)}
.ht-best i{display:inline-block;font-style:normal;background:var(--accent);color:var(--black);font-weight:800;font-size:9px;letter-spacing:.1em;text-transform:uppercase;padding:2px 6px;margin-left:8px;vertical-align:2px}
.ht-go{appearance:none;border:0;background:transparent;font-family:var(--font-body);font-weight:800;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--royal-blue);cursor:pointer;padding:4px 0 4px 16px;text-decoration:underline}
.ht-read{font-size:13px;line-height:20px;color:var(--silver-grey);margin-top:16px;max-width:64ch}
@media (max-width:768px){
  .ht,.ht thead,.ht tbody,.ht th,.ht td,.ht tr{display:block}
  .ht thead{display:none}
  .ht tr{padding:16px 0;box-shadow:inset 0 -1px 0 var(--light-grey)}
  .ht th[scope=row]{padding:0 0 8px;box-shadow:none;font-weight:700}
  .ht td{display:inline-block;padding:0 16px 0 0;box-shadow:none;text-align:left}
  .ht td.n{font-size:20px}
  .ht td.d::before{content:attr(data-l) " "}
  .ht td.a{display:block;padding:8px 0 0}
  .ht-go{padding-left:0}
}
'''

V4_JS = '''
(function(){
  var E=window.EWPricing; if(!E) return; var P=E.P;
  var gos=document.querySelectorAll('.ht-go'); if(!gos.length) return;
  [].forEach.call(gos,function(b){
    b.addEventListener('click',function(){
      if(b.dataset.v){
        var v=P.visitor.filter(function(x){return x.id===b.dataset.v})[0];
        E.track('pricing_row',{plan:v.id});
        E.review({id:v.id,title:v.name+' pass',price:v.price,totalLabel:'To pay at the desk',
          lines:[[v.name+' pass',E.money(v.price)],['Sports insurance','Included']]});
      } else {
        var m=E.memberPlan(b.dataset.m), f=E.memberFirst(m,true);
        E.track('pricing_row',{plan:m.id});
        E.review({id:m.id,title:m.name+' member plan',price:f.total,totalLabel:'To pay on your first visit',
          lines:[['First 2 weeks',E.money(f.rate)],['Sports insurance, once a year',E.money(f.insurance)]],
          notes:['Then '+E.money(m.dd)+' every 2 weeks by direct debit, or '+E.money(m.desk)+' at the desk.',
                 'A year works out at '+E.money(E.memberYear(m,true))+' all in.']});
      }
    });
  });
})();
'''

# ============================================================ 2.4.5 the receipt
V5_SEC = (KICKER % 'build it and see') + '''  <div class="rc">
    <div class="rc-build">
      <fieldset class="rc-set">
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
    </div>
    <aside class="rc-receipt" aria-live="polite">
      <p class="rc-k">Your plan</p>
      <div class="rc-lines" id="rc-lines"></div>
      <div class="rc-total"><span id="rc-total-l">To pay on your first visit</span><b id="rc-total">€0</b></div>
      <p class="rc-note" id="rc-note"></p>
      <button class="btn" type="button" id="rc-go">Get this plan</button>
    </aside>
  </div>
''' + LEGAL

V5_CSS = ALLCSS + '''
.rc{display:grid;grid-template-columns:1fr 380px;gap:64px;align-items:start}
.rc-set{border:0;padding:0;margin:0 0 32px;min-width:0}
.rc-leg{font-weight:800;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey);padding:0;margin-bottom:12px}
.rc-chips{display:flex;flex-wrap:wrap;gap:8px}
.rc-chip{appearance:none;border:2px solid var(--light-grey);background:var(--white);font-family:var(--font-body);font-weight:700;font-size:14px;line-height:20px;padding:10px 16px;cursor:pointer;transition:border-color .15s,background .15s,color .15s}
.rc-chip:hover{border-color:var(--black)}
.rc-chip.on{background:var(--royal-blue);border-color:var(--royal-blue);color:var(--white)}
.rc-chip small{display:block;font-weight:400;font-size:11px;opacity:.75}
.rc-receipt{background:var(--black);color:var(--white);padding:32px 24px;position:sticky;top:96px}
.rc-k{font-weight:800;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.55);margin-bottom:16px}
.rc-lines{min-height:96px}
.rc-line{display:flex;justify-content:space-between;gap:16px;align-items:baseline;padding:10px 0;box-shadow:inset 0 -1px 0 rgba(255,255,255,.18);font-size:14px;line-height:20px}
.rc-line b{white-space:nowrap}
.rc-line.sub{color:rgba(255,255,255,.6);font-size:12px;box-shadow:none;padding-top:0}
.rc-total{display:flex;justify-content:space-between;gap:16px;align-items:baseline;padding-top:24px;font-size:13px;color:rgba(255,255,255,.7)}
.rc-total b{font-family:var(--font-display);font-size:44px;line-height:1;color:var(--accent)}
.rc-note{font-size:12px;line-height:18px;color:rgba(255,255,255,.6);margin-top:16px}
.rc-receipt .btn{width:100%;justify-content:center;margin-top:24px}
@media (max-width:768px){
  .rc{grid-template-columns:1fr;gap:32px}
  .rc-receipt{position:static}
}
'''

V5_JS = '''
(function(){
  var E=window.EWPricing; if(!E) return; var P=E.P;
  var wrap=document.querySelector('.rc'); if(!wrap) return;
  var st={who:'visitor',stay:'s1',plan:'un',pay:'dd',pack:'p8'};

  document.getElementById('rc-stay').innerHTML = P.visitor.map(function(v){
    return '<button class="rc-chip'+(v.id===st.stay?' on':'')+'" type="button" data-stay="'+v.id+'">'+v.name+'<small>'+E.money(v.price)+'</small></button>';
  }).join('');
  document.getElementById('rc-plan').innerHTML = P.member.plans.map(function(p){
    return '<button class="rc-chip'+(p.id===st.plan?' on':'')+'" type="button" data-plan="'+p.id+'">'+p.name+'<small>'+E.money(p.dd)+' / 2 weeks</small></button>';
  }).join('');
  document.getElementById('rc-pack').innerHTML = P.pt.packs.map(function(k){
    return '<button class="rc-chip'+(k.id===st.pack?' on':'')+'" type="button" data-pack="'+k.id+'">'+k.name+'<small>'+E.money(k.total)+'</small></button>';
  }).join('');

  function pick(group, attr, val){
    [].forEach.call(document.getElementById(group).children,function(b){
      b.classList.toggle('on', b.dataset[attr]===val);
    });
  }
  function sets(){
    document.getElementById('rc-set-stay').hidden = st.who!=='visitor';
    document.getElementById('rc-set-plan').hidden = st.who!=='member';
    document.getElementById('rc-set-pay').hidden  = st.who!=='member';
    document.getElementById('rc-set-pack').hidden = st.who!=='pt';
  }
  wrap.addEventListener('click',function(e){
    var b=e.target.closest('.rc-chip'); if(!b) return; var d=b.dataset;
    if(d.who!=null){ st.who=d.who; pick('rc-who','who',d.who); sets(); E.track('pricing_who',{who:d.who}) }
    else if(d.stay!=null){ st.stay=d.stay; pick('rc-stay','stay',d.stay) }
    else if(d.plan!=null){ st.plan=d.plan; pick('rc-plan','plan',d.plan) }
    else if(d.pay!=null){ st.pay=d.pay; pick('rc-pay','pay',d.pay) }
    else if(d.pack!=null){ st.pack=d.pack; pick('rc-pack','pack',d.pack) }
    render();
  });

  var cur=null;
  function render(){
    var lines=[], notes=[], total=0, title, id, label;
    if(st.who==='visitor'){
      var v=P.visitor.filter(function(x){return x.id===st.stay})[0];
      lines=[[v.name+' visitor pass',E.money(v.price)],['Sports insurance','Included',true]];
      total=v.price; title=v.name+' visitor pass'; id=v.id; label='To pay at the desk';
      if(v.days<4) notes.push('The day pass is paid each time you come. From four days on, the week pass costs less.');
      if(v.days>=28) notes.push('Four weeks as a member is '+E.money(E.fourWeeks().member)+' and it does not stop after four weeks.');
    } else if(st.who==='member'){
      var p=E.memberPlan(st.plan), dd=st.pay==='dd', rate=dd?p.dd:p.desk;
      lines=[[p.name+', first 2 weeks',E.money(rate)],['Sports insurance, once a year',E.money(P.insurance.year)],
             ['Then '+E.money(rate)+' every 2 weeks','',true]];
      total=rate+P.insurance.year; title=p.name+' member plan'; id=p.id; label='To pay on your first visit';
      notes.push(dd ? 'Direct debit saves you '+E.money(P.member.ddSavingYear)+' a year against paying at the desk.'
                    : 'Switching to direct debit would save you '+E.money(P.member.ddSavingYear)+' a year.');
    } else {
      var k=P.pt.packs.filter(function(x){return x.id===st.pack})[0];
      lines=[[k.name+' with a coach',E.money(k.total)]];
      if(k.sessions>1) lines.push([E.money(k.each)+' a session, valid '+k.months+' months','',true]);
      total=k.total; title=k.name+' with a coach'; id=k.id; label='To pay at the desk';
      notes.push('Bring someone with you and the second person is '+E.money(P.pt.second)+' a session.');
      if(k.sessions>1) notes.push(P.pt.note);
    }
    document.getElementById('rc-lines').innerHTML = lines.map(function(l){
      return '<div class="rc-line'+(l[2]?' sub':'')+'"><span>'+l[0]+'</span><b>'+(l[1]||'')+'</b></div>';
    }).join('');
    document.getElementById('rc-total').textContent = E.money(total);
    document.getElementById('rc-total-l').textContent = label;
    document.getElementById('rc-note').textContent = notes.join(' ');
    cur={id:id,title:title,price:total,totalLabel:label,lines:lines.filter(function(l){return !l[2]}),notes:notes};
  }
  document.getElementById('rc-go').addEventListener('click',function(){ if(cur) E.review(cur) });
  sets(); render();
})();
'''


# ------------------------------------------------------------------------ build
VARIANTS = [
  ('2-4-1', V1_SEC, V1_CSS, V1_JS),
  ('2-4-2', V2_SEC, V2_CSS, V2_JS),
  ('2-4-3', V3_SEC, V3_CSS, V3_JS),
  ('2-4-4', V4_SEC, V4_CSS, V4_JS),
  ('2-4-5', V5_SEC, V5_CSS, V5_JS),
]
base = shared(s0)
for name, sec, css, js in VARIANTS:
    out = swap(base, sec, css, js)
    f = 'elite-wellness-landing_%s.html' % name
    io.open(f, 'w', encoding='utf-8').write(out)
    print(f, len(out))
