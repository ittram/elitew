# -*- coding: utf-8 -*-
"""The cross check for prices.js, run before a price change is committed.

    python3 build/check_prices.py            # compares with the last commit
    python3 build/check_prices.py HEAD~1     # or with any other version

1. Prints the price list in the printed sheet's own words and order, to read
   against the photo of the sheet line by line.
2. Lists every price that changed since the last commit.
3. Checks the arithmetic the page relies on (the direct debit discount is the
   same on every plan, pack totals are sessions x price a session, longer
   passes cost more, and so on).
4. Checks every live draft: its full price list and the prices in its copy
   must be what build/pricelist.py writes now, and no other euro amount may
   appear anywhere on the page.
Stops with errors for anything wrong on the page; warnings are worth a look.
The calculator itself is tested in a browser by build/test_calculator.py."""
import io, math, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pricelist as PL

ROOT = PL.ROOT
m = PL.m
errors, warnings = [], []
def err(t): errors.append(t)
def warn(t): warnings.append(t)


def sheet(P):
    w = 44
    out = ['LIVRE (GINÁSIO + AULAS)%s%s%s' % (' ' * (w - 23), 'débito direto'.rjust(14), 'balcão'.rjust(10))]
    for p in P['member']['plans']:
        out.append('  %-*s%14s%10s' % (w - 2, p['pt'], '%.2f€' % p['dd'], '%.2f€' % p['desk']))
    out.append('VISITANTES (insurance included)')
    for v in P['visitor']:
        out.append('  %-*s%14s' % (w - 2, v['pt'], '%.2f€' % v['price']))
    if P.get('assessments'):
        out.append('PACK AVALIAÇÕES FÍSICAS')
        for a in P['assessments']['packs']:
            out.append('  %-*s%14s' % (w - 2, a['pt'], '%.2f€' % a['price']))
    out.append('PT, TREINO PERSONALIZADO (por sessão)%s%s' % (' ' * (w - 37), 'total'.rjust(24)))
    for k in P['pt']['packs']:
        out.append('  %-*s%14s%10s' % (w - 2, k['pt'], '%.2f€' % k['each'], '%.2f€' % k['total']))
    out.append('  %-*s%14s' % (w - 2, 'Pessoa extra', '%.2f€' % P['pt']['second']))
    out.append('SEGURO (members, once a year)%s%14s' % (' ' * (w - 29), '%.2f€' % P['insurance']['year']))
    return '\n'.join(out)


def flat(P):
    """Every price as label -> value, for the change list."""
    d = {'insurance': P['insurance']['year'], 'pt extra person': P['pt']['second'], 'dd saving a year': P['member']['ddSavingYear']}
    for p in P['member']['plans']:
        d[p['name'] + ' direct debit'] = p['dd']; d[p['name'] + ' at reception'] = p['desk']
    for v in P['visitor']:
        d['pass ' + v['name']] = v['price']
    for k in P['pt']['packs']:
        d['pt ' + k['name'] + ' a session'] = k['each']; d['pt ' + k['name'] + ' total'] = k['total']
    for a in P.get('assessments', {}).get('packs', []):
        d['assessment ' + a['name']] = a['price']
    return d


def arithmetic(P):
    plans = P['member']['plans']
    offs = {round(p['desk'] - p['dd'], 2) for p in plans}
    for p in plans:
        if p['dd'] >= p['desk']: err('%s: direct debit must be below the reception price' % p['name'])
    if len(offs) != 1: err('the direct debit discount differs between plans %s; the page says one amount' % sorted(offs))
    off = offs.pop() if offs else 0
    if abs(P['member']['ddSavingYear'] - off * 26) > 0.005:
        err('ddSavingYear is %s but %s x 26 payments is %s' % (m(P['member']['ddSavingYear']), m(off), m(off * 26)))
    if [p['desk'] for p in plans] != sorted(p['desk'] for p in plans): warn('plans are not in order of price')
    V = P['visitor']
    for a, b in zip(V, V[1:]):
        if not (a['days'] < b['days'] and a['price'] < b['price']): err('passes: %s and %s are out of order' % (a['name'], b['name']))
    day, week = V[0]['price'], V[1]['price']
    if week >= 7 * day: err('the week pass costs as much as seven day passes')
    k = P['pt']['packs']
    for x in k:
        if abs(x['each'] * x['sessions'] - x['total']) > 0.005:
            err('pt %s: %d x %s is %s, not %s' % (x['name'], x['sessions'], m(x['each']), m(x['each'] * x['sessions']), m(x['total'])))
        if x['sessions'] > 1 and not x.get('months'): err('pt %s: says nothing about how long it is valid' % x['name'])
    for a, b in zip(k, k[1:]):
        if not b['each'] < a['each']: err('pt: %s does not cost less a session than %s' % (b['name'], a['name']))
    for a in P.get('assessments', {}).get('packs', []):
        if not (a['price'] > 0 and a.get('months')): err('assessment %s needs a price and months' % a['name'])
    for label, v in flat(P).items():
        if abs(v * 100 - round(v * 100)) > 1e-6 or v < 0: err('%s: %r is not a price in euro and cent' % (label, v))
    un = max(plans, key=lambda p: p['desk'])
    member4 = un['dd'] * 2 + P['insurance']['year']
    print('\nWhat the page works out from these:')
    print('  direct debit takes %s off each payment, %s a year' % (m(off), m(off * 26)))
    print('  from %s days on, the week pass costs less than day passes' % math.ceil(week / day))
    print('  four weeks: %s as a visitor, %s as an Unlimited member by direct debit with the insurance' % (m(V[-1]['price']), m(member4)))
    if member4 >= V[-1]['price']: warn('four weeks of membership is not cheaper than the 4 week pass; the pass note on the page reads oddly then')


def pages(P):
    allowed = set(round(v, 2) for v in flat(P).values()) | {0.0}
    off = P['member']['plans'][0]['desk'] - P['member']['plans'][0]['dd']
    allowed.add(round(off, 2))
    for f in PL.live_drafts():
        name = PL.draft_name(f)
        s = io.open(os.path.join(ROOT, f), encoding='utf-8').read()
        if PL.render(s, name, P) != s:
            err('%s: the price list or the prices in the copy are out of date; run python3 build/pricelist.py' % name)
        body = re.sub(r'<!-- price-list:start.*?<!-- price-list:end -->', '', s, flags=re.S)
        # code must read prices.js; the search engines' data block (ld+json) is text written by pricelist.py
        code = lambda t: 'ld+json' not in t
        for attrs, sc in re.findall(r'<script\b([^>]*)>(.*?)</script>', body, re.S):
            if code(attrs):
                for x in re.findall(r'€\s?\d[\d.,]*', sc):
                    err('%s: a price is written into a script (%s); scripts must read prices.js' % (name, x))
        text = re.sub(r'<script\b(?![^>]*ld\+json)[^>]*>.*?</script>', '', body, flags=re.S)
        for mo in re.finditer(r'€\s?(\d+(?:[.,]\d{1,2})?)', text):
            v = round(float(mo.group(1).replace(',', '.')), 2)
            if v not in allowed:
                ctx = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', text[max(0, mo.start() - 60):mo.end() + 20])).strip()
                err('%s: %s is not a price in prices.js: "%s"' % (name, m(v), ctx))
        print('  %s checked' % name)


if __name__ == '__main__':
    rev = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'
    P = PL.load()
    print('Price list from prices.js, updated %s, in the order of the printed sheet:\n' % P['updated'])
    print(sheet(P))
    try:
        old = PL.load(subprocess.run(['git', 'show', rev + ':prices.js'], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
        a, b = flat(old), flat(P)
        ch = ['  %s: %s -> %s' % (k, m(a[k]) if k in a else 'new', m(b[k]) if k in b else 'removed')
              for k in list(b) + [k for k in a if k not in b] if a.get(k) != b.get(k)]
        print('\nChanged since %s:' % rev); print('\n'.join(ch) if ch else '  nothing')
    except subprocess.CalledProcessError:
        print('\n(no %s version to compare with)' % rev)
    arithmetic(P)
    print('\nLive drafts:')
    pages(P)
    todos = [v.get('todo') for v in P['visitor'] if v.get('todo')] + list(P.get('unconfirmed', {}).values()) + \
            [P.get('assessments', {}).get('todo')]
    print('\nStill open (shown as todo chips or kept for the family):')
    for t in filter(None, todos): print('  ' + t)
    for w_ in warnings: print('warning:', w_)
    for e in errors: print('ERROR:', e)
    print('\n%s' % ('Not ready: fix the errors above.' if errors else 'prices.js, the arithmetic and every live draft agree.'))
    sys.exit(1 if errors else 0)
