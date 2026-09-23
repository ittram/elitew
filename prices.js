/*
  ELITE WELLNESS PRICE LIST
  The only file to change when prices change. Taken from the printed preçário
  (proposed corrections, 23 September 2026). All prices include VAT.

  Rules:
  - member plans are priced PER 2 WEEKS and debited every 2 weeks, not monthly
  - members pay the annual sports insurance on top; visitors have it included
  - a price with `todo` is not confirmed yet and the page says so out loud
*/
window.ELITE_PRICES = {
  updated: "2026-09-23",
  vatIncluded: true,

  insurance: { year: 24.00, note: "Annual sports insurance, required by law. Covers accidents during training." },

  member: {
    every: 14,                // days per payment
    plans: [
      { id:"w1", name:"Once a week",   pt:"1x por semana",   visits:1, dd:13.00, desk:18.00 },
      { id:"w3", name:"Three a week",  pt:"3x por semana",   visits:3, dd:19.50, desk:24.50 },
      { id:"un", name:"Unlimited",     pt:"Livre trânsito",  visits:0, dd:21.00, desk:26.00, best:true }
    ],
    ddSavingYear: 130.00      // 5.00 every 2 weeks, 26 times a year
  },

  visitor: [
    { id:"d1", name:"1 day",   days:1,  price:10.00 },
    { id:"s1", name:"1 week",  days:7,  price:35.90 },
    { id:"s2", name:"2 weeks", days:14, price:45.90 },
    { id:"s3", name:"3 weeks", days:21, price:51.90 },
    { id:"s4", name:"4 weeks", days:28, price:61.90, todo:"[PLACEHOLDER: the corrections document proposes 69.90 so that four weeks as a member is the cheaper choice. Until the family decides, this stays at the current 61.90]" }
  ],

  pt: {
    packs: [
      { id:"one", name:"Single session", sessions:1,  each:50.00, total:50.00 },
      { id:"p8",  name:"8 sessions",     sessions:8,  each:45.00, total:360.00, months:2 },
      { id:"p12", name:"12 sessions",    sessions:12, each:40.00, total:480.00, months:2 },
      { id:"p20", name:"20 sessions",    sessions:20, each:30.00, total:600.00, months:3 }
    ],
    second: 15.00,
    note: "Packs of two sessions a week or fewer do not include the gym on the other days. To train on the other days, add a member plan."
  },

  includes: [
    "The gym floor and every group class",
    "A first fitness assessment with a coach",
    "Coaching on the floor whenever you need it"
  ],

  /* open questions from the price list review, answered out loud rather than guessed */
  unconfirmed: {
    ddMinimum: "[PLACEHOLDER: does the direct debit price need a minimum period? e.g. 'no minimum, cancel any time' or 'three months minimum']",
    weekMeaning: "[PLACEHOLDER: does once a week mean one visit each calendar week, or two visits in any two weeks?]",
    assessment: "[PLACEHOLDER: confirm the first assessment is free on every plan, including once a week]"
  }
};
