# -*- coding: utf-8 -*-
import io, sys
sys.path.insert(0, 'build')
import pricebuild as B          # reuses shared(), swap(), KICKER, LEGAL
from v5x import VARIANTS_X

base = B.shared(io.open(B.SRC, encoding='utf-8').read())
for name, kicker, sec, css, js in VARIANTS_X:
    section = (B.KICKER % kicker) + sec + B.LEGAL
    out = B.swap(base, section, css, js)
    f = 'elite-wellness-landing_%s.html' % name
    io.open(f, 'w', encoding='utf-8').write(out)
    print(f, len(out))
