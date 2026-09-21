/*
  ELITE WELLNESS CLASS TIMETABLE
  This file is the only thing to change when the timetable changes.
  See TIMETABLE.md for the update workflow and the prompt for ChatGPT.

  Rules:
  - day: mon, tue, wed, thu, fri, sat or sun
  - time: 24h "HH:MM"
  - class: one of the keys in "classes" below (add a new key for a new class)
  - isNew: true shows a "new" tag next to the class
*/
window.ELITE_SCHEDULE = {
  updated: "2026-09-21",
  poster: "assets/timetable.webp",

  classes: {
    hyrox:    { name: "HYROX",           en: "Hybrid training",         pt: "Aula híbrida" },
    gap:      { name: "GAP",             en: "Glutes, abs and legs",    pt: "Glúteos, abdominais e pernas" },
    trx:      { name: "TRX",             en: "Suspension training",     pt: "Suspension training" },
    mobility: { name: "Mobility",        en: "Flexibility and mobility", pt: "Flexibilidade e mobilidade" },
    abs:      { name: "Abs",             en: "Core strength",           pt: "Abdominais" },
    bike:     { name: "Bike Elite",      en: "Indoor cycling",          pt: "Bike Elite" },
    pilates:  { name: "Pilates",         en: "Mat pilates",             pt: "Pilates" },
    hiit:     { name: "Circuit HIIT",    en: "High intensity circuit",  pt: "Circuito HIIT" }
  },

  sessions: [
    { day: "mon", time: "09:30", minutes: 30, class: "hyrox" },
    { day: "mon", time: "18:30", minutes: 40, class: "gap" },
    { day: "mon", time: "19:20", minutes: 40, class: "hyrox" },

    { day: "tue", time: "09:30", minutes: 30, class: "mobility", isNew: true },
    { day: "tue", time: "18:30", minutes: 40, class: "trx" },
    { day: "tue", time: "19:20", minutes: 40, class: "bike" },

    { day: "wed", time: "09:30", minutes: 30, class: "trx" },
    { day: "wed", time: "18:30", minutes: 40, class: "gap" },
    { day: "wed", time: "19:20", minutes: 40, class: "pilates", isNew: true },

    { day: "thu", time: "09:30", minutes: 30, class: "gap" },
    { day: "thu", time: "18:30", minutes: 40, class: "abs" },
    { day: "thu", time: "19:20", minutes: 40, class: "bike" },

    { day: "fri", time: "09:30", minutes: 30, class: "abs" },
    { day: "fri", time: "18:30", minutes: 40, class: "trx" },
    { day: "fri", time: "19:20", minutes: 40, class: "hiit" }
  ]
};
