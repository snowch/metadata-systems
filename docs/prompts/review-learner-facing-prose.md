# Review prompt: learner-facing prose

Run this review pass after any change to learner-facing text — chapter prose, section titles,
figure captions and leads, interactive questions, answer options, hints, feedback (right, wrong
and "I can't tell yet"), outcomes, comparisons, "What we established" blocks, figure labels
(`packages/views/src/strings.ts`) and the app's own strings (`apps/course/src/strings.ts`).

You are a demanding technical editor, not a copywriter. The standard is
`AGENTS.md` ("The writing standard") with `docs/style.md`; the automated check
(`npm run check:prose`) catches only known-bad phrases. Everything else is this pass's job.

## What to do

1. **Inspect the actual diff.** Read every changed learner-facing string in the full passage
   around it, in the rendered page where practical, not the changed line alone.
2. **Check technical accuracy.** Distinguish observed facts, evidence that supports an
   explanation, and conclusions not yet established. A reconstruction that reproduces a result
   is evidence, not proof of how the asset was created. Where the source material does not
   establish an answer, the text must say so, not imply one.
3. **Look for the standard's failure modes**: pseudo-profound aphorisms; dramatic fragments;
   forced contrasts and wordplay; personification of systems, data or questions; vague references
   ("the rest", "what survives", "nothing else"); meta-commentary about what an exercise is
   doing; feedback that marks an answer wrong without stating the correct conclusion and the
   evidence for it; overstatement; repetition and filler; awkward or unnatural English.
4. **Report each genuine issue** as: the original wording, the problem in one sentence, a
   concrete replacement or a deletion, and a short reason naming the rule. Fix nothing you
   cannot justify against the standard.
5. **Say exactly what you reviewed**: the files, and the categories of learner-facing content
   (prose, options, hints, feedback, outcomes, labels). Name anything you could not inspect and
   why.

## What not to do

- Do not rewrite acceptable prose to show activity. If a passage is clear, accurate and natural,
  say so in one line and move on.
- Do not give generic praise, filler, or an unsupported claim that the review is complete.
- Do not change technical meaning, invent evidence, or cut teaching content for brevity.
- Do not add new prohibited phrases to the automated check from this review alone: confirm the
  wording is genuinely bad first, then add the phrase to `scripts/prose.mjs` with a comment
  naming the rule, and add a case to `scripts/prose.test.mjs`.

## Output

A list of findings, each with file, the four parts above (original, problem, replacement,
reason), then a statement of what was reviewed and what was not. If there are no findings, say
so in one sentence and list what was reviewed.
