// Copyright © 2026 Christopher Snow

// Every word the figures put in front of a learner, in one place. Drafted by the course's prose
// process (CLAUDE.md) from the brief in docs/notes/chapter-01/briefs/F-figure-labels.md and
// checked against the lab. Slots in braces are filled by `format`.

import { createContext, useContext } from "react";

export const DEFAULT_VIEW_STRINGS = {
  labNote:
    "This figure runs the Metadata Lab, a small data platform in your browser. The lab holds the shop's files and tables for the week of 7 to 13 September 2026. The programs in the lab run in SQL over the rows you see. What the figure shows is worked out from those rows each time. The lab's clock is the week's own, not real time. Nothing leaves your browser.",
  badge: "Lab",
  badgeLabel: "How this figure works: {model}",
  modelNote: "How the figures run",
  modelVsReality: "How this lab differs from a real platform",
  modelVsRealityNone: "How the course's model differs from a real platform",
  inputs: "For",
  actual: "Your result",
  expected: "Expected",
  checkPrediction: "Check my prediction",
  predictAgain: "Predict again",
  yourPrediction: "Prediction",
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
    "computed.dashboard": "What does it show?",
    "read-by": "What reads it?",
    worked: "Did last night's write work?",
    responsible: "Who is responsible for it?",
    unit: "In what units are its numbers?",
    changed: "What changed in it this week?",
  } as Record<string, string>,
  a: {
    answered: "Storage records the last write, at {time}.",
    columns: "Storage records {count} column names and their types, not what they mean.",
    title:
      "The reporting tool records the title, {title}, and nothing about where the values come from.",
    "owner-role": "The warehouse records the account {role}, not a person or a team.",
    creator: "The reporting tool records who created it, {person}, not who answers for it now.",
    types: "Storage records {column} as {type}, a number with no unit.",
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
  noChange: "No change",
  runWeek: "Run the week again",
  ranWith: "The week ran with this change: {change}.",
  storageDiffHeading: "What storage shows differently",
  newAsset: "A new file, {asset}, at {location}.",
  changedTime: "{asset} last written at {after}, not {before}.",
  changedRows: "{asset} has {after} rows, not {before}.",
  changedValue: "In {asset}, the row for {day} reads {after}, not {before}.",
  noDiff: "Storage shows no difference.",
  yourQueryHeading: "Your query on the new daily_sales",
  usingYours: "This uses your query from the construction section.",
  usingCourse: "You have not built a passing query yet, so this uses the course's.",
  fitsHeading: "Every query in the builder's choices that rebuilds daily_sales",
  fitsNone: "No query in the builder's choices rebuilds it.",
  describeQuery: "from {source}, {keep}, add up {measure} per {per}",
  place: {
    storage: "Storage records it",
    suggested: "The data suggests it",
    record: "Only a record kept at the time answers it",
  } as Record<string, string>,
  e: {
    time: "Last written at {time}.",
    oneQuery: "One query rebuilds it: {query}.",
    oneSource: "One asset rebuilds it: {source}.",
    manySources: "{count} assets rebuild it equally well: {sources}.",
    manyQueries: "{count} queries rebuild it, from {sources}.",
    noQuery: "No query rebuilds it.",
    readers: "{assets} shows the same numbers.",
    noReaders: "No other asset shows the same numbers.",
    nightDone: "Last written at {time}, with a row for {day}.",
    nightMissing: "Last written at {time}; the latest row is for {latest}, not {expected}.",
    account: "Storage names {role}, an account, not who answers for it.",
    types: "{column} is {type}, with no unit.",
    currentOnly: "Storage keeps only the current rows.",
  } as Record<string, string>,
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
