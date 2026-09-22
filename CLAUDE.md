# Elite Wellness landing page: house rules

## Drafts and the version bar
- A **new draft file** is for a new direction or a version the user asks for: `elite-wellness-landing_<version>.html`, with dots as dashes (`1.9.6.1` → `elite-wellness-landing_1-9-6-1.html`).
- **Small design iterations and fixes go into the current draft**, in place. Do not spin up a new version for a font size, a wrap, a colour or a bug.
- Register every new draft in the `DRAFTS` list at the top of the script in `index.html`, with `v`, `file`, `label` (2 to 4 words saying what it tests), `date`, a `status`, `tested` and `next`.
- **The newest version is always first and is the one the page loads.** `index.html` sorts `DRAFTS` by version number, so a new entry orders itself; give the new draft `status:'latest'` and drop the previous latest to `status:'open'`.
- Drafts we no longer compare get `archived:true` and a one line `why`. They stay in the Archive panel and still open.
- The bar must stay **one line tall** and work on a phone: chips scroll sideways, the tools stay pinned on the right.

## Copy
- No dashes in the copy: no "—", "–" or "-", except where unavoidable, such as the postcode 8600-530.
- Every "ask us" and contact link goes to WhatsApp on +351926565836 as a `wa.me` link. Never a phone link.
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
