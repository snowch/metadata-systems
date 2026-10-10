# Brief AQ: part 1 opens with the story

The author kept the chapter in two parts and asked for the story to be introduced differently: the
head of the shop's message opens part 1 again, as it opened the chapter before the split, so the
tour of the platform has a purpose; part 2 still holds the investigation. Two slots. Every fact
below is the chapter's own. Write each slot as plain sentences, following `docs/style.md` and the
writing standard in `AGENTS.md`. Do not add facts. Do not mention a lab, an engine, a simulator,
marimo, Pyodide or WebAssembly. Do not describe how the page or the chapter is organised beyond the
facts given. The reader is "you", a data engineer. British English. No em dashes.

## What part 1 says around the slots, kept word for word

1. The first paragraph, restored as it was: "You start work on Monday 14 September 2026 at 09:00, as
   the data engineer of an online shop that sells bicycle parts. The shop opened its online store a
   week ago, on Monday 7 September. Nobody who built its data platform is there to ask, and nothing
   about it is written down. Before you have sat down, the head of the shop sends you one line:
   Thursday's revenue looks wrong." Then slot **bridge**, as the paragraph's last sentence.
2. The next paragraph: "The platform has three systems: object storage, which holds files; a
   warehouse, which holds tables; and a reporting tool, which holds a dashboard. Every night,
   programs read the files, write the tables and refresh the dashboard. You can read everything the
   three systems hold. You cannot see the programs, when they are due to run, or any note anybody
   kept."
3. Then how to run a cell, the systems' figure, the week, and a section each for the product
   catalogue, the customers, the orders, the warehouse's three tables and the dashboard, each with
   cells that read it. The dashboard's figure shows each day's revenue, 7 to 13 September. Then
   slot **close**, the last paragraph of part 1.

## Slots

- **bridge**: one sentence. Facts: you cannot yet tell whether Thursday's figure is wrong; to tell,
  you first need to know what the platform holds and what happens on it each night.
- **close**: one or two sentences, after the dashboard. Facts: part 2 goes back to the head of the
  shop's line and starts on Thursday's revenue. Include a Markdown link to part 2, written as
  `[link text](part-2.html)`. Do not repeat the line itself.
