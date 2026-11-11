# Backlog

Tasks and issues noticed while building. Not a full backlog. Rules: `~/dev/CLAUDE.md`.

## Now

The order across projects is in `~/dev/PORTFOLIO.md` (Priority list). Updated 2026-11-11.

**[Gym site] Finish the landing page**
- **What:** The landing page for Elite Wellness, the gym in Lagos.
- **Where it stands:** Draft 2.7 is draft 2.6 with the last four stock photos replaced by the gym's
  own, from the 51 photos taken in the gym in October (they sit in `assets/raw/`, which is kept out
  of git). New: the second and third hero photos (a member holding a barbell, a class in a side
  stretch seen from behind), the HYROX card (a coach pushing the sled) and the Pilates card (an
  instructor and the class balancing on one leg). No stock photo is left on the page. The dumbbell
  rack, TRX, GAP, Bike Elite and the personal training photo are unchanged: the set has nothing
  better for them. Ricardo's portrait is still missing (his initial shows). Both drafts are on the
  bar and the price check passes on both. Martti and the owner have not looked at either yet.
- **Next:** Martti looks at 2.7 on a phone and a desktop. When it is signed off, 2.6 is archived and
  CLAUDE.md names 2.7 as the page.
- **Needs from you:** A look at 2.7. Three questions for the gym: is the balance class in the photo
  Pilates, are the people in that photo happy to be on the site, and which photo shows Ricardo (or
  a new head and shoulders photo of him). Still to shoot: the outdoor deck in use, and a coach with
  a client if the personal training photo should change. And where the page should go live.
- **Time:** A few minutes of Claude work per answer. A new photo takes about 10 minutes each.

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
- **On a phone the hero shows little of the people (11 Nov 2026).** A phone shows the dumbbell rack
  and only the left edge of the second photo; the third photo is never seen. Seen at 390 wide on
  2.7. If a person should be in the first screen on a phone, the order of the photos or the strip
  has to change. The hero is still open, so it belongs to that decision.
- **Some photos in the October set show members' faces (11 Nov 2026).** The Pilates card on 2.7 has
  three members sharp behind the instructor, faces visible. The house rule prefers people from
  behind. Ask the gym whether they agreed, or reshoot from behind.
