# Brief BL: fixes after the review of round 22

Read `BK-common.md` first; its rules hold. Each slot replaces a passage now on the page, which is
quoted. Write each slot under its own `## BLn` heading in your draft file, exactly as it should
appear on the page.

## BL1: the failed night's result (replaces the paragraph after the third what-if's cell)

Now: "The table has 6 rows, none for Sunday, and was last altered on Sunday at 02:30, a day earlier
than `clean_orders` and the dashboard. The dashboard refreshed at 03:00 on Monday as usual and shows
the 6 values it found. The query over `clean_orders` is still listed: it gives every row of
`daily_sales`, and one row more, for Sunday. Each record is normal on its own. The gap shows only
when you compare the last-altered times. Only a record of the failure would say that a write was
due and did not happen."

The fault: the records do show a shortfall (6 rows where there were 7; six values on a dashboard
titled "Sales, last 7 days"), so "normal" is wrong. What no record holds is the failure itself.
1. Keep word for word: "The table has 6 rows, none for Sunday, and was last altered on Sunday at
   02:30, a day earlier than `clean_orders` and the dashboard. The dashboard refreshed at 03:00 on
   Monday as usual and shows the 6 values it found."
2. Keep word for word: "The query over `clean_orders` is still listed: it gives every row of
   `daily_sales`, and one row more, for Sunday."
3. The shortfall is there to see: 6 rows where the week as it ran has 7, and six values on a
   dashboard titled "Sales, last 7 days".
4. No record says that it is a failure. Seeing it takes knowing to expect 7 rows, or comparing the
   last-altered times.
5. Keep word for word: "Only a record of the failure would say that a write was due and did not
   happen."

## BL2: one cell of a figure (at most 14 words)

The figure's third row asks "What did each night's job do?". Its middle cell, what the platform
holds, now says "Nothing; after a failed night, each record looks normal". Replace it: the platform
holds nothing about the job; a failed night shows only as a missing row and an older last-altered
time. Start with "Nothing;".

## BL3: "Before Chapter 3" (replaces both paragraphs)

Now: "The platform's state answers what exists. It does not answer what happened or why. Inferring
the history from the data gave an explanation that fitted, and three ordinary changes made it
ambiguous, made it wrong, or left a failed night looking like a normal one. The records that would
have answered had to be made when the work was done." and "Chapter 3 starts making them: a
description of each asset, kept beside the data, with what the asset means and who is responsible
for it. It then asks the four questions at the start again, to see which of them that record
answers. Chapter 6 records what was made from what, which is called lineage. Chapter 7 records each
run of a job: when it started and ended, which version of its code ran, what it read and wrote, and
whether it succeeded."

First paragraph:
1. Keep word for word: "The platform's state answers what exists. It does not answer what happened
   or why."
2. Inferring the history from the data gave an explanation that fitted. Keep the words "three
   ordinary changes": they made it ambiguous (the copy), made it wrong (the edit), or left a failed
   night that no record names as a failure.
3. The records that would have answered had to be made when the work was done.
Second paragraph, as one paragraph:
4. Keep word for word the start: "Chapter 3 starts making them: a description of each asset, kept
   beside the data, with what the asset means and who is responsible for it."
5. It then asks the four questions at the start again.
6. Keep these words: "Chapter 6 records what was made from what, which is called lineage" and
   "each run of a job", in one sentence that also says Chapter 7 records each run of a job. Do not
   list what a run record holds: the figure above did.

## BL4: the metadata paragraph (replaces it)

Now: "Information of this kind, about an asset or about the platform, is called **metadata**: what
an asset is, where it came from, who is responsible for it, what its numbers mean, how it is made,
and how it relates to other assets. Some of it the systems already keep for their own purposes: the
names, types, counts and times you read above. The systems do not keep what an asset means, what
happened to it or what it was made from; somebody has to record those, and the second and third
have to be recorded when the thing happens. A note of what a job read, written the next morning
from the data, is a reconstruction, with the limits shown above."

The fault: "the second and third" makes the reader count back, and it says what a table is made
from can only be recorded at the time, but Chapter 6 reads it from the jobs' code.
1. Keep the first sentence word for word, from "Information of this kind" to "other assets."
2. Keep word for word: "Some of it the systems already keep for their own purposes: the names,
   types, counts and times you read above."
3. They do not keep what an asset means, what it was made from, or what happened to it. Somebody
   has to record those.
4. What happened, such as which tables a night's job read, has to be recorded when it happens.
5. What a table is made from can also be read later, from the jobs' code (Chapter 6). That shows
   what the code says, not what the job did on a given night.
6. Keep word for word: "A note of what a job read, written the next morning from the data, is a
   reconstruction, with the limits shown above."

## BL5: why each system records what it does (replaces the first paragraph under its heading)

Now: "Each of the shop's systems records the things about an asset that its own work needs. The
warehouse keeps column names and types so that it can run a query. Object storage keeps a file's
key so that it can serve the file. The reporting tool keeps the values so that it can draw the
chart. In the shop's platform, a system records what its own work needs and nothing more. The
questions you want answered are not its work."

The fault: "nothing more" is false (an owner, created times, `created_by`), and "not its work" is
vague.
1. Keep word for word the three sentences: "The warehouse keeps column names and types so that it
   can run a query. Object storage keeps a file's key so that it can serve the file. The reporting
   tool keeps the values so that it can draw the chart."
2. Before them: each system records what its own work needs.
3. After them: each keeps a little more, an owner, created times and who created the dashboard.
4. None of it says what an asset means or how it was made.

## BL6: the owner rule's result (replaces the paragraph after the table)

Now: "The rule is met as written, and you did nothing to meet it. The owner it found answers only
the last reading, which account controls the table, so you still do not know whom to ask about
`daily_sales`."
1. The rule is met as written: the warehouse fills in an owner for every table by itself.
2. Keep word for word the second sentence: "The owner it found answers only the last reading, which
   account controls the table, so you still do not know whom to ask about `daily_sales`."

## BL7: the reconstruction's result (replaces the five paragraphs after the cell that prints True)

Two parts: one before two new cells, one after them.

Before the cells:
1. Keep word for word: "It prints `True`: the query gives all 7 rows of `daily_sales`, Thursday's
   5150 pence included."
2. The query also explains the other three days that differ. The two cells below list the
   cancelled orders that `clean_orders` holds, and the orders that `orders.jsonl` holds more than
   once.

After the cells, one paragraph:
3. `clean_orders` holds 2 cancelled orders, 7009 on Tuesday, worth 2999 pence, and 7037 on
   Saturday, worth 2400 pence. Keep the words "2 cancelled orders".
4. The query leaves them out, and so does `daily_sales`: they are Tuesday's and Saturday's gaps.
5. `orders.jsonl` holds order 7015, placed on Wednesday, twice, and `clean_orders` holds it once,
   so Wednesday's gap is its second copy, worth 4500 pence.

## BL8: the check's scenario (replaces its first two sentences)

Now: "A data engineer wants to know which inputs one particular run of a job read." and "They have
three pieces of evidence. Which is the strongest evidence of what that run read?"

The fault: it reads as if the engineer holds all three, which the shop's platform does not.
1. A data engineer wants to know which inputs one particular run of a job read. ("run" as a noun is
   allowed here.)
2. Consider three pieces of evidence they could have. Which is the strongest evidence of what that
   run read?

## BL9: stage 2's box of findings (replaces its two paragraphs)

Keep the form: one paragraph starting `**Established.**`, one starting `**Not established.**`.
Established:
1. Each record describes an asset as it is this morning.
2. For `daily_sales`: its columns and their types, 7 rows, a size, when it was created, a
   last-altered time of 02:30 on Monday 14 September, and an owner, `etl_service`.
3. For each file: its key, size and last-modified time.
4. For the dashboard: its title, who created it, when it last refreshed and the values it shows.
Not established:
5. Which job wrote any of these assets, what the job read, which version of its code ran, what the
   rows were the day before, or who decided the rules that shaped them.
Do not add a sentence after fact 5.
