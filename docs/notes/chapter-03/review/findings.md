# Chapter 3 review: findings (first read, 12 October 2026)

Reviewed as a learner who has done Chapters 1 and 2. Ranked most serious first. Quotes are from the page as built (as-built) or after the edit (after-edit). I checked the numbers the page states against the page and Chapter 2, and none was wrong. They are 3850x2 + 4500 + 3200 = 15400; 20550 - 15400 = 5150; 5 + 7 + 2 = 14 columns; 5 + 7 = 12; 3 + 2 + 3 = 8 products. No finding gives the answer to a prediction cell.

## Blocking

### 1. The page's own instructions put the answers on screen before the learner has written a prediction
- Quoted:
  - "Nothing on the page runs until you run it. Run every cell first: press **Run all**, at the top of the page." (steps box)
  - "Then select the cell and press **Run below**." (record cell)
  - "Before you run the cells below, write in the next cell, for each question, whether your record answers it..." (The four questions again)
  - "Before you read on, write in the next cell whether the line ... meets it" (requirement section)
  - "Before you run the cells below, write in the next cell, for each change, whether the check of `daily_sales` will report a problem." (A record nobody updates)
- Problem: all three prediction cells say "before you run the cells below", but the learner has been told to run every cell first. **Run below** on the record cell also runs every cell beneath it. After either step the outputs already sit under each prediction cell, so the learner can predict only by choosing not to look. The page never says that is what "before you run" asks. CLAUDE.md requires a prediction to commit the learner before the figure answers.
- Direction: decide how a prediction is protected in a notebook that is run in bulk. Options:
  - Tell the learner at the first prediction that the outputs below already exist, and ask them to write before scrolling.
  - Name the cells to run (record cell alone, then each prediction, then the rest) instead of **Run below** from the top.
  - Restructure so the answering cells do not run until the prediction is saved.
  Whichever is chosen, the "before you run" sentences must be true of the page as the learner meets it.

### 2. The record is filled in with a fact the two messages do not state: who is responsible for `daily_sales`
- Quoted:
  - "Replace each `........` with what the head of the shop and Jo Marsh told you." (A record of `daily_sales`)
  - The head's message: "Jo Marsh, in finance, built the dashboard and decides what counts as revenue. Sam Lund keeps the product catalogue. The two cleaned tables ... are now yours."
  - "The record answers the fourth question: it names Jo Marsh as responsible for `daily_sales`." (The four questions again)
- Problem:
  - Neither message says who is responsible for the table `daily_sales`. They say who decides what counts as revenue, who built the dashboard, and that the cleaned tables are the reader's. Who to ask about the job that writes `daily_sales`, or about a failed night, is not stated.
  - The page turns "decides what counts as revenue" into `responsible` without comment, then reports as a result that the record "answers" who to ask. Chapter 2 spent a section on "owner" meaning several questions. This chapter treats `responsible` as settled one chapter later, which is the failure "Question the requirement" exists to prevent.
  - The lookup also returns exactly what the learner typed, so "answers" overstates what the cell shows.
- Direction:
  - Either have a message say who is responsible for the table and for what, or let the `responsible` line carry the narrower fact the message gives and say what question it answers (who decides what the numbers mean).
  - Say plainly that the cell returns what was written, and what makes that useful (it is kept and the next engineer can query it).

### 3. "A record nobody updates" concludes more than its own last cell supports, and mislabels what changed
- Quoted:
  - "Your record still says what Jo means by revenue. From Saturday the table counts a cancelled order. Nothing on the platform recorded the edit. So nothing prompted a change to your record, and the check could not see the edit. A record written by hand stays as written while the platform changes. An operational record ... would have shown the edit."
  - "The check caught a new column, but not a changed meaning." (Before Chapter 4)
  - "how would you find out when a table's meaning changed?" (closing question)
  - The section heading "A record nobody updates".
- Problems:
  - The record is not stale after the edit. Jo's meaning has not changed; the table has moved away from it. The heading, "a changed meaning" and "when a table's meaning changed" describe the wrong thing changing.
  - The cell just above ("Saturday now differs too: 21549 pence ... against 19149") shows that the recorded meaning, queried against the table, does reveal the edit's effect. The next paragraph then says the edit could not be seen.
  - `records.check` compares columns. The Jo query compares values with the recorded meaning. The page runs both and then speaks as if there were one detector.
  - "would have shown the edit" overreaches. The comparison with Jo's meaning already shows a difference from Saturday. What a record made at the time of the change adds is which job version wrote each night and what changed, not that something differs.
  - Chapter 7 (plan row 7, and Chapter 2) records a code version per run, not "which version of the job's code wrote each row".
- Direction:
  - Say what each check compares and what each detects.
  - Name the new column as an incomplete record, and the edit as a table that no longer matches its recorded meaning.
  - Say what the value comparison cannot tell: what changed, when the job changed, who changed it.
  - Rename the heading and the closing question to match.
  - Align the Chapter 7 description with Chapter 2's.

### 4. A false claim about what changes with every write
- Quoted: "The row count, the size and the last-altered time change with every write to the table." (What the platform records already)
- Problem:
  - For this table the row count does not change with the nightly write. `daily_sales` has 7 rows every night. Chapter 2 says of the edited week "The table still has 7 rows and the same last-altered time".
  - Size is "an estimate from its rows" (Chapter 2's closing note), so it follows rows, not writes.
  - Only the last-altered time is tied to a write.
- Direction: say only what holds. The last-altered time records when the last write happened; the row count and size describe the table now.

### 5. The sort into "what happened to it" contradicts Chapter 2's finding about the warehouse
- Quoted: "Together with the created time, they record what happened to the table." (What the platform records already). Chapter 2 says: "The platform records the current state of each asset and none of its history." and "The platform's state answers what exists. It does not answer what happened or why."
- Problem:
  - A learner just told the warehouse keeps no history is now told it records what happened to the table.
  - A row count and a size are current state. Only the created and last-altered times trace events, and each is a single time.
  - "Records of the second kind say what happened to it" gives a file's size the same status as an event.
  - The dashboard's creator is sorted as "what happened", while the table's owner (an account) is sorted as "what it is". Both name who, and the criterion that separates them is not given.
- Direction: reconcile with Chapter 2, so these fields are traces of the last event and not a history. State the criterion that puts a creator with events and an owner with description, or move the creator.

### 6. After **Run all**, the prose describes output the page does not show
- Quoted (as-built):
  - "The record answers the fourth question: it names Jo Marsh as responsible for `daily_sales`." sits above an output of "........".
  - "For change 2, the check reports nothing: the edit changed no column." sits under an output that lists two problems.
  - "so the check lists the 12 columns" sits above a 14-row table.
- Problem: the step order is Run all, fill in the record, Run below. Between the first and the last, three passages say things the screen contradicts, and nothing tells the learner this is expected. Only the record cell's own "Replace each ..." warns that anything is unfilled.
- Direction: add a one-line note at the record cell that everything below is stale until it is filled in and run, or make the dependent prose conditional ("once your record is written, it names ..."). Related to finding 1; fixing 1 may fix this.

### 7. The definition of metadata does not sort the chapter's own example
- Quoted:
  - "`updated_by` says who last changed each product. ... It is data about the shop's business."
  - "So what makes information metadata is what it describes: an asset, or the work done on the platform. Where the information is kept, and who wrote it, does not decide that." (A column that names a person)
- Problem:
  - "Who last changed each product" is a fact about an edit, which is work done. A last-modified-by column on a row is audit information in most systems.
  - The page asserts it is business data without applying its own criterion. The edit happens in the catalogue, outside the three systems, and a product is a business thing and not one of the platform's assets, but none of that is said.
  - A definition must hold for every case the course meets (CLAUDE.md), and this one can be turned against the example it was built from.
  - The wording also differs from Chapter 2's ("about an asset or about the platform").
- Direction: say what `updated_by` describes (a product in the catalogue, and an edit made outside the platform). Say what would make such a column metadata (if it were read as a fact about the file or table that holds it). Reuse Chapter 2's wording of the definition and do not give a second one.

### 8. "Record" is used for three things
- Quoted:
  - "A record is a set of lines of text that you write and keep beside the data."
  - "Records of the first kind say what an asset is. Records of the second kind say what happened to it."
  - "The warehouse records each table's columns" (verb)
  - The check's "The records do not describe this column, because there is no means line for it..." (plural, while the learner has one record, in a variable `records`)
  - "An operational record, made when the job changed ..."
  - Also "meaning", "description" and "requirement" are used for one thing in "Jo Marsh's description came from the person who decides ...".
- Problem: the definition makes a record a document of several lines. The next section uses the word for one kind of information a system keeps, and the check's message uses it for the learner's whole set. CLAUDE.md names *record* among the words that may not mean two things on one page.
- Direction: keep "record" for the learner's set of lines and give the other senses another word ("information", "facts"), or use one sense everywhere. Make the check's message agree with the variable. Use "meaning" for what Jo gave and "description" for the `means` line.

## Minor

9. **The example line is one of the five to be written.** The example "`daily_sales revenue_pence unit: pence`" matches the cell's `daily_sales revenue_pence unit: ........`. Use another asset or column.

10. **The lookup of lines naming `products.csv` or `orders.jsonl` cannot fail.**
    - Quoted: "The last cell lists each line of your record that names `products.csv` or `orders.jsonl`." and "It finds none."
    - All five lines the learner wrote are about `daily_sales`, so "No rows." follows from what they typed. "The last cell" is wrong, since eight sections follow.
    - Direction: frame the cell as showing that no line could say what reads a file, or have the learner try to write one, and drop "last".

11. **"The words ... do not say what to do with an order the export wrote twice" overstates the ambiguity.**
    - An order written twice is still one order; the ambiguity is in what a line of the file is. The paragraph before has already said the query "keeps each completed order once, even an order the export wrote twice", so the decision is announced before it is discussed.
    - Direction: say the file can hold one order on two lines and the query chose to count orders, or cut one of the two mentions.

12. **The comparison with the reconstruction's meaning says more than it shows.**
    - Quoted: "A description written from the data agrees with the data on every day, so it cannot show that any day is wrong."
    - A description chosen because it reproduces `daily_sales` cannot differ from it by construction, and the page does not say so.
    - The earlier cell does not say why Tuesday, Wednesday and Saturday, which differed from the raw totals in Chapter 2, now agree with Jo's meaning.
    - Direction: one clause on each.

13. **The requirement exercise's readings do not fit the line it asks about.**
    - Quoted: "whether the line `daily_sales revenue_pence means: the revenue in pence` meets it", "The unit. It needs a `unit` line that says pence.", "Under the other readings", and "the requirement is met as written".
    - The line already says "in pence". "Needs a `unit` line" comes from this notation having a `unit` field, not from the requirement.
    - One line cannot meet "Every column must have a description".
    - "Under the other readings" has no listed first reading; as-written was never listed as one.
    - "Met as written" is the check's rule (a `means` line with a value), not the requirement's.
    - Direction: ask about the one column, say "the check's rule" where it is the check, and list the readings so that "as written" is one of them.

14. **The check's output repeats one sentence 12 or 14 times.**
    - Quoted: "The records do not describe this column, because there is no means line for it or its value is still only dots."
    - The "or" hedges between two causes the check can tell apart, and "dots" means nothing for a table the learner wrote no line for.
    - Direction: make the message state which cause applies, and shorten or group the rows.

15. **The "line" column is unexplained and starts at 2.** The record shows "2 | daily_sales | | means ..." and `by_name` shows "13 | daily_sales | day ...". The record's first line is 2 because the string starts with a newline, while `by_name` starts at 1. Explain the number or start at 1.

16. **The check's second capability is never exercised.** The page says the check will "list each line that names a column the warehouse does not have", but nothing in the chapter triggers it. `responsible` and `unit` are never checked either. Use it or drop the sentence.

17. **The opening is narration, not the first question.**
    - Quoted: "Next, you write what you have learnt as a record kept beside the data, then ask Chapter 2's four questions again." (AGENTS.md rule 12)
    - "You asked the head of the shop who decides what `daily_sales` should count" is an action the learner did not take in Chapter 2.
    - Direction: state the problem instead, namely what the next engineer would need written down.

18. **"A column that names a person" puts an instrument before any question.** The count has no question in front of it. The prose then restates the output ("The cell counts `k.adeyemi` 3, `r.novak` 2 and `s.lund` 3. Three people last edited the 8 products.") before giving the conclusion. Ask whether `s.lund` in the column says who to ask about the file, then run the count, and cut the restating sentence.

19. **"What the platform records already" is five paragraphs of prose with no action.**
    - The warehouse, object storage and dashboard paragraphs largely restate Chapter 2's "What the platform holds". The new content is the sort and the word schema.
    - "Object storage records a file's key, which says what the file is and where it is": a key is a name and a location, so "what the file is" overstates.
    - Direction: shorten the section to the sort, with the fields as a list.

20. **`schema` has a second meaning on screen.** Chapter 2's output showed `table_schema | analytics`, a namespace. This chapter defines schema as columns and types and queries `information_schema`. One clause saying what `information_schema` is would keep the two apart.

21. **The closing questions.**
    - Quoted: "Which question does a column's description need to answer before a check can tell it apart from the column's name?" The chapter said a check "cannot tell whether a description says more than the column's name", so the question presupposes it can.
    - "how would you find out when a table's meaning changed?" is partly answered in the chapter (see 3).
    - None of the three leads towards Chapter 4. The paragraph above them carries that.
    - "Whether those are one person" is answered by the head's message ("Jo Marsh ... built the dashboard") and the dashboard's `j.marsh`; what no record says is that they are the same.
    - Direction: say what no record connects, and end with a question about identity.

22. **Objectives and wording.**
    - Quoted: "Tell what a record of an asset holds, from what the systems record about it." and "Test a requirement about descriptions, and a check, against changes to the shop." The first is hard to parse; the second mixes two experiments.
    - The "Before Chapter 4" summary ("The experiments showed that your record answered ...") omits the requirement result and the descriptive/operational sort, which two of the four objectives are about.

## What I read
- `docs/notes/chapter-03/review/brief.md`, CLAUDE.md as given in the task, `AGENTS.md`, `docs/prompts/review-learner-facing-prose.md`.
- Chapter 2 as built (`docs/notes/chapter-02/review/round-17/chapter_02-after-reviews.md`) in full.
- Chapter 3 as built and after the edit, in full.
- `docs/notes/chapter-03.md`, and the Chapter 3 and Chapter 7 rows of `docs/plan.md`.
- `notebook/chapter_03.py` and `notebook/shop/data.py` only for the order-7015 sentence and the Chapter 7 wording.

## What I could not check
- I did not run the notebook, so outputs are those in the two built pages. The Wednesday claim (order 7015 on the 9th, written twice) is confirmed by `notebook/shop/data.py` and the tests.
- I did not check the PostgreSQL `COMMENT ON` paragraph against the documentation; the notes record the source. Plain `\d` does not show descriptions (`\d+` and `\dt+` do), so a reader trying plain `\d` will see none.
- I did not read `docs/style.md`, `docs/sources.md` or `docs/authoring.md`, so term-gate and filler-list conformance is not checked.
- Layout, phone width, dark theme and the figures' appearance are not checked; only the captions are in the text pages.
