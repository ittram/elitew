# Backlog

Tasks and issues noticed while building. Not a full backlog. Rules: `~/dev/CLAUDE.md`.

## Now

The order across projects is in `~/dev/PORTFOLIO.md` (Priority list). Updated 2026-11-11.

**[Gym site] Portuguese and English, then go live**
- **What:** The landing page for Elite Wellness, the gym in Lagos, as a real site in two languages.
- **Where it stands:** The site is the folder `site/`: Portuguese at the main address, English at
  `/en`. Served on its own as the main address it works (every file both pages ask for is found,
  except Ricardo's photo). A second, independent read of the Portuguese by Claude fixed about 20
  spots; no native speaker has read it yet. Not pushed, not live.
- **Next:** Martti picks where the live site's files are kept (a new clean private repository, or
  this one made private). Then Claude sets it up on a private test address at Cloudflare, the
  family reads the Portuguese there, and the real address is connected last.
- **Needs from you:** The choice above. A GitHub and a Cloudflare account for the gym (or yours).
  The address the site will live at. Still open for the gym: the Google links for three reviews,
  the two lines about each class, a photo of Ricardo.
- **Time:** About 2 hours of Claude work, one session. 15 minutes for Martti to create the accounts
  and connect them. 20 minutes of reading for the family.
- **To see it:** in this folder's Claude session, the server "drafts" shows `localhost:8765/site/`
  and the server "site-as-live" shows the site as it will be at its own address, `localhost:8766/`.

## Noticed, not done

- **Three team photos carry a hidden "made with" tag (11 Nov 2026).** `assets/team/andre.jpg`,
  `joana.jpg` and `jorge.jpg` hold a content credentials (C2PA) block. No location or camera data.
  Seen while checking the photos before a push; they were already public. `build/strip_c2pa.py`
  removes it.
- **Before the site is public (11 Nov 2026).** Found while checking the site folder as it would go
  live. (1) A link to the site shared on WhatsApp or Instagram shows no picture and no title card:
  the page has no share picture. (2) There is no "page not found" page, so a mistyped address would
  show a broken copy of the home page. (3) Two "todo" marks still show: whether direct debit has a
  minimum period (Good to know) and the privacy policy (footer). (4) The page tells search engines
  about a photo, `elite-wellness-lagos-outdoor-training-deck.jpg`, that does not exist. (5) No list
  of pages for search engines (sitemap) yet; it needs the real address.
- **The drafts are public today (11 Nov 2026).** This repository is public and GitHub shows it as a
  website at `ittram.github.io/elitew/`, drafts and all. Making the repository private on a free
  GitHub account switches that address off. Seen with `gh` while preparing to go live.
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
- **Portuguese words for the family to decide (11 Nov 2026).** A second read by Claude (not a
  native speaker) fixed the clear mistakes and left these as questions.
  (1) **"Adesão" may read as a joining fee.** In Portugal the word means the act of joining, so
  "Adesão desde 13 €" can sound like a one time fee. Gyms say "sócio" and "plano". The suggestion:
  the tab "Sócios", the plans "Plano 3 vezes por semana", the menu "Sócios desde 13 €". It touches
  the house rule in CLAUDE.md and the price script, so it waits for a yes.
  (2) **"Bom saber" is a word for word copy of Good to know.** Suggested: "Informações úteis"
  (standard) or "Antes de vires" (warmer).
  (3) Taste: "a cada 2 semanas" or "de 2 em 2 semanas"; "ginásio de família" or "ginásio
  familiar"; "avaliações" or "opiniões" for the Google reviews; "máquinas Smith" or "multipower";
  "Melhor preço" or "Compensa mais" on the membership box; "Mais" or "Ler mais" on a review.
  (4) Left as they were on purpose: the opening hours as "07:00 às 21:00" (the second read wanted
  "Das 07:00 às 21:00"; signs in Portugal use the short form) and "Documento de identificação com
  fotografia" (shorter would drop the photo, and what to bring is still unconfirmed).
  (5) The data file keeps the price sheet's own words, and for the single personal training
  session they are "Sessão avulso". Correct Portuguese is "Sessão avulsa". If the printed sheet
  really says "avulso", it is worth fixing on the sheet. The site does not show this line.
  Confirmed fine by the second read: "Livre-trânsito" (now with its hyphen), "Inscreve-te",
  "Passe diário", "Treina em Lagos", and the "tu" form throughout.
- **Does membership have a minimum period? (11 Nov 2026).** Good to know answers "Is there a
  contract?" for passes but does not say whether members commit to a minimum time. It is one of the
  "todo" marks. Ask the gym.
