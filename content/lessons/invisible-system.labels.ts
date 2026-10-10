// Copyright © 2026 Christopher Snow

// Titles, objectives, captions and labels of Chapter 1, written as a book: titles name the
// story's movements, captions say what a view shows. Captions, titles and option labels are
// plain text: no Markdown.

export const LABELS = {
  objectives: [
    "See what a platform's current state can and cannot tell you about how its data came to be.",
    "Rebuild an asset from the data, and test what that reconstruction establishes.",
    "Break your own evidence: a copy, an edit, a failed write.",
    "Name the records that would have answered what the state could not.",
  ],
  titles: {
    question: "State and history",
    motivation: "The questions nobody can answer from state",
    prediction: "Thursday",
    investigation: "What the platform holds",
    construction: "What the platform records",
    failureExperiment: "Why reconstruction is unreliable",
    explanation: "Rules the data cannot validate",
    generalisation: "The records a platform needs",
    challenge: "The rule that never fired",
    reflection: "The handover",
  },
  challengeTitles: {
    c1: "Rebuild daily_sales",
    c2: "Which rules filter orders.parquet?",
  },
  captions: {
    platform: "The pipeline: the shop's three systems and what each holds.",
    week: "The shop's first week: order days, a night's work after each, and the morning you start.",
    dashboard: "Monday morning's dashboard: revenue per day, 7 to 13 September.",
    explore: "The four assets this chapter works with. Open each to see what it holds.",
    p2: "Put a number on Thursday before you look.",
    c1: "Build a query that rebuilds daily_sales from another asset.",
    change:
      "Choose a change to the shop, predict how many queries will rebuild daily_sales afterwards, run the week again with it, and read what the systems hold.",
    c2: "Choose which orders the rules keep.",
  },
  /** The control that opens how the lab is built (brief AF). */
  labDetails: "How the lab is built",
  p2Options: {
    same: "51.50, the same total",
    different: "a different total",
  },
  p2Undecided: "I can't tell yet",
  changeOptions: {
    none: "none, so the data no longer points to any query",
    one: "one, so the data still points to a single query",
    twoOrMore: "two or more, so the data fits more than one query",
  },
  hOptions: {},
  cButton: "Read Thursday's rows",
  cHeadings: {},
  c1Fields: {
    source: "Asset to read",
    keep: "Rows to keep",
    measure: "Measure",
    per: "Per",
  },
  c1Options: {
    keep: {
      all: "every row",
      completed: "completed orders only",
      cancelled: "cancelled orders only",
    },
    measure: { revenue: "price times quantity", quantity: "quantity", rows: "the number of rows" },
    per: { day: "day", customer: "customer", product: "product" },
  },
  caseLabels: [
    "Monday 7 September",
    "Tuesday 8 September",
    "Wednesday 9 September",
    "Thursday 10 September",
    "Friday 11 September",
    "Saturday 12 September",
    "Sunday 13 September",
  ],
  changeLabels: {
    copy: "an analyst copies clean_orders every night",
    refunds:
      "the program that writes daily_sales is edited to keep orders that are not refunded, from Saturday's row on",
    failed: "the last night's write of daily_sales fails",
  },
  c2Fields: {
    duplicates: "Orders that appear twice",
    missingCustomer: "Orders with no customer id",
    cancelled: "Cancelled orders",
    quantity: "Orders with a quantity of 0 or less",
  },
  c2Options: {
    duplicates: { keep: "keep both rows", one: "keep one row" },
    missingCustomer: { keep: "keep", drop: "drop" },
    cancelled: { keep: "keep", drop: "drop" },
    quantity: { keep: "keep", drop: "drop" },
  },
  caseLabels2: ["every row of clean_orders is kept", "no row that clean_orders lacks is kept"],
} as const;
