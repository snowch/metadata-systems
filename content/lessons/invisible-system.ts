// Copyright © 2026 Christopher Snow

// Chapter 1: The invisible data system (Part I, Why metadata exists), written as an essay.
//
// The prose carries the whole investigation: the shop's state, the questions it cannot answer,
// Thursday's gap, the fields and what they are for, a reconstruction of `daily_sales` and the
// three changes that break it, the rule the week never tests, and the records that would have
// answered. The four figures are the essay's diagrams and its evidence: the pipeline, the week,
// the asset cards and the dashboard, each a view of the lab. Every number in the prose is read
// off the lab and pinned by invisible-system.facts.test.ts.

import type { LessonInput } from "@platform/lesson-schema";

import { LABELS } from "./invisible-system.labels";
import { PROSE } from "./invisible-system.prose";

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
            // The four assets the essay works through, one card each. A card shows up to seven
            // rows, so the two small tables appear whole; the large files show a head.
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
      interactives: [],
    },
    {
      kind: "failureExperiment",
      title: LABELS.titles.failureExperiment,
      prose: PROSE.failureExperiment,
      interactives: [],
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
      prose: PROSE.handover,
      interactives: [],
    },
    {
      kind: "reflection",
      title: LABELS.titles.reflection,
      prose: PROSE.reflection,
    },
  ],
  challenges: [],
  modelVsReality: PROSE.modelVsReality,
  originalityNote: {
    textbookExample:
      "A tour of a data catalogue's screens over a ready-made sample project, such as dbt's jaffle shop, with its documentation and its dependency diagram already generated for the reader.",
    howThisDiffers:
      "This chapter is a first morning told as an essay: the learner is handed an undocumented platform and one line from the head of the shop, and every conclusion is drawn from the shop's own data, which the lab computes and the figures show. The chapter's spine is the gap between a reconstruction that fits and the truth: the rebuild is evidence, and the copy, the edit and the failed night each break that evidence in a way the data alone cannot repair. The shop, a bicycle-parts retailer, its data, its Thursday incident and its programs in the course's own SQL are invented for the course.",
  },
};
