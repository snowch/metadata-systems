# Brief H: the objectives and Sections 1 to 3

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/revision/H.md`.

## objectives

Four items, shown at the top of the chapter before anything else. Each says what the learner will
do, as an imperative, in plain words, without saying what they will find. No word the learner has
not met: not "metadata", not "record kept at the time", not "match", not "ambiguous".

1. Read what each of the shop's three systems keeps about a file, a table and a dashboard.
2. Rebuild one asset from another with a query, and test what that shows.
3. Change the shop in three ways and see what the data can still tell you.
4. Sort questions about an asset by what can answer them, then check your sort against the lab.

## question

Section 1's prose, above a figure of the dashboard. Facts, in this order:

- You start work on Monday 14 September 2026 at 09:00, as a data engineer at an online shop that
  sells bicycle parts. The shop opened its online store on Monday 7 September.
- The platform holds seven assets. Define "asset" here: anything the platform stores or shows, a
  file, a table or a dashboard.
- Three files sit in object storage, three tables in the warehouse, one dashboard in the reporting
  tool. In this chapter, "storage" means all three systems and what they keep.
- Every night the three files are written again; then programs you cannot see yet write the
  tables and refresh the dashboard.
- The dashboard below shows revenue per day for the shop's first week. Thursday is far lower than
  the other days. The head of the shop asks you why.
- You can read everything storage holds. You cannot see anything else yet: not the code, not when
  each program is due to run, not anybody's notes.
- Every figure on this page runs the Metadata Lab, a small data platform that holds the shop and
  runs in your browser. The lab works out everything a figure shows. (One or two sentences.)
- End with the question: how much can you find out from what storage holds?

## motivation

Section 2's prose. Facts:

- A data engineer who joins a platform they did not build is asked questions like these four.
  Give them as a Markdown list, exactly as written:
  - Can we delete `products.parquet`?
  - What stops working if the checkout renames a column in `orders.parquet`?
  - Is Thursday's figure wrong, and since when?
  - Who should I ask about `daily_sales`?
- A wrong answer to the first breaks a program that still reads the file.
- A wrong answer to the third can leave a figure wrong for weeks before anybody notices.
- None of the four can be answered by reading rows alone.

Do not say the questions are "about the assets, not the rows". No "real things", no vague cost.

## prediction

Section 3's prose, above two predictions. Facts: before you open storage, make two predictions;
choose an answer for each, then press its button to check it. Keep it to one or two sentences.

## p1Question

Shown before the learner commits. Facts: the warehouse records an owner for every table; what
will it name as the owner of `daily_sales`? One or two sentences.

## p1Options

Four option labels, shown before the learner commits, one per line as a Markdown list in this
order, with the key before a colon (`person: ...`). Each names a kind of owner; all four must be
the same kind of thing (a candidate owner) and equally plausible:

- person: a person, for example whoever built it
- team: a team, for example finance
- program: the program that writes it
- account: an account that programs log in as

## p1Explain

Shown after the learner commits, under the lab's answer. Facts:

- The warehouse records the name `etl_service` as the owner of all three tables.
- `etl_service` is the account all four of the shop's programs log in as. The lab tells you this;
  storage does not.
- So the owner field names an account. It does not say which person or team is responsible for
  the table.
- A field with the right name answered a different question.

Do not say the owner is whoever created the table: storage records no creator for a table.

## p2Question

Shown before the learner commits. Facts:

- `daily_sales` has one row per day, with the day and the revenue.
- The prediction: add up price times quantity over every row of `orders.parquet`, for each day,
  and compare the totals with `daily_sales`.
- Ask: on how many of the seven days will the two be equal?

Do not say or suggest that `daily_sales` is built from `orders.parquet`.

## p2Options

Four option labels, shown before the learner commits, as a Markdown list with the key before a
colon, in this order:

- all: all seven
- six: six, every day but Thursday
- fourOrFive: four or five
- threeOrFewer: three or fewer

## p2Explain

Shown after the learner commits, under a table of each day's two totals. Facts:

- The totals are equal on three days: Monday, Friday and Sunday.
- They differ on the other four, Thursday among them.
- The reason is in the rows of `orders.parquet`, and the next section lets you read them.

Do not say what the rows are or how many there are.

## captions

Three captions, one per figure, as a Markdown list with the key before a colon. Plain text, one
sentence each, ending with a full stop:

- dashboard: on Monday morning the dashboard shows daily revenue for 7 to 13 September.
- p1: predict the owner the warehouse records for `daily_sales` (write the name without
  backticks in a caption).
- p2: predict on how many days the totals of `orders.parquet` equal `daily_sales` (no
  backticks).
