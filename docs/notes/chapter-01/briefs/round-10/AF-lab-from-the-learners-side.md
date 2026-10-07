# Brief AF: the lab from the learner's side first

Read `docs/notes/chapter-01/briefs/round-4/common.md` first, and the files it names: every rule
there holds for this brief, and `docs/style.md`'s rule "silence is preferable to filler" above all.
Write your draft to `docs/notes/chapter-01/drafts/round-10/AF.md`.

The author found the Metadata Lab still explained in technical terms before the learner is told,
in plain English, what they do with it. The rule now: explain a mechanism from the learner's side
first. First answer "What do I do, and what happens when I do it?"; only then "How is it built?".
The page's plain model of every figure: you ask, the lab checks, it shows you, you work out what
it means.

The opening section's prose starts with this paragraph, which stays as it is and is not yours:
"You start work on Monday 14 September 2026 at 09:00. You are a data engineer at an online shop
selling bicycle parts. The shop opened its online store on Monday 7 September." Your text follows
it directly. Under your text, a control the reader may open holds how the lab is built; then come
the map and the rest of the page.

The facts are in `docs/notes/chapter-01/facts.md`, under "The opening, in the order the page gives
it": fact 2 for the lab's paragraphs, fact 3 for the control's text. Use only those facts.

## labParagraphs

Markdown: the paragraphs right after the situation. One or two short paragraphs, no list, no
heading, no more than 110 words. Fact 2, all of it, in its order: what the figures are for, the
lab's name, that it runs in your browser, what happens when you use a figure, the two kinds of
figure, and why you work from what the lab shows you.

- Keep this sentence exactly as it is, word for word: "It runs in your browser: there is nothing
  to install, open or sign in to."
- Keep the name "the Metadata Lab".
- Say what you do and what happens in plain words: you ask, the lab checks the shop's data, it
  shows you what it found, you work out what it means. Use these verbs or plain ones like them.
- Do not use these words here: SQL, query, engine, memory, page load, code, data model,
  underlying. They belong in the control's text, not here.
- Do not say that every figure is interactive: the map and the week's figure are only read.

## labDetails

Markdown: the text the control opens. One paragraph, no list, no more than 100 words. Fact 3, all
of it, in its order, in plain words. Keep the words "query engine". Do not say "the week" alone:
say "the shop's first week" or "its first week".

## labDetailsSummary

Plain text: the words on the control that opens labDetails. No more than five words, no
punctuation. They say that it opens how the lab is built. Not a question.

Rules for every key:

- Put the subject first in every sentence. Name each thing before a sentence uses it with "the".
- Do not use these words: metadata (except in the name "the Metadata Lab"), simulate or
  simulation, schema, dataset, job, event, lineage, environment, instrument; or "run" as a noun
  (as a verb it is fine).
- Do not say how many programs there are, which asset a program reads or writes, or what any
  program does.
- No reassurance, no motivation, no sentence about what the reader has been told or already
  knows. Verbs for what the lab does (checks, works out, shows) are fine; nothing gives the lab or
  a figure a wish, a mood or a wait, as a person would have.
