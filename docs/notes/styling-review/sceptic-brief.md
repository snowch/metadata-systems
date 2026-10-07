# Brief: the sceptic's pass over the styling review

A reviewer on another model read the course site's look from screenshots and wrote 25 findings,
`findings.md` in this directory, to the brief in `brief.md`. Reviewers over-call. Your job is to
attack each finding before anybody acts on it: is what it says it sees really there, is it really
a fault for a reader, and is its severity right?

## What you have

- The screenshots in `/tmp/claude-0/-home-user/8fe2150f-cb84-52b9-b63b-9e8644068234/scratchpad/style-review/`
  (named as `brief.md` says). Open the ones each finding cites, and look for yourself.
- The stylesheets: `apps/course/src/styles/tokens.css`, `app.css`, `figures.css`; the figures in
  `packages/views/src/`; the runtime's lesson page in `platform/lesson-runtime/src/` (the course
  may not edit `platform/`: a fix there is a change to another repository, so say so).
- A preview of the built site may be running at http://localhost:4173/metadata-systems/; you may
  drive it with Playwright from `/home/user/metadata-systems` to check a claim. The screenshots of
  the fixed "The map" button are full-page captures, so the button sits wherever the window was;
  judge that finding on a real window, not on the capture alone.
- The design's stated intent, in the header comment of `tokens.css`. A finding that only prefers
  a different taste is not a fault.

## For each finding, write

- **Verdict**: upheld, upheld in part, or rejected, with the reason in a sentence or two, citing
  what you saw (a screenshot, a line of CSS, a measurement).
- **Severity**: the one you would give, high, medium or low, by the brief's definitions.
- **Where the fix lives**: the course's own styles or figures, or the platform's runtime.

Do not propose rewrites; say only whether the finding stands. Then list, in one line each, any
fault you saw that the reviewer missed, with its screenshot.

Write your verdicts to `/home/user/metadata-systems/docs/notes/styling-review/verdicts.md`,
numbered as the findings are, and reply with only that path. Do not edit any other file.
