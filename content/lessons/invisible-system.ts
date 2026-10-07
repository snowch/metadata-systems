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

/**
 * Options that stand for what a probe names: each label with the answers it stands for. Each
 * option is an explanation the learner could hold; the lab's answer picks one.
 */
const meaning = (
  labels: Readonly<Record<string, string>>,
  means: Readonly<Record<string, readonly string[]>>,
) =>
  Object.entries(labels).map(([value, label]) => {
    const m = means[value];
    if (!m) throw new Error(`no answers for the option ${value}`);
    return { value, label, means: [...m] };
  });

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

/** The explanations the learner can test for Thursday, and what the rows must show for each. */
const THURSDAY = meaning(LABELS.hOptions, { left: ["left"], lower: ["lower"], moved: ["moved"] });

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
          id: "platform",
          kind: "platform-map",
          timeModel: "lab",
          caption: LABELS.captions.platform,
        },
        {
          id: "dashboard",
          kind: "dashboard",
          timeModel: "lab",
          caption: LABELS.captions.dashboard,
          lead: PROSE.dashboardLead,
          after: PROSE.dashboardAfter,
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
          kind: "requirement",
          timeModel: "lab",
          caption: LABELS.captions.p1,
          props: {
            // A requirement that does not say what it is for (CLAUDE.md, "Question the
            // requirement"): the learner chooses what to store, then sees the four questions it
            // could be asking, then what the warehouse records and which question that answers.
            requirement: LABELS.p1Requirement,
            question: PROSE.p1Question,
            options: meaning(LABELS.p1Options, {
              person: ["person"],
              team: ["team"],
              program: ["program"],
              account: ["account"],
            }).map((o) => ({
              ...o,
              short: LABELS.p1Short[o.value as keyof typeof LABELS.p1Short],
              asks: LABELS.p1Asks[o.value as keyof typeof LABELS.p1Asks],
            })),
            undecided: { value: "undecided", label: LABELS.p1Undecided },
            probe: { kind: "owner-kind", asset: "daily_sales" },
            buttons: { choose: LABELS.p1Commit, show: LABELS.p1Show },
            headings: LABELS.p1Headings,
            text: {
              mine: PROSE.p1Mine,
              undecided: PROSE.p1Undecided,
              meanings: PROSE.p1Meanings,
              lab: PROSE.p1Lab,
              explain: PROSE.p1Explain,
            },
          },
        },
        {
          id: "predict-days",
          kind: "lab-prediction",
          timeModel: "lab",
          caption: LABELS.captions.p2,
          props: {
            question: PROSE.p2Question,
            // A total and the belief behind it, or "I can't tell yet": what the raw orders add up
            // to, not why they might differ, which the investigation finds.
            options: meaning(LABELS.p2Options, { same: ["same"], different: ["more", "less"] }),
            undecided: {
              value: "undecided",
              label: LABELS.p2Undecided,
              line: PROSE.p2UndecidedLine,
            },
            probe: {
              kind: "day-total",
              source: "orders.parquet",
              keep: "all",
              target: "daily_sales",
              day: "2026-09-10",
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
          id: "why-thursday",
          kind: "hypothesis",
          timeModel: "lab",
          caption: LABELS.captions.hypothesis,
          props: {
            // The effect is established; now the cause, as an explanation the learner chooses
            // and tests with the figures that follow, checked after their rebuild passes.
            question: PROSE.hQuestion,
            options: THURSDAY,
            commit: LABELS.hCommit,
            mine: PROSE.hMine,
            test: PROSE.hTest,
          },
        },
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
        {
          id: "why-thursday-check",
          kind: "hypothesis-check",
          timeModel: "lab",
          caption: LABELS.captions.check,
          props: {
            of: "why-thursday",
            options: THURSDAY,
            requires: "rebuild-daily-sales",
            probe: {
              kind: "day-gap",
              source: "orders.parquet",
              via: "clean_orders",
              keep: "completed",
              target: "daily_sales",
              day: "2026-09-10",
            },
            button: LABELS.cButton,
            headings: LABELS.cHeadings,
            text: {
              mine: PROSE.cMine,
              none: PROSE.cNone,
              lab: PROSE.cLab,
              explain: PROSE.cExplain,
            },
          },
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
      interactives: [
        {
          id: "map",
          kind: "question-map",
          timeModel: "lab",
          caption: LABELS.captions.map,
          lead: PROSE.mapLead,
          after: PROSE.mapAfter,
          props: {
            challengeId: "rebuild-daily-sales",
            weeks: (["copy", "refunds", "failed"] as const).map((id) => ({
              id,
              label: LABELS.changeLabels[id],
            })),
          },
        },
      ],
    },
    { kind: "generalisation", title: LABELS.titles.generalisation, prose: PROSE.generalisation },
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
        {
          id: "predict-rules",
          kind: "lab-prediction",
          timeModel: "lab",
          caption: LABELS.captions.p3,
          props: {
            question: PROSE.p3Question,
            // Asked once the learner's rules pass, so the count is at least one: theirs alone,
            // or more than one, of the sixteen settings.
            options: counted(LABELS.p3Options, { one: [1, 1], more: [2, 16] }),
            probe: { kind: "clean-fits" },
            explain: PROSE.p3Explain,
            requires: "clean-orders-rules",
          },
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
      "Nothing is generated for the learner: they get storage alone, and a map of the platform's systems and assets that shows no asset made from another, and try to recover what a catalogue would hold, by rebuilding one asset from the others with a query and the raw orders' cleaning rules from their output. Each prediction offers explanations of how the platform works, not numbers to guess. Where a catalogue's tour shows an owner field already filled in, this chapter starts from a requirement in words, \"Every table must have an owner.\": the learner chooses what to store, meets the four questions the requirement could be asking, and only then sees the warehouse's own meaning and which question it answers. The failure experiment then makes that inference ambiguous (an analyst's copy), out of the builder's reach (an unrecorded edit to a program) and misleading (a failed night that leaves the dashboard looking up to date), each after the learner predicts it; and the learner sorts the chapter's questions before the lab places them in three groups, computed, not listed. The shop, a bicycle-parts retailer with no payments table, its data, its Thursday incident and its programs in the course's own SQL are invented for the course.",
  },
};
