# Brief: requirement boxes, Chapter 2's rule, and Chapter 8's ownership facet

Read `docs/style.md` first; its rules hold. Every chapter from 2 to 17 questions one requirement.
Each chapter's requirement now stands in a box of its own, the same style in every chapter. Write
only what each slot below asks, from its facts. Never write "field", "figure", "lab" or an em dash.

## Slot C2a: Chapter 2, the sentences before the box (replaces a paragraph)

- Keep this sentence as it is: "The owner the warehouse records shows how far that goes."
- "Who should I ask about `daily_sales`?" wants a person or a team.

## Slot C2b: Chapter 2, the one sentence inside the box

- Data teams often adopt a rule so that every table has someone to ask about it.
- The rule's words, quoted exactly: "Every table must have an owner."
- One sentence, ending with the quoted rule.

## Slot C2c: Chapter 2, the sentences after the box

- You adopt the rule for the shop's platform.
- The cell below lists the owner the warehouse records for each table.
- Do not name `etl_service` or say what the cell shows.

## Slots H3 to H17: nine section headings

Each of these sections is headed now by its requirement's words in quotes, and the box with the
requirement now comes straight below the heading, so the heading must not repeat the requirement.
Write a short heading (two to six words) that names the section's technical subject, in plain
words. A heading names the subject, never the reader's activity ("Questioning", "Thinking about",
"What do you think"), and is not a question. It must differ from the chapter's other headings,
listed with each slot. Use `code` for a name only where the facts give one.

- H3, Chapter 3. Requirement: "Every column must have a description." Subject: what a column's
  description must say; the section sets five meanings (the check's rule, the column's meaning, its
  unit, where its values come from, whether it may be empty). Other headings: Monday afternoon; A
  record of `daily_sales`; The four questions again; What the platform keeps; A column that names a
  person; When the platform changes; Before Chapter 4.
- H6, Chapter 6. Requirement: "Record the lineage of `daily_sales`." Subject: four things the lineage
  of `daily_sales` could be (what someone says the job reads; what its code reads now; what it read
  each night; which columns each column is made from). Other headings: The jobs' code; Lineage; What
  the rename affects; A line from a belief; A line gone stale; Before Chapter 7.
- H7, Chapter 7. Requirement: "Record every run." Subject: which fields a record of every run needs,
  set against four readings. Other headings: How many orders, each night; Events; Telling runs apart;
  What each run read; Before Chapter 8.
- H9, Chapter 9. Requirement: "The graph must show the current lineage." Subject: three meanings of
  "current" for the graph's lineage. Other headings: From events to a graph; Parse; Normalise;
  Objects; A facet the stage does not read; Edges; Before Chapter 10.
- H11, Chapter 11. Requirement: "Warn us of breaking changes." Subject: which readers a change breaks,
  for three kinds of reader. Other headings: The supplier's three changes; The schema over time; What
  each reader gets; Who reads the column; Before Chapter 12.
- H12, Chapter 12. Requirement: "The same table must have one identity." Subject: when two names are
  the same table, four meanings of "the same". Other headings: A run in development; The same asset?;
  A database for each producer; Before Chapter 13.
- H14, Chapter 14. Requirement: "No order without a customer." Subject: orders with no customer id,
  and where the rule applies. Other headings: What each run counted; A test on every run; Rows read
  and rows written; Three readings; The counts as OpenLineage facets; Before Chapter 15.
- H15, Chapter 15. Requirement: "Show where Thursday's total came from." Subject: four meanings of
  where a total came from. Other headings: Thursday's £51.50; What the record leaves out; Sunday's
  total; Before Chapter 16.
- H17, Chapter 17. Requirement: "Find the cause of the wrong total." Subject: three meanings of "the
  cause". Other headings: "Thursday's revenue looks wrong."; Back from Thursday's total; Two causes;
  Saturday with the `refunds` change; Before Chapter 18.

## Slot C8: Chapter 8, one short paragraph after the requirement's readings

It follows the paragraph that ends: the shop does not meet the requirement until the export and the
analyst's copy send events too. The learner met "owner" in Chapter 2, where the warehouse's owner of
every table is an account, and the readings of "Every table must have an owner" were: a person
responsible, a team responsible, the job that writes it, the account that controls it.

- One of the standard facets, `ownership`, holds a dataset's owners.
- Each owner is an identifier, which can name a user, a team or an application.
- So the facet records an owner without saying which of Chapter 2's readings of "owner" it answers.
- The shop does not send it.

## Output

Write the file `docs/notes/requirement-boxes/drafts/boxes.md` with one section per slot, headed
`## C2a`, `## C2b`, `## C2c`, `## H3`, `## H6`, `## H7`, `## H9`, `## H11`, `## H12`, `## H14`,
`## H15`, `## H17` and `## C8`, each holding only the exact text to place (a heading's text without
the `##`), and nothing else in the file.
