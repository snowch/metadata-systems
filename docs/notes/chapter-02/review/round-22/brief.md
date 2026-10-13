# Review brief: Chapter 2 after its redesign (round 22)

You review one chapter of an interactive course on metadata and data lineage, written as a
marimo-format Python file that a build turns into a JupyterLite notebook:
`/home/user/metadata-systems/notebook/chapter_02.py`. Each `mo.md(...)` is a Markdown cell; each
`mo.callout(..., kind="success")` is a box of findings ("Established" / "Not established");
`kind="neutral"` is a requirement box; `mo.Html(figures....)` is a figure the build draws from the
shop's engine (`/home/user/metadata-systems/notebook/shop/figures.py`, functions `totals`,
`inferred`, `three_records`, `pipeline`, `dashboard_chart`); plain `@app.cell` functions are code
cells the reader runs. The figures' and cells' outputs come from the engine in
`/home/user/metadata-systems/notebook/shop/`; you may run Python there
(`cd /home/user/metadata-systems/notebook && python3 -c "import shop; w = shop.run_week(); ..."`)
to check any number.

Read as the intended reader: a practising data engineer who knows files, tables, SQL, pipelines and
dashboards, has done Chapter 1 (a tour of the shop's platform, ending with a written guess at what
each table is made from) and no later chapter. Read the whole file in order.

The author's goals for the chapter:

1. The reader discovers that current metadata describes what an asset is and its state; that
   lineage connects assets and transformations; that recorded execution history is evidence of
   what a particular run did; and that the current state, or a query that reproduces an output,
   cannot by itself establish the history of a past execution.
2. The chapter is a focused technical investigation in three stages: find the discrepancy; inspect
   what the platform records; test an explanation. No teaching of familiar basics. No query
   explained in advance, paraphrased after, then restated a third time. No filler or AI-sounding
   prose. Technical depth kept, optional depth folded away.
3. After each substantial investigation, a box states what was established and what was not, only
   where that adds value.
4. A short multiple-choice check (three answers, A, B, C) with specific feedback and retries, then
   the takeaway.
5. No invented fields, records, outputs or capabilities. Precise about the difference between a
   run record's evidence and proof that its instrumentation was complete.

Write your findings to
`/home/user/metadata-systems/docs/notes/chapter-02/review/round-22/findings.md`, numbered. For
each: quote the page exactly; say what is wrong and why it matters to this reader; suggest a
direction, never rewritten text. Check any number or cross-reference before you assert it. Look in
particular for: a sentence the reader would not miss; repetition across sections; a claim the
evidence shown does not support; a number that disagrees with the engine; a term used before it is
explained; an instruction or label that does not match what the reader sees; a figure that gives
away an answer before the reader has worked for it; anything in the check that is ambiguous or
gives the answer away in its wording. Rank findings by how much they would cost the reader. Do not
pad: if a section is sound, say nothing about it. Reply with only the number of findings.
