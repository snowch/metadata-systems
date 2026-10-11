// Copyright © 2026 Christopher Snow

// Chapter 1: The shop and its platform (Part I, Why metadata exists), a tour.
//
// The learner reads what the shop's platform holds before Chapter 2 investigates Thursday's
// revenue: the three systems, the three files, the warehouse's three tables, the dashboard and the
// nights, then what the tour could not show. Like Chapter 2 it is an essay with figures and no
// prediction, experiment or challenge to grade (docs/plan.md, "Chapter 1 as an essay"). The map
// and the week are diagrams; the asset cards and the dashboard show the shop's data. Each is
// computed from the shop's data by the engine (packages/lab), which the page never names: a figure
// carries no badge, no mark and no note (timeModel "none", no role). Every number in the prose is
// read off the engine and pinned by shop-and-platform.facts.test.ts.

import type { LessonInput } from "@platform/lesson-schema";

import { LABELS } from "./shop-and-platform.labels";
import { PROSE } from "./shop-and-platform.prose";

/** One file's card, opened to its first rows. */
const card = (id: "products" | "customers" | "orders", asset: string) => ({
  id,
  kind: "asset-cards",
  timeModel: "none" as const,
  caption: LABELS.captions[id],
  props: { cards: [{ id: asset, role: LABELS.roles[id] }], head: 8 },
});

export const shopAndPlatform: LessonInput = {
  id: "shop-and-platform",
  title: "The shop and its platform",
  module: 1,
  order: 1,
  objectives: [...LABELS.objectives],
  introduces: ["asset"],
  termExemptions: [
    {
      term: "run",
      reason:
        "Used as the verb: when the programs are due to run. The noun, one execution of a program, arrives in Chapter 7.",
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
          timeModel: "none",
          caption: LABELS.captions.platform,
          lead: PROSE.platformLead,
          after: PROSE.platformAfter,
          props: { tally: true },
        },
      ],
    },
    {
      kind: "motivation",
      title: LABELS.titles.motivation,
      prose: PROSE.products,
      interactives: [{ ...card("products", "products.parquet"), lead: PROSE.cardsLead }],
    },
    {
      kind: "prediction",
      title: LABELS.titles.prediction,
      prose: PROSE.customers,
      interactives: [card("customers", "customers.parquet")],
    },
    {
      kind: "investigation",
      title: LABELS.titles.investigation,
      prose: PROSE.orders,
      interactives: [card("orders", "orders.parquet")],
    },
    {
      kind: "construction",
      title: LABELS.titles.construction,
      prose: PROSE.warehouse,
      interactives: [
        {
          id: "tables",
          kind: "asset-cards",
          timeModel: "none",
          caption: LABELS.captions.tables,
          props: {
            cards: [
              { id: "clean_customers", role: LABELS.roles.cleanCustomers },
              { id: "clean_orders", role: LABELS.roles.cleanOrders },
              { id: "daily_sales", role: LABELS.roles.dailySales },
            ],
            head: 8,
          },
        },
      ],
    },
    {
      kind: "failureExperiment",
      title: LABELS.titles.failureExperiment,
      prose: PROSE.dashboard,
      interactives: [
        {
          id: "dashboard",
          kind: "dashboard",
          timeModel: "none",
          caption: LABELS.captions.dashboard,
        },
      ],
    },
    {
      kind: "explanation",
      title: LABELS.titles.explanation,
      prose: PROSE.nights,
      interactives: [
        {
          id: "week",
          kind: "week-timeline",
          timeModel: "none",
          caption: LABELS.captions.week,
        },
      ],
    },
    {
      kind: "generalisation",
      title: LABELS.titles.generalisation,
      prose: PROSE.unseen,
    },
    {
      kind: "challenge",
      title: LABELS.titles.challenge,
      prose: PROSE.task,
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
      "A tour of a ready-made sample project, such as dbt's jaffle shop, browsed through its generated documentation and dependency diagram.",
    howThisDiffers:
      "The learner is handed an undocumented platform of an invented bicycle-parts shop, with one line from its head in front of the tour, and reads the shop's own files, tables and dashboard as the systems hold them, with no diagram of what is made from what: the chapter ends by asking the learner to guess, and Chapter 2 asks what such guesses can establish. The shop, its data and its programs are invented for the course.",
  },
};
