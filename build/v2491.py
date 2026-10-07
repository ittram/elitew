# -*- coding: utf-8 -*-
"""Drafts 2.4.9.1 to 2.4.9.5: five ways to present personal training, on 2.4.9.
Run build/v249.py first (this reuses its style, script and page), then
build/pricelist.py.

What 2.4.9 got wrong (7 October 2026): choosing Personal training started
abruptly with a numbered list, the contact block was cold, a new customer
could not tell how it would work, and the buttons had been restyled. So every
version here: opens with a warm, plain introduction (who trains you, what you
can work on), explains how it works, invites contact in a human way, and uses
the site's own button (.btn) exactly as it is everywhere else.

Facts used, nothing more: one to one; André, Joana and Ricardo, all qualified
in physical education (the About band); general fitness and strength, rehab
after an injury, nutrition, or a mix (the owner); the plan and its price are
agreed with the coach; sessions from the lowest price a session on the sheet;
a second person can join (the sheet's "pessoa extra")."""
import io, re

src = io.open('build/v249.py', encoding='utf-8').read()
ns = {}
exec(src[:src.index("if __name__ == '__main__':")], ns)
BASE, CSS, JS, make = ns['s'], ns['CSS'], ns['JS'], ns['make']
i, j = JS.index('  /* PT:start'), JS.index('  /* PT:end */\n') + len('  /* PT:end */\n')

COMMON_JS = r'''
  var PT_MSG='Hi! I would like to start personal training and talk to a coach about what I need.';
  var COACHES=[['André','andre'],['Joana','joana'],['Ricardo','ricardo']];
  function face(c){ return '<span class="pt-face"><b aria-hidden="true">'+c[0].charAt(0)+'</b><img src="assets/team/'+c[1]+'.jpg" alt="" onerror="this.remove()"></span>' }
  function faces(){ return '<span class="pt-faces" aria-hidden="true">'+COACHES.map(face).join('')+'</span>' }
  var WORK='getting fitter and stronger, coming back from an injury, eating better, or a mix of these';
  var FROM='One to one, from '+money(ptFrom)+' a session';
'''
COMMON_CSS = r'''
/* ---------- 2.4.9.x personal training: shared pieces ---------- */
.pt-lead{clear:both;font-size:20px;line-height:28px;font-weight:600;max-width:40ch}
.pt-p{margin-top:16px;font-size:16px;line-height:24px;color:#3A3A3A;max-width:56ch}
.pt-face{position:relative;display:inline-grid;place-items:center;width:48px;height:48px;border-radius:50%;background:var(--royal-blue);color:var(--white);font-family:var(--font-display);font-size:20px;line-height:1;overflow:hidden;box-shadow:0 0 0 2px var(--white)}
.pt-face img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1)}
.pt-faces{display:inline-flex}
.pt-faces .pt-face+.pt-face{margin-left:-8px}
.pt-note{margin-top:12px;font-size:12px;line-height:16px;color:#6A6A6A}
@media (max-width:768px){ .pt-lead{font-size:18px;line-height:24px} .pt-p{font-size:15px;line-height:24px} }
'''

V = {}

# =====================================================================
# 2.4.9.1  The coaches. Faces and names first: you are writing to people.
# =====================================================================
V['2.4.9.1'] = ('Personal training, the coaches', r'''
  function ptLeft(){
    return '<div class="pc-set"><p class="pc-leg">Personal training</p>'+
      '<p class="pt-lead">Train one to one with a coach who plans every session around you.</p>'+
      '<ul class="v1-coaches">'+COACHES.map(function(c){ return '<li>'+face(c)+'<span><b>'+c[0]+'</b><small>Qualified in physical education</small></span></li>' }).join('')+'</ul>'+
      '<p class="pt-p">Whatever brings you in: '+WORK+'. You and your coach decide the plan together.</p></div>'+
      '<div class="pc-set"><p class="pc-leg">How it starts</p><ol class="v1-steps">'+
      [['Message us','on WhatsApp, in your own words'],['Meet your coach','at the gym, at a time that suits you'],['Start training','with a plan made for you']].map(function(x,i){
        return '<li><span class="v1-n">'+(i+1)+'</span><b>'+x[0]+'</b><span>'+x[1]+'</span></li>' }).join('')+'</ol></div>';
  }
  function ptRight(href){
    return '<p class="pc-leg">Say hello</p><div class="v1-c">'+faces()+
      '<p class="v1-h">Talk to a coach</p>'+
      '<p class="pt-p">Send us a message and we find a time for you to meet your coach at the gym. You agree the plan and its price together, before you start.</p>'+
      '<a class="btn" id="pt-wa" href="'+href+'" target="_blank" rel="noopener">Message us on WhatsApp</a>'+
      '<p class="pt-note">'+FROM+'</p></div>';
  }
  function ptBand(){ return '' }
''', r'''
.v1-coaches{list-style:none;margin:24px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.v1-coaches li{display:flex;align-items:center;gap:12px;padding:12px;border:2px solid var(--light-grey)}
.v1-coaches b{display:block;font-size:16px;line-height:24px}
.v1-coaches small{display:block;font-size:12px;line-height:16px;color:#6A6A6A}
.v1-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.v1-steps li{display:flex;flex-direction:column;gap:4px;padding-top:16px;box-shadow:inset 0 2px 0 var(--black)}
.v1-n{font-family:var(--font-display);font-size:24px;line-height:24px;color:var(--royal-blue)}
.v1-steps b{font-size:16px;line-height:24px;margin-top:8px}
.v1-steps span:last-child{font-size:14px;line-height:20px;color:#4A4A4A}
.v1-c{background:#F4F4F2;padding:32px}
.v1-h{margin-top:16px;font-family:var(--font-display);font-size:32px;line-height:32px;text-transform:uppercase}
.v1-c .btn{margin-top:24px}
@media (max-width:1100px){ .v1-coaches{grid-template-columns:1fr} }
@media (max-width:768px){
  .v1-coaches{grid-template-columns:1fr}
  .v1-steps{grid-template-columns:1fr;gap:16px}
  .v1-c{padding:24px}
}
''')

# =====================================================================
# 2.4.9.2  The journey. A full width band: three steps across, one invitation.
# =====================================================================
V['2.4.9.2'] = ('Personal training, the journey', r'''
  function ptLeft(){
    return '<div class="pc-set"><p class="pc-leg">Personal training</p>'+
      '<p class="pt-lead">Training planned around you, with a coach by your side.</p>'+
      '<p class="pt-p">André, Joana and Ricardo are all qualified in physical education. Tell them what you want: '+WORK+'.</p></div>';
  }
  function ptRight(){ return '' }
  function ptBand(href){
    return '<div class="v2"><p class="pc-leg">How it works</p><ol class="v2-steps">'+
      [['Send a message','Say hello on WhatsApp and tell us what you would like to work on. A few words are enough.'],
       ['Meet your coach','We agree a time and you meet your coach at the gym to talk it through. No commitment.'],
       ['Start training','Your coach proposes a plan and its price. Once you agree, you train one to one, from '+money(ptFrom)+' a session.']].map(function(x,i){
        return '<li><span class="v2-n">0'+(i+1)+'</span><b>'+x[0]+'</b><span>'+x[1]+'</span></li>' }).join('')+'</ol>'+
      '<div class="v2-cta">'+faces()+'<p><b>Ready when you are.</b> The message is written for you, just press send.</p>'+
      '<a class="btn" id="pt-wa" href="'+href+'" target="_blank" rel="noopener">Message us on WhatsApp</a></div></div>';
  }
''', r'''
.pt-band{margin-top:48px}
.v2{background:#F4F4F2;padding:48px}
.v2-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;counter-reset:s}
.v2-steps li{position:relative;display:flex;flex-direction:column;gap:8px;padding-top:24px;box-shadow:inset 0 2px 0 var(--royal-blue)}
.v2-n{font-family:var(--font-display);font-size:48px;line-height:48px;color:var(--royal-blue)}
.v2-steps b{font-size:18px;line-height:24px}
.v2-steps span:last-child{font-size:15px;line-height:24px;color:#3A3A3A}
.v2-cta{display:flex;align-items:center;gap:24px;margin-top:40px;padding-top:32px;box-shadow:inset 0 1px 0 var(--light-grey)}
.v2-cta p{flex:1 1 auto;font-size:16px;line-height:24px;color:#3A3A3A}
.v2-cta b{color:var(--black)}
@media (max-width:768px){
  .pt-band{margin-top:32px}
  .v2{padding:24px}
  .v2-steps{grid-template-columns:1fr;gap:24px}
  .v2-n{font-size:40px;line-height:40px}
  .v2-cta{flex-direction:column;align-items:flex-start;gap:16px}
}
''')

# =====================================================================
# 2.4.9.3  The chat. Show how the conversation goes, then start it.
# =====================================================================
V['2.4.9.3'] = ('Personal training, the chat', r'''
  function ptLeft(){
    return '<div class="pc-set"><p class="pc-leg">Personal training</p>'+
      '<p class="pt-lead">It starts with a message. Tell us what you would like, and we take it from there.</p>'+
      '<p class="pt-p">You train one to one with André, Joana or Ricardo, all qualified in physical education. After a first talk at the gym your coach proposes a plan and its price, and you decide.</p>'+
      '<ul class="v3-list">'+['Getting fitter and stronger','Coming back from an injury','Eating better','A mix of these'].map(function(x){ return '<li>'+x+'</li>' }).join('')+'</ul>'+
      '<p class="pt-note">'+FROM+'</p></div>';
  }
  function ptRight(href){
    var chat=[['me','Hi! I would like to start personal training. My knee has been sore since a fall, so I want to get stronger carefully.'],
              ['them','Hi! Happy to help. Can you come in this week to meet Joana? She will look at what you need and plan it with you.'],
              ['me','Thursday after work?'],
              ['them','Thursday at 18:00 works. See you then!']];
    return '<p class="pc-leg">How it goes</p><div class="v3-phone">'+
      '<div class="v3-top">'+face(COACHES[1])+'<span><b>Elite Wellness</b><small>WhatsApp</small></span></div>'+
      '<div class="v3-chat">'+chat.map(function(m){ return '<p class="v3-m '+m[0]+'">'+m[1]+'</p>' }).join('')+'</div>'+
      '<p class="v3-eg">An example of how a first chat goes.</p></div>'+
      '<a class="btn v3-go" id="pt-wa" href="'+href+'" target="_blank" rel="noopener">Start the chat on WhatsApp</a>'+
      '<p class="pt-note">A first message is ready for you to change or send as it is.</p>';
  }
  function ptBand(){ return '' }
''', r'''
.v3-list{list-style:none;margin:24px 0 0;padding:0;box-shadow:inset 0 1px 0 var(--light-grey)}
.v3-list li{position:relative;padding:12px 0 12px 32px;font-size:16px;line-height:24px;box-shadow:inset 0 -1px 0 var(--light-grey)}
.v3-list li::before{content:"";position:absolute;left:4px;top:20px;width:12px;height:6px;border-left:2px solid var(--royal-blue);border-bottom:2px solid var(--royal-blue);transform:rotate(-45deg)}
.v3-phone{background:#ECE9E4;border-radius:16px;overflow:hidden}
.v3-top{display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--black);color:var(--white)}
.v3-top .pt-face{width:40px;height:40px;font-size:16px;box-shadow:none}
.v3-top b{display:block;font-size:14px;line-height:20px}
.v3-top small{display:block;font-size:12px;line-height:16px;color:rgba(255,255,255,.6)}
.v3-chat{display:flex;flex-direction:column;gap:8px;padding:16px}
.v3-m{max-width:85%;padding:8px 12px;font-size:14px;line-height:20px;border-radius:12px;box-shadow:0 1px 1px rgba(0,0,0,.08)}
.v3-m.me{align-self:flex-end;background:#DCF2D4;border-bottom-right-radius:4px}
.v3-m.them{align-self:flex-start;background:var(--white);border-bottom-left-radius:4px}
.v3-eg{padding:0 16px 16px;font-size:12px;line-height:16px;color:#6A6A6A;text-align:center}
.v3-go{margin-top:24px}
''')

# =====================================================================
# 2.4.9.4  The questions. Answer what a new customer wonders, then invite.
# =====================================================================
V['2.4.9.4'] = ('Personal training, questions', r'''
  function ptLeft(){
    var qa=[['How does it start?','Send us a message on WhatsApp. We agree a time for you to meet your coach at the gym, and you talk through what you would like to work on.'],
            ['Who will train me?','André, Joana or Ricardo. All three are qualified in physical education and run the gym with their family.'],
            ['What can I work on?','Getting fitter and stronger, coming back from an injury, eating better, or a mix. The plan is made for you.'],
            ['What does it cost?','Sessions start at '+money(ptFrom)+'. Your coach proposes a plan and its price after your first talk, and you decide before you start.'],
            ['Can I bring a friend?','Yes, you can train together with one coach. Mention it in your message.']];
    return '<div class="pc-set"><p class="pc-leg">Personal training</p>'+
      '<p class="pt-lead">One to one training, planned with you. Here is how it works.</p>'+
      '<div class="v4-qa">'+qa.map(function(x,i){ return '<details'+(i===0?' open':'')+'><summary>'+x[0]+'</summary><p>'+x[1]+'</p></details>' }).join('')+'</div></div>';
  }
  function ptRight(href){
    return '<p class="pc-leg">Talk to us</p><div class="v4-c">'+faces()+
      '<p class="v4-h">Not sure where to start? Ask us.</p>'+
      '<p class="pt-p">Tell us a little about what you would like. We reply on WhatsApp and find a time for you to meet your coach.</p>'+
      '<a class="btn" id="pt-wa" href="'+href+'" target="_blank" rel="noopener">Message us on WhatsApp</a>'+
      '<p class="pt-note">'+FROM+'</p></div>';
  }
  function ptBand(){ return '' }
''', r'''
.v4-qa{margin-top:24px;box-shadow:inset 0 1px 0 var(--black)}
.v4-qa details{box-shadow:inset 0 -1px 0 var(--light-grey)}
.v4-qa summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 0;cursor:pointer;font-size:16px;line-height:24px;font-weight:700}
.v4-qa summary::-webkit-details-marker{display:none}
.v4-qa summary::after{content:"";flex:0 0 auto;width:8px;height:8px;border-right:2px solid var(--royal-blue);border-bottom:2px solid var(--royal-blue);transform:rotate(45deg);margin:-4px 4px 0 0;transition:transform .2s}
.v4-qa details[open] summary::after{transform:rotate(225deg);margin-top:4px}
.v4-qa summary:focus-visible{outline:2px solid var(--royal-blue);outline-offset:2px}
.v4-qa details p{padding:0 32px 16px 0;font-size:15px;line-height:24px;color:#3A3A3A}
.v4-c{background:var(--black);color:var(--white);padding:32px}
.v4-c .pt-face{box-shadow:0 0 0 2px var(--black)}
.v4-h{margin-top:16px;font-family:var(--font-display);font-size:32px;line-height:32px;text-transform:uppercase}
.v4-c .pt-p{color:rgba(255,255,255,.8)}
.v4-c .pt-note{color:rgba(255,255,255,.6)}
.v4-c .btn{margin-top:24px}
@media (max-width:768px){ .v4-c{padding:24px} .v4-h{font-size:28px} }
''')

# =====================================================================
# 2.4.9.5  The photo. An editorial panel across the page: a real class
#          photo, a few plain facts, one invitation.
# =====================================================================
V['2.4.9.5'] = ('Personal training, the photo', r'''
  function ptLeft(){ return '' }
  function ptRight(){ return '' }
  function ptBand(href){
    return '<div class="v5"><img class="v5-img" src="assets/class-trx.webp" srcset="assets/class-trx-600.webp 600w, assets/class-trx.webp 900w" sizes="(max-width:768px) 100vw, 40vw" width="900" height="1200" alt="A member training on the TRX straps at Elite Wellness">'+
      '<div class="v5-t"><p class="pc-leg">Personal training</p>'+
      '<p class="v5-h">Made around you</p>'+
      '<p class="pt-p">One to one training with André, Joana or Ricardo, all qualified in physical education. Getting fitter, coming back from an injury, eating better: you say what you want, your coach plans it with you.</p>'+
      '<ul class="v5-facts">'+['A first talk with your coach at the gym','A plan and a price agreed together','One to one sessions from '+money(ptFrom)].map(function(x){ return '<li>'+x+'</li>' }).join('')+'</ul>'+
      '<div class="v5-go"><a class="btn" id="pt-wa" href="'+href+'" target="_blank" rel="noopener">Message us on WhatsApp</a>'+
      '<span class="pt-note">We reply and agree a time with you.</span></div></div></div>';
  }
''', r'''
.pt-band{margin-top:48px}
.v5{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:24px;background:#F4F4F2}
.v5-img{grid-column:1 / span 5;width:100%;height:100%;min-height:480px;object-fit:cover;object-position:50% 30%;display:block}
.v5-t{grid-column:6 / span 7;padding:48px 48px 48px 24px;align-self:center}
.v5-h{font-family:var(--font-display);font-size:56px;line-height:56px;text-transform:uppercase;margin-top:8px}
.v5-facts{list-style:none;margin:24px 0 0;padding:0}
.v5-facts li{position:relative;padding:8px 0 8px 32px;font-size:16px;line-height:24px}
.v5-facts li::before{content:"";position:absolute;left:4px;top:15px;width:12px;height:6px;border-left:2px solid var(--royal-blue);border-bottom:2px solid var(--royal-blue);transform:rotate(-45deg)}
.v5-go{display:flex;align-items:center;flex-wrap:wrap;gap:16px;margin-top:32px}
.v5-go .pt-note{margin:0}
@media (max-width:1100px){ .v5-img{grid-column:1 / span 5} .v5-t{padding:32px 32px 32px 0} .v5-h{font-size:44px;line-height:48px} }
@media (max-width:768px){
  .pt-band{margin-top:32px}
  .v5{display:block}
  .v5-img{height:240px;min-height:0}
  .v5-t{padding:24px}
  .v5-h{font-size:40px;line-height:40px}
}
''')


# =====================================================================
# 2.4.9.6  The photo banner of 2.4.9.5 with the chat of 2.4.9.3: photo,
#          the plain facts, and a chat window that ends in a centred
#          "book a time" button, with a phone call or a visit for people
#          who do not use WhatsApp.
# =====================================================================
V['2.4.9.6'] = ('PT, photo and chat', r"""
  var BOOK_MSG='Hi! I would like to book a time to talk to a coach about personal training.';
  function ptLeft(){ return '' }
  function ptRight(){ return '' }
  function ptBand(){
    var href=WA+encodeURIComponent(BOOK_MSG);
    var chat=[['me','Hi! I would like to start personal training. I want to get stronger after a knee injury.'],
              ['them','Happy to help! Can you come in to meet Joana and talk it through?'],
              ['me','Thursday after work?'],
              ['them','Thursday at 18:00 is booked. See you then!']];
    return '<div class="v6"><img class="v6-img" src="assets/class-trx.webp" srcset="assets/class-trx-600.webp 600w, assets/class-trx.webp 900w" sizes="(max-width:768px) 100vw, 30vw" width="900" height="1200" alt="A member training on the TRX straps at Elite Wellness">'+
      '<div class="v6-t"><p class="pc-leg">Personal training</p>'+
      '<p class="v6-h">Made around you</p>'+
      '<p class="pt-p">One to one training with André, Joana or Ricardo, all qualified in physical education. Getting fitter, coming back from an injury, eating better: you say what you want, your coach plans it with you.</p>'+
      '<ul class="v6-facts">'+['A first talk with your coach at the gym','A plan and a price agreed together','One to one sessions from '+money(ptFrom)].map(function(x){ return '<li>'+x+'</li>' }).join('')+'</ul></div>'+
      '<div class="v6-c"><div class="v6-top">'+face(COACHES[1])+'<span><b>Elite Wellness</b><small>WhatsApp</small></span></div>'+
        '<div class="v6-chat">'+chat.map(function(m){ return '<p class="v6-m '+m[0]+'">'+m[1]+'</p>' }).join('')+
        '<p class="v6-eg">How booking works, for example</p></div>'+
        '<div class="v6-cta"><a class="btn" id="pt-wa" href="'+href+'" target="_blank" rel="noopener">Book a time on WhatsApp</a>'+
        '<p class="v6-alt">No WhatsApp? <a href="tel:+351926565836">Call +351 926 565 836</a> or <a href="#find-us">come by reception</a>.</p></div>'+
      '</div></div>';
  }
""", r"""
.pt-band{margin-top:48px}
.v6{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:24px;background:#F4F4F2}
.v6-img{grid-column:1 / span 4;width:100%;height:100%;min-height:560px;object-fit:cover;object-position:50% 30%;display:block}
.v6-t{grid-column:5 / span 4;align-self:center;padding:48px 0}
.v6-h{margin-top:8px;font-family:var(--font-display);font-size:48px;line-height:48px;text-transform:uppercase}
.v6-facts{list-style:none;margin:24px 0 0;padding:0}
.v6-facts li{position:relative;padding:8px 0 8px 32px;font-size:16px;line-height:24px}
.v6-facts li::before{content:"";position:absolute;left:4px;top:15px;width:12px;height:6px;border-left:2px solid var(--royal-blue);border-bottom:2px solid var(--royal-blue);transform:rotate(-45deg)}
.v6-c{grid-column:9 / span 4;align-self:center;margin:48px 48px 48px 0;border-radius:16px;overflow:hidden;background:var(--white);box-shadow:0 8px 24px rgba(0,0,0,.08)}
.v6-top{display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--black);color:var(--white)}
.v6-top .pt-face{width:40px;height:40px;font-size:16px;box-shadow:none}
.v6-top b{display:block;font-size:14px;line-height:20px}
.v6-top small{display:block;font-size:12px;line-height:16px;color:rgba(255,255,255,.6)}
.v6-chat{display:flex;flex-direction:column;gap:8px;padding:16px;background:#ECE9E4}
.v6-m{max-width:85%;padding:8px 12px;font-size:14px;line-height:20px;border-radius:12px;box-shadow:0 1px 1px rgba(0,0,0,.08)}
.v6-m.me{align-self:flex-end;background:#DCF2D4;border-bottom-right-radius:4px}
.v6-m.them{align-self:flex-start;background:var(--white);border-bottom-left-radius:4px}
.v6-eg{margin-top:4px;font-size:12px;line-height:16px;color:#6A6A6A;text-align:center}
.v6-cta{padding:24px;text-align:center}
.v6-alt{margin-top:16px;font-size:13px;line-height:20px;color:#4A4A4A}
.v6-alt a{color:var(--royal-blue);font-weight:700;text-decoration:none;white-space:nowrap}
@media (hover:hover){ .v6-alt a:hover{text-decoration:underline;text-underline-offset:4px} }
@media (max-width:1100px){
  .v6-img{grid-column:1 / span 5;min-height:0}
  .v6-t{grid-column:6 / span 7;padding:32px 32px 32px 0}
  .v6-h{font-size:40px;line-height:40px}
  .v6-c{grid-column:1 / -1;margin:32px;justify-self:center;width:min(480px,100%)}
}
@media (max-width:768px){
  .pt-band{margin-top:32px}
  .v6{display:block}
  .v6-img{height:220px;min-height:0}
  .v6-t{padding:24px}
  .v6-h{font-size:40px;line-height:40px}
  .v6-c{width:auto;margin:0 16px 16px}
  .v6-cta{padding:24px 16px}
}
""")


# =====================================================================
# 2.4.9.7  The photo banner of 2.4.9.5, built around a picture of a
#          personal training session (a coach working with one person),
#          and a centred booking card with a call or a visit as backup.
#          The photo is a stock stand-in until the gym's own one is taken
#          (shot brief in the draft's notes); it goes through build/photo.py.
# =====================================================================
PT_PHOTO = 'https://images.unsplash.com/photo-1648542036561-e1d66a5ae2b1?q=80&w=1400&auto=format&fit=crop'
V['2.4.9.7'] = ('PT, session photo', r"""
  var BOOK_MSG='Hi! I would like to book a time to talk to a coach about personal training.';
  function ptLeft(){ return '' }
  function ptRight(){ return '' }
  function ptBand(){
    var href=WA+encodeURIComponent(BOOK_MSG);
    return '<div class="v7"><div class="v7-ph"><img class="v7-img" src="%(photo)s" alt="PLACEHOLDER: replace with a real photo of a personal training session at Elite Wellness, a coach working with one member"></div>'+
      '<div class="v7-t"><p class="pc-leg">Personal training</p>'+
      '<p class="v7-h">Made around you</p>'+
      '<p class="pt-p">Everyone starts from a different place. An injury to come back from, pain that holds you back, a goal you keep missing, or simply not knowing where to begin. Your coach looks at where you are, sets the goal with you and builds every session around it, so you progress safely and spend no time on what does not work for you.</p>'+
      '<p class="v7-lab">It helps with</p>'+
      '<ul class="v7-facts">'+['Coming back from an injury','Getting stronger and fitter','Training for a goal or event','Starting out with confidence'].map(function(x){ return '<li>'+x+'</li>' }).join('')+'</ul>'+
      '<p class="pt-p">That is also why there is no fixed price. You first talk it through with your coach, then agree a plan and its price. Sessions start at '+money(ptFrom)+'.</p>'+
      '<div class="v7-go"><a class="btn" id="pt-wa" href="'+href+'" target="_blank" rel="noopener">Book a time on WhatsApp</a>'+
        '<p class="v7-alt">No WhatsApp? <a href="tel:+351926565836">Call +351 926 565 836</a> or <a href="#find-us">come by reception</a>.</p></div>'+
      '</div></div>';
  }
""".replace('%(photo)s', PT_PHOTO), r"""
.pt-band{margin-top:48px}
.v7{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:24px;background:#F4F4F2}
.v7-ph{grid-column:1 / span 6;position:relative;min-height:560px;background:#222}
.v7-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 50%;filter:grayscale(100%) contrast(110%)}
.v7-t{grid-column:7 / span 6;align-self:center;padding:48px 48px 48px 24px}
.v7-h{margin-top:8px;font-family:var(--font-display);font-size:56px;line-height:56px;text-transform:uppercase}
.v7-lab{margin-top:24px;font-weight:800;font-size:11px;line-height:16px;letter-spacing:.14em;text-transform:uppercase;color:var(--silver-grey)}
.v7-facts{list-style:none;margin:8px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:24px}
.v7-facts li{position:relative;padding:8px 0 8px 32px;font-size:16px;line-height:24px;white-space:nowrap}
.v7-facts li::before{content:"";position:absolute;left:4px;top:15px;width:12px;height:6px;border-left:2px solid var(--royal-blue);border-bottom:2px solid var(--royal-blue);transform:rotate(-45deg)}
.v7-facts+.pt-p{margin-top:24px}
.v7-go{margin-top:32px}
.v7-alt{margin-top:16px;font-size:13px;line-height:20px;color:#4A4A4A}
.v7-alt a{color:var(--royal-blue);font-weight:700;text-decoration:none;white-space:nowrap}
@media (hover:hover){ .v7-alt a:hover{text-decoration:underline;text-underline-offset:4px} }
@media (max-width:1360px){ .v7-facts{grid-template-columns:1fr} }
@media (max-width:1100px){
  .v7-ph{grid-column:1 / span 5;min-height:0}
  .v7-t{grid-column:6 / span 7;padding:32px 32px 32px 0}
  .v7-h{font-size:44px;line-height:48px}
}
@media (max-width:768px){
  .pt-band{margin-top:32px}
  .v7{display:block}
  .v7-ph{height:240px}
  .v7-t{padding:24px}
  .v7-h{font-size:40px;line-height:40px}
  .v7-facts{grid-template-columns:1fr}
  .v7-facts li{font-size:15px}
}
@media (max-width:374px){ .v7-h{font-size:30px;line-height:32px} }
""")


def variant_css(extra):
    k = CSS.rindex('</style>')
    return CSS[:k] + COMMON_CSS + extra + CSS[k:]


if __name__ == '__main__':
    for name, (label, js, css) in V.items():
        out = make(BASE, variant_css(css), JS[:i] + '  /* PT:start (' + name + ': ' + label + ') */\n' + COMMON_JS + js + '  /* PT:end */\n' + JS[j:])
        f = 'elite-wellness-landing_%s.html' % name.replace('.', '-')
        io.open(f, 'w', encoding='utf-8').write(out)
        print(name, len(out))
