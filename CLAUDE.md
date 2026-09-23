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
- Prices: day pass €10 (single entry, full access), week €35.90, monthly €21 with a 3 month minimum plus €24 a year insurance billed separately, personal training is "ask us" on WhatsApp, cash only at the desk.
- Closed on all Portuguese public holidays and on Lagos's municipal holiday.
- Placeholders always carry an example of what goes there.

## Design system
- Fonts: Anton (display), Inter (body), Rock Salt (script).
- Colours: royal blue `#2B3EAA`, greys `#8A8A8A`, `#E5E5E5`, `#F4F4F2`, black and white.
- Second accent: **Volt `#D4F04A`**, special cases only (the entrance tag on the plan, "best value", "new!", the open now dot, button hover). Never as text on white: on white it is a filled shape with black on top. At most once per screen.
- 12 column grid, 8px and 4px spacing, torn edges between bands.
- **On a phone everything is one column.** No two column rows in the footer or anywhere else.
- Motion is small and purposeful: the route draws itself once, the action bar slides up, nothing loops.

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
