# Backlog

Tasks and issues noticed while building. Not a full backlog. Rules: `~/dev/CLAUDE.md`.

## Now

The order across projects is in `~/dev/PORTFOLIO.md` (Priority list). Updated 2026-11-11.

**[Gym site] Portuguese and English, then go live**
- **What:** The landing page for Elite Wellness, the gym in Lagos, as a real site in two languages.
- **Where it stands:** The site now lives in the folder `site/` as two plain pages: Portuguese at
  the main address, English at `/en`. Looks and behaviour are in two shared files, so they are
  changed once. The Portuguese is written by Claude, speaking to people as "tu". A new check
  (`build/check_pages.py`) compares the two pages and stops a change that is made in one only; the
  price check covers both pages. Checked on a phone and a desktop. Not pushed, not live.
- **Next:** The family reads the Portuguese page and corrects what sounds off. Then go live:
  a private repository, Cloudflare Pages, the real address, and the update skills for the owner.
- **Needs from you:** Someone from the gym to read the Portuguese page. The Google links for three
  reviews (Alessandro, Sahirah, Emily). The address the site will live at. For the gym: check the
  two lines about each class; is the balance class in the photo Pilates; are the people in it happy
  to be on the site; a photo of Ricardo.
- **Time:** 20 minutes of reading for the family. Going live: about 2 hours of Claude work, one
  session, plus Martti creating the Cloudflare and GitHub accounts or giving access.

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
- **Three reviews open the gym's page, not the review (11 Nov 2026).** Martin's and Brian's cards
  open their own review. Alessandro, Sahirah and Emily need their link: on Google Maps open the
  review, tap Share, copy the link, paste it as `url` in `reviews.js`.
- **Google now says 157 reviews, the page says 153 (11 Nov 2026).** Seen on Google Maps while
  collecting the review links. The number is typed in several places (hero, menu, reviews, the
  data for search engines). Update it in one go before the page goes live.
- **The class descriptions are general, not the gym's own words (11 Nov 2026).** The two lines per
  class in `schedule.js` (`about`) say what each format is in general. Ask the coaches to check
  them. Mobility, Abs and Circuit HIIT have no card, so their lines show only from the timetable.
- **The photo grain is laid over in the page, not in the files (11 Nov 2026).** If it stays, it
  could move into `build/photo.py` so every new photo gets it.
- **The site folder borrows files through links (11 Nov 2026).** In `site/`, the photos and the
  price, timetable and review files are links to the ones in the root, so the drafts and the site
  share one copy. For going live they must become real files in the new repository, and the raw
  photos must stay out of it.
- **The address is a stand in (11 Nov 2026).** Both pages name `https://example.com/` as their
  address for search engines. Put the real one in when it is known (the head of both pages).
- **English reviews on the Portuguese page (11 Nov 2026).** The reviews are shown as written, in
  English, on both pages. If the gym has Portuguese reviews it likes, add them to `reviews.js`.
- **Portuguese words to confirm with the gym (11 Nov 2026).** "Adesão" for membership, "Livre
  trânsito" for unlimited (from the price sheet), "Deck exterior", "Racks", "Bom saber" for Good to
  know, "Inscreve-te" on the Join button.
