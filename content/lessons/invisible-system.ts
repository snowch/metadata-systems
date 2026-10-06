// Copyright © 2026 Christopher Snow

// Chapter 1: The invisible data system (Part I, Why metadata exists).
//
// The learner gets the shop's storage and nothing else, and tries to answer the questions anybody
// asks of a platform they did not build. The structure is here; the words are in
// invisible-system.prose.ts and invisible-system.labels.ts. Every figure runs the lab; every
// answer, expected value and number is computed by it, and the chapter's facts test pins the
// numbers the prose states.

import { DAYS } from "@ms/lab";
import type { LessonInput } from "@platform/lesson-schema";

import { LABELS } from "./invisible-system.labels";
import { PROSE } from "./invisible-system.prose";

const options = (labels: Readonly<Record<string, string>>) =>
  Object.entries(labels).map(([value, label]) => ({ value, label }));

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
      interactives: [
        {
          id: "dashboard",
          kind: "dashboard",
          timeModel: "lab",
          caption: LABELS.captions.dashboard,
        },
      ],
    },
    { kind: "motivation", title: LABELS.titles.motivation, prose: PROSE.motivation },
    {
      kind: "prediction",
      title: LABELS.titles.prediction,
      prose: PROSE.prediction,
      interactives: [
        {
          id: "predict-owner",
          kind: "lab-prediction",
          timeModel: "lab",
          caption: LABELS.captions.p1,
          props: {
            question: PROSE.p1Question,
            options: options(LABELS.p1Options),
            probe: { kind: "owner-kind", asset: "daily_sales" },
            explain: PROSE.p1Explain,
          },
        },
        {
          id: "predict-days",
          kind: "lab-prediction",
          timeModel: "lab",
          caption: LABELS.captions.p2,
          props: {
            question: PROSE.p2Question,
            options: options(LABELS.p2Options),
            probe: {
              kind: "days-matching",
              source: "orders.parquet",
              keep: "all",
              target: "daily_sales",
            },
            explain: PROSE.p2Explain,
          },
        },
      ],
    },
    {
      kind: "investigation",
      title: LABELS.titles.investigation,
      prose: "",
      interactives: [
        {
          id: "storage",
          kind: "storage-inspector",
          timeModel: "lab",
          caption: LABELS.captions.inspector,
          lead: PROSE.inspectorLead,
          after: PROSE.inspectorAfter,
          props: { initial: "orders.parquet" },
        },
      ],
    },
    {
      kind: "construction",
      title: LABELS.titles.construction,
      prose: PROSE.construction,
      interactives: [
        {
          id: "build-daily-sales",
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
      prose: "",
      interactives: [
        {
          id: "changes",
          kind: "change-lab",
          timeModel: "lab",
          caption: LABELS.captions.change,
          lead: PROSE.changeLead,
          props: {
            challengeId: "rebuild-daily-sales",
            changes: [
              { id: "copy", label: LABELS.changeLabels.copy, outcome: PROSE.outcomeCopy },
              { id: "refunds", label: LABELS.changeLabels.refunds, outcome: PROSE.outcomeRefunds },
              { id: "failed", label: LABELS.changeLabels.failed, outcome: PROSE.outcomeFailed },
            ],
            afterAll: PROSE.afterAll,
          },
        },
      ],
    },
    {
      kind: "explanation",
      title: LABELS.titles.explanation,
      prose: PROSE.explanation,
      interactives: [
        {
          id: "map",
          kind: "question-map",
          timeModel: "lab",
          caption: LABELS.captions.map,
          lead: PROSE.mapLead,
          after: PROSE.mapAfter,
          props: { challengeId: "rebuild-daily-sales" },
        },
      ],
    },
    {
      kind: "generalisation",
      title: LABELS.titles.generalisation,
      prose: PROSE.generalisation,
      interactives: [
        {
          id: "map-copy",
          kind: "question-map",
          timeModel: "lab",
          caption: LABELS.captions.map2,
          lead: PROSE.map2Lead,
          after: PROSE.map2After,
          props: { challengeId: "rebuild-daily-sales", changes: ["copy"] },
        },
      ],
    },
    {
      kind: "challenge",
      title: LABELS.titles.challenge,
      prose: "",
      interactives: [
        {
          id: "build-rules",
          kind: "challenge",
          timeModel: "lab",
          caption: LABELS.captions.c2,
          lead: PROSE.c2Lead,
          props: { challengeId: "clean-orders-rules" },
        },
      ],
    },
    { kind: "reflection", title: LABELS.titles.reflection, prose: PROSE.reflection },
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
      "A tour of a data catalogue's screens over a ready-made sample project, such as dbt's jaffle shop (the café dbt's guides use: its quickstart's data is customers, orders and payments, and its structure guide builds staging, intermediate and marts models), with its documentation and its dependency diagram already generated for the reader.",
    howThisDiffers:
      "Nothing is generated for the learner: they get storage alone and try to recover what a catalogue would hold, by rebuilding one asset from the others with a query and the raw orders' cleaning rules from their output. The failure experiment then makes that inference ambiguous (an analyst's copy), impossible (an unrecorded edit to a program) and misleading (a failed night), and the chapter's three columns of questions are computed by the lab, not listed. The shop, a bicycle-parts retailer with no payments table, its data, its Thursday incident and its programs in the course's own SQL are invented for the course.",
  },
};
