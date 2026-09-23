# Prices

`prices.js` is the only file to change when a price changes. Every 2.4.x draft
reads from it, so one edit updates the picker, the flow and the arithmetic.

## Where the numbers come from

The printed preçário, as corrected in the price list review of 23 September 2026.
All prices include VAT.

## The two things people get wrong

1. **Member plans are priced per 2 weeks, not per month.** €21 is a fortnight of
   unlimited training, so a month is roughly €42. Every treatment says this out
   loud, because a customer who reads €21 as monthly feels tricked when the bank
   shows two payments.
2. **Insurance sits in different places.** Visitor passes include the €24 sports
   insurance. Member plans add it once a year on top. Any comparison between the
   two has to add it, or it is not a comparison.

## Still to confirm

These are in `prices.js` under `unconfirmed`, and the page shows a `todo` chip
rather than guessing:

- Does the direct debit price need a minimum period?
- Does "once a week" mean one visit each calendar week, or two in any two weeks?
- Is the first fitness assessment free on every plan, including once a week?
- The 4 week visitor pass: the review proposes €69.90 so that four weeks as a
  member (€66) is the cheaper choice. The drafts show the current €61.90 until
  the family decides.

## Tracking

Every step of the flow calls `EW_TRACK`, which does nothing until it is pointed
somewhere. To switch it on with Plausible, add the script and one line:

    window.EW_TRACK = function(name, props){ plausible(name, {props:props}) }

The events, in order: `pricing_who` or `pricing_door` or `pricing_dial` or
`pricing_row` (a choice was made), `pricing_review` (the plan was opened),
`pricing_confirm` (they said yes), `pricing_close` (they left, with the step
they left from), plus `pricing_see_all` and `pricing_restart`.

The drop from `pricing_review` to `pricing_confirm` is the number that says
whether paying online is worth building.
