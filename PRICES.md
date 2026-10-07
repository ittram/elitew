# Prices

`prices.js` is the only file to change when a price changes. Every 2.4.x draft
reads from it, so one edit updates the picker, the flow and the arithmetic.

The full price list folded under the calculator is plain HTML, so it can be read
without JavaScript and by search engines, and the copy quotes a few prices (the
meta description, the menu line, the FAQ, the price range for search engines).
All of it is written from `prices.js`. After changing a price:

    python3 build/pricelist.py          # writes the list and the copy in every live draft
    python3 build/check_prices.py       # the cross check: sheet order, changes, arithmetic, every page
    python3 build/test_calculator.py    # in the sandbox: every total, clicked through in a browser

The full process, with the reading of a new printed sheet, is in CLAUDE.md under Prices.

## What the site shows

Since 7 October 2026 personal training is quoted per customer: `pt.quote` is
true, so the site shows only where it starts (the lowest price a session on the
sheet) and a WhatsApp button for a personal quote. Assessments have
`onSite: false`. The sheet's prices stay in `prices.js` so the list is complete;
`check_prices.py` fails if one of them appears on a page.

## Where the numbers come from

The printed preçário "em vigor desde 1/10/2026". All prices include VAT.

## The two things people get wrong

1. **Member plans are priced per 2 weeks, not per month.** €21 is a fortnight of
   unlimited training, so a month is roughly €42. Every treatment says this out
   loud, because a customer who reads €21 as monthly feels tricked when the bank
   shows two payments.
2. **Insurance sits in different places.** Visitor passes include the €24 sports
   insurance. Member plans add it once a year on top. Any comparison between the
   two has to add it, or it is not a comparison.

## Still to confirm

These are in `prices.js` under `unconfirmed` (and `assessments.todo`), and the
page shows a `todo` chip rather than guessing. `check_prices.py` lists them.

- Does the direct debit price need a minimum period?
- Does "once a week" mean one visit each calendar week, or two in any two weeks?
- Is the first fitness assessment still free on every plan, now that assessment packs are sold?
- The 1/10/2026 sheet has a second, unlabelled personal training block (single
  €40, packs €32.50 / €30 / €25 a session, extra person €12.50). The site uses
  the labelled block until someone explains who the second one is for.
- What the assessment packs (training €55, nutrition €70, three months) include.

## Tracking

Every step of the flow calls `EW_TRACK`, which does nothing until it is pointed
somewhere. To switch it on with Plausible, add the script and one line:

    window.EW_TRACK = function(name, props){ plausible(name, {props:props}) }

The events, in order: `pricing_who` or `pricing_door` or `pricing_dial` or
`pricing_row` (a choice was made), `pricing_review` (the plan was opened),
`pricing_confirm` (they said yes), `pricing_close` (they left, with the step
they left from), plus `pricing_see_all` and `pricing_restart`.

The folding steps (2.4.5.4.1 on) add `pricing_kind` (Passes, Membership or
Personal training was chosen) and `pricing_insured` (a member said their
insurance is already paid, which takes the 24 euro off the first payment).

`pricing_list_open` and `pricing_list_close` count the people who prefer the
full table to the calculator.

The drop from `pricing_review` to `pricing_confirm` is the number that says
whether paying online is worth building.
