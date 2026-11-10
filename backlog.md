# Backlog

Tasks and issues noticed while building. Not a full backlog. Rules: `~/dev/CLAUDE.md`.

## Now

The order across projects is in `~/dev/PORTFOLIO.md` (Priority list). Updated 2026-11-10.

**[Gym site] Finish the landing page (due today, 10 Nov)**
- **What:** The landing page for Elite Wellness, the gym in Lagos.
- **Where it stands:** The price section has its final version, draft 2.6, the only draft on the bar.
  A price is always showing (the day pass is chosen when you tap Passes), the texts are cut short,
  the insurance switch is gone, and Get this plan leads to a check screen with Buy now, then to
  "Finish at reception". No payment is taken; the two steps count who would buy online. Martti and
  the owner have not looked at 2.6 yet. All earlier drafts are in `archive/`, grouped by what they
  tested. The price check passes; every total was clicked through by hand.
  Five photos are still missing. Four are stock photos from the internet: hero frame 2 (the outdoor
  deck in use), hero frame 3 (a class or coaching moment), the HYROX class card and the Pilates
  class card. The fifth is Ricardo's portrait (his initial shows). Everything else is the gym's own.
- **Next:** Martti looks at 2.6 on a phone and a desktop and says what to change. Then the photos.
- **Needs from you:** A look at 2.6. The five photos, in this folder (not Downloads, which Claude
  cannot read): two wide ones for the hero (4:3, landscape), two tall ones for HYROX and Pilates
  (3:4, portrait, the whole movement in the frame), one square head and shoulders of Ricardo. And
  where the page should go live: nothing in this folder says.
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
- **Nothing counts the buyers yet (10 Nov 2026).** The buy screens send their counts (Get this plan,
  Buy now) to a hook that is connected to nothing. A counting tool, such as Plausible, has to be
  connected when the page goes live, or the test measures nothing. How: PRICES.md, Tracking.
- **What to bring is partly a guess (10 Nov 2026).** The last buy screen says members bring photo ID
  (from the earlier draft) and, for direct debit, their IBAN (my assumption). Ask the gym.
