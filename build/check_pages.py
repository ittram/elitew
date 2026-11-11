# -*- coding: utf-8 -*-
"""The cross check for the two pages of the site, run before any change to
them is committed.

    python3 build/check_pages.py

The site is two plain pages: site/index.html (Portuguese, the main address)
and site/en/index.html (English). They must be the same page in two
languages. This check stops with an error when they are not:

1. The same structure: every heading, paragraph, button, link, image and
   question is in both pages, in the same order.
2. The same links, images and phone numbers (only the words differ).
3. Each page says its language and links to the other one.
4. Every word a script writes (WORDS in site/site.js) exists in both
   languages, and every price, class and review note has its Portuguese name.
5. No dash in the copy, and no sentence left in English on the Portuguese page.

Warnings are worth a look; errors block."""
import io, json, os, re, subprocess, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PT, EN = 'site/index.html', 'site/en/index.html'
errors, warnings = [], []
def err(t): errors.append(t)
def warn(t): warnings.append(t)

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
# the same in both languages, on purpose
SAME = {'Juntos Somos Elite', 'Livro de Reclamações', 'Rua Capitão Salgueiro Maia', 'Lote 13, Cave, 8600-530 Lagos',
        'Rua Capitão Salgueiro Maia, Lagos', 'Rua Capitão Salgueiro Maia, Lote 13, Cave', '8600-530 Lagos, Algarve, Portugal',
        'Lagos, Algarve, Portugal', 'André · Joana · Ricardo · Jorge', 'Elite Wellness by Santos',
        'Livro de Reclamações Eletrónico, abre numa nova janela'}


class Page(HTMLParser):
    """The page as a list of things in order: tags with their class and id, and the words between them."""
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.items, self.skip, self.where, self.lang = [], 0, 'the top of the page', None
        self.links, self.images, self.texts = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang')
        if tag in ('script', 'style'): self.skip += 1
        if a.get('id') and tag in ('section', 'footer', 'header', 'div', 'details'): self.where = '#' + a['id']
        self.items.append(('tag', tag, ' '.join(sorted((a.get('class') or '').split())), a.get('id') or '', self.getpos()[0], self.where))
        if tag == 'a' and a.get('href'): self.links.append((a['href'], self.getpos()[0]))
        if tag == 'img': self.images.append((a.get('src') or '', a.get('alt'), self.getpos()[0]))
        for k in ('alt', 'aria-label'):
            if a.get(k): self.texts.append((a[k], self.getpos()[0], self.where, k))

    def handle_startendtag(self, tag, attrs): self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        t = re.sub(r'\s+', ' ', data).strip()
        if t and not self.skip:
            self.items.append(('text', '', '', '', self.getpos()[0], self.where))
            self.texts.append((t, self.getpos()[0], self.where, 'text'))


def read(f):
    s = io.open(os.path.join(ROOT, f), encoding='utf-8').read()
    p = Page(); p.feed(s)
    return s, p


def show(i):
    return '<%s%s%s>' % (i[1], ' class="%s"' % i[2] if i[2] else '', ' id="%s"' % i[3] if i[3] else '') if i[0] == 'tag' else 'words'


def structure(pt, en):
    a = [(i[0], i[1], i[2], i[3]) for i in pt.items]
    b = [(i[0], i[1], i[2], i[3]) for i in en.items]
    if a == b:
        return
    n = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
    p = pt.items[n] if n < len(pt.items) else None
    e = en.items[n] if n < len(en.items) else None
    err('the two pages stop matching in %s:\n      Portuguese page, line %s: %s\n      English page, line %s: %s\n    One page has something the other lacks. Make the same change in both.' % (
        (p or e)[5], p[4] if p else 'end', show(p) if p else 'nothing more', e[4] if e else 'end', show(e) if e else 'nothing more'))


def norm(href):
    """A link without the part that differs by language: the folder step and the words of a WhatsApp message."""
    h = re.sub(r'^\.\./', '', href)
    h = re.sub(r'(wa\.me/\d+)\?text=.*$', r'\1?text=', h)
    return h


def links(pt, en):
    a = [norm(h) for h, _ in pt.links if 'lang-btn' not in h]
    b = [norm(h) for h, _ in en.links if 'lang-btn' not in h]
    a = [h for h in a if h not in ('en/', '')]
    b = [h for h in b if h not in ('en/', '')]
    for x, y in zip(a, b):
        if x != y:
            err('a link differs: Portuguese page has %s, English page has %s' % (x, y)); break
    for p, name in ((pt, 'Portuguese'), (en, 'English')):
        for h, line in p.links:
            if 'wa.me' in h and 'wa.me/351926565836' not in h: err('%s page, line %s: a WhatsApp link with the wrong number: %s' % (name, line, h[:60]))
            if h.startswith('tel:') and h != 'tel:+351926565836': err('%s page, line %s: a phone link with the wrong number: %s' % (name, line, h))
    ia = [re.sub(r'^\.\./', '', s) for s, _, _ in pt.images]
    ib = [re.sub(r'^\.\./', '', s) for s, _, _ in en.images]
    if ia != ib: err('the two pages do not show the same images, in the same order')
    for p, name in ((pt, 'Portuguese'), (en, 'English')):
        for src, alt, line in p.images:
            if alt is None: err('%s page, line %s: an image without a description (alt): %s' % (name, line, src))
            f = re.sub(r'^\.\./', '', src)
            if f.startswith('assets/') and '/team/' not in f and not os.path.exists(os.path.join(ROOT, 'site', f)):
                err('%s page, line %s: the image file is missing: %s' % (name, line, f))


def language(spt, sen, pt, en):
    if pt.lang != 'pt-PT': err('the Portuguese page must start with <html lang="pt-PT">, it has %r' % pt.lang)
    if en.lang != 'en': err('the English page must start with <html lang="en">, it has %r' % en.lang)
    if 'id="lang-btn" href="en/"' not in spt: err('the Portuguese page has no language button to en/')
    if 'id="lang-btn" href="../"' not in sen: err('the English page has no language button back to the Portuguese page')
    for s, name, base in ((spt, 'Portuguese', ''), (sen, 'English', '../')):
        for f in ('site.css', 'prices.js', 'schedule.js', 'reviews.js', 'site.js'):
            if ('"%s%s"' % (base, f)) not in s: err('the %s page does not load %s%s' % (name, base, f))
        if s.count('hreflang="pt-PT"') < 1 or s.count('hreflang="en"') < 1: err('the %s page does not name both languages for search engines (hreflang)' % name)
        if re.search(r'<style\b', s): warn('the %s page has styles of its own; styles belong in site/site.css so both pages get them' % name)
        if re.search(r'<script\b(?![^>]*(?:src=|ld\+json))[^>]*>(?!/\* 2\.8)', s): warn('the %s page has a script of its own; scripts belong in site/site.js so both pages get them' % name)


def copy(pt, en):
    for p, name in ((pt, 'Portuguese'), (en, 'English')):
        for t, line, where, kind in p.texts:
            if u'—' in t or u'–' in t or ' - ' in t:
                err('%s page, line %s (%s): a dash in the copy: "%s"' % (name, line, where, t[:70]))
    # a sentence that is word for word the same in both pages was probably not translated
    english = {t for t, _, _, k in en.texts}
    for t, line, where, kind in pt.texts:
        if t in english and t not in SAME and len(t.split()) >= 3 and not re.fullmatch(r'[\d\s:+·().,/-]+', t) and '[PLACEHOLDER' not in t:
            warn('Portuguese page, line %s (%s): the same words as the English page, not translated? "%s"' % (line, where, t[:70]))


def node(code):
    return json.loads(subprocess.run(['node', '-e', code], capture_output=True, text=True, check=True, cwd=ROOT).stdout)


def words():
    """Every word a script writes must be there in both languages, and of the same kind."""
    js = io.open(os.path.join(ROOT, 'site', 'site.js'), encoding='utf-8').read()
    m = re.search(r'var WORDS=\{.*?\n\};\n', js, re.S)
    if not m: err('site/site.js: the WORDS table was not found'); return
    shape = node(m.group(0) + '''
      function shape(o){ if(typeof o==='function') return 'fn'+o.length; if(Array.isArray(o)) return o.map(shape); if(o&&typeof o==='object'){ var r={}; Object.keys(o).sort().forEach(function(k){ r[k]=shape(o[k]) }); return r } return typeof o }
      process.stdout.write(JSON.stringify({en:shape(WORDS.en),pt:shape(WORDS.pt)}))''')
    def walk(a, b, path):
        if isinstance(a, dict) and isinstance(b, dict):
            for k in sorted(set(a) | set(b)):
                if k not in a: err('site/site.js: "%s" is in the Portuguese words but not in the English ones' % (path + k))
                elif k not in b: err('site/site.js: "%s" is in the English words but not in the Portuguese ones' % (path + k))
                else: walk(a[k], b[k], path + k + '.')
        elif a != b:
            err('site/site.js: "%s" is not the same kind of thing in both languages' % path.rstrip('.'))
    walk(shape['en'], shape['pt'], '')


def data():
    d = node('''global.window={};["prices.js","schedule.js","reviews.js"].forEach(function(f){eval(require("fs").readFileSync(f,"utf8"))});
      process.stdout.write(JSON.stringify({p:window.ELITE_PRICES,s:window.ELITE_SCHEDULE,r:window.ELITE_REVIEWS}))''')
    P, S, R = d['p'], d['s'], d['r']
    for x in P['member']['plans'] + P['visitor']:
        if not x.get('namePt'): err('prices.js: "%s" has no Portuguese name (namePt)' % x['name'])
    for k, c in S['classes'].items():
        if not c.get('pt'): err('schedule.js: the class %s has no Portuguese line (pt)' % c['name'])
        if c.get('about') and not c.get('aboutPt'): err('schedule.js: the class %s is described in English only (aboutPt is missing)' % c['name'])
        if c.get('aboutPt') and not c.get('about'): err('schedule.js: the class %s is described in Portuguese only (about is missing)' % c['name'])
    for r in R['reviews']:
        if r.get('note') and not r.get('notePt'): err('reviews.js: the note on %s\'s review has no Portuguese (notePt)' % r['name'])
        if not r.get('url'): warn('reviews.js: %s\'s review has no link of its own, so its card opens the gym\'s page on Google' % r['name'])


if __name__ == '__main__':
    spt, pt = read(PT); sen, en = read(EN)
    structure(pt, en); links(pt, en); language(spt, sen, pt, en); copy(pt, en); words(); data()
    print('Portuguese page: %d things, English page: %d things' % (len(pt.items), len(en.items)))
    for w_ in warnings: print('warning:', w_)
    for e in errors: print('ERROR:', e)
    print('\n%s' % ('Not ready: fix the errors above.' if errors else 'The two pages are the same page in two languages.'))
    sys.exit(1 if errors else 0)
