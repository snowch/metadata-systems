// Copyright © 2026 Christopher Snow

// Titles, objectives, captions and labels of Chapter 1, drafted by the prose process from the
// briefs in docs/notes/chapter-01/briefs and checked against the lab (CLAUDE.md). Captions,
// titles and option labels are plain text: no Markdown.

export const LABELS = {
  objectives: [
    "Say what the shop's storage records about a file, a table and a dashboard, and what it does not.",
    "Rebuild an asset from another asset with a query, and say what a match does and does not prove.",
    "Show, with three changes to the shop, how evidence from data becomes ambiguous, impossible or misleading.",
    "Sort questions about an asset by what can answer them: storage, the data, or only a record kept at the time.",
  ],
  titles: {
    question: "A week of questions",
    motivation: "Why these questions matter",
    prediction: "What you expect storage to tell you",
    investigation: "What storage records",
    construction: "Rebuilding daily_sales",
    failureExperiment: "Three changes storage does not record",
    explanation: "What each system needs to record",
    generalisation: "Data and the records around it",
    challenge: "Recovering the rules of clean_orders",
    reflection: "What you could not find out",
  },
  challengeTitles: {
    c1: "Rebuild daily_sales",
    c2: "Which rules filter orders.parquet?",
  },
  captions: {
    dashboard: "On Monday morning, the dashboard shows daily revenue for 7 to 13 September.",
    p1: "Predict the owner the warehouse records for daily_sales.",
    p2: "How many days do orders.parquet totals match daily_sales?",
    inspector: "Browse the seven assets and what storage records about each.",
    c1: "Use the query builder to find what builds daily_sales.",
    change: "Choose a change to the shop, run the week again, and compare what storage shows.",
    map: "Each question about daily_sales sits in one column: where storage records the answer, where the data suggests it, or where only a record kept at the time can answer it.",
    map2: "Each question about daily_sales with the analyst's copy in storage: the data can now suggest two sources.",
    c2: "Choose which orders to filter out.",
  },
  p1Options: {
    account: "an account that programs log in as",
    person: "a person",
    team: "a team, such as finance",
    none: "no owner at all",
  },
  p2Options: {
    all: "on all seven days",
    some: "on some days but not all",
    none: "on no day",
  },
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
    refunds: "the program that writes daily_sales is edited for refunds",
    failed: "the last night's write of daily_sales fails",
  },
  c2Fields: {
    duplicates: "Copies of the same order",
    missingCustomer: "Orders with no customer id",
    cancelled: "Cancelled orders",
    quantity: "Orders with a quantity of 0 or less",
  },
  c2Options: {
    duplicates: { keep: "keep every copy", one: "keep one" },
    missingCustomer: { keep: "keep", drop: "drop" },
    cancelled: { keep: "keep", drop: "drop" },
    quantity: { keep: "keep", drop: "drop" },
  },
  caseLabels2: ["every row of clean_orders is kept", "no row that clean_orders lacks is kept"],
} as const;
