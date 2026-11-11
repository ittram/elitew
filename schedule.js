/*
  ELITE WELLNESS CLASS TIMETABLE
  This file is the only thing to change when the timetable changes.
  See TIMETABLE.md for the update workflow and the prompt for ChatGPT.

  Rules:
  - day: mon, tue, wed, thu, fri, sat or sun
  - time: 24h "HH:MM"
  - class: one of the keys in "classes" below (add a new key for a new class)
  - isNew: true shows a "new" tag next to the class
  - in classes: en and pt are the short line under the name on the English and the Portuguese page;
    about and aboutPt are one or two plain sentences on what the class is, shown when a class is tapped
*/
window.ELITE_SCHEDULE = {
  updated: "2026-10-07",
  poster: "assets/timetable.webp",

  classes: {
    hyrox:    { name: "HYROX",           en: "Hybrid training",         pt: "Treino híbrido",
               about: "Running mixed with strength work: sled pushes, lunges, wall balls. Built on the HYROX race format and scaled to your level.",
               aboutPt: "Corrida intercalada com exercícios de força: empurrar o trenó, lunges, wall balls. Segue o formato das provas HYROX, adaptado ao teu nível." },
    gap:      { name: "GAP",             en: "Glutes, abs and legs",    pt: "Glúteos, abdominais e pernas",
               about: "Floor and standing work for the glutes, abs and legs, with your bodyweight or light weights.",
               aboutPt: "Trabalho no chão e de pé para glúteos, abdominais e pernas, com o peso do corpo ou pesos leves." },
    trx:      { name: "TRX",             en: "Suspension training",     pt: "Treino em suspensão",
               about: "Strength training on suspension straps, using your own bodyweight. You make it harder or easier by how you stand.",
               aboutPt: "Treino de força em fitas de suspensão, com o peso do teu corpo. Ficas com mais ou menos carga conforme a posição dos pés." },
    mobility: { name: "Mobility",        en: "Flexibility and mobility", pt: "Flexibilidade e mobilidade",
               about: "Slow, controlled stretches and joint work. Good for stiff hips, backs and shoulders, and for recovery days.",
               aboutPt: "Alongamentos lentos e controlados e trabalho articular. Bom para ancas, costas e ombros presos, e para dias de recuperação." },
    abs:      { name: "Abs",             en: "Core strength",           pt: "Abdominais",
               about: "A short, focused session for the core: abs, obliques and lower back.",
               aboutPt: "Uma sessão curta e focada no core: abdominais, oblíquos e lombar." },
    bike:     { name: "Bike Elite",      en: "Indoor cycling",          pt: "Ciclismo indoor",
               about: "Indoor cycling with climbs, sprints and recovery. You set your own resistance.",
               aboutPt: "Ciclismo indoor com subidas, sprints e recuperação. És tu que escolhes a resistência." },
    pilates:  { name: "Pilates",         en: "Mat pilates",             pt: "Pilates de solo",
               about: "Mat pilates: slow, precise movements for core strength, posture and control.",
               aboutPt: "Pilates de solo: movimentos lentos e precisos para a força do core, a postura e o controlo." },
    hiit:     { name: "Circuit HIIT",    en: "High intensity circuit",  pt: "Circuito HIIT",
               about: "Short bursts of hard work with short rests, moving round a circuit of stations.",
               aboutPt: "Períodos curtos de esforço intenso com pausas curtas, a rodar por um circuito de estações." }
  },

  sessions: [
    { day: "mon", time: "09:30", minutes: 30, class: "hyrox" },
    { day: "mon", time: "18:30", minutes: 40, class: "gap" },
    { day: "mon", time: "19:20", minutes: 40, class: "hyrox" },

    { day: "tue", time: "09:30", minutes: 30, class: "mobility", isNew: true },
    { day: "tue", time: "18:30", minutes: 40, class: "abs" },
    { day: "tue", time: "19:20", minutes: 40, class: "bike" },

    { day: "wed", time: "09:30", minutes: 30, class: "trx" },
    { day: "wed", time: "18:30", minutes: 40, class: "gap" },
    { day: "wed", time: "19:20", minutes: 40, class: "trx" },

    { day: "thu", time: "09:30", minutes: 30, class: "gap" },
    { day: "thu", time: "18:30", minutes: 40, class: "bike" },
    { day: "thu", time: "19:20", minutes: 40, class: "pilates", isNew: true },

    { day: "fri", time: "09:30", minutes: 30, class: "abs" },
    { day: "fri", time: "18:30", minutes: 40, class: "trx" },
    { day: "fri", time: "19:20", minutes: 40, class: "hiit" }
  ]
};
