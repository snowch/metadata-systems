// Copyright © 2026 Christopher Snow

// Chapter 1: The invisible data system (Part I, Why metadata exists), written as a book.
//
// The prose carries the investigation; a lab appears only where the story needs the learner's
// own hands: the Thursday prediction (put a number on your model before you look), the rebuild
// (the reconstruction), the failure experiment (the evidence breaks), and the cleaning rules
// (the reconstruction underdetermined). The pipeline, the week, the dashboard and the asset
// cards are the book's diagrams. Everything else is prose and a table, both computed by the lab
// and pinned by the facts test.

import { DAYS } from "@ms/lab";
import type { LessonInput } from "@platform/lesson-schema";

import { LABELS } from "./invisible-system.labels";
import { PROSE } from "./invisible-system.prose";

const options = (labels: Readonly<Record<string, string>>) =>
  Object.entries(labels).map(([value, label]) => ({ value, label }));

/** Options that stand for counts: each label with the counts it covers, inclusive. */
const counted = (
  labels: Readonly<Record<string, string>>,
  ranges: Readonly<Record<string, readonly [number, number]>>,
) =>
  Object.entries(labels).map(([value, label]) => {
    const range = ranges[value];
    if (!range) throw new Error(`no range for the option ${value}`);
    return { value, label, range: [range[0], range[1]] as [number, number] };
  });

/** The assets a query in the builder may read: every file or table except the one to rebuild. */
const SOURCES = [
  "customers.parquet",
  "orders.parquet",
  "products.parquet",
  "clean_customers",
  "clean_orders",
];

const HINTS = (h: readonly string[]) => h as unknown as [string, string, string, string, string];

export const invisibleSystem: LessonInput = {
  id: "invisible-data-system",
  title: "The invisible data system",
  module: 1,
  order: 1,
  objectives: [...LABELS.objectives],
  introduces: ["asset", "metadata"],
  termExemptions: [
    {
      term: "run",
      reason:
        "Used as the verb: run a query, run the week again, run the tests. The noun, one execution of a program, arrives in Chapter 6.",
    },
  ],
  sections: [
    {
      kind: "question",
      title: LABELS.titles.question,
      prose: PROSE.question,
      details: { summary: LABELS.labDetails, prose: PROSE.labDetails },
      interactives: [
        {
          id: "platform",
          role: "reference",
          kind: "platform-map",
          timeModel: "lab",
          caption: LABELS.captions.platform,
          lead: PROSE.platformLead,
          after: PROSE.platformAfter,
          props: { tally: true },
        },
        {
          id: "week",
          role: "reference",
          kind: "week-timeline",
          timeModel: "lab",
          caption: LABELS.captions.week,
          lead: PROSE.weekLead,
        },
        {
          id: "explore",
          role: "inspect",
          kind: "asset-cards",
          timeModel: "lab",
          caption: LABELS.captions.explore,
          lead: PROSE.exploreLead,
          props: {
            // The four assets the chapter works through, one card each. A card shows up to
            // seven rows, so the two small tables appear whole; the large files show a head.
            head: 7,
            cards: [
              {
                id: "orders.parquet",
                role: "The raw orders the shop took, written each night to a file",
              },
              { id: "clean_orders", role: "Orders after the cleaning step, held in the warehouse" },
              { id: "daily_sales", role: "One row per day: the totals the dashboard reports" },
              { id: "sales_dashboard", role: "The reporting view built from the data" },
            ],
          },
        },
        {
          id: "dashboard",
          role: "inspect",
          kind: "dashboard",
          timeModel: "lab",
          caption: LABELS.captions.dashboard,
          after: PROSE.dashboardAfter,
        },
      ],
    },
    {
      kind: "motivation",
      title: LABELS.titles.motivation,
      prose: PROSE.motivation,
    },
    {
      kind: "prediction",
      title: LABELS.titles.prediction,
      prose: PROSE.prediction,
      interactives: [],
    },
    {
      kind: "investigation",
      title: LABELS.titles.investigation,
      prose: PROSE.investigation,
    },
    {
      kind: "construction",
      title: LABELS.titles.construction,
      prose: PROSE.construction,
      interactives: [
        {
          id: "build-daily-sales",
          role: "experiment",
          kind: "challenge",
          timeModel: "lab",
          caption: LABELS.captions.c1,
          lead: PROSE.c1Lead,
          props: { challengeId: "rebuild-daily-sales" },
        },
      ],
    },
    {
      kind: "failureExperiment",
      title: LABELS.titles.failureExperiment,
      prose: PROSE.changeLead,
      interactives: [
        {
          id: "changes",
          role: "experiment",
          kind: "change-lab",
          timeModel: "lab",
          caption: LABELS.captions.change,
          props: {
            challengeId: "rebuild-daily-sales",
            changes: [
              { id: "failed", label: LABELS.changeLabels.failed, outcome: PROSE.outcomeFailed },
            ],
            afterAll: PROSE.afterAll,
            prediction: {
              question: PROSE.changeQuestion,
              options: counted(LABELS.changeOptions, {
                none: [0, 0],
                one: [1, 1],
                twoOrMore: [2, 1000],
              }),
            },
          },
        },
      ],
    },
    {
      kind: "explanation",
      title: LABELS.titles.explanation,
      prose: PROSE.explanation,
    },
    {
      kind: "generalisation",
      title: LABELS.titles.generalisation,
      prose: PROSE.generalisation,
    },
    {
      kind: "challenge",
      title: LABELS.titles.challenge,
      prose: PROSE.c2Lead,
      interactives: [
        {
          id: "build-rules",
          role: "experiment",
          kind: "challenge",
          timeModel: "lab",
          caption: LABELS.captions.c2,
          props: { challengeId: "clean-orders-rules" },
        },
      ],
    },
    {
      kind: "reflection",
      title: LABELS.titles.reflection,
      prose: PROSE.reflection,
    },
  ],
  challenges: [
    {
      id: "rebuild-daily-sales",
      title: LABELS.challengeTitles.c1,
      task: PROSE.c1Task,
      gradedDirection: "answer",
      fields: [
        {
          id: "source",
          label: LABELS.c1Fields.source,
          kind: "choice",
          options: SOURCES.map((s) => ({ value: s, label: s })),
        },
        {
          id: "keep",
          label: LABELS.c1Fields.keep,
          kind: "choice",
          options: options(LABELS.c1Options.keep),
        },
        {
          id: "measure",
          label: LABELS.c1Fields.measure,
          kind: "choice",
          options: options(LABELS.c1Options.measure),
        },
        {
          id: "per",
          label: LABELS.c1Fields.per,
          kind: "choice",
          options: options(LABELS.c1Options.per),
        },
      ],
      initial: {
        answers: { source: "orders.parquet", keep: "all", measure: "revenue", per: "day" },
      },
      tests: {
        kind: "answers",
        grader: "reproduces",
        cases: DAYS.map((day, i) => ({
          label: LABELS.caseLabels[i] ?? day,
          given: { day, target: "daily_sales" },
          expect: { row: "same" },
        })),
      },
      hints: HINTS(PROSE.c1Hints),
      reference: {
        answers: { source: "clean_orders", keep: "completed", measure: "revenue", per: "day" },
      },
    },
    {
      id: "clean-orders-rules",
      title: LABELS.challengeTitles.c2,
      task: PROSE.c2Task,
      gradedDirection: "answer",
      fields: (["duplicates", "missingCustomer", "cancelled", "quantity"] as const).map((id) => ({
        id,
        label: LABELS.c2Fields[id],
        kind: "choice" as const,
        options: options(LABELS.c2Options[id]),
      })),
      initial: {
        answers: {
          duplicates: "keep",
          missingCustomer: "keep",
          cancelled: "keep",
          quantity: "keep",
        },
      },
      tests: {
        kind: "answers",
        grader: "same-rows",
        cases: [
          {
            label: LABELS.caseLabels2[0],
            given: { target: "clean_orders" },
            expect: { missing: 0 },
          },
          { label: LABELS.caseLabels2[1], given: { target: "clean_orders" }, expect: { extra: 0 } },
        ],
      },
      hints: HINTS(PROSE.c2Hints),
      // The program the shop really runs: it drops orders with a quantity of 0 or less, a rule
      // this week's data cannot show (docs/lab.md).
      reference: {
        answers: {
          duplicates: "one",
          missingCustomer: "drop",
          cancelled: "keep",
          quantity: "drop",
        },
      },
    },
  ],
  modelVsReality: PROSE.modelVsReality,
  originalityNote: {
    textbookExample:
      "A tour of a data catalogue's screens over a ready-made sample project, such as dbt's jaffle shop, with its documentation and its dependency diagram already generated for the reader.",
    howThisDiffers:
      "This chapter is a first morning told as a story: the learner is handed an undocumented platform and one line from the head of the shop, and every conclusion is one they reconstruct from the data themselves. The chapter's spine is the gap between a reconstruction that fits and the truth: the rebuild is evidence, and the copy, the edit and the failed night each break that evidence in a way the data alone cannot repair. The shop, a bicycle-parts retailer, its data, its Thursday incident and its programs in the course's own SQL are invented for the course.",
  },
};
