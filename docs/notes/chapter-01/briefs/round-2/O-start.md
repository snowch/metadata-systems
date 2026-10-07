# Brief O: Sections 1 and 3, the map, and the two first predictions

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/round-2/O.md`.

Section 1 now has two figures: a map of the platform, then the dashboard. Its text splits in
three: the section's prose above the map, a lead above the dashboard, and a closing text below the
dashboard.

## question

Section 1's prose, above the map. It replaces the start of the old text, which said: "You start
work on Monday 14 September 2026 at 09:00. You are a data engineer at an online shop that sells
bicycle parts. The shop opened its online store on Monday 7 September. The platform holds seven
assets, anything it stores or shows: files, tables and a dashboard. Three files sit in object
storage, three tables in the warehouse, one dashboard in the reporting tool. In this chapter,
storage means all three. Every night the three files are written again. Then programs write the
tables and refresh the dashboard." Facts, in this order:

- You start work on Monday 14 September 2026 at 09:00, as a data engineer at an online shop that
  sells bicycle parts. The shop opened its online store on Monday 7 September.
- Every figure on this page runs the Metadata Lab, a small data platform that holds the shop and
  runs in your browser. The lab works out everything a figure shows.
- The shop's data platform has three systems: object storage, a warehouse and a reporting tool.
- Each system holds assets. Define "asset" here, in one sentence, with the fact sheet's meaning:
  something in the platform that can be stored, described, changed, related to other assets, or
  depended on. The shop's assets are files, tables and a dashboard.
- The platform holds seven assets: three files in object storage, three tables in the warehouse,
  one dashboard in the reporting tool. In this chapter, "storage" means all three systems.
- Every night the three files are written again. Then programs write the tables and refresh the
  dashboard. You cannot see the programs.
- The map below shows the systems and their assets, in the order data moves through them each
  night. Once you scroll past it, a button at the foot of the window opens it again.

Do not say what the map leaves out, and do not say which asset is made from which.

## dashboardLead

Shown above the dashboard. Facts:

- The dashboard shows revenue per day for the shop's first week.
- Thursday is far lower than the other days.
- The head of the shop asks you why.

## dashboardAfter

Shown below the dashboard, closing Section 1. Facts:

- You can read everything storage holds.
- You cannot see the code, when each program is due to run, or anybody's notes.
- End with the question: how much can you find out from what storage holds?

## prediction

Section 3's prose, above two predictions. It replaces: "Before you open storage, make two
predictions. Choose an answer for each, then press its button to check it." Facts:

- Before you open storage, make two predictions.
- Each option is an explanation of how the platform works. Choose the one you think more likely,
  then press its button to check it.

One or two sentences.

## p1Question

Shown before the learner commits. Facts:

- The warehouse records an owner for every table.
- Ask: will the owner it records for `daily_sales` name someone you could ask about the table?

## p1Options

Two option labels, each an explanation, parallel in form and length:

- yes: yes, because an owner field names whoever is responsible for the table;
- no: no, because an owner field names the account that writes the table, and programs write the
  tables.

## p2Question

Shown before the learner commits. Facts:

- The dashboard shows 51.50 for Thursday, and `daily_sales` holds the same figure for Thursday.
- Add up price times quantity over Thursday's rows of `orders.parquet`.
- Ask: will the total be 51.50 too?

Do not say or suggest that `daily_sales` is built from `orders.parquet`, or that any orders are
left out.

## p2Options

Two option labels, each an explanation, parallel in form and length. Plain text: write the file
name without backticks.

- same: yes, because Thursday was a slow day, and the raw orders show it too;
- more: no, the total is more, because the orders came in and something on the way to daily_sales
  left some out.

## p2Explain

Shown after the learner commits, under a table that compares every day's two totals. Facts:

- Thursday's rows of `orders.parquet` add up to 205.50. `daily_sales` has 51.50.
- That is close to Wednesday's raw total (198.75) and Friday's (204.24). In `orders.parquet`,
  Thursday was not a slow day.
- The table shows the other days too. The totals are equal on three days: Monday, Friday and
  Sunday. They differ on four, Thursday among them.
- The reason is in the rows of `orders.parquet`, and the next section lets you read them.

Do not say what the rows are or how many there are.

## captions

Three captions, plain text, one sentence each, ending with a full stop:

- platform: the map: the shop's three systems and the assets each holds;
- p1: predict whether the owner the warehouse records for daily_sales is someone you could ask;
- p2: predict whether Thursday's rows of orders.parquet add up to the dashboard's figure.

## mapStrings

The words inside the map, plain text, as a Markdown list with the key before a colon. Keep each
to a few words.

- label: the map's name, read out by a screen reader and shown as the title of the map when it
  opens over the page: the shop's data platform;
- objectStorage, warehouse, reporting: the three systems' names: object storage, warehouse,
  reporting tool (capital first letter, as a heading);
- flow: the label under each arrow between two systems: programs, which you cannot see, move data
  this way each night (a short phrase, under eight words);
- open: the button at the foot of the window that opens the map: names the map;
- close: the button that closes the map: one word.
