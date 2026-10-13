# Brief BK: Chapter 2 as an investigation in three stages (common part)

The author asked for Chapter 2 to read as a focused technical investigation for practising data
engineers: less instructional scaffolding, the important evidence and conclusions easy to find,
and no explanation of familiar SQL or table operations. The chapter is reorganised round three
stages: find the discrepancy; inspect what the platform records; test an explanation. After each
substantial investigation a box states what the evidence established and what it did not. The
free-text handover note and the reflective questions at the end are replaced by a short
multiple-choice check.

Rules for every slot:

- Follow `docs/style.md` and `AGENTS.md`. British English. No em dashes. Short sentences.
- The reader is "you", a competent data engineer who has done Chapter 1. Assume they know SQL,
  `information_schema`, object storage, buckets and keys, JSON Lines and dashboards. Do not
  explain any of those.
- Say each thing once. Do not announce what a cell will do and then repeat what it showed. Where a
  cell's code is clear, the lead before it is one short line or nothing.
- No filler, no reassurance, no motivation, no "in this chapter", no rhetorical questions, no
  slogans, no personification of systems ("the platform remembers", "the data says").
- A block of code is a "cell". Never use "run" as a noun, except in slot BK9, where the brief says
  so. Do not use the words "lineage", "event" or "metadata" except where a slot's facts use them.
- Keep names in backticks exactly as written in the facts. Keep every phrase the facts mark
  "word for word" exactly.
- Numbers: write them exactly as the facts give them. Do not compute new ones.
- Each slot goes under its own heading `## BKn` (or `## BKn.m`) in your draft file, with the text
  exactly as it should appear on the page, Markdown included.
