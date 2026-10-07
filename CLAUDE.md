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
- The prices themselves live only in `prices.js` (from the sheet in force since 1/10/2026). Never write a price into this file, a build script or the page copy by hand: see Prices below.
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

## Prices
`prices.js` is the one source for every price on the site. The calculator reads it in the browser; `build/pricelist.py` writes everything else from it (the fold-open full price list, and the prices quoted in the meta description, the menu, the FAQ, the legal line and the search engines' price range). When the user sends a new price list (a photo of the printed preçário or a file), update it like this without being asked for each step:

1. **Read the sheet** line by line: each section (Livre, Visitantes, packs, PT), both columns where there are two (débito direto and balcão), the validity of each pack, "por sessão" or total, the date it is in force from, and every footnote.
2. **Check the sheet against itself and against `prices.js` before changing anything.** Look for a block without a heading, the same thing priced twice, a column that does not add up (pack totals, the discount being the same on every plan), a footnote that contradicts a line, something from the current list that disappeared (October 2026: the €24 insurance was not on the sheet; it still applies) and anything new. Report every finding to the user in plain words and ask about the ones that change what goes on the page; never resolve them silently. While a question is open, the line goes into `unconfirmed` (or a `todo`) so the page shows a chip instead of a guess.
3. **Edit `prices.js` only.** Keep each item's `pt` as the line is printed on the sheet, so the check can print the list in the sheet's own words. Set `updated` to the date the sheet is in force from. A new kind of product (October 2026: assessment packs) is a design change: ask whether it goes into the calculator, the full list or both, then add it to `pricelist.py` (the list) and to the calculator draft (as `v247.py` did).
4. **Write the pages: `python3 build/pricelist.py`.** It finds every live draft that loads `prices.js` on its own. Run it again after rebuilding any draft, because the build scripts start from older copy.
5. **Cross check: `python3 build/check_prices.py`.** It prints the list in the order and words of the printed sheet (read it against the photo, line by line, once more), lists every price that changed since the last commit (each change must be one you meant), checks the arithmetic the page relies on, and checks every live draft: the list and the copy must match `prices.js`, and no other euro amount may appear anywhere on the page or be typed into a script. Errors block; explain warnings to the user.
6. **Click through: `python3 build/test_calculator.py`** in the sandbox (the latest draft by default, or name drafts). It picks every pass, every plan with both ways to pay, the insurance switch, every personal training pack and every assessment pack, at 390 and 1440 wide, and compares each total with its own arithmetic from `prices.js`.
7. **Look at the page** at 1440 and 390: the calculator, and the full price list opened.
8. **Commit** as "Prices from the sheet of <date>", listing the changes (the check's "Changed since" list) and the open questions. Update `PRICES.md` (Still to confirm) and the pricing note in the project. The user pushes.

## Photos
When the user sends training photos, give them the house look without being asked: **run `build/photo.py`, never edit by hand.** It is the look of the TRX card in 2.4.8, and it reproduces that file byte for byte.

1. **Pick** when there are several shots of one thing. Choose the one that shows a whole movement with the equipment in the frame (anchor, straps, bar, bike), sharp, people from behind or turned away rather than faces, no big brand logos. Say in one line why it won and what was wrong with the others.
2. **Run it in the sandbox** (it needs `pip install --break-system-packages "rembg[cpu]" opencv-python-headless pillow numpy`; the models download once):
   `python3 build/photo.py SOURCE class-hyrox` for a class card, or `--kind hero` for a hero photo.
   It does black and white (levels, slightly darker mids, a touch of contrast and sharpening), cuts out the people and what they hold, blurs everything behind them with a round lens kernel (most on the far wall, least on the floor in front), crops (card 3:4 portrait, hero 4:3, 14% of the frame above the person's head), adds a light vignette, and writes webp at quality 80 with no metadata: card `NAME.webp` 900 wide and `NAME-600.webp`, hero `NAME.webp` 1600 wide and `NAME-800.webp`.
3. **Look at the result** before using it, at card size and up close at the edges (hands, hair, straps). In a busy class photo add `--main` (only the biggest person stays sharp, the people behind blur like the wall) and, for anyone on a mat or the floor, `--near` (the floor close to them stays in focus, so they do not float); Pilates in 2.4.8 used both. If the crop cuts something that matters, rerun with `--top N` (the crop's top edge in source pixels); if the vignette sits wrong, `--focus X Y` (0 to 1, default 0.58 0.42). Do not change the defaults for one photo: change the flag.
4. **Copy back and clean**: commit the two files to `assets/`, then on the Mac `python3 build/strip_c2pa.py assets/NAME.webp assets/NAME-600.webp`. Files from the sandbox pick up a C2PA chunk on the way; the strip also clears any EXIF or XMP (phone photos carry location).
5. **Use it**: a class card image is `<img class="class-img" src="assets/NAME.webp" srcset="assets/NAME-600.webp 600w, assets/NAME.webp 900w" sizes="(max-width:768px) 86vw, (max-width:1100px) 34vw, 20vw" width="900" height="1200" loading="lazy" style="object-position:50% 30%" alt="...">`. Move `object-position` sideways (e.g. `75% 30%`) when the person is off centre, so the narrow desktop card does not cut them. The alt says what is happening, e.g. "A member rowing on the TRX straps in a class at Elite Wellness". A new class also gets its own card (name and the `en` line from schedule.js as the tag); five cards sit in one row on desktop and three over two on a tablet.
6. **Names say what the photo shows**: `class-trx`, `class-hyrox`, `hero-free-weights`.
7. Swapping a photo is a small change and goes into the current draft. A first real photo for a section, or a new set, is a new draft, opened at that section (`at:'#classes'`).

## Timetable
The page's timetable is built from `schedule.js` alone; every draft reads it, so a change shows everywhere at once. When the user sends a new poster (the digital file or a photo of the print), update it like this, without being asked for each step:

1. **Read the grid** cell by cell: the day columns, the three time rows (the time and length in each row header), the class in each cell, and every "Novidade" mark.
2. **Check the poster against itself before publishing anything.** Compare the grid with every other line on it: the "Novidade" footnote (the day and time it gives for each new class), the legend at the bottom (morning, afternoon and evening times and lengths), the row headers, the order of the day headers. Look for a class twice in one day, an empty cell, a class that disappeared. Then compare with the current `schedule.js` and ask whether each change looks intended. **The grid wins** as the working assumption, but every conflict goes to the user in plain words, with the fix for the poster, before the work is called done. Never correct a conflict silently. Example, October 2026: the footnote said Pilates "quarta-feira às 19h20" while the grid had it on Thursday; the grid was right and the footnote was a leftover on the poster, worth fixing before it goes on social media.
3. **Edit `schedule.js` only**: the `sessions`, `updated` set to today, `isNew: true` for each "Novidade". A new class gets a key in `classes` with `name`, `en` (a short English line in the style of the others, it becomes the tag under the name) and `pt`; ask whether it should also get a class card (see Photos).
4. **Run `python3 build/check_schedule.py`.** It prints the timetable as the same grid as the poster and lists what changed since the last commit; read that grid against the poster once more, row by row. It stops on anything that would show wrong (an unknown class, a clash, a bad time) and warns about things worth a look (outside opening hours, rows of mixed length, a class on no day). Fix errors; explain warnings to the user.
5. **Look at the page** at 1440 (the week table, today and next highlighted) and at 390 (the day tabs, open the changed days).
6. **The poster image**, `assets/timetable.webp`, is only the fallback link for browsers without JavaScript. Use the digital file when there is one; for a photo of the print run `python3 build/poster.py PHOTO` in the sandbox (squares the sheet up, trims the border, whitens the paper, colour webp), then `build/strip_c2pa.py` on the Mac.
7. **Commit** as "Timetable from the <month> poster", with each changed slot in the message (the check script's "Changed since" list). The user pushes.

TIMETABLE.md is the same process for the family, using ChatGPT instead of Claude.

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
