# Review brief, round 17: Chapter 2 after Chapter 1's changes

You are reviewing Chapter 2 of an interactive course on metadata, a Jupyter notebook a learner
runs in the browser. Read as a learner: a data engineer who has done Chapter 1 and no later chapter.

## What to read

- `chapter_01-as-built.md`: Chapter 1 as the learner meets it after Run all. Text, code cells,
  what each prints (`[output]`), each figure's caption and words (`[figure]`), and two boxes
  (`[box: warning]`, `[box: steps]`). `[hidden code cell]` is setup the learner does not see.
- `chapter_02-as-built.md`: Chapter 2 the same way. This is what you review.
- `/home/user/metadata-systems/CLAUDE.md`: the course's rules, in particular "Voice", "Interaction
  is the explanation", "Question the requirement" and "What no check can catch".
- `/home/user/metadata-systems/docs/style.md`: the style checklist.

## What changed in Chapter 1 today

Chapter 1 was split out of Chapter 2 on 11 October and has changed since:

- The things that run each night are now called **jobs** (they were "programs"), and the
  **export** from the shop's checkout and catalogue is named as what writes the three files.
- The head of the shop's line is quoted: "Thursday's revenue looks wrong."
- The variables `storage`, `warehouse` and `reporting` are introduced as Python variables.
- The run steps (Run all, Run below, Save) are a box under the warning.
- Figures are drawn into the page; the week diagram's key says "the export and jobs".
- Chapter 1 ends by asking the learner to write down which file or table each warehouse table is
  made from, and why.

## What to look for

1. **Repeats.** Anything Chapter 2 explains that Chapter 1 now explains: a thing should be
   explained once, where the reader first meets it. Chapter 2 may remind briefly; it should not
   teach it again.
2. **Mismatches.** Words, names or facts Chapter 2 uses differently from Chapter 1 (for example
   "program" where Chapter 1 says "job"; a different description of the export, the week, the
   systems, the files or the tables).
3. **Gaps.** Anything Chapter 2 assumes the reader saw in Chapter 1 that Chapter 1 does not say,
   or names before explaining.
4. **The link between the chapters.** Chapter 1 ends with the learner's written guesses; does
   Chapter 2 pick them up where it should, and does its opening recap say only what the next
   question needs?
5. **Anything else from CLAUDE.md's "What no check can catch"**, in Chapter 2.

## How to write each finding

- Number it. Give a severity: **high** (wrong, contradicts Chapter 1, or loses the learner),
  **medium** (a repeat, a gap or a mismatch a learner would notice), **low** (wording).
- Quote the page exactly, and say which chapter and which section (the `## ` heading above it).
- Say what is wrong and why, citing the rule or the Chapter 1 passage it conflicts with.
- Suggest a direction. Never rewrite the passage.
- Check any number against the outputs before you assert it.

Write your findings to `findings.md` in this folder, most severe first. Do not edit any other file.
