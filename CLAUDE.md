# CLAUDE.md

Project instructions for anyone, human or AI, working on this course. They are binding.

## What this is

*Metadata Systems: From Raw Files to a Working Metadata Platform*: an interactive, browser-based
course on metadata and data lineage, built on the author's shared learning platform
(`snowch/learning-platform`). The learner does not read about metadata systems; they build a
small one inside a small data platform, break it, and repair it.

Every chapter follows one loop: **predict, build, run, inspect, explain, change, run again.**
Read as the learner meets it, the loop is a sequence of questions: here is a real question; what
can I believe about it now; predict; act on the lab; what did I see; what did that prove; what can
the data not tell me; what would a system have to record? Every chapter protects one principle
above the rest: do not teach the learner what metadata systems contain; make them experience the
information gap that makes such a system necessary.

Every figure uses one vocabulary, shared with the author's other courses: inspect, predict, step,
experiment, break, explain, drill down, replay.

Read `docs/plan.md` for the parts and chapters, what each builds and in what order, and the
decisions taken since the brief; `docs/lab.md` for the Metadata Lab, the data platform every
figure runs; `docs/platform.md` for what this course takes from the learning platform and what is
its own; `docs/sources.md` for the specifications every technical claim is checked against; and
`docs/authoring.md` for how a chapter is made. Edit every learner-facing string against
`docs/style.md`.

## The thesis every chapter serves

> Metadata describes what exists. Lineage describes how things become related through
> computation and change.

Lineage is the time-and-process dimension of metadata, not a separate subject. The course keeps
three kinds of record apart and shows, chapter by chapter, that they are one model:

- **Descriptive**: name, type, schema, owner, location, tags, meaning, classification.
- **Operational**: jobs, runs, times, status, inputs and outputs, row counts, freshness, quality
  observations.
- **Lineage**: asset to asset, job to asset, run to asset, column to column, model to training
  data, dashboard to the data it shows.

## First principles, every time

Before a technology or a standard appears, the chapter answers, in this order:

1. What problem exists?
2. Why is the naive solution not enough?
3. What abstraction solves it?
4. What information does the abstraction need?
5. How is that information represented?
6. What happens when the abstraction is wrong or incomplete?
7. How does a real system implement it?

No chapter starts with a product's terminology. OpenLineage is the course's main case study and
an open standard, not the definition of metadata: the learner designs an event for a run in
Chapter 6, from the problem, and meets OpenLineage in Chapter 7 as one answer to a problem they
already understand. The course is not an OpenLineage tutorial and not a catalogue of metadata
products; a product appears where it illuminates an idea, and its architecture is compared, never
its marketing.

## Every figure is a view of the lab

`packages/lab` is a small data platform that really runs: files and tables with real rows,
programs that really transform them, a clock, a scheduler, and the learner's own metadata system
on top. A figure shows what the lab computes. It is never a scripted animation and never a
hand-drawn diagram of something the lab could compute. If a chapter needs a figure that shows
something the lab does not compute, the lab is where the work goes first.

A number in a learner-facing string is a number the lab produced, and a facts test pins it. A
prediction's answer comes from running the lab, never from the lesson's data.

**A figure shows only what the learner has been told or has built.** It never draws a relation the
chapter asks the learner to find, and no caption, label or text gives away a challenge's or a
prediction's answer before the learner has worked for it. The platform map is the standing
example. It stays to hand through every chapter, and in Chapter 1 it has no arrow from one asset to
another, because which asset is made from which is what that chapter shows storage cannot tell.
The map gains a relation only once something the learner built records it.

## Accuracy

- **Check every technical claim** about a standard or a system against its authoritative source,
  and record the source in `docs/sources.md`: the specification, the project's own
  documentation, or its source code. Memory is not a source.
- **Distinguish a specification from an implementation.** "The OpenLineage specification
  requires" and "Marquez does" are different claims, checked against different sources.
- **Distinguish facts, design choices and hypotheses**, on the page and in the documents. The
  lab's own choices are labelled as the lab's; the model-versus-reality note of every chapter says
  where the lab differs from a real platform.
- **A definition is a technical claim**, and must hold for every case the course will meet, not
  only for the chapter's example. "Metadata is information kept apart from the data" failed this:
  a Parquet file carries its own column names and types, and a warehouse keeps its tables' types
  inside itself. Check a definition against the sources as you would any other claim.
- **Never invent behaviour for an open standard.** Where a specification is silent (OpenLineage
  says nothing on what a consumer does with a duplicate event), say that it is silent and show
  what the lab does and why.

## Originality and copyright

The course covers ground that documentation, vendor tutorials and papers cover, and it must be
original work.

- Do not reproduce, closely paraphrase or structurally mirror any existing text, diagram or
  worked example. In particular: not dbt's jaffle shop or its staging-and-marts layout, not the
  OpenLineage or Marquez documentation's examples, not the DataHub, OpenMetadata or Atlas
  documentation's examples or diagrams, and not the textbook provenance examples. If you notice
  you are reconstructing a known example, stop and design a different one. The feeling of "this
  is the standard way to present this" is the signal, not the permission.
- Describe a specification in your own words. A quotation is short, marked as a quotation, and
  attributed to its source in the text and in `docs/sources.md`. Field names, event type names
  and other interface names are used as names; their documentation's prose is not copied.
- Do not copy a schema, a code sample or a figure from any project into this repository. Where
  the course must show a standard's real format, the lab produces it, and a test checks it against
  the standard's published rules.
- The shop, its people, its data and every scenario are invented for the course. Names of real
  companies, people or products do not appear as part of the scenario.
- Every lesson carries an `originalityNote` in its data: the obvious textbook or vendor example
  for its topic and how this chapter's example differs. It is written in the same commit as the
  lesson, and a test fails a lesson without one.
- Every dependency and every typeface carries an open licence, recorded in `docs/sources.md`.

## Haiku drafts the prose; you check it

Every string a learner reads goes to a Haiku subagent to draft before it lands: chapter prose,
hints, the feedback after a failed test, model-versus-reality notes, labels inside the figures.
Haiku writes shorter, plainer sentences than a model with the whole repository in its head. It
also drops facts and gets them wrong. So the work splits four ways:

1. **You write the brief as a list of facts**, not as prose: what the text must say, each point
   checked against the lab, the lesson data or the code *before* the brief goes out. Haiku copies
   a wrong fact faithfully. Attach `docs/style.md`. A prose brief gets its wording copied.
2. **Haiku writes the sentences, a section at a time.**
3. **You check the facts, and nothing else.** Where a fact is missing, add the fewest words that
   carry it. Do not rewrite Haiku's sentences. If a draft is wrong, send it back with a note.
4. **Then read the whole chapter, start to finish.** This is `docs/style.md`'s second pass, where
   repeats and broken joins show. It also asks whether each figure showed the mechanism the prose
   claims it shows. Read it from the built page in every state its figures reach, before and after
   each commitment and after each change: some faults show only there, such as a correct
   prediction printing its long option twice.

The mechanism is the Agent tool with `model: "haiku"`. Engineering documents (this file, the plan,
`docs/lab.md`, `docs/platform.md`) are written directly. They still pass the checklist.

## Voice

Direct, precise, British English, active voice, short sentences. The learner is *you*, a
competent software or data engineer. No marketing tone, no filler, no "in this chapter we will",
no technology worship. No em dashes.

**Say the thing. Do not perform it.** No label where a statement belongs, no withholding then
revealing, no roundabout purpose. Prefer: here is the problem; here is the smallest model that
solves it; here is where that model fails; here is what we must add; now the model explains this
real behaviour.

That is a rule for sentences, not for experiments. A chapter may ask a question and let the lab
answer it: whether a query that rebuilds an asset shows how the asset was made is asked in Chapter
1's construction and answered by its failure experiment. What a chapter must not do is answer its
own question in prose before the learner has run the experiment that answers it.

**Terms are rationed per chapter.** A term arrives because the lab in front of the learner has
just raised the question that needs it, never as a definition up front: plain English first, the
term second. `docs/plan.md` lists the terms each chapter introduces; the term gate
(`termProblems`) fails a chapter that uses a term before the chapter that introduces it, unless
the chapter lists the word under `termExemptions` with a reason. *Metadata* itself is introduced
at the end of Chapter 1, by the questions the learner could not answer.

**Length follows the material.** The ten sections of the lesson format (question, motivation,
prediction, investigation, construction, failure experiment, explanation, generalisation,
challenge, reflection) stay whatever the length. A chapter closes with a short summary of what its
experiments showed and could not show, said once and not explained again, then reflective
questions that carry it to new situations and lead into the next chapter. To improve a chapter,
sharpen what its interactions ask before adding material.

## Interaction is the explanation

Every interactive has a reason to exist. Not "click here to see a graph": "predict which assets
this change affects", then let the learner act. No chapter is a sequence of quizzes; a prediction
commits the learner to an expectation about the lab that the lab then answers. Every chapter
deliberately produces at least one surprising result: a dependency the lab cannot prove, a graph
that did not join, an event that changed nothing, a duplicate that was or was not harmless. The
learner learns what metadata systems cannot do, not only what they can.

**A prediction asks for a belief the learner can already hold.** Before a prediction goes in, ask:
what has the learner seen by this point; what explanations could they reasonably hold; could they
say why they chose one; and does the lab's answer tell those explanations apart? Each option is
one such explanation of how the platform works. None is a hidden fact about the shop, a number
nobody could reason to, an answer that is plainly right, or a guess at what the author decided. A
count is offered as the explanations it stands for (none, one, more than one), never as an exact
figure to hit. Where nothing the learner has seen can tell the options apart, as with how this shop
happened to set up its warehouse, do not ask them to guess: ask what they would do in the shop's
place, and let the lab show what the shop does beside their choice, called neither right nor
wrong (the prediction figure's `choose` mode). The chapter's notes answer the four questions for
every prediction, in a table the content tests check.

**After a result, ask what it proved.** A query that rebuilds an asset suggests how the asset was
made; it does not show it. A chapter asks what its experiment proved and what the data could not
tell before it names what a metadata system would record, and it does not tell the learner what
metadata is for before they have needed it.

## Reviewing a chapter

A review has two halves, and the test suite does neither on its own.

- **The mechanical half** drives the built page at phone and desktop widths and in the dark
  theme, presses every control, moves every input to both ends, reaches each part of the page by a
  jump as well as by scrolling, runs every challenge with the reference and with plausible wrong
  attempts, and writes down what broke.
- **The reading half** gives each chapter to its own reviewer with a written brief, reading as a
  learner who has done every earlier chapter and none after. Every finding quotes the page;
  a finding suggests a direction and never rewrites; a number or a cross-reference is checked
  before it is asserted; a review never contains a challenge's answer. Reviewers over-call, so
  each finding is attacked by an independent sceptic before it is acted on.

Reviewers and sceptics run on a model other than the one that built the chapter. After a review,
fixes to code come first, then fact briefs per finding go to Haiku, then the whole chapter is
read once more.

## What no check can catch

Read for these before calling a chapter finished:

- a claim about the repository's own state, which rots silently; if the repository can compute
  it, generate it;
- a word that means two things on one page: *table* (the warehouse's and the page's), *record*,
  *event*, *run* (the noun and the verb), *version*, *source*, *owner*, *schema* (a structure and
  a database's namespace), *model* (the lab, a data model, an ML model), *map* (the platform map;
  no other figure is called one);
- a definite article in front of a noun the chapter has not introduced;
- a term doing work before it is defined;
- a table nobody chose for this chapter, rendered because the component had it;
- a prediction its notes justify but its page does not: read the page above it as the learner, and
  ask whether they could say why they chose their option;
- a figure, caption or label that shows what the chapter asks the learner to find;
- the same argument made twice, far apart;
- a number spelled as a word that the lab did not produce;
- a claim about a standard or a product that `docs/sources.md` does not support.

## Things that will break the build

`npm run check` is exactly what CI runs (`scripts/check.sh`). Each line below is a check and the
reason it exists.

- **Prettier, with `*.md` ignored.** Prose files keep their own line breaks.
- **The copyright line** ("Copyright © 2026 Christopher Snow") near the top of every source file,
  and on every page's footer. `node scripts/copyright.mjs` adds it.
- **The platform copy is unedited.** `platform/` is a copy of `snowch/learning-platform`'s
  packages at the commit `platform/SOURCE.json` records; `node scripts/sync-platform.mjs --check`
  fails if a file there differs. Change the platform in its own repository, then sync.
- **`tsc` strict**, with `noUncheckedIndexedAccess` and `verbatimModuleSyntax`.
- **A lesson without an `originalityNote`, with its sections out of order, or with a challenge
  nobody mounts, fails to parse.** The content tests parse every lesson.
- **The term gate** across chapters, and **the model gate**: a figure may name only a model the
  book has a note for (`modelProblems`).
- **Every challenge's reference passes its own tests, and its starting point does not.**
- **The whole chapter renders in jsdom with no figure problem.**
- **The chapter's stated numbers are pinned** by its facts test against the lab.
- **The lab is deterministic.** The same code gives the same rows, times and identifiers on every
  machine: no clock, no `Math.random`, no locale-dependent formatting.
- **The Playwright suite drives the built site at desktop and phone widths**: every challenge
  completable with its reference and refusing a wrong attempt, saved work graded again on load
  and not bypassable through storage, resettable, a prediction committed before it is answered,
  no console error, no horizontal scroll even after every figure is used, no visible text under
  11 pixels, every phone control at least 40 pixels tall, no line of prose over about 85
  characters.
