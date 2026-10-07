# Brief AE: the opening in short steps, around two figures

Read `docs/notes/chapter-01/briefs/round-4/common.md` first, and the files it names: every rule
there holds for this brief, and `docs/style.md`'s rule "silence is preferable to filler" above all.
Write your draft to `docs/notes/chapter-01/drafts/round-9/AE.md`.

The opening section carried too much continuous prose before the learner did anything: the date,
the shop, three systems, what an asset is, seven assets, the nights, the programs, the lab, how
the lab runs and what the browser keeps. It now reaches the first question in short steps, with
two figures carrying what prose carried:

1. the situation and the lab, in the section's own prose;
2. a control the reader may open, with how the lab runs;
3. the map: the shop's systems and what each holds, and under them a count the lab computes,
   "3 files + 3 tables + 1 dashboard = 7 assets";
4. a figure of the shop's first week: the days, a night's work after each, and the morning you
   start;
5. then the dashboard and its question (already written; not yours).

The facts are in `docs/notes/chapter-01/facts.md`, under "The opening, in the order the page gives
it", numbered 1 to 6, and under "The map of the platform" and "The week, as the lab ran it". Use
only those facts. Each key below says which facts it carries. A figure shows what it shows: the
text around it says what the reader needs and does not describe the figure again.

## question

The section's own prose, in Markdown. Two short paragraphs, no list, no heading, no more than 100
words. First paragraph: fact 1, the situation. Second paragraph: fact 2, the lab.

- Keep these sentences exactly as they are, word for word: "You start work on Monday 14 September
  2026 at 09:00." and "It runs in your browser: there is nothing to install, open or sign in to."
- Keep the words "Monday 7 September" for the day the shop opened its online store.

## labDetails

The Markdown the reader sees on opening the control. One paragraph, no list, no more than 90
words. Fact 3, all of it, in its order. It follows the paragraph above directly, so it starts
with the lab's engine, not with what the lab is.

- Do not say "the week" here: the page gives the week's dates only further down. Say "the shop's
  first week" or "its first week".

## labDetailsSummary

Plain text: the words on the control that opens labDetails. No more than six words. Say what
opening it shows: how the lab runs and what your browser keeps. Not a question.

## platformLead

Markdown, shown directly above the map. No more than 45 words. Fact 4, except the count, which
the figure shows. Keep the words "has three systems" and "in the order data moves through them
each night". Say that you cannot see the programs. Say that a button at the foot of the window
opens the map again once you scroll past it.

- Do not use the word "asset" or "assets": the count under the map gives the word, and the text
  under the map says what it means.

## platformAfter

Markdown, shown directly under the map. No more than 45 words. Fact 5. Keep this sentence exactly
as it is, word for word: "An asset is something in the platform that can be stored, described,
changed, related to other assets, or depended on." Keep the words "seven assets".

## captions.platform

Plain text: the map's caption, in the figure's head. No more than 12 words. It starts "The map: "
and says what the map shows: the shop's three systems and what each holds. Do not use "asset".

## weekLead

Markdown, shown directly above the week's figure. No more than 45 words. Fact 6, its first two
sentences: the dates and what each night does. Keep the words "Monday 7 to Sunday 13 September
2026".

## weekAfter

Markdown, shown directly under the week's figure. One sentence. Fact 6, its last sentence. Keep
the words "The last night ends early on Monday 14 September".

## captions.week

Plain text: the week figure's caption. No more than 16 words. What the figure shows: the shop's
first week, the days it took orders, a night's work after each, and the morning you start.

## weekLabels

Plain text labels inside the week's figure, as a Markdown list, each with its key before a colon,
in this order:

- weekOrders: the key to the band across the seven days: the days the shop took orders. No more
  than 8 words, lower case first letter.
- weekNight: the key to the narrow bar after each day: a night's work, the three files written
  again and then the programs. No more than 12 words, lower case first letter.
- weekStart: the words at the line on Monday 14 September: that you start work then. Keep the
  slot `{time}`. No more than 5 words.
- weekSummary: one sentence a screen reader hears instead of the drawing. It says what the drawing
  shows: the days from `{first}` to `{last}`, a night's work after each day, the last ending early
  on `{night}`, before you start work on `{start}` at `{time}`. Keep those five slots. No more than
  35 words.

## tallyLabels

Plain text: the words of the count under the map, as a Markdown list, each with its key before a
colon. Each says a number of one kind of thing, with the slot `{count}`, once for one ("one") and
once for any other number ("other"):

- file.one, file.other
- table.one, table.other
- dashboard.one, dashboard.other
- asset.one, asset.other

Rules for every key:

- Put the subject first in every sentence. Name each thing before a sentence uses it with "the".
- Do not say how many programs there are, which asset a program reads or writes, or what any
  program does.
- Do not use these words: metadata (except in the name "the Metadata Lab"), simulate or
  simulation, schema, dataset, job, event, lineage, environment, timeline; or "run" as a noun (as
  a verb it is fine). Do not call the week's figure a map: only the map is a map.
- No reassurance, no motivation, no sentence about what the reader has been told or already
  knows, and nothing that describes the platform as a person.
