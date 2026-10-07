// Copyright © 2026 Christopher Snow

// Every word the figures put in front of a learner, in one place. A name between backticks is set
// as code where the figure draws the sentence itself (`Rich`), and dropped where only plain text
// will do (`plain`). Drafted by the course's prose
// process (CLAUDE.md) from the briefs in docs/notes/chapter-01/briefs (F, then the revision's I,
// J, K and L after the review) and checked against the lab. Slots in braces are filled by
// `format`.

import { createContext, useContext } from "react";

export const DEFAULT_VIEW_STRINGS = {
  // What the lab is and holds, its week, how it runs, how a reader uses it and what the browser
  // keeps, in that order (briefs AA, AA2 and AB). It opens from every badge and closes every
  // chapter.
  labNote:
    "The Metadata Lab is a small data platform written for this course. It comes with the page, as code, and runs in your browser: nothing to install, open or sign in to. The shop holds files, tables and a dashboard with real rows, and programs written in SQL that write the tables and the dashboard. The lab holds one week of the shop: its first week online, Monday 7 to Sunday 13 September 2026, invented for the course. The programs run each night of the week. The last night ends early on Monday 14 September.\n\nThe lab reads and runs the programs' SQL itself, with a query engine of its own. Nothing about the shop is stored: each time the page loads, the lab builds the shop's data and runs the whole week, night by night, in memory. Rows and times are the same for every reader. Every date and time a figure shows comes from the week, not today or your clock.\n\nYou use it through figures, each asking the lab something and showing its answer. A figure that shows storage reads what the lab's storage records. The lab runs a query you build, with the same query engine. The lab runs the week again when you change the shop. Your browser keeps your predictions, choices and answers. Nothing you do leaves your browser.",
  badge: "Lab",
  badgeLabel: "How this figure works: {model}",
  // What each figure asks of the learner, on its badge, and the note the badge opens, above the
  // lab's (briefs Z and AC; CLAUDE.md, "Experiments, instruments and explanations"). A reference asks
  // nothing to be done, so its badge opens the lab's note alone (silence is preferable to filler).
  roles: {
    experiment: "Experiment",
    inspect: "Inspect",
    reference: "Reference",
  } as Record<string, string>,
  roleBadgeLabel: "What this figure asks of you is {role}",
  roleNotes: {
    experiment:
      "Commit first to a prediction, a choice or a query you build. Compare what the lab shows with what you expected.",
    inspect:
      "Use this to answer the question just above. Look for the evidence the question needs.",
  } as Record<string, string>,
  modelNote: "How the figures run",
  modelVsReality: "How this lab differs from a real platform",
  modelVsRealityNone: "How the course's model differs from a real platform",
  inputs: "For",
  actual: "Your result",
  expected: "Expected",
  checkPrediction: "Check my prediction",
  yourPrediction: "Prediction",
  yourChoice: "Your choice",
  // Set small above a requirement's own words (brief V).
  requirement: "Requirement",
  youSaid: "You predicted: {choice}.",
  labFound: "The lab found: {answer}.",
  match: "The prediction was correct.",
  noMatch: "The prediction was not correct.",
  daysCaption: "orders.parquet by day compared with daily_sales",
  day: "Day",
  addedUp: "Total from orders.parquet",
  same: "Match",
  yours: "Your result",
  yes: "Yes",
  no: "No",
  assetsHeading: "Assets in storage",
  objectStorage: "Object storage, bucket {bucket}",
  warehouse: "Warehouse, {place}",
  reporting: "Reporting tool",
  recordCaption: "What storage records about {asset}",
  location: "Location",
  kind: "Kind",
  format: "Format",
  columns: "Columns",
  rows: "Rows",
  size: "Size",
  lastModified: "Last modified",
  lastAltered: "Last altered",
  lastRefreshed: "Last refreshed",
  created: "Created",
  ownerRole: "Owner",
  createdBy: "Created by",
  title: "Title",
  kindFile: "file",
  kindTable: "table",
  kindDashboard: "dashboard",
  field: "Field",
  recorded: "Recorded",
  columnsCaption: "Columns and types",
  column: "Column",
  type: "Type",
  rowsCaption: "The {count} rows",
  valuesCaption: "The values the dashboard shows",
  questionsHeading: "What storage says",
  q: {
    "last-written": "When was it last written?",
    "made-from": "What is it made from?",
    computed: "How are its numbers worked out?",
    "read-by": "What reads it?",
    worked: "Did last night's write work?",
    responsible: "Who is responsible for it?",
    unit: "In what units are its numbers?",
    changed: "What changed in it this week?",
  } as Record<string, string>,
  a: {
    answered: "Storage records the last write, at {time}.",
    columns:
      "Storage records the column names and their types, not how the values were worked out.",
    title: "The reporting tool records the title “{title}”, not how the values were worked out.",
    "owner-role":
      "The warehouse records the name `{role}` as the owner, which does not say who is responsible for the table.",
    creator:
      "The reporting tool records who created it, `{person}`, not who is responsible for it now.",
    types: "Storage records `{column}` as `{type}`, a number with no unit.",
    "time-only": "Storage records the last write, at {time}, not whether a write was due.",
    nothing: "Storage records nothing that answers this.",
  } as Record<string, string>,
  builderSql: "Your query, as SQL",
  builderResult: "Result",
  resultCaption: "{count} rows",
  keptRows: "The rules keep {count} rows.",
  p: {
    "unknown-column": "{table} has no column called {column}.",
    "unknown-table": "There is no asset called {name}.",
    other: "The query cannot run.",
  } as Record<string, string>,
  noRow: "no row",
  missingRows: "Your rules drop {count} rows that clean_orders keeps, orders {ids}.",
  extraRows: "Your rules keep {count} rows that clean_orders does not, orders {ids}.",
  changeLegend: "Change",
  firstWeek: "the week as it first ran",
  firstWeekStatus: "This is the week as it first ran, the one you have been reading.",
  runWithChange: "Run with this change",
  ranWith: "The lab ran the whole week again with this change: {change}.",
  locked: "This figure starts once your answer to the challenge called “{title}” passes its tests.",
  // In place of a figure that waits for an answer above it (brief Z3).
  waits: "This figure starts once your answer to “{caption}”, above, is committed.",
  storageNowHeading: "What storage holds on Monday morning",
  compareNote:
    "Storage holds only this week's values. Each comparison with the week as it first ran is the lab's, because it ran both weeks.",
  newAsset: "A new file, `{asset}`, at `{location}`, last modified at {time}.",
  changedTime: "`{asset}` was last written at {after}; in the week as it first ran, at {before}.",
  changedRows: "`{asset}` has {after} rows; in the week as it first ran, {before}.",
  changedValue:
    "In `{asset}`, the row for {day} reads {after}; in the week as it first ran, {before}.",
  noDiff: "Storage holds the same as in the week as it first ran.",
  yourQueryHeading: "Your query against this week's `daily_sales`",
  fitsHeading: "The queries in the builder's choices that rebuild `daily_sales`",
  fitsNone: "None of the builder's choices rebuilds it.",
  describeQuery: "from `{source}`, {keep}, add up {measure} per {per}",
  place: {
    storage: "Storage records it",
    suggested: "The data suggests it",
    record: "Only a record kept at the time answers it",
  } as Record<string, string>,
  sortLegend: "Where each question about `{asset}` is answered",
  sortPick: "Choose a group",
  checkSort: "Check my sorting",
  sortScore: "{matching} of {total} questions are where the lab places them.",
  youPlaced: "You placed it under “{place}”.",
  weekLegend: "Week",
  movedFrom: "In the week as it first ran, it was under “{place}”.",
  needsRecord: "A record of {kind} would answer it.",
  recordKind: {
    "what-it-is": "what the asset is",
    "what-happened": "what happened",
    "made-from-what": "what was made from what",
  } as Record<string, string>,
  e: {
    time: "Last written at {time}.",
    oneQuery: "One query rebuilds it: {query}.",
    oneQueryHidden: "One query in the builder's choices rebuilds it (no query named).",
    oneSource: "One asset rebuilds it: `{source}`.",
    oneSourceHidden: "One asset rebuilds it (no asset named).",
    manySources: "{count} assets rebuild it equally well: {sources}.",
    manySourcesHidden: "{count} assets rebuild it equally well (no assets named).",
    manyQueries: "{count} queries rebuild it, from {sources}.",
    manyQueriesHidden: "{count} queries in the builder's choices rebuild it.",
    noQuery: "None of the builder's choices rebuilds it.",
    readers: "{assets} shows the same numbers.",
    noReaders: "No other asset shows the same numbers.",
    nightDone: "Last written at {time}, with a row for {day}.",
    nightMissing: "Last written at {time}; the latest row is for {latest}, not {expected}.",
    account: "Storage records the name `{role}`, not who is responsible.",
    types: "The column `{column}` is `{type}`, with no unit.",
    currentOnly: "Storage keeps only the current rows.",
  } as Record<string, string>,
  mapLabel: "The shop's data platform",
  systems: {
    "object-storage": "Object storage",
    warehouse: "Warehouse",
    reporting: "Reporting tool",
  } as Record<string, string>,
  mapFlow: "unseen programs move data each night",
  mapOpen: "The map",
  mapClose: "Close",
  scrollCue: "Scroll sideways to see every column.",
  chartLabel: "{title}, last refreshed {time}.",
  refreshed: "Last refreshed {time}.",
  weekdays: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] as readonly string[],
  problem: "Could not display: {message}",
};

export type ViewStrings = typeof DEFAULT_VIEW_STRINGS;

export const ViewStringsContext = createContext<ViewStrings>(DEFAULT_VIEW_STRINGS);
export const useViewStrings = (): ViewStrings => useContext(ViewStringsContext);

/** Fills `{slot}`s in a template. A slot with no value is left as written. */
export function format(template: string, slots: Readonly<Record<string, string | number>>): string {
  return template.replace(/\{(\w+)\}/g, (whole, key: string) => {
    const v = slots[key];
    return v === undefined ? whole : String(v);
  });
}
