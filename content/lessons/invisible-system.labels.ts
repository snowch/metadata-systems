// Copyright © 2026 Christopher Snow

// Titles, objectives and captions of Chapter 1. Titles name the section's subject; a caption says
// what a figure shows. All plain text: no Markdown.

export const LABELS = {
  objectives: [
    "Read what the shop's three systems record about a file, a table and a dashboard.",
    "Work out from the data how `daily_sales` could have been made, and see what that does and does not establish.",
    "Follow three changes to the shop that leave the data unable to say what happened.",
    "Name the records that would have answered the questions the platform could not.",
  ],
  titles: {
    question: "The shop and its platform",
    motivation: "Questions the platform cannot answer",
    prediction: "Thursday",
    investigation: "What the platform holds",
    construction: "What the fields are for",
    failureExperiment: "Reconstruction",
    explanation: "A rule the week never tests",
    generalisation: "Records made at the time",
    challenge: "The handover",
    reflection: "Before Chapter 2",
  },
  captions: {
    platform: "The shop's three systems and what each holds.",
    week: "The shop's first week: order days, a night's work after each, and the morning you start.",
    explore: "Four of the platform's seven assets.",
    dashboard: "Monday morning's dashboard: revenue per day, 7 to 13 September.",
  },
} as const;
