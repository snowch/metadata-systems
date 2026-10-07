// Copyright © 2026 Christopher Snow

// Titles, objectives, captions and labels of Chapter 1, drafted by the prose process from the
// briefs in docs/notes/chapter-01/briefs and checked against the lab (CLAUDE.md). Captions,
// titles and option labels are plain text: no Markdown.

export const LABELS = {
  objectives: [
    "Read what each of the shop's three systems keeps about a file, a table and a dashboard.",
    "Rebuild one asset from another with a query, and test what that shows.",
    "Change the shop in three ways and see what the data can still tell you.",
    "Sort questions about an asset by what can answer them, then check your sort against the lab.",
  ],
  titles: {
    question: "A week of questions",
    motivation: "Why these questions matter",
    prediction: "What you expect storage to tell you",
    investigation: "What storage records",
    construction: "Rebuilding daily_sales",
    failureExperiment: "The shop changed three ways",
    explanation: "What each system keeps",
    generalisation: "Data and the records around it",
    challenge: "Recovering the rules of clean_orders",
    reflection: "What you could not find out",
  },
  challengeTitles: {
    c1: "Rebuild daily_sales",
    c2: "Which rules filter orders.parquet?",
  },
  captions: {
    platform: "The map: the shop's three systems and the assets each holds.",
    dashboard: "On Monday morning the dashboard shows daily revenue for 7 to 13 September.",
    p1: "Predict whether the owner the warehouse records for daily_sales is someone you could ask.",
    p2: "Predict whether Thursday's rows of orders.parquet add up to the dashboard's figure.",
    inspector: "Browse the seven assets and what storage records about each.",
    c1: "Build a query that rebuilds daily_sales from another asset.",
    change:
      "Choose a change to the shop, predict how many queries will rebuild daily_sales afterwards, run the week again with it, and read what storage holds.",
    map: "Sort the eight questions about daily_sales by what can answer them, then let the lab place them.",
    c2: "Choose which orders the rules keep.",
    p3: "Predict whether your setting of the four rules is the only one that passes.",
  },
  p1Options: {
    yes: "yes, because an owner field names whoever is responsible for the table",
    no: "no, because an owner field names the account that writes the table, and programs write the tables",
  },
  p2Options: {
    same: "yes, because Thursday was a slow day, and the raw orders show it too",
    more: "no, the total is more, because the orders came in and something on the way to daily_sales left some out",
  },
  changeOptions: {
    none: "none, so the data no longer points to any query",
    one: "one, so the data still points to a single query",
    twoOrMore: "two or more, so the data fits more than one query",
  },
  p3Options: {
    one: "yes, because every rule you chose decides some row this week",
    more: "no, because some rule decides no row this week",
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
