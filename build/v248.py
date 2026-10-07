# -*- coding: utf-8 -*-
"""Draft 2.4.8: 2.4.7 with the first real class photo, TRX, in the Classes
section. Run build/v247.py first; this reads its output.

The photo: a member rowing on the straps in a split stance, from behind, so
no face; chosen from three TRX shots of 29 September because it is the only
one showing a whole movement with the anchor and the straps. Black and white
baked in, cropped to a 3:4 portrait (the card is portrait on every screen),
900 and 600 wide, no metadata.

7 October: a shallow depth of field added to match the stock photos. The
person and the straps were cut out with rembg (u2net_human_seg for the body,
isnet-general-use for the straps, the two masks combined); the background was
blurred with a round lens kernel, strongest on the far wall and lighter on
the floor in front, then the sharp subject laid back on top with a soft edge."""
import io
s = io.open('elite-wellness-landing_2-4-7.html', encoding='utf-8').read()
old = '<img class="class-img" src="https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?q=80&w=800&auto=format&fit=crop" alt="PLACEHOLDER: replace with a real TRX class photo">'
new = ('<img class="class-img" src="assets/class-trx.webp" '
       'srcset="assets/class-trx-600.webp 600w, assets/class-trx.webp 900w" '
       'sizes="(max-width:768px) 86vw, (max-width:1100px) 50vw, 25vw" width="900" height="1200" loading="lazy" '
       'style="object-position:50% 30%" '
       'alt="A member rowing on the TRX straps in a class at Elite Wellness">')
assert s.count(old) == 1
s = s.replace(old, new)
io.open('elite-wellness-landing_2-4-8.html', 'w', encoding='utf-8').write(s)
print('2.4.8', len(s))
