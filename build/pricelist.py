# -*- coding: utf-8 -*-
"""Writes everything on the page that comes from prices.js but is not drawn by
the calculator: the fold-open full price list under the calculator, and the
prices quoted in the copy (meta description, the search engines' price range,
the menu line, the FAQ answers, the legal line). Safe to run again: it
replaces its own block and rewrites the same phrases.

    python3 build/pricelist.py            # every live draft that loads prices.js
    python3 build/pricelist.py 2-4-8      # or the drafts named

Run it after changing prices.js, and after rebuilding any draft. Then run
build/check_prices.py."""
import io, json, os, re, subprocess, sys, html
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(source=None):
    js = source if source is not None else io.open(os.path.join(ROOT, 'prices.js'), encoding='utf-8').read()
    out = subprocess.run(['node', '-e', "global.window={};eval(require('fs').readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(window.ELITE_PRICES))"],
                         input=js, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def m(n, lang='en'):
    """12 is €12 on the English page and 12 € on the Portuguese one; 40.9 is €40.90 and 40,90 €."""
    s = '%.2f' % n
    s = s[:-3] if s.endswith('.00') else s
    return s.replace('.', ',') + u' €' if lang == 'pt' else '€' + s


def todo(t):
    return '<span class="pr-todo" title="%s">todo</span>' % html.escape(t, quote=True)


# the words of the full price list, once for each page
LIST = {
    'en': dict(show='See the full price list', hide='Hide the full price list',
               passes='Day and week passes', passes_s='No commitment. Gym, classes and insurance included.',
               mem='Membership', mem_s='Paid every 2 weeks, plus %s sports insurance once a year.',
               desk='At reception', dd='Direct debit', best='Recommended',
               mem_n='Direct debit takes %s off every payment, %s a year.',
               pt='Personal training', pt_s='One to one, planned around you.', pt_row='A session', pt_from='from %s',
               pt_n='The price is agreed with your coach. <a href="%s" target="_blank" rel="noopener">Book a time on WhatsApp</a>.',
               wa='Hi! I would like to book a time to talk to a coach about personal training.',
               pt_s2='One to one with a coach.', total='Total', valid='%s, valid %d months',
               pt_n2='Bring someone with you and the second person is %s a session. %s',
               assess='Assessments', assess_s='Packs for training or nutrition.', months='%s, %d months'),
    'pt': dict(show='Ver a tabela de preços completa', hide='Esconder a tabela de preços',
               passes='Passes diários e semanais', passes_s='Sem compromisso. Ginásio, aulas e seguro incluídos.',
               mem='Adesão', mem_s='Paga a cada 2 semanas, mais o seguro desportivo de %s uma vez por ano.',
               desk='Na receção', dd='Débito direto', best='Recomendado',
               mem_n='O débito direto tira %s a cada pagamento, %s por ano.',
               pt='Treino personalizado', pt_s='Individual, planeado à tua medida.', pt_row='Uma sessão', pt_from='desde %s',
               pt_n='O preço é combinado com o teu treinador. <a href="%s" target="_blank" rel="noopener">Marca pelo WhatsApp</a>.',
               wa='Olá! Gostava de marcar uma conversa com um treinador sobre treino personalizado.',
               pt_s2='Individual, com um treinador.', total='Total', valid='%s, válido %d meses',
               pt_n2='Traz alguém contigo e a segunda pessoa paga %s por sessão. %s',
               assess='Avaliações', assess_s='Packs de treino ou nutrição.', months='%s, %d meses'),
}


def nm(x, lang):
    return x.get('namePt', x['name']) if lang == 'pt' else x['name']


def list_html(P, lang='en'):
    W = LIST[lang]
    mm = lambda n: m(n, lang)
    rows_pass = ''.join('<tr><th scope="row">%s</th><td>%s%s</td></tr>' % (nm(v, lang), mm(v['price']), todo(v['todo']) if v.get('todo') else '') for v in P['visitor'])
    # reception is the normal price and comes first; direct debit is the discount off it
    rows_mem = ''.join('<tr><th scope="row">%s%s</th><td class="std">%s</td><td>%s</td></tr>' % (
        nm(p, lang), ' <span class="pl-tag">%s</span>' % W['best'] if p.get('best') else '', mm(p['desk']), mm(p['dd'])) for p in P['member']['plans'])
    rows_pt = ''.join('<tr><th scope="row">%s</th><td class="dim">%s</td><td>%s</td></tr>' % (
        nm(k, lang) if k['sessions'] == 1 else W['valid'] % (nm(k, lang), k['months']), mm(k['each']), mm(k['total'])) for k in P['pt']['packs'])
    A = P.get('assessments')
    grp_as = ''
    if A and A.get('onSite', True):
        rows_as = ''.join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (W['months'] % (nm(a, lang), a['months']), mm(a['price'])) for a in A['packs'])
        grp_as = ('''
      <section class="pl-grp" aria-label="%s">
        <h3 class="pl-h">%s</h3>
        <p class="pl-s">%s%s</p>
        <table class="pl-t"><tbody>%s</tbody></table>
      </section>''' % (W['assess'], W['assess'], W['assess_s'], todo(A['todo']) if A.get('todo') else '', rows_as))
    off = P['member']['plans'][0]['desk'] - P['member']['plans'][0]['dd']
    if P['pt'].get('quote'):
        # personal training is agreed with the coach: only where it starts, and how to get in touch
        wa = 'https://wa.me/351926565836?text=' + urllib.parse.quote(W['wa'], safe='!')
        grp_pt = '''
      <section class="pl-grp" aria-label="%s">
        <h3 class="pl-h">%s</h3>
        <p class="pl-s">%s</p>
        <table class="pl-t"><tbody><tr><th scope="row">%s</th><td>%s</td></tr></tbody></table>
        <p class="pl-n">%s</p>
      </section>''' % (W['pt'], W['pt'], W['pt_s'], W['pt_row'], W['pt_from'] % mm(min(k['each'] for k in P['pt']['packs'])), W['pt_n'] % wa)
    else:
        grp_pt = '''
      <section class="pl-grp" aria-label="%s">
        <h3 class="pl-h">%s</h3>
        <p class="pl-s">%s</p>
        <table class="pl-t"><thead><tr><td></td><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table>
        <p class="pl-n">%s</p>
      </section>''' % (W['pt'], W['pt'], W['pt_s2'], W['pt_row'], W['total'], rows_pt, W['pt_n2'] % (mm(P['pt']['second']), P['pt']['note']))
    return '''<!-- price-list:start (generated by build/pricelist.py from prices.js) -->
  <details class="pl" id="price-list">
    <summary class="pl-sum"><span class="pl-show">%(show)s</span><span class="pl-hide">%(hide)s</span></summary>
    <div class="pl-body">
      <section class="pl-grp" aria-label="%(passes)s">
        <h3 class="pl-h">%(passes)s</h3>
        <p class="pl-s">%(passes_s)s</p>
        <table class="pl-t"><tbody>%(pass)s</tbody></table>
      </section>
      <section class="pl-grp" aria-label="%(mem)s">
        <h3 class="pl-h">%(mem)s</h3>
        <p class="pl-s">%(mem_s)s</p>
        <table class="pl-t"><thead><tr><td></td><th scope="col">%(desk)s</th><th scope="col">%(dd)s</th></tr></thead><tbody>%(rows_mem)s</tbody></table>
        <p class="pl-n">%(mem_n)s</p>
      </section>%(ptg)s%(as)s
    </div>
  </details>
<!-- price-list:end -->
  ''' % {'show': W['show'], 'hide': W['hide'], 'passes': W['passes'], 'passes_s': W['passes_s'], 'mem': W['mem'],
         'mem_s': W['mem_s'] % mm(P['insurance']['year']), 'desk': W['desk'], 'dd': W['dd'],
         'mem_n': W['mem_n'] % (mm(off), mm(P['member']['ddSavingYear'])),
         'pass': rows_pass, 'rows_mem': rows_mem, 'ptg': grp_pt, 'as': grp_as}


def every_price(P):
    A = P.get('assessments', {})
    return [v['price'] for v in P['visitor']] + [p['desk'] for p in P['member']['plans']] + \
           ([min(k['each'] for k in P['pt']['packs'])] if P['pt'].get('quote') else [k['total'] for k in P['pt']['packs']]) + \
           ([a['price'] for a in A.get('packs', [])] if A.get('onSite', True) else [])


def copy_rules(P, lang='en'):
    """The phrases in the page copy that quote a price, and what they must say."""
    day, week = P['visitor'][0]['price'], P['visitor'][1]['price']
    low = min(p['dd'] for p in P['member']['plans'])
    every = every_price(P)
    if lang == 'pt':
        amt = u'\\d+(?:,\\d{2})?[  ]€'
        mm = lambda n: m(n, 'pt')
        return [
            (r'(?i)(passe diário(?: custa)? )' + amt, lambda g: g.group(1) + mm(day)),
            (r'(?i)(passe semanal(?: custa)? )' + amt, lambda g: g.group(1) + mm(week)),
            (r'(?i)(adesão desde )' + amt, lambda g: g.group(1) + mm(low)),
            (r'(a cada 2 semanas, desde )' + amt, lambda g: g.group(1) + mm(low)),
            (r'(seguro desportivo de )' + amt, lambda g: g.group(1) + mm(P['insurance']['year'])),
            (r'"priceRange":"[^"]*"', lambda g: '"priceRange":"%s a %s"' % (mm(min(every)), mm(max(every)))),
        ]
    return [
        (r'(?i)(day pass(?: is)? )€[\d.]+', r'\g<1>' + m(day)),
        (r'(?i)(week pass(?: is)? )€[\d.]+', r'\g<1>' + m(week)),
        (r'(?i)((?:membership|member plans|members) from )€[\d.]+', r'\g<1>' + m(low)),
        (r'(every 2 weeks, from )€[\d.]+', r'\g<1>' + m(low)),
        (r'(the )€[\d.]+( (?:sports )?insurance)', r'\g<1>' + m(P['insurance']['year']) + r'\g<2>'),
        (r'"priceRange":"€[\d.]+ to €[\d.]+"', '"priceRange":"%s to %s"' % (m(min(every)), m(max(every)))),
    ]


def sync_copy(s, P, lang='en'):
    for pat, rep in copy_rules(P, lang):
        s = re.sub(pat, rep, s)
    return s


# the site itself: two plain pages, one for each language. Their styles and scripts are in
# site/site.css and site/site.js, so here only the list and the prices in the copy are written
SITE = [('site/index.html', 'pt'), ('site/en/index.html', 'en')]


def render_site(s, P, lang):
    s = re.sub(r'<!-- price-list:start.*?<!-- price-list:end -->\n  ', '', s, flags=re.S)
    assert s.count('<!-- price-list:here -->') == 1, lang
    s = s.replace('<!-- price-list:here -->', list_html(P, lang) + '<!-- price-list:here -->', 1)
    return sync_copy(s, P, lang)


def live_drafts():
    """Drafts on the version bar (not archived) whose page loads prices.js."""
    idx = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    out = []
    for e in re.findall(r"\{ v:'[^']+', file:'([^']+)'(.*?)\}", idx, re.S):
        f, rest = e
        if 'archived:true' in rest.split('tested:')[0]:
            continue
        p = os.path.join(ROOT, f)
        if os.path.exists(p) and 'src="prices.js"' in io.open(p, encoding='utf-8').read():
            out.append(f)
    return out

CSS = '''<style id="price-list-css">
/* the full price list: a fold-open table under the calculator, generated from prices.js */
.pl{margin:64px 0 0}
.pl-sum{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:18px 0;box-shadow:inset 0 1px 0 var(--black),inset 0 -1px 0 var(--light-grey);cursor:pointer;font-weight:800;font-size:12px;line-height:16px;letter-spacing:.12em;text-transform:uppercase;color:var(--black)}
.pl-sum::-webkit-details-marker{display:none}
.pl-sum::after{content:"";flex:0 0 auto;width:8px;height:8px;border-right:2px solid var(--royal-blue);border-bottom:2px solid var(--royal-blue);transform:rotate(45deg);margin:-4px 4px 0 0;transition:transform .2s}
.pl[open] .pl-sum::after{transform:rotate(225deg);margin-top:4px}
.pl-hide,.pl[open] .pl-show{display:none}
.pl[open] .pl-hide{display:inline}
.pl-sum:hover span{text-decoration:underline;text-underline-offset:4px}
.pl-sum:focus-visible{outline:2px solid var(--royal-blue);outline-offset:4px}
.pl-body{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(380px,100%),1fr));column-gap:48px}
.pl-grp{margin-top:32px;min-width:0}
.pl-h{font-family:var(--font-display);font-weight:400;font-size:24px;line-height:1;text-transform:uppercase}
.pl-s{font-size:13px;line-height:20px;color:var(--silver-grey);margin:6px 0 12px}
.pl-t{width:100%;border-collapse:collapse;font-size:15px;line-height:22px}
.pl-t th,.pl-t td{padding:10px 0;box-shadow:inset 0 -1px 0 var(--light-grey);text-align:right;font-weight:700;white-space:nowrap;vertical-align:baseline}
.pl-t tbody th{text-align:left;font-weight:400;white-space:normal;padding-right:16px}
.pl-t thead th{font-weight:800;font-size:10px;line-height:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--silver-grey);padding:0 0 8px}
.pl-t thead td,.pl-t thead th{box-shadow:inset 0 -1px 0 var(--black)}
.pl-t td+td,.pl-t th+th{padding-left:24px}
.pl-t .dim{color:var(--silver-grey);font-weight:400}
.pl-t .std{font-weight:400;color:#3a3a3a}
.pl-tag{display:inline-block;background:var(--accent);color:var(--black);font-weight:800;font-size:9px;line-height:14px;letter-spacing:.1em;text-transform:uppercase;padding:1px 5px;margin-left:6px;vertical-align:1px}
.pl-n{font-size:12px;line-height:18px;color:var(--silver-grey);margin-top:10px}
@media (max-width:768px){ .pl{margin-top:40px} .pl-t{font-size:14px} .pl-t td+td,.pl-t th+th{padding-left:16px} .pl-grp{margin-top:28px} }
%(extra)s</style>
'''

JS = '''<script id="price-list-js">
/* open the list when someone arrives at #price-list, and count who prefers the table */
(function(){
  var d=document.getElementById('price-list'); if(!d) return;
  function hash(){ if(location.hash==='#price-list') d.open=true }
  hash(); window.addEventListener('hashchange',hash);
  d.addEventListener('toggle',function(){ if(window.EWPricing) window.EWPricing.track(d.open?'pricing_list_open':'pricing_list_close',{}) });
})();
</script>
'''

def strip(s):
    s = re.sub(r'<!-- price-list:start.*?<!-- price-list:end -->\n  ', '', s, flags=re.S)
    s = re.sub(r'<style id="price-list-css">.*?</style>\n', '', s, flags=re.S)
    s = re.sub(r'<script id="price-list-js">.*?</script>\n', '', s, flags=re.S)
    return s

# the steps draft is a narrow centred column, so its list matches that width
EXTRA = {'2-4-5-4-1': '#prices .pl{max-width:760px;margin:48px auto 0}\n', '2-4-5-4-2': '#prices .pl{max-width:760px;margin:48px auto 0}\n'}



def render(s, name, P):
    s = strip(s)
    # the list goes in right before the legal line; a page without that line marks the place instead
    here = [a for a in ('<p class="pr-legal">', '<!-- price-list:here -->') if a in s]
    assert len(here) == 1 and s.count(here[0]) == 1, name
    s = s.replace(here[0], list_html(P) + here[0], 1)
    s = s.replace('</head>', CSS.replace('%(extra)s', EXTRA.get(name, '')) + '</head>', 1)
    s = s.replace('</body>', JS + '</body>', 1)
    return sync_copy(s, P)


def draft_name(f):
    return re.sub(r'^elite-wellness-landing_|\.html$', '', os.path.basename(f))


if __name__ == '__main__':
    P = load()
    files = ['elite-wellness-landing_%s.html' % a for a in sys.argv[1:]] or live_drafts()
    for f in files:
        p = os.path.join(ROOT, f)
        out = render(io.open(p, encoding='utf-8').read(), draft_name(f), P)   # read before opening for write
        io.open(p, 'w', encoding='utf-8').write(out)
        print(draft_name(f), 'price list and copy written from prices.js')
    if len(sys.argv) == 1:
        for f, lang in SITE:
            p = os.path.join(ROOT, f)
            if os.path.exists(p):
                out = render_site(io.open(p, encoding='utf-8').read(), P, lang)
                io.open(p, 'w', encoding='utf-8').write(out)
                print(f, 'price list and copy written from prices.js')
