# Brief A: question, motivation, prediction

Attach: `common.md`, `../facts.md`, `docs/style.md`. Write to `docs/notes/chapter-01/drafts/A.md`.

## titles.question
A section heading of three to six words for the opening situation: seven assets and a dashboard
whose Thursday looks low.

## question
The chapter's opening, two or three short paragraphs. Facts, in order:
1. You start work as a data engineer at an online shop that sells bicycle parts. It is Monday 14
   September 2026, 09:00.
2. The shop opened its online store a week ago, on Monday 7 September.
3. Its data platform holds seven assets: three files in object storage, three tables in a
   warehouse, and one dashboard in a reporting tool. An asset is anything the platform stores or
   shows: a file, a table or a dashboard. (This is where "asset" is introduced.)
4. Every night, something writes the files, programs you cannot see yet write the tables, and the
   dashboard refreshes.
5. The dashboard below shows revenue per day for the shop's first week. Thursday's figure is far
   lower than the others. The head of the shop asks you why.
6. You can read everything the shop's storage holds. You cannot see anything else yet: not the
   code, not the timetable, not anybody's notes.
7. End with the chapter's question, as a question: how much can you find out from what storage
   holds?

## dashboardCaption
One sentence: the shop's dashboard as the reporting tool shows it on Monday morning: revenue per
day for 7 to 13 September.

## titles.motivation
A heading of three to six words: why these questions come up.

## motivation
One short paragraph and a short list. Facts:
1. A data engineer who joins a platform they did not build is asked questions like these. Give
   them as a list of four questions:
   - Can we delete `products.parquet`?
   - What stops working if the checkout renames a column in `orders.parquet`?
   - Is Thursday's figure wrong, and since when?
   - Who should I ask about `daily_sales`?
2. A wrong answer costs something: a deleted file that a program still reads; a dashboard that is
   wrong for weeks before anybody notices.
3. Each question is about the assets, not about the rows inside them.

## titles.prediction
A heading of three to six words: what you expect storage to tell you.

## prediction
One or two sentences: before you open storage, commit to two predictions; choose an answer, then
press the button to check it.

## p1Caption
One sentence caption for a prediction about the owner the warehouse records for `daily_sales`.

## p1Question
The question, shown before the learner chooses. Facts: the warehouse records an owner for every
table. What will it name as the owner of `daily_sales`? Do not hint at the answer.

## p1Options
Four option labels, one per line, in this order, each a short phrase:
- account: an account that programs log in as
- person: a person
- team: a team, such as finance
- none: no owner at all

## p1Explain
Shown only after the learner commits. Two to four sentences. Facts:
1. The warehouse names `etl_service` as the owner of all three tables.
2. `etl_service` is the account the shop's programs log in as. Storage does not tell you this; the
   course does.
3. So the owner field says which login created the table, not which person or team answers for
   it.
4. A field with the right name answered a different question.

## p2Caption
One sentence caption: predict how many days the raw orders, added up, give the same revenue as
`daily_sales`.

## p2Question
The question, shown before the learner chooses. Facts: `daily_sales` has one row per day: the day
and its revenue. Add up price times quantity over every row of `orders.parquet`, for each day. On
how many of the seven days will your total equal `daily_sales`? Do not hint at the answer.

## p2Options
Three option labels, one per line, in this order:
- all: on all seven days
- some: on some days but not all
- none: on no day

## p2Explain
Shown only after the learner commits, above a table of every day. Two to four sentences. Facts:
1. The totals are the same on 3 days: Monday, Friday and Sunday.
2. They differ on the other 4. On each of those days, `orders.parquet` holds a row that
   `daily_sales` leaves out of revenue.
3. You find those rows in the next section.
