# Instructions for every Chapter 1 brief

You are drafting learner-facing text for an interactive course, *Metadata Systems*. Read these
first, in full:

- `docs/notes/chapter-01/facts.md`: the only facts you may use. Every number you write must be in
  it. Do not invent a number, a name, a time or a behaviour.
- `docs/style.md`: the style checklist. Apply both passes.

Rules that matter most here:

- British English. Address the learner as "you". Active voice. One idea per sentence, about
  twenty words at most. No em dashes (the long dash). No marketing tone, no filler, no "in this
  chapter we will", no "let's".
- State the point. Do not withhold it, label it or build up to it.
- Use the words in the fact sheet's "Words on this page" with exactly those meanings. Never use a
  word from "Words this chapter must not use". In particular: no "run" as a noun, no "job", no
  "lineage", no "dataset", no "schema", no "graph", no "event", and no "metadata" except where a
  brief says this is the place it is introduced.
- Write names of files, tables, columns and accounts in backticks, exactly as the fact sheet spells
  them: `orders.parquet`, `clean_orders`, `daily_sales`, `customer_id`, `etl_service`.
- Markdown is allowed: paragraphs, short lists, backticks, bold for at most a few words.
- Where a brief says a text is shown before the learner commits to a prediction or runs a
  figure, that text must not give away what the figure will show.

Write your draft to the file the brief names, as Markdown with one `## key` heading per item, in
the brief's order, and nothing else under each heading but the text itself.
