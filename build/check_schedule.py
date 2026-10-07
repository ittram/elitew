# -*- coding: utf-8 -*-
"""Checks schedule.js before a timetable change is committed, and prints it
as the same grid as the poster so the two can be read side by side.

    python3 build/check_schedule.py            # compares with the last commit
    python3 build/check_schedule.py HEAD~1     # or with any other version

Stops with an error for anything that would show wrong on the page; prints
warnings for things that are allowed but worth a second look."""
import json, re, subprocess, sys

DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
NAMES = dict(zip(DAYS, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))
OPEN = {d: ('07:00', '21:00') for d in DAYS[:5]}          # as in the page's opening hours; weekends closed
LOAD = "global.window={};eval(require('fs').readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(window.ELITE_SCHEDULE))"


def load(source):
    return json.loads(subprocess.run(['node', '-e', LOAD], input=source, capture_output=True, text=True, check=True).stdout)


def mins(t):
    h, m = t.split(':'); return int(h) * 60 + int(m)


def check(S):
    errors, warnings = [], []
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', S.get('updated', '')):
        errors.append('updated must be a date like 2026-10-07')
    keys = S['classes']
    for k, c in keys.items():
        for f in ('name', 'en', 'pt'):
            if not c.get(f): errors.append('class %s has no %s' % (k, f))
    seen, used = {}, set()
    for s in S['sessions']:
        where = '%s %s' % (s.get('day'), s.get('time'))
        before = len(errors)
        if s.get('day') not in DAYS: errors.append('%s: day must be one of %s' % (where, ', '.join(DAYS)))
        if not re.fullmatch(r'([01]\d|2[0-3]):[0-5]\d', s.get('time', '')): errors.append('%s: time must be 24h HH:MM' % where)
        if s.get('class') not in keys: errors.append('%s: class "%s" is not in classes, the page would show the raw key' % (where, s.get('class')))
        if not isinstance(s.get('minutes'), int) or s['minutes'] <= 0: errors.append('%s: minutes must be a whole number' % where)
        if len(errors) > before: continue
        used.add(s['class'])
        if (s['day'], s['time']) in seen: errors.append('%s: two classes at the same time' % where)
        seen[(s['day'], s['time'])] = s
        o = OPEN.get(s['day'])
        if not o: warnings.append('%s: the gym is closed that day' % where)
        elif mins(s['time']) < mins(o[0]) or mins(s['time']) + s['minutes'] > mins(o[1]):
            warnings.append('%s: runs outside opening hours %s to %s' % (where, *o))
    by_day = {}
    for s in S['sessions']:
        if (s.get('day'), s.get('time')) in seen and seen[(s['day'], s['time'])] is s:
            by_day.setdefault(s['day'], []).append(s)
    for d, ss in by_day.items():
        ss.sort(key=lambda s: mins(s['time']))
        for a, b in zip(ss, ss[1:]):
            if mins(a['time']) + a['minutes'] > mins(b['time']):
                errors.append('%s: %s %s runs into %s %s' % (d, a['time'], a['class'], b['time'], b['class']))
    # every slot at one time should last the same, as the poster's legend says (09h30 30 min, 18h30 and 19h20 40 min)
    for t in sorted({s['time'] for s in S['sessions']}, key=mins):
        lens = {s['minutes'] for s in S['sessions'] if s['time'] == t}
        if len(lens) > 1: warnings.append('%s: classes at this time have different lengths %s' % (t, sorted(lens)))
    for k in keys:
        if k not in used: warnings.append('class %s is defined but on no day (fine if it is paused)' % k)
    return errors, warnings


def grid(S):
    days = [d for d in DAYS if any(s['day'] == d for s in S['sessions'])]
    times = sorted({s['time'] for s in S['sessions']}, key=mins)
    cell = {(s['day'], s['time']): S['classes'][s['class']]['name'] + (' *new' if s.get('isNew') else '') for s in S['sessions'] if s['class'] in S['classes']}
    w = 18
    lines = ['%-8s' % '' + ''.join('%-*s' % (w, NAMES[d]) for d in days)]
    for t in times:
        m = sorted({s['minutes'] for s in S['sessions'] if s['time'] == t})
        lines.append('%-8s' % t + ''.join('%-*s' % (w, cell.get((d, t), '-')) for d in days) + '  (%s min)' % '/'.join(map(str, m)))
    return '\n'.join(lines)


def changes(old, new):
    o = {(s['day'], s['time']): s for s in old['sessions']}
    n = {(s['day'], s['time']): s for s in new['sessions']}
    nm = lambda S, s: S['classes'].get(s['class'], {}).get('name', s['class']) + (' (new)' if s.get('isNew') else '')
    out = []
    for k in sorted(set(o) | set(n), key=lambda k: (DAYS.index(k[0]) if k[0] in DAYS else 9, mins(k[1]))):
        a, b = o.get(k), n.get(k)
        if a and b and (a['class'], a['minutes'], bool(a.get('isNew'))) == (b['class'], b['minutes'], bool(b.get('isNew'))): continue
        out.append('  %s %s: %s -> %s' % (NAMES.get(k[0], k[0]), k[1], nm(old, a) if a else 'nothing', nm(new, b) if b else 'nothing'))
    for k in sorted(set(new['classes']) - set(old['classes'])):
        out.append('  new class: %s (%s)' % (new['classes'][k]['name'], new['classes'][k]['en']))
    return out


if __name__ == '__main__':
    rev = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'
    S = load(open('schedule.js', encoding='utf-8').read())
    print(grid(S))
    print('\nupdated', S['updated'])
    try:
        old = load(subprocess.run(['git', 'show', rev + ':schedule.js'], capture_output=True, text=True, check=True).stdout)
        ch = changes(old, S)
        print('\nChanged since %s:' % rev); print('\n'.join(ch) if ch else '  nothing')
    except subprocess.CalledProcessError:
        print('\n(no %s version to compare with)' % rev)
    errors, warnings = check(S)
    for w_ in warnings: print('warning:', w_)
    for e in errors: print('ERROR:', e)
    print('\n%s' % ('Not ready: fix the errors above.' if errors else 'schedule.js is consistent.'))
    sys.exit(1 if errors else 0)
