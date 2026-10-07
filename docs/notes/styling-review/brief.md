# Brief: a review of the course site's styling

You are a senior product designer reviewing the visual styling of an interactive, browser-based
course, *Metadata Systems*, as its learners see it: a competent software or data engineer reading
on a phone, a tablet or a desktop, in a light or a dark theme. You review the look, not the words:
another review reads the prose.

## What to read first

- `apps/course/src/styles/tokens.css`: the design system. Its header comment states the intended
  look: "a catalogue's: hairline rules, values and names set in a monospace with tabular figures,
  labels set small and spaced, one ink accent", IBM Plex in three cuts, one colour per kind of
  asset. Judge the site against that intent. Do not propose replacing the typefaces, the palette
  or the overall direction unless something in them fails a reader.
- `apps/course/src/styles/app.css` and `apps/course/src/styles/figures.css`: the shell, the lesson
  page and the figures.
- The screenshots in `/tmp/claude-0/-home-user/8fe2150f-cb84-52b9-b63b-9e8644068234/scratchpad/style-review/`.
  Names are `<width>-<theme>-<nn>-<part>.png`: widths 0390 (a phone), 0834 (a tablet) and 1280 (a
  desktop); themes light and dark; `00-front` is the front page; `01-header` the chapter's title and
  objectives; `02` to `11` the chapter's ten sections in order, each after every figure in it has
  been used; `12-notes` the notes at the chapter's foot; `13-foot` the page's foot; `14-map-open`
  the map of the platform opened from its button at the foot of the window. `1280-light-fresh-*`
  show three sections before anything is used, and `*-challenge-failing` a challenge that has run
  and failed, with one hint shown.

A preview of the built site may be running at http://localhost:4173/metadata-systems/; you may
drive it with Playwright from `/home/user/metadata-systems` (Chromium is installed) to check a
detail, but the screenshots should be enough. Do not edit any file in the repository except your
findings file.

## What to look for

- Typography: hierarchy (can a reader tell a section heading from a figure's caption from a
  label?), the type scale, line length, the three faces each in its role.
- Colour: the palette in use, contrast of text and controls, whether the accent and the kind
  colours carry meaning consistently, the dark theme given the same care as the light one.
- Space and rhythm: margins between sections, figures and paragraphs; density inside figures.
- Consistency: repeated elements (figures, captions, the Lab badge, buttons, radio options, tables,
  status lines, notes) with the same edges, padding and placement each time.
- Hierarchy of containers: borders, fills, radii and shadows used by role, or applied to
  everything so that nothing stands out; boxes inside boxes.
- The dashboard's bar chart, as a chart: marks, labels, scale, its look beside the tables.
- Each width: what a phone squeezes, what a tablet wastes, what a desktop leaves empty.
- Anything that looks broken: overlap, clipping, misalignment, a control that does not look like
  one, text that is hard to read.

## How to write each finding

- Number them S1, S2, and so on, at most 25, most important first.
- Each names the screenshot file or files that show it and says exactly what is seen there.
- Each has a severity: **high** (broken, unreadable or misleading), **medium** (noticeably weakens
  clarity, hierarchy or consistency), **low** (polish).
- Each suggests a direction in a sentence or two, never a rewrite of the code.
- Say what works too, briefly, at the end, so that a fix does not undo it.

Write your findings to `/home/user/metadata-systems/docs/notes/styling-review/findings.md`, and
reply with only that path.
