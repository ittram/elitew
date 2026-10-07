# Elite Wellness landing page: house rules

## Drafts and the version bar
- A **new draft file** is for a new direction or a version the user asks for: `elite-wellness-landing_<version>.html`, with dots as dashes (`1.9.6.1` → `elite-wellness-landing_1-9-6-1.html`).
- **Small design iterations and fixes go into the current draft**, in place. Do not spin up a new version for a font size, a wrap, a colour or a bug.
- Register every new draft in the `DRAFTS` list at the top of the script in `index.html`, with `v`, `file`, `label` (2 to 4 words saying what it tests), `date`, a `status`, `tested` and `next`.
- **The newest version is always first and is the one the page loads.** `index.html` sorts `DRAFTS` by version number, so a new entry orders itself; give the new draft `status:'latest'` and drop the previous latest to `status:'open'`.
- Drafts we no longer compare get `archived:true`, a `group` (the archive panel's subheading) and a one line `why` replacing `next`. They stay in the Archive panel and still open.
- When a section is signed off, archive every other draft of it and leave only the latest on the bar. The bar carries the current page plus whatever decision is still open.
- A new archive group goes to the top of the `order` list in `renderArchive()`, so the newest work reads first.
- Give each draft an `at`: the section its work lives in, as a selector (`'#find-us'`, `'footer.site-footer'`). The bar opens the draft there instead of at the top, and the About panel says so. Leave it off for drafts about the hero or the header.
- Clicking the draft you are already on opens its About panel. There is no separate About button, to keep room for the chips on a phone.
- The bar must stay **one line tall** and work on a phone: chips scroll sideways, the tools stay pinned on the right.

## Copy
- No dashes in the copy: no "—", "–" or "-", except where unavoidable, such as the postcode 8600-530.
- Every "ask us" and contact button goes to WhatsApp on +351926565836 as a `wa.me` link. The one exception is the phone number printed in the footer, which is a `tel:` link so it dials.
- Google Maps link: https://maps.app.goo.gl/ks6o4URGCYT7rzHJ8
- Prices live in `prices.js` and nowhere else. See PRICES.md. Two things to never get wrong: **membership is priced per 2 weeks, not per month**, and the €24 sports insurance is **included** in day and week passes but **added once a year** to membership.
- **Direct debit is a discount, never the other way round.** The price at reception is the normal price (€18 / €24.50 / €26 every 2 weeks) and direct debit takes €5 off (€13 / €19.50 / €21). Never write that reception costs more: EU law (PSD2 art. 62, in Portugal Decreto-Lei 91/2018 art. 101) bans charging extra for a payment method but allows a discount for one. A "from" price must say its condition, e.g. "From €13 every 2 weeks with direct debit".
- Names, as people already say them: **Day and week passes** (Day pass, 1 week pass...), **Membership** (Once a week, Three times a week, Unlimited; "3x per week" reads as shorthand, not English), **Personal training**. The place to pay is **reception**, not "the desk".
- Day and week passes: 1 day €10, 1 week €35.90, 2 weeks €45.90, 3 weeks €51.90, 4 weeks €61.90. Personal training: €50 a session, or packs of 8, 12 and 20 at €360, €480 and €600, second person €15 a session.
- Never write "monthly", "3 month minimum" or "cash only" on the page. None of them is in the price list.
- Closed on all Portuguese public holidays and on Lagos's municipal holiday.
- Placeholders always carry an example of what goes there.

## Design system
- Fonts: Anton (display), Inter (body), Rock Salt (script).
- Colours: royal blue `#2B3EAA`, greys `#8A8A8A`, `#E5E5E5`, `#F4F4F2`, black and white.
- Second accent: **Volt `#D4F04A`**, special cases only (the entrance tag on the plan, "best value", "new!", the open now dot, button hover). Never as text on white: on white it is a filled shape with black on top. At most once per screen.
- 12 column grid, 8px and 4px spacing, torn edges between bands.
- **On a phone everything is one column.** No two column rows in the footer or anywhere else.
- Motion is small and purposeful: the route draws itself once, the action bar slides up, nothing loops.
- **Photos are black and white**, with a soft background. See Photos below.

## Photos
When the user sends training photos, give them the house look without being asked: **run `build/photo.py`, never edit by hand.** It is the look of the TRX card in 2.4.8, and it reproduces that file byte for byte.

1. **Pick** when there are several shots of one thing. Choose the one that shows a whole movement with the equipment in the frame (anchor, straps, bar, bike), sharp, people from behind or turned away rather than faces, no big brand logos. Say in one line why it won and what was wrong with the others.
2. **Run it in the sandbox** (it needs `pip install --break-system-packages "rembg[cpu]" opencv-python-headless pillow numpy`; the models download once):
   `python3 build/photo.py SOURCE class-hyrox` for a class card, or `--kind hero` for a hero photo.
   It does black and white (levels, slightly darker mids, a touch of contrast and sharpening), cuts out the people and what they hold, blurs everything behind them with a round lens kernel (most on the far wall, least on the floor in front), crops (card 3:4 portrait, hero 4:3, 14% of the frame above the person's head), adds a light vignette, and writes webp at quality 80 with no metadata: card `NAME.webp` 900 wide and `NAME-600.webp`, hero `NAME.webp` 1600 wide and `NAME-800.webp`.
3. **Look at the result** before using it, at card size and up close at the edges (hands, hair, straps). If the crop cuts something that matters, rerun with `--top N` (the crop's top edge in source pixels); if the vignette sits wrong, `--focus X Y` (0 to 1, default 0.58 0.42). Do not change the defaults for one photo: change the flag.
4. **Copy back and clean**: commit the two files to `assets/`, then on the Mac `python3 build/strip_c2pa.py assets/NAME.webp assets/NAME-600.webp`. Files from the sandbox pick up a C2PA chunk on the way; the strip also clears any EXIF or XMP (phone photos carry location).
5. **Use it**: a class card image is `<img class="class-img" src="assets/NAME.webp" srcset="assets/NAME-600.webp 600w, assets/NAME.webp 900w" sizes="(max-width:768px) 86vw, (max-width:1100px) 50vw, 25vw" width="900" height="1200" loading="lazy" style="object-position:50% 30%" alt="...">`. The alt says what is happening, e.g. "A member rowing on the TRX straps in a class at Elite Wellness".
6. **Names say what the photo shows**: `class-trx`, `class-hyrox`, `hero-free-weights`.
7. Swapping a photo is a small change and goes into the current draft. A first real photo for a section, or a new set, is a new draft, opened at that section (`at:'#classes'`).

## Working habits
- Verify with a screenshot at 1440 and at 390 wide before saying it is done, and check the page never scrolls sideways.
- Commit each step with a plain description. **The user pushes**, so end with the push command rather than pushing.
- Do not commit the "Claude outputs" folder.

## Decided so far
- The gym section with the isometric floor plan (1.8).
- Hours and location: one blue band with the live status, the map filling the right half on desktop and a band on a phone (1.9.6.6).
- The footer: brand, address, phone, email and languages on the left, then Explore, Social and press, and Legal, right aligned to the content, no buttons in it (2.2).
- The action bar: black, follows you from the hero to the end of the page, on every width, WhatsApp and Directions.
- Still open: the hero headline, drafts 1.2, 1.2.1, 1.3, 1.5 and 1.6.
