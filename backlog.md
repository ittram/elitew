# Backlog

Tasks and issues noticed while building. Not a full backlog. Rules: `~/dev/CLAUDE.md`.

## Now

The order across projects is in `~/dev/PORTFOLIO.md` (Priority list). Updated 2026-11-10.

**[Gym site] Finish the landing page (due today, 10 Nov)**
- **What:** The landing page for Elite Wellness, the gym in Lagos.
- **Where it stands:** 2.5.4 is the base of the page since 10 Nov, picked with the gym owner, and
  the only draft left on the bar. It still needs iterating (Martti, 10 Nov; what exactly is not said
  yet). Its personal training view is a photo card with the WhatsApp button, not a price receipt.
  All 78 earlier drafts are in `archive/`, one folder per thing tested, with the five price rounds as
  `prices-1` to `prices-5`; the Archive panel shows the same groups. The price check passes.
  Five photos are still missing. Four are stock photos from the internet: hero frame 2 (the outdoor
  deck in use), hero frame 3 (a class or coaching moment), the HYROX class card and the Pilates
  class card. The fifth is Ricardo's portrait (his initial shows). Everything else is the gym's own.
- **Next:** Martti says what to change on 2.5.4 and sends the five photos. Claude makes the changes
  in place and swaps the photos in with `build/photo.py`, one section at a time.
- **Needs from you:** What to iterate on 2.5.4. The five photos, in this folder (not Downloads, which Claude cannot read):
  two wide ones for the hero (4:3, landscape), two tall ones for HYROX and Pilates (3:4, portrait,
  the whole movement in the frame), one square head and shoulders of Ricardo. And where the page
  should go live: nothing in this folder says.
- **Time:** About 1 hour of Claude work once the photos are in (rough guess).

## Noticed, not done

- **"todo" marks on the page (10 Nov 2026).** The page shows small "todo" marks where five price
  questions for the gym are unanswered (PRICES.md, Still to confirm). They need answers or hiding
  before the page is public. Seen in the legal line under the price list.
- **The browser tab title is old (10 Nov 2026).** 2.5.4 still starts its title with "Draft 2.2
  (footer: full width, text only)". Seen in the tab while testing. Needs a real title before going live.
- **Stand-in web address in the page head (10 Nov 2026).** The page names `https://example.com/` as
  its own address for English and Portuguese. Seen in the head of 2.5.4. Needs the real address once
  we know where the page goes live.
- **The click-through price test was not run (10 Nov 2026).** `build/test_calculator.py` needs
  Playwright, which is not on this Mac. Every pass, both ways to pay, the insurance switch and the
  personal training card were clicked by hand in the browser on 2.5.4 instead, and the totals matched.
