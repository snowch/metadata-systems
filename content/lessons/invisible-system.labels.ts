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
    prediction: "What you expect the systems to tell you",
    investigation: "What the systems record",
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
    platform: "The pipeline: the shop's three systems and what each holds.",
    week: "The shop's first week: order days, a night's work after each, and the morning you start.",
    dashboard: "On Monday morning the dashboard shows daily revenue for 7 to 13 September.",
    p1: "Choose what you would store to meet a requirement, see what it could mean, then see what the shop's warehouse holds.",
    p2: "Predict what Thursday's rows of orders.parquet add up to.",
    where: "Decide which asset you would inspect first, and what you would look for there.",
    hypothesis: "Choose the explanation you will test for the difference on Thursday.",
    check: "Check the explanation you chose against Thursday's rows.",
    inspector: "Inspect what the systems record about each asset, starting with the one you chose.",
    c1: "Build a query that rebuilds daily_sales from another asset.",
    change:
      "Choose a change to the shop, predict how many queries will rebuild daily_sales afterwards, run the week again with it, and read what the systems hold.",
    map: "Sort the eight questions about daily_sales by what can answer them, then let the lab place them.",
    c2: "Choose which orders the rules keep.",
    p3: "Predict whether your setting of the four rules is the only one that passes.",
  },
  /** The control that opens how the lab is built (brief AF). */
  labDetails: "How the lab is built",
  // The requirement, in the author's words, and the figure that questions it (brief V).
  p1Requirement: "Every table must have an owner.",
  p1Commit: "Show what this could mean",
  p1Show: "Show the warehouse",
  p1Options: {
    person: "a person, for example whoever built it",
    team: "a team, for example finance",
    program: "the program that writes it",
    account: "an account that programs log in as",
  },
  p1Undecided: "nothing yet; ask what the owner is for",
  /** What each reading needs stored, for the figure's table. */
  p1Short: {
    person: "a person",
    team: "a team",
    program: "the program that writes it",
    account: "an account that programs log in as",
  },
  /** The question each reading asks; names between backticks, which the figure sets as code. */
  p1Asks: {
    person: "Who is responsible for `daily_sales`?",
    team: "Which team is responsible for `daily_sales`?",
    program: "Which program writes `daily_sales`?",
    account: "Which account controls `daily_sales` in the warehouse?",
  },
  p1Headings: {
    asks: "The question the owner would answer",
    store: "What you would store for it",
    answers: "Whether the warehouse's owner answers it",
  },
  p2Options: {
    same: "51.50: daily_sales holds the total of Thursday's orders",
    different: "a different total: daily_sales is not simply the total of Thursday's orders",
  },
  p2Undecided: "I can't tell yet: nothing so far says what daily_sales measures",
  changeOptions: {
    none: "none, so the data no longer points to any query",
    one: "one, so the data still points to a single query",
    twoOrMore: "two or more, so the data fits more than one query",
  },
  // Where the learner looks first for Thursday's difference: an asset, and the evidence sought
  // there (brief Z).
  wOptions: {
    orders: "orders.parquet, for the orders that make up Thursday's 205.50",
    clean: "clean_orders, to set its Thursday orders beside the raw ones",
    daily: "daily_sales, for how its 51.50 was worked out",
    dashboard: "the dashboard, for where its 51.50 comes from",
  },
  wCommit: "I'll start here",
  // The explanation the learner tests for Thursday, and its check (brief Y).
  hOptions: {
    left: "some of Thursday's orders are not counted in daily_sales",
    lower: "Thursday's orders are counted, but at lower values",
    moved: "some of Thursday's orders are counted on another day",
  },
  hCommit: "Test this explanation",
  cButton: "Read Thursday's rows",
  cHeadings: {
    explanation: "The explanation",
    supported: "Whether Thursday's rows support it",
  },
  p3Options: {
    one: "yes, a setting that gives clean_orders exactly is the only one that does",
    more: "no, another setting can give exactly the same rows",
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
