# Backlog

Tasks and issues noticed while building. Not a full backlog. Rules: `~/dev/CLAUDE.md`.

## Now

The order across projects is in `~/dev/PORTFOLIO.md` (Priority list). Updated 2026-11-11.

**[Gym site] Final polish before translation**
- **What:** The last round of small design changes on the landing page for Elite Wellness, the gym
  in Lagos, before it is translated into Portuguese.
- **Where it stands:** Five polish drafts are on the bar, 2.8.1 to 2.8.5, all built on 2.7 (the
  page with the gym's own photos). All five share the same small fixes: clearer wording in seven
  places, a real title for the browser tab, the empty slot gone from the phone timetable, and one
  row of reviews so no review shows twice on a screen. Then each pushes one idea: Motion (2.8.1),
  Type and spacing (2.8.2), Touch and feedback (2.8.3), First screen (2.8.4), Marker strokes
  (2.8.5). Checked on a phone and a desktop; the price check passes on all of them. Nothing is
  pushed. 2.6 and 2.7 are still on the bar.
- **Next:** Martti looks through the five and says which parts to keep. Claude merges them into one
  page (2.9), archives the rest, then the translation starts.
- **Needs from you:** Your picks from the five. Still open from before, for the gym: is the balance
  class in the photo Pilates, are the people in it happy to be on the site, and a photo of Ricardo.
  And where the page should go live.
- **Time:** 15 minutes of looking for Martti. About 1 hour for Claude to merge the picks.

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
- **Squat rack: the page says two different things (11 Nov 2026).** Good to know says "Two squat
  racks, Smith machines and a full free weight setup". The floor plan list says "A squat stand, a
  landmine and a pull up rig". Seen while reviewing 2.7. Ask the gym which is right.
- **"Terms of entry" in the footer jumps to Good to know (11 Nov 2026).** It reads like a legal
  page but there is none. Seen while reviewing 2.7. Either write the terms or take the link out.
- **Only five reviews on the page (11 Nov 2026).** With five, two rows showed the same review twice
  on one screen. The 2.8 drafts show one row until there are eight. Paste more reviews from Google
  into `reviews.js` and the second row comes back by itself.
- **Volt behind blue letters in 2.8.5 (11 Nov 2026).** The highlighter stroke behind "In Lagos"
  puts blue letters on volt. The house rule says volt on white carries black on top. If the stroke
  is kept, the rule gets an exception; if not, the stroke turns black or grey.
- **The house rules still name 2.6 as the page (11 Nov 2026).** `CLAUDE.md` says the page is 2.6.
  Update it when the polish picks are merged and one draft is the page again.
