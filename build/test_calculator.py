# -*- coding: utf-8 -*-
"""Clicks through the price calculator in a real browser and checks every
total against prices.js, worked out here independently of the page's code.

    python3 build/test_calculator.py                 # the latest draft, phone and desktop
    python3 build/test_calculator.py 2-4-8 2-4-6     # or the drafts named

Runs in the cloud sandbox (Playwright with Chromium). Serves this folder on
a local port by itself. For drafts whose calculator is built from radio
buttons in #pc-opts (2.4.6 and later)."""
import functools, http.server, json, os, re, subprocess, sys, threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.loads(subprocess.check_output(['node', '-e',
    "global.window={};require('./prices.js');process.stdout.write(JSON.stringify(window.ELITE_PRICES))"], cwd=ROOT))


def m(n):
    s = '%.2f' % n
    return '€' + (s[:-3] if s.endswith('.00') else s)


def cases():
    """(name, clicks, insured, expected total) for every price on the list."""
    out = []
    for v in P['visitor']:
        out.append(('pass ' + v['name'], [('kind', 'pass'), ('stay', v['id'])], False, v['price']))
    for p in P['member']['plans']:
        for pay, rate in (('dd', p['dd']), ('desk', p['desk'])):
            out.append(('%s, %s' % (p['name'], pay), [('kind', 'mem'), ('plan', p['id']), ('pay', pay)], False, rate + P['insurance']['year']))
    p = P['member']['plans'][-1]
    out.append(('%s, dd, insurance already paid' % p['name'], [('kind', 'mem'), ('plan', p['id']), ('pay', 'dd')], True, p['dd']))
    for k in P['pt']['packs']:
        out.append(('pt ' + k['name'], [('kind', 'pt'), ('pack', k['id'])], False, k['sessions'] * k['each']))
    for a in P.get('assessments', {}).get('packs', []):
        out.append(('assessment ' + a['name'], [('kind', 'as'), ('asmt', a['id'])], False, a['price']))
    return out


def latest():
    idx = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    f = re.search(r"\{ v:'[^']+', file:'([^']+)'[^}]*?status:'latest'", idx).group(1)
    return re.sub(r'^elite-wellness-landing_|\.html$', '', f)


def main():
    from playwright.sync_api import sync_playwright
    drafts = sys.argv[1:] or [latest()]
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    handler = functools.partial(Quiet, directory=ROOT)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = 'http://127.0.0.1:%d/' % srv.server_port
    fails, runs = [], 0
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium'))
        for d in drafts:
            for w in (390, 1440):
                for name, clicks, insured, want in cases():
                    pg = b.new_page(viewport={'width': w, 'height': 844 if w < 500 else 900}, is_mobile=w < 500, has_touch=w < 500)
                    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
                    pg.goto(base + 'elite-wellness-landing_%s.html' % d); pg.wait_for_timeout(500)
                    tag = '%s %d %s' % (d, w, name)
                    missing = None
                    for c in clicks:                             # each choice appears once the one before is made
                        r = pg.locator('#pc-opts input[name="%s"][value="%s"]' % c)
                        if not r.count():
                            missing = c; break
                        r.locator('xpath=..').click(); pg.wait_for_timeout(120)
                    if missing:
                        if missing == ('kind', 'as'):
                            pg.close(); continue                 # this draft has no assessments product
                        fails.append('%s: no choice %s' % (tag, missing)); pg.close(); continue
                    if insured:
                        pg.click('.pc-ins'); pg.wait_for_timeout(120)
                    got = pg.evaluate("(document.querySelector('.pc-total b')||{}).textContent")
                    runs += 1
                    if got != m(want): fails.append('%s: page says %s, prices.js says %s' % (tag, got, m(want)))
                    if errs: fails.append('%s: script error %s' % (tag, errs))
                    pg.close()
        b.close()
    srv.shutdown()
    print('%d totals checked in %s at 390 and 1440 wide' % (runs, ', '.join(drafts)))
    for f in fails: print('FAIL:', f)
    print('All totals match prices.js.' if not fails else 'Not ready.')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
