# AGENTS.md

Instructions for AI coding agents working in this repository. `CLAUDE.md` is binding for anyone,
human or AI; this file adds the parts an agent most often gets wrong. Read both before editing.

## Where the rules live

- `CLAUDE.md` — the course's binding instructions: what this is, the voice, the term ration,
  accuracy, originality, and the Haiku prose process.
- `docs/style.md` — the style checklist every learner-facing string is edited against.
- `docs/authoring.md` — how a chapter is made.
- `scripts/check.sh` — exactly what CI runs; run it before pushing.
- `notebook/tests/test_words.py` — the notebooks' words: every number pinned against the engine,
  the filler backstop, the prohibited phrases, the term gate; `notebook/tests/test_notes.py` holds
  each written chapter's notes to their "Requirements" and "Originality" sections.

## What counts as learner-facing text

Every string a learner reads: a notebook's markdown cells and section titles, the labels,
options, placeholders and messages its code cells print, the figures' captions, and the front
page's words. The chapters' words live in `notebook/chapter_NN.py` (the source each notebook is
built from) and in the helpers under `notebook/shop` that print to the reader; the front page's
live in `apps/course/src/strings.ts`.

## The writing standard (added to the Voice rules in CLAUDE.md and docs/style.md)

Write clear, natural technical English: a knowledgeable engineer explaining something
accurately to another person. Prefer concrete meaning over rhetorical effect. Explain what
happened, what the evidence shows, what can be inferred, and what remains unknown. Prefer
specific nouns and verbs over vague abstractions, and ordinary English over manufactured
slogans, dramatic phrasing, or literary flourishes. Make every sentence earn its place. Short
sentences where they improve clarity, but not every sentence artificially short. Explain
technical terms when learners need them. Preserve technical precision: never simplify a
statement so far that it misleads.

Reject these failure modes:

1. **Pseudo-profound aphorisms.** "A wrong belief, once tested, tells you something; an untested
   one tells you nothing." Explain the activity instead: "Make a prediction before checking the
   evidence, then compare your prediction with the result."
2. **Artificially dramatic fragments.** "One thing to take away." "Three words to keep apart."
   "The data might." Use a complete, direct sentence unless a fragment is genuinely natural.
3. **Forced contrasts, symmetry and wordplay.** If a distinction matters, explain it explicitly
   and accurately; do not make it sound memorable instead of clear.
4. **Unnecessary personification.** Do not make systems, data, rows, records or questions speak,
   decide, remember or act like people. "Nothing says who made it" becomes "The available
   metadata does not identify who created it."
5. **Vague references.** Scrutinise "the rest", "these things", "what survives", "nothing
   else", "the groups", "the data might". Name the specific object, observation or relationship.
6. **Unnecessary meta-commentary.** Do not narrate what an exercise or section is doing
   ("this exercise makes the sorting explicit") when you can simply explain the thing.
7. **Making learners do the author's explanatory work.** Wrong-answer feedback must state the
   correct conclusion and why the evidence supports it, not leave a cryptic clue.
8. **Unsupported claims and overstatement.** Distinguish observed facts from inferences and
   hypotheses. Evidence that supports an explanation does not prove a cause. State what is
   unknown and why, when the uncertainty matters.
9. **Repetition and filler.** Do not restate a conclusion in several slightly different ways.
   No atmospheric emphasis, formulaic closing slogans, or generic "takeaway" paragraphs.
10. **Awkward or unnatural English.** A grammatically valid sentence is not necessarily good
    prose. Check idiom, referents, and whether a competent technical educator would say it.
11. **Instructional scaffolding in the prose.** Headings and sentences that name the reader's
    cognitive activity ("A number on your own model", "Reflection", "What you would write down")
    instead of the technical subject. Name the subject ("State and history", "Why
    reconstruction is unreliable"); an experienced engineer navigates by content, not by
    pedagogy.
12. **Curriculum narration and over-signposting.** Telling the reader how the chapter is
    organised ("This chapter works through five ideas"), announcing an argument before making it
    ("What follows is..."), narrating structure ("The fourth idea deserves its own moment"), or
    directing the reader's attention ("Notice what this table claims"). Make the point instead.
13. **Redundant summary layers.** "What this chapter established", "The one-sentence version",
    "The key takeaway", "The general principle:", "The conclusion is structural, not
    incidental". These restate a conclusion the reader has just met or frame it rhetorically.
    One statement, in place, does the work. Also challenge absolutes that sound profound but
    are imprecise: say exactly what is and is not established.

When you change learner-facing text, read the complete changed passage in context, not just the
changed line, and ask: is the meaning immediately clear; does every sentence carry a concrete,
useful idea; is it natural read aloud; are facts, evidence, inferences and unknowns
distinguished correctly; does the learner receive enough explanation to understand the result?
Fix genuine problems. Do not rewrite good prose to demonstrate activity, change technical
meaning, invent evidence, or cut useful teaching content for brevity.

## The automated prose check

`node scripts/prose.mjs` (also `npm run check:prose`) fails the front page's words on known-bad
phrases — confirmed regressions, each added when found — and on "the lab" and "Metadata Lab": the
page names no lab, and never says what computes a figure (`CLAUDE.md`, "No lab on the page").
`notebook/tests/test_words.py` reads the same list and holds the notebooks to it. It is a narrow
backstop for wording the standard rejects, not
a general style judge: short sentences, passive constructions, "nothing" and metaphor are fine in
themselves. When a review finds a new failure mode, add its phrase to the list in
`scripts/prose.mjs` with a comment naming the rule; both checks pick it up.

`docs/prompts/review-learner-facing-prose.md` is the editorial review pass for a human or an
agent to run after any change to learner-facing text. The automated check and the editorial
review are different jobs: the first catches known regressions, the second catches everything
else.
