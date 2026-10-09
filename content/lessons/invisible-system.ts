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
          after: PROSE.weekAfter,
        },
        {
          id: "dashboard",
          role: "inspect",
          kind: "dashboard",
          timeModel: "lab",
          caption: LABELS.captions.dashboard,
          lead: PROSE.dashboardLead,
          after: PROSE.dashboardAfter,
        },
        {
          id: "explore",
          role: "inspect",
          kind: "asset-cards",
          timeModel: "lab",
          caption: LABELS.captions.explore,
          lead: PROSE.exploreLead,
          props: {
            // The four assets the chapter works through, one card each: see what the platform
            // holds before any question. Nothing is asked or scored here. A card shows up to
            // seven rows, so the two small tables appear whole; the two large files show a head.
            head: 7,
            cards: [
              { id: "orders.parquet", role: LABELS.roles.orders },
              { id: "clean_orders", role: LABELS.roles.clean },
              { id: "daily_sales", role: LABELS.roles.daily },
              { id: "sales_dashboard", role: LABELS.roles.dashboard },
            ],
          },
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
          id: "predict-days",
          role: "experiment",
          kind: "lab-prediction",
          timeModel: "lab",
          caption: LABELS.captions.p2,
          props: {
            known: PROSE.p2Known,
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
          id: "where-first",
          role: "experiment",
          kind: "decision",
          timeModel: "lab",
          caption: LABELS.captions.where,
          props: {
            // The effect is established; first, where to look. Each option is an asset and the
            // evidence sought there; the line after the choice says what that asset can show, a
            // fact of its shape, never what it shows for Thursday. The inspector opens on it.
            question: PROSE.wQuestion,
            options: Object.entries(LABELS.wOptions).map(([value, label]) => ({
              value,
              label,
              after: PROSE.wAfter[value as keyof typeof PROSE.wAfter],
            })),
            commit: LABELS.wCommit,
            mine: PROSE.wMine,
            test: PROSE.wNext,
          },
        },
        {
          id: "storage",
          role: "inspect",
          kind: "storage-inspector",
          timeModel: "lab",
          caption: LABELS.captions.inspector,
          lead: PROSE.inspectorLead,
          props: {
            initial: "orders.parquet",
            from: {
              figure: "where-first",
              assets: {
                orders: "orders.parquet",
                clean: "clean_orders",
                daily: "daily_sales",
                dashboard: "sales_dashboard",
              },
            },
          },
        },
        {
          id: "predict-owner",
          role: "experiment",
          kind: "lab-prediction",
          timeModel: "lab",
          caption: LABELS.captions.p1,
          props: {
            // Ownership, from evidence (the user's redesign): the learner has just read what the
            // warehouse records about daily_sales, so each option is a conclusion they could draw
            // from it, and the lab says which the record supports. The requirement wording stays
            // in the authoring notes, not on the page.
            known: PROSE.p1Known,
            question: PROSE.p1Question,
            options: meaning(LABELS.p1Options, {
              person: ["person"],
              team: ["team"],
              none: ["none"],
              account: ["account"],
            }),
            undecided: {
              value: "undecided",
              label: LABELS.p1Undecided,
              line: PROSE.p1UndecidedLine,
            },
            probe: { kind: "owner-kind", asset: "daily_sales" },
            explain: PROSE.p1Explain,
          },
        },
        {
          id: "why-thursday",
          role: "experiment",
          kind: "decision",
          timeModel: "lab",
          caption: LABELS.captions.hypothesis,
          props: {
            // Then the cause, as an explanation the learner chooses and tests with the figures
            // that follow, checked after their rebuild passes.
            question: PROSE.hQuestion,
            options: THURSDAY,
            commit: LABELS.hCommit,
            mine: PROSE.hMine,
            test: PROSE.hTest,
          },
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
          role: "experiment",
          kind: "challenge",
          timeModel: "lab",
          caption: LABELS.captions.c1,
          lead: PROSE.c1Lead,
          props: { challengeId: "rebuild-daily-sales" },
        },
        {
          id: "why-thursday-check",
          role: "experiment",
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
          role: "experiment",
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
          role: "experiment",
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
          role: "experiment",
          kind: "challenge",
          timeModel: "lab",
          caption: LABELS.captions.c2,
          lead: PROSE.c2Lead,
          props: { challengeId: "clean-orders-rules" },
        },
        {
          id: "predict-rules",
          role: "experiment",
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
      "Nothing is generated for the learner: they get the systems alone, and a pipeline of the platform's systems and assets that shows no asset made from another, and try to recover what a catalogue would hold, by rebuilding one asset from the others with a query and the raw orders' cleaning rules from their output. Each prediction offers conclusions the evidence could support, not facts about the shop to guess: the owner prediction asks what the warehouse's record, read moments before in the inspector, establishes about who to ask, and its options are the conclusions that record could support. Where a catalogue's tour shows an owner field already filled in, this chapter makes the learner read the record and conclude from it that the field names an account, not a person, so the question stays open. The failure experiment then makes that inference ambiguous (an analyst's copy), out of the builder's reach (an unrecorded edit to a program) and misleading (a failed night that leaves the dashboard looking up to date), each after the learner predicts it; and the learner sorts the chapter's questions before the lab places them in three groups, computed, not listed. The shop, a bicycle-parts retailer with no payments table, its data, its Thursday incident and its programs in the course's own SQL are invented for the course.",
  },
};
