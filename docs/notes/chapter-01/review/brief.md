# Reviewer's brief: Chapter 1, the reading half

You review one chapter of an interactive course, *Metadata Systems*, as its learner meets it. The
learner is a competent software or data engineer who has done no earlier chapter (this is the
first) and has read none of the course's documents.

## What to read

1. `docs/notes/chapter-01/review/page.md`: the built chapter's text in page order, as it loads and
   after each figure is used. This is the page; review it.
2. The screenshots in the directory named in your instructions, to see the figures as drawn (phone
   width, dark theme, and the whole page on a desktop in the light theme).
3. To check a number or a claim, and only for that: `docs/notes/chapter-01/facts.md`, and the lab
   that computes everything, `packages/lab/src` (the shop's data is in `shop/data.ts`, its
   programs in `shop/programs.ts`).

## What to look for

- **Does the chapter work for its learner?** Can they do what its objectives say by the end?
  Where do they get stuck, misled or bored?
- **Is every claim true?** A number, a time, a count or a statement about what the figure shows
  that the lab does not support. Check before you assert.
- **Does each figure show what the words around it say it shows?** A figure whose state
  contradicts its text is the most serious finding.
- **Words.** A word used in two senses on the page; a term used before it is explained; a
  sentence a competent engineer must read twice; repetition of the same point far apart;
  anything `docs/style.md` forbids (em dashes, marketing tone, filler, labels instead of
  statements).
- **Interaction.** A prediction answered before the learner commits; a control whose effect is
  unclear; a result that appears before the action that produces it; a figure that teaches
  nothing.
- **First principles.** The chapter should make the learner discover what cannot be known from
  data alone, not tell them. Say where it tells instead of shows.

## How to write findings

Write `docs/notes/chapter-01/review/findings.md`. Number each finding (R1, R2, ...). For each:

- **Where**: the section and figure.
- **Quote**: the exact words from the page (or describe the figure's state precisely).
- **Problem**: what is wrong, for this learner, and why it matters.
- **Severity**: high (wrong, misleading, or blocks learning), medium (confusing or weak), low
  (polish).
- **Direction**: what kind of change would fix it. Do not rewrite the text yourself.

A review never contains a challenge's answer. Check every number you mention against the lab or
the fact sheet before you assert it. Be specific; a finding nobody can act on is noise.
