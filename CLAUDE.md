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
information gap that makes such a system necessary. The experience is a means, not the law:
where prose names a mechanism more exactly than an interaction can, write the prose, and keep
the interaction for what doing teaches better than reading (a failure seen, a limit felt). A
chapter may state its conclusion and still offer the experiment that shows it.

Beside metadata itself, the course teaches one habit the learner can take anywhere: when a
requirement sounds obvious, ask what it actually means ("Question the requirement", below).

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

**A diagram carries what prose would make the learner hold in mind.** Where a passage asks the
learner to keep a date, a set of systems, a count, a sequence of nights or their own place in an
investigation in working memory, a figure carries it, and the prose says only what the next
question needs. Each such figure has one job, named in its notes: the platform's architecture,
its assets, time, a flow, or where the learner stands. It is a reference, still a view of the lab,
and still shows only what the learner has been told or has built; it is never decoration. Detail
the learner's next step does not need, such as how the lab itself runs, goes in a section's
`details`, a control the reader opens, where it first matters, and nowhere else. A chapter's
opening sets up the smallest model its first question needs, and adds structure when the
investigation makes it relevant. Chapter 1's opening is the standing example: a short situation,
the lab, the map with its count, the shop's week, then the question.

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
own question in prose before the learner has run the experiment that answers it, unless the
prose is the better teacher: then say the thing, and let the experiment show it to those who
run it.

**Clear, natural technical English.** The prose sounds like a knowledgeable engineer
explaining something accurately to another person, never like writing trying to sound insightful.
Prefer concrete meaning over rhetorical effect: specific nouns and verbs over vague abstractions,
ordinary English over manufactured slogans, dramatic phrasing or literary flourishes. Reject
pseudo-profound aphorisms ("a wrong belief, once tested, tells you something" - explain the
activity instead), artificially dramatic fragments ("one thing to take away"), forced contrasts
and wordplay, personification of systems or data ("nothing says who made it" - say what the
metadata does not hold), vague references ("the rest", "what survives"), meta-commentary about
what an exercise is doing, feedback that marks an answer wrong without explaining the correct
conclusion, overstatement of what evidence shows, and closing slogans. `scripts/prose.mjs`
(`npm run check:prose`, run by `npm run check`) fails on confirmed regressions of these; the
editorial review pass in `docs/prompts/review-learner-facing-prose.md` catches the rest.
`AGENTS.md` states the same rules for agents and where the checks live.

**Silence is preferable to filler.** Write for the learner's next action, not for narrative flow,
and do not imitate a textbook's teacherly tone. Every sentence tells the learner something
concrete, changes what they should do, explains why something matters, or sets up a prediction or
a decision. Test each one: if it were removed, would the learner lose information, understanding
or a useful instruction? If not, remove it, and put nothing in its place unless the learner needs
an action there: what to inspect, predict or find out, and why. No reassurance ("you have what you
need"), no motivation ("this is where things get interesting"), no platform described as a person
("the system is waiting", a figure that "asks nothing of you"), and nothing about what the learner
"has been told" or "already knows" unless that fact is the point. `docs/style.md` has the rule
and its standing example.

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

**Explain a mechanism from the learner's side first.** Before the page says how anything
interactive is built, it says what the learner does with it and what happens when they do: first
"What do I do, and what happens when I do it?", only then "How does the technology behind it
work?". The plain model, in the words every chapter uses: in a figure the learner uses, you ask,
the lab checks, it shows you, you work out what it means; a figure they only read shows what the
lab works out. The page says which figures are which, and says how the learner asks in the actions
on the page (choose an answer, an asset or the parts of a query, and press a button), never only
that they ask: "You ask the lab a question by using a figure" was false of Chapter 1's first
figure, which asks nothing, and silent on how. Where the learner needs "you ask it something and
it shows you what it finds", a sentence such as "the lab queries the underlying data model" does
not belong. How a mechanism is built comes after, and where the learner's next step does not need
it, in a section's `details`.

**A prediction is built around what the learner should learn.** Before one is written, its author
says what the learner should understand, or be able to do differently, afterwards; if that cannot
be said clearly, the exercise is redesigned. A prediction then asks for a belief the learner can
already hold, about a result they can observe, and keeps the stages of an investigation apart:
the question; the plausible hypotheses; the observable result that would tell them apart; the
evidence, from an independent source wherever there is one; what the result means; and, if it
shows a discrepancy, the investigation of why. The learner predicts, observes, compares and
explains; they never guess an explanation the page then reveals.

- **Each option is a result the learner could expect, and the belief it reflects**: "51.50:
  `daily_sales` holds the total of Thursday's orders". No option contains the explanation the
  chapter is heading for ("more, because something on the way left some out"), and none is a
  hidden fact about the shop, a number nobody could reason to, an answer that is plainly right, or
  a guess at what the author decided.
- **The effect before its cause.** A chapter never asks for a cause before the learner has
  evidence that the effect exists: first "is there a discrepancy?", then "why?".
- **Independent evidence.** A prediction tests a belief against something the learner could check
  for themselves (what adding up the raw orders gives), not an implementation failure they would
  have to guess (did the program drop some orders?).
- **"I can't tell yet" is an option** where nothing the learner has seen settles the question.
  It is never marked wrong: refusing an unjustified assumption is part of the skill, and its
  result says what evidence settled the question.
- **A count is offered as the explanations it stands for** (none, one, more than one), never as an
  exact figure to hit.
- **Where nothing the learner has seen can tell the options apart**, as with how this shop happened
  to set up its warehouse, do not ask them to guess: ask what they would do in the shop's place,
  and let the lab show what the shop does beside their choice, called neither right nor wrong (the
  prediction figure's `choose` mode); where the question is what a requirement means, question the
  requirement (below).

A prediction is an experiment, and its notes answer the twelve questions every experiment's do
("Experiments, instruments and explanations", below).

**After a result, ask what it proved.** A query that rebuilds an asset suggests how the asset was
made; it does not show it. A chapter asks what its experiment proved and what the data could not
tell before it names what a metadata system would record, and it does not tell the learner what
metadata is for before they have needed it.

## Experiments, instruments and explanations

A figure is one of three things, and its badge says which (its `role`):

- **An explanation** (`reference`): the page telling the learner something, in a figure because a
  figure tells it better. The map is one. It asks nothing.
- **An instrument** (`inspect`): something the learner examines to obtain evidence, such as
  storage through the inspector, or the dashboard. It is never presented as the activity itself:
  the page puts a question in front of it first and says what evidence to look for, so that it is
  the instrument of an investigation, not a browser.
- **An experiment** (`experiment`): the learner has a question, a hypothesis or a decision, and
  uses the system to answer it. Prefer it.

What the author's guide calls a lab, the page calls an experiment: on the page, "the lab" is the
Metadata Lab, which every figure runs, and one word must not mean two things. "Figure" is the
page's word for one interactive box, and nothing else: a number is a total, a value or a count.

The three roles are the only labels the learner sees. When a figure is designed or reviewed, a
finer list of what a figure can do is the lens, and it stays in the notes: show (a system, a
relation, a stretch of time), inspect (examine data or what storage records), predict (commit
before the evidence), test (a hypothesis or an expectation), investigate (evidence that lets the
learner work out what happened), experiment (change something and observe the consequence). A
figure may combine them (show, then predict, then inspect, compare, explain). A figure need not
ask a question or take a prediction: sometimes the right first step is something important to
observe. But it must have a learning purpose and a learner action that serves it, and its notes
say both. A notes block's objective says what the learner should understand or discover, never
what the figure displays. Weak: "the learner sees what storage records about a table". Strong:
"the learner discovers that the warehouse's owner, an account, does not say who is responsible
for the table". The content tests fail an objective written as what the figure shows; only
reading catches the rest.

An experiment has a learning job: what the learner will understand, discover or be able to do
because they did it, and the action that causes that learning. "They can see the metadata" is an
instrument's job, not an experiment's. It runs a reasoning loop (question, prediction, action,
evidence, interpretation; or hypothesis, inspect, compare, discover, revise; or requirement,
ambiguity, investigate, evidence, conclusion), so that the learner does the thinking. Everything it
shows has a purpose: it supports or contradicts a hypothesis, answers a question, allows an
inference, shows what still cannot be concluded, or says what to investigate next; anything else
belongs in the prose. An investigation runs in order: is there a discrepancy; where is it; what
could explain it; which explanation fits the evidence. "I don't know yet" and "the requirement is
underspecified" are outcomes the learner can reach, where the evidence does not tell the
alternatives apart. The system is the learner's instrument, and the habit to build is: I have a
question; what observation would answer it; where can I obtain it? An experiment has a
consequence (what the learner believed before, the evidence, what they can believe after, and the
next question), never a bare "correct". And it teaches a skill that outlives the course:
questioning a requirement, forming competing hypotheses, comparing independent sources, tracing a
transformation, separating observation from inference, deciding what to inspect next. A
platform's field can be an experiment's evidence; it is rarely its objective.

Before an experiment is built, the chapter's notes answer twelve questions about it, in its block
under "Figures": what the learner should learn; what they know before; the question or hypothesis
that drives it; what they do; why that action is necessary; what evidence it produces; how that
evidence changes their understanding, a wrong prediction's included; whether they could have
predicted the outcome; whether any option gives the explanation away; whether "I don't know yet"
could be the right engineering response; the question that follows; and whether it is really an
experiment, or an instrument or a reference. An instrument or a reference answers two: the
question it serves, and why the learner needs it then. A figure that completes another experiment
(a check after the learner's own work) names the experiment it is part of. The content tests fail
a figure without a role, without its block, or with a question unanswered.

## Question the requirement

The learner should leave able to interrogate a requirement, not having memorised what a product's
fields hold. A metadata system is full of names that sound settled (*owner*, *fresh*, *source*,
*complete*, *duplicate*), and each of its fields holds one system's answer to a question its
requirement may never have stated. The habit the course builds is to ask, of a requirement, a
field's name or a definition: what question is this actually asking, and why is that answer
needed?

So some exercises carry a requirement that is deliberately underspecified, and keep five things
apart:

1. what the requirement literally says;
2. what it might mean: the questions it could be asking;
3. what information each of those questions needs;
4. what the platform actually records, and by which meaning;
5. whether that record meets the requirement, as written and as meant.

The learner commits first, as they would at work, where a familiar word invites a quick answer.
The exercise then shows the other reasonable readings, each beside what it needs, before the lab
shows what the platform records; last, it shows which readings that record satisfies. No
reasonable reading is marked wrong because the platform chose another, and "there is not enough
information to choose yet" is an option the learner can take. The lesson is never "this field
means X". It is that the platform has its own meaning, the requirement did not say which meaning
it wanted, and a field's name does not say which question the field answers.

Chapter 1's owner is the standing example. "Every table must have an owner" could ask who is
responsible for a table, which team is, which program writes it, or which account controls it in
the warehouse, and each needs something different stored. The lab's warehouse records an account:
that meets the requirement as written, and answers only the last question, while "Who should I
ask about `daily_sales`?" needed one of the first two. The figure is `requirement`.

Every chapter looks for its own chance to do this, wherever its material raises a requirement that
sounds obvious; `docs/plan.md` lists a candidate for each. A chapter's notes say, under
"Requirements", which requirement the chapter questions and with which figure, or why none fits,
and the content tests fail notes that say neither. A requirement exercise is not a prediction
with a hidden answer: the prediction rule above holds for its choice, and the lab answers only
what the platform does.

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
- a sentence the learner would not miss: reassurance, motivation, the platform described as a
  person, a line about what they were told; silence is preferable to filler;
- a block of description before the learner's first question that a figure could carry, or that
  the question does not need yet;
- a mechanism explained by how it is built before the page says what the learner does with it and
  what happens when they do, or said of every figure when it holds for some;
- a word that means two things on one page: *table* (the warehouse's and the page's), *record*,
  *event*, *run* (the noun and the verb), *version*, *source*, *owner*, *schema* (a structure and
  a database's namespace), *model* (the lab, a data model, an ML model), *map* (the platform map;
  no other figure is called one), *figure* (an interactive box; a number is a total);
- a definite article in front of a noun the chapter has not introduced;
- a thing named before the page explains it, or explained again wherever it appears: explain it
  once, where the reader first meets it (the lab is explained where Chapter 1 first names it, and
  behind no badge);
- a term doing work before it is defined;
- a table nobody chose for this chapter, rendered because the component had it;
- a prediction its notes justify but its page does not: read the page above it as the learner, and
  ask whether they could say why they chose their option;
- an option that carries the explanation its result is about to give, or a cause asked for before
  the learner has seen its effect;
- a figure, caption or label that shows what the chapter asks the learner to find, including one
  just below a prediction, which is in view while the learner is still choosing;
- an instrument with no question in front of it, or a figure showing what no question needs;
- a field's name taken for its meaning: a page that says what a field holds without saying which
  question it answers;
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
- **The filler check** fails learner-facing text that uses the commonest forms of filler
  (`docs/style.md`): a backstop for the rule, which only reading enforces.
- **The term gate** across chapters, and **the model gate**: a figure may name only a model the
  book declares (`modelProblems`).
- **Every figure declares its role** (an experiment, an instrument to inspect with, or a reference),
  which its badge shows, **and has its block in the chapter's notes** under "Figures": twelve
  answers for an experiment, two for an instrument or a reference.
- **A figure below a prediction states what the prediction found only if it waits for the
  learner's answer** (`waits`), directly or through another figure that does, and no caption,
  lead, after-text, task or section prose below it states it: the next figure down is in view
  while the learner is still choosing.
- **Every chapter's notes say which requirement it questions, or why none,** under "Requirements",
  naming each requirement figure; and a requirement figure's record answers some of its readings
  and not all, and no text the learner reads before its second press names that record.
- **Every challenge's reference passes its own tests, and its starting point does not.**
- **The whole chapter renders in jsdom with no figure problem.**
- **The chapter's stated numbers are pinned** by its facts test against the lab.
- **The lab is deterministic.** The same code gives the same rows, times and identifiers on every
  machine: no clock, no `Math.random`, no locale-dependent formatting.
- **The icon and the manifest keep to the course** (`node scripts/icons.mjs` draws the icon and
  writes every file). Every icon `index.html` or the manifest names is there at the size it claims,
  their colours are the tokens', the manifest's paths and identity stay inside the course's own
  path on an origin the author's courses share, and the maskable icon keeps its mark inside the
  safe zone.
- **The Playwright suite drives the built site at desktop and phone widths**: every challenge
  completable with its reference and refusing a wrong attempt, saved work graded again on load
  and not bypassable through storage, resettable, a prediction committed before it is answered,
  no console error, no horizontal scroll even after every figure is used, no visible text under
  11 pixels, every phone control at least 40 pixels tall, no line of prose over about 85
  characters.
