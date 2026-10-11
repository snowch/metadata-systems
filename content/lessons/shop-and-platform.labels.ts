// Copyright © 2026 Christopher Snow

// Titles, objectives, captions and card roles of Chapter 1. Titles name the section's subject; a
// caption says what a figure shows. All plain text: no Markdown. Drafted from brief AV
// (docs/notes/chapter-01/briefs/), with the first title from brief AW and the objectives the
// chapter's notebook already had (brief AO).

export const LABELS = {
  objectives: [
    "Name the shop's three systems, and what each one holds: files, tables or a dashboard.",
    "Read the shop's products, customers and orders as their files store them.",
    "Read the rows of the warehouse's three tables, and the values the dashboard shows.",
    "Say what happens on the platform each night, and what you cannot see of it: the programs, when they are due to run, and any notes.",
  ],
  titles: {
    question: "The platform's three systems",
    motivation: "The files in object storage",
    prediction: "The customers file",
    investigation: "The orders file",
    construction: "The warehouse tables",
    failureExperiment: "The dashboard",
    explanation: "What happens each night",
    generalisation: "What the tour cannot show",
    challenge: "Your guesses about the warehouse tables",
    reflection: "Before Chapter 2",
  },
  captions: {
    platform: "The shop's three systems and what each holds.",
    products: "The card for products.parquet, one of the three files in object storage.",
    customers: "The card for customers.parquet, one of the three files in object storage.",
    orders: "The card for orders.parquet, one of the three files in object storage.",
    tables: "The cards for the three tables in shop.analytics.",
    dashboard: "Monday morning's dashboard: revenue per day, 7 to 13 September.",
    week: "The shop's first week: order days, a night's work after each, and the morning you start.",
  },
  roles: {
    products: "The shop's product catalogue, with prices and last editors.",
    customers: "The shop's customers, with their countries and sign-up dates.",
    orders: "Checkout orders, one row per order line.",
    cleanCustomers: "The shop's customers, in the warehouse, with five columns.",
    cleanOrders: "The shop's orders, in the warehouse, with seven columns.",
    dailySales: "Revenue for each day, from 7 to 13 September.",
  },
} as const;
