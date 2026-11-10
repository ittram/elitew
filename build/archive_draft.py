# -*- coding: utf-8 -*-
"""Moves archived drafts out of the root into archive/<folder>/, so the root
holds only the current page and the experiments sit together by what they
tested.

    python3 build/archive_draft.py prices-5-empty-screen 2.5.1 2.5.2 2.5.5

For each version it: moves the file with git mv (history follows it), rewrites
the page's links to the shared files (assets/, prices.js, pricing.js and .css,
pricing-disclose.js and .css, reviews.js, schedule.js) so they point two
folders up, and updates the draft's `file:` in index.html. It does not touch
`archived`, `group` or `why` in index.html: write those by hand, the folder
name here must be the one the group has in GROUPS.

Run from anywhere. Then open the draft from the Archive panel to see it loads."""
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED = r'(?:assets/|prices\.js|pricing\.js|pricing\.css|pricing-disclose\.js|pricing-disclose\.css|reviews\.js|schedule\.js)'
UP = '../../'


def rewrite(s):
    """Point every link to a shared file two folders up. Only inside quotes,
    url( ) and the later entries of a srcset, so words in comments stay put."""
    s = re.sub(r'''(?<=["'(])(?=%s)''' % SHARED, UP, s)
    s = re.sub(r'(?<=[0-9][wx], )(?=assets/)', UP, s)
    return s


def name(v):
    return 'elite-wellness-landing_%s.html' % v.replace('.', '-')


def main():
    folder, versions = sys.argv[1], sys.argv[2:]
    dest = os.path.join(ROOT, 'archive', folder)
    os.makedirs(dest, exist_ok=True)
    ip = os.path.join(ROOT, 'index.html')
    idx = io.open(ip, encoding='utf-8').read()
    for v in versions:
        f = name(v)
        src = os.path.join(ROOT, f)
        if not os.path.exists(src):
            sys.exit('not in the root: ' + f)
        new = 'archive/%s/%s' % (folder, f)
        subprocess.check_call(['git', 'mv', f, new], cwd=ROOT)
        p = os.path.join(ROOT, new)
        s = io.open(p, encoding='utf-8').read()
        io.open(p, 'w', encoding='utf-8').write(rewrite(s))
        idx = idx.replace("file:'%s'" % f, "file:'%s'" % new)
        print(new)
    io.open(ip, 'w', encoding='utf-8').write(idx)


if __name__ == '__main__':
    main()
