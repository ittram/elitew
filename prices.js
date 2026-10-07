/*
  ELITE WELLNESS PRICE LIST
  The only file to change when prices change. Copied from the printed preçário
  "em vigor desde 1/10/2026" (photo of 7 October 2026). All prices include VAT.
  The process for a new price list is in CLAUDE.md (Prices) and PRICES.md.

  Rules:
  - member plans are priced PER 2 WEEKS and debited every 2 weeks, not monthly
  - desk is the reception price ("Balcão, sem desconto"), dd the direct debit
    price ("Campanha desconto, com adesão ao débito direto")
  - members pay the annual sports insurance on top; visitors have it included
  - personal training: `each` is the price a session as printed, `total` is
    sessions x each (the pack is paid up front)
  - `pt` is the line as printed on the sheet, so the check script can print the
    list in the sheet's own words and order
  - a price with `todo` is not confirmed yet and the page says so out loud
*/
window.ELITE_PRICES = {
  updated: "2026-10-01",
  vatIncluded: true,

  insurance: { year: 24.00, note: "Annual sports insurance, required by law. Covers accidents during training." },

  member: {
    every: 14,                // days per payment
    plans: [
      { id:"w1", name:"Once a week",        pt:"1x semana (quinzenal)",       visits:1, dd:13.00, desk:18.00 },
      { id:"w3", name:"Three times a week", pt:"3x semana (quinzenal)",       visits:3, dd:19.50, desk:24.50 },
      { id:"un", name:"Unlimited",          pt:"Livre trânsito (quinzenal)",  visits:0, dd:21.00, desk:26.00, best:true }
    ],
    ddSavingYear: 130.00      // 5.00 every 2 weeks, 26 times a year
  },

  visitor: [
    { id:"d1", name:"1 day",   pt:"Diária (1 session)",      days:1,  price:12.00 },
    { id:"s1", name:"1 week",  pt:"1 semana (1 week)",       days:7,  price:40.90 },
    { id:"s2", name:"2 weeks", pt:"2 semanas (2 weeks)",     days:14, price:51.90 },
    { id:"s3", name:"3 weeks", pt:"3 semanas (3 weeks)",     days:21, price:61.90 },
    { id:"s4", name:"4 weeks", pt:"4 semanas (4 weeks)",     days:28, price:69.90 }
  ],

  assessments: {
    packs: [
      { id:"at", name:"Training", pt:"Pack treino (trimestral)",   months:3, price:55.00 },
      { id:"an", name:"Nutrition", pt:"Pack nutrição (trimestral)", months:3, price:70.00 }
    ],
    todo: "[PLACEHOLDER: what each pack includes, e.g. an assessment with a coach and a new programme each month for three months]"
  },

  pt: {
    packs: [
      { id:"one", name:"Single session", pt:"Sessão avulso",                 sessions:1,  each:55.00, total:55.00 },
      { id:"p8",  name:"8 sessions",     pt:"Pack 8 sessões (válido 2 meses)",  sessions:8,  each:47.50, total:380.00, months:2 },
      { id:"p12", name:"12 sessions",    pt:"Pack 12 sessões (válido 2 meses)", sessions:12, each:42.50, total:510.00, months:2 },
      { id:"p20", name:"20 sessions",    pt:"Pack 20 sessões (válido 3 meses)", sessions:20, each:32.50, total:650.00, months:3 }
    ],
    second: 17.50,            // "Pessoa extra", a session
    note: "Packs of two sessions a week or fewer do not include the gym on the other days. To train on the other days, add a member plan."
  },

  includes: [
    "The gym floor and every group class",
    "A first fitness assessment with a coach",
    "Coaching on the floor whenever you need it"
  ],

  /* open questions, answered out loud rather than guessed */
  unconfirmed: {
    ddMinimum: "[PLACEHOLDER: does the direct debit price need a minimum period? e.g. 'no minimum, cancel any time' or 'three months minimum']",
    weekMeaning: "[PLACEHOLDER: does once a week mean one visit each calendar week, or two visits in any two weeks?]",
    assessment: "[PLACEHOLDER: confirm the first assessment is free on every plan, now that assessment packs are sold separately]",
    ptSecondBlock: "[PLACEHOLDER: the 1/10/2026 sheet has a second, unlabelled personal training block (single 40.00, packs 32.50 / 30.00 / 25.00 a session, extra person 12.50). Who is it for, e.g. members?]"
  }
};
