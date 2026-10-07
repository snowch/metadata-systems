# Styling review: the sceptic's verdicts

Each of the 25 findings in `findings.md` was tested against the screenshots, the three stylesheets,
the figures in `packages/views/src` and the runtime in `platform/`, and every claim about a real
window or a size was measured on the preview (http://localhost:4173/metadata-systems/, driven with
Playwright from 320 to 1280 px wide, light and dark). "Measured" below means that. Every contrast
ratio the reviewer quoted was recomputed from `tokens.css` and is right.

**A caution about the evidence.** The screenshots were taken at 07:21. `figures.css`, the lesson
data, `labels.ts`, `strings.ts` and `LabPrediction.tsx` were edited between 07:25 and 07:30, and the
preview was rebuilt at 07:31. The first prediction is now a `choose` figure (four options, a
regular-weight neutral note) where the screenshots show a `predict` figure (two options, a bold
green verdict). Findings that quote that figure's options or verdict (S3, S4, S8, S11) are checked
here against the second prediction and the change lab, which are unchanged and show the same thing.
Everything else I compared (lead heights, tables, the second prediction's verdict, the change lab)
matches the screenshots.

**How I graded severity.** High: a reader cannot read, or is misled, in a common state. Medium: a
typical reader would notice the inconsistency or its cost in a common state. Low: local,
width-specific or polish. No finding reaches high.

| # | Verdict | Severity: reviewer, mine | The fix lives in |
| --- | --- | --- | --- |
| S1 | upheld | high, medium | course |
| S2 | upheld in part | medium, low | course |
| S3 | upheld in part | medium, low | course |
| S4 | upheld | medium, low | course |
| S5 | upheld in part | medium, low | platform for the structure; course for style or content |
| S6 | upheld | medium, medium | course |
| S7 | upheld | medium, medium | course |
| S8 | upheld in part | medium, low | course |
| S9 | upheld in part | medium, low | course |
| S10 | upheld in part | medium, low | course |
| S11 | upheld in part | medium, low | course style; the disabling is in the platform |
| S12 | upheld in part | medium, low | course |
| S13 | upheld | medium, low | course figures; platform for radio labels and headings |
| S14 | rejected | low, none | course, if wanted |
| S15 | rejected | low, none | course, if wanted |
| S16 | rejected | low, none | course, if wanted |
| S17 | upheld | low, low | course |
| S18 | upheld in part | low, low | course |
| S19 | upheld | low, low | course |
| S20 | upheld in part | low, low | course |
| S21 | upheld in part | low, low | course |
| S22 | upheld | low, low | course |
| S23 | rejected | low, none | none |
| S24 | upheld in part | low, low | course |
| S25 | upheld in part | low, low | course |

## Verdicts

### S1. A table's caption is clipped inside its scroll box on a phone

**Verdict**: Upheld. The caption wraps to the table's width, not the box's. The days table is 388 px
wide in a box of 294, 309, 324 and 348 px at viewport widths of 360, 375, 390 and 414, and its
one-line caption ends 331 px in, so 37, 22, 7 and 0 px of it are cut (measured; `0390-light-04-prediction.png`
and the dark twin show "daily_sale" under the thick border). Only this one table has a caption long
enough in the chapter (the others read "The 48 rows" and "7 rows"), so "every table" holds only for
a long caption.

**Severity**: Medium, not high. What is lost is the tail of a title that the region's accessible name
repeats and the column headings already say, and the sideways scroll the page cues reveals it. It
does look broken, on the 360 to 390 px phones that are most of them.

**Where the fix lives**: The course (`ScrollRegion`, `DataTable`, `figures.css`). The platform's
`StateInspector` only emits the `<caption>`; the course already hides one such caption in
`figures.css` (`.change-result .days-table caption`).

### S2. The 48-row table is drawn in full, and on a wide screen beside an empty column

**Verdict**: Upheld in part. The measurements hold: at 1280 the list is 240 by 434 px and the detail
702 by 2,782 px, so 2,348 px of column beside the detail is blank; the rows table is 738 px in a
702 px box, so ORDERED_AT loses 40 px; at 834 the detail column is 512 px and the table loses
230 px (`0834-light-05-investigation.png`). But drawing all 48 rows is the point of the section: the
lead sends the learner to find the rows that make Thursday's total differ, which needs every row
on show, and a capped or collapsed table would hide them (and put a scroll box inside a scrolling
page on a phone). What is fair is the wasted column, the clip at 1280, and the list (the control)
scrolling away from its detail.

**Severity**: Low.

**Where the fix lives**: The course (`figures.css` `.inspector`, `StorageInspector`).

### S3. The fixed "The map" button covers text on a phone, and the footer at every width

**Verdict**: Upheld in part. On real windows the toggle is 101 by 44 px at the bottom right. At the
foot of the page it covers the end of the copyright line on phones (18 px of "© 2026 Christopher
Snow" at 360 wide, 10 at 375, 3 at 390, which in `0390-light-13-foot.png` clips the last letter of
"Snow" rather than hiding the word) and 93 px of the footer sentence at 414. At 834 and 1280 it
covers nothing at the foot, because the footer text is centred and the button sits at the edge
(`0834-light-13-foot.png`, `1280-light-13-foot.png`), so "at every width" is wrong. Elsewhere it is
the ordinary overlay of a fixed control: the other cited captures are full-page or element captures
that show where the window happened to be, and text scrolls out from under it.

**Severity**: Low.

**Where the fix lives**: The course (`figures.css` `.map-dock`; page padding in `app.css`).

### S4. Radio buttons float beside the middle of multi-line labels

**Verdict**: Upheld. `.prediction-option, .fault-choice` use `align-items: center` (`app.css`).
Measured at 390 px, the radio sits 16 px below the first line's centre for a two-line label and
43 px below it for a four-line one (beside line three), and 14 of the chapter's 19 options wrap on a
phone (none at 1280, three at 834). The label stays in a block beside the control and the whole row
is the click target, so it is untidy rather than confusing.

**Severity**: Low.

**Where the fix lives**: The course (`app.css`).

### S5. Figure cards hold running prose, so the card no longer marks the lab's view

**Verdict**: Upheld in part. The observation is accurate: the lead is 347 px (investigation), 363 px
(change lab) and 374 px (sort) tall at 1280, and 565 to 581 px at 390, at body size and measure and
before the badge. In the investigation and failure-experiment sections the section's own prose is
empty (`prose: ""` in `invisible-system.ts`), so the card is the whole section. But the lead and
after text are the figure's own parts in the lesson schema, which the platform's `LessonView` draws
inside `<figure>`, and nothing I saw suggests a reader is misled by it.

**Severity**: Low.

**Where the fix lives**: Moving the prose out of the card is a platform change
(`lesson-runtime/src/LessonView.tsx`, another repository) or a content change (the course puts the
text in the section's `prose`). Setting it off is the course's `app.css` (`.figure-lead`,
`.figure-after`).

### S6. The badge-and-caption line changes layout with the caption's length

**Verdict**: Upheld. Measured at 1280 and 834: six of the ten figures have the caption beside the
badge (captions of 35 to 75 characters) and four below it (83 to 147); at 390 nine of ten stack.
In the stacked case there is a 20 px gap under the badge, because `.time-model-toggle` is 44 px tall
(`min-height: var(--control)`) around a 24 px badge. The caption is an anonymous flex item in a
wrapping 36rem row, so it drops at about 75 to 80 characters (the reviewer's 70 is close).

**Severity**: Medium. It repeats in every figure and is the consistency the brief names.

**Where the fix lives**: The course (`app.css` `figure.interactive > figcaption`,
`.time-model-toggle`).

### S7. Tables are framed three ways, and one frame is wider than its table

**Verdict**: Upheld. Measured at 1280: the days table is 470 px in a 958 px frame, the change lab's
table 359 px in 958; the result table in the construction figure is stretched to 956 px
(`.data-table { width: 100% }`), so REVENUE starts 527 px from DAY (`1280-light-06-construction.png`);
the record and columns tables are 702 px with no frame; the rows table is framed. The border belongs
to `.data-scroll`, a block box, not to the table, and only tables in a `ScrollRegion` get one. The
same holds at 834.

**Severity**: Medium. It shows in most figures, and the stretched two-column table makes the eye
cross a wide blank to join a day to its figure (the row rules help).

**Where the fix lives**: The course (`figures.css`).

### S8. Options, verdicts and generated lists run the card's full width while prose keeps its measure

**Verdict**: Upheld in part. The numbers hold on the live page: at 1280 the longest option runs 106
characters on one line, the first prediction's neutral note 114 on one line, and the second
prediction's amber verdict is three lines of 117, 111 and 8 characters; the verdict boxes are
958 px against a 576 px measure. The green-verdict example is stale (that figure is now a
regular-weight note). Single-line options and status lines are not paragraphs, so their length does
no harm. The multi-line verdict is the real case: the project's own 85-character test covers only
`.prose` text of three lines or more (`aesthetics.spec.ts`), so it never reaches a verdict, and a
verdict's lines run well past that ceiling. The other strong half is weight: `.prediction-match`
and `.prediction-nomatch` are 600 throughout, which is seven bold lines on a 390 px phone (measured,
236 characters).

**Severity**: Low.

**Where the fix lives**: The course (`figures.css`).

### S9. Containers inside a card come in eight treatments

**Verdict**: Upheld in part. The list of treatments is right and the diagnosis is not. "All share a
3 px radius" is false: the left-rule callouts (`.lesson-model-note`, `.change-outcome`,
`.change-after-all`, `.figure-locked`, `.verdict-failure`, `.verdict.blocked`) have no radius. The
pattern is mostly coherent: a tint with a 3 px left rule, the rule's colour naming the kind
(accent, grey, red, amber). The real inconsistencies are narrower: a verdict drawn with a rule when
a challenge fails and without one when a prediction is marked, and the note tint drawn with a rule
(notes) and without (`.time-model-note`, `.prediction-compare`). Nesting reaches a card and one
box, and three levels only for a table frame. In dark, the SQL block and the hint (`#0a0e0d` on a
`#151b19` card) read as inset code panels, not as holes (`1280-dark-06-construction.png`).

**Severity**: Low.

**Where the fix lives**: The course (`app.css`, `figures.css`).

### S10. The accent and the kind colours overlap in meaning

**Verdict**: Upheld in part. The numbers are right: `--kind-file` equals `--accent` (#0a6658),
`--ok` is 1.35:1 from it, `--kind-dashboard` is 1.02:1 from `--warn`; and the sort's top rules do
take blue, warn and accent (`.map-storage`, `.map-suggested`, `.map-record`), while the warn brown
does stand for "dashboard", "not matched" and "the data suggests it". But the accent is meant to be
the one ink for links, labels and files ("one ink accent" in `tokens.css`), the sort's rules are
decoration beside headings, and I found no screen where two of these meanings compete for the same
reading. The collision worth noting is dashboard brown against warn, a token matter more than a
reading one. In dark, `#facc15` is the loudest colour on the page, but it is the warn state's job
and reads at 8.7:1.

**Severity**: Low.

**Where the fix lives**: The course (`tokens.css`, `figures.css` `.map-*`).

### S11. After a prediction is checked, the chosen option looks unavailable

**Verdict**: Upheld in part. `PredictionChallenge` (platform) sets `<fieldset disabled>` once the
learner commits, so every radio draws in the browser's disabled grey and the chosen one differs
only by a grey dot (at 3x: faint in light, a lighter dot in dark; `1280-light-04-prediction.png`,
`1280-dark-07-failureExperiment.png`). It is weak but legible, and the verdict directly below
restates the choice ("You predicted: ..."). One thing the reviewer did not say: `.prediction-option:hover`
has no disabled exception, so a locked group still shows the pointer cursor and the hover fill
(measured: light `rgb(232, 236, 234)`, dark `rgb(10, 14, 13)`), inviting a click that does nothing;
in light it shows as a grey bar on an unchosen option in `1280-light-10-challenge.png`. That the
dark hover fill is darker than the card is taste.

**Severity**: Low.

**Where the fix lives**: The course's styles (`app.css` radio and option rules). The disabling
itself is in the platform's `PredictionChallenge`, so a different disabled treatment there is a
platform change.

### S12. The LAB + badge is a button that looks like a tag

**Verdict**: Upheld in part. There is no hover or pressed style (measured: border, colour and
background are unchanged on hover; only `cursor: pointer`), and the only affordance is the "+" and
"−" mark (`.badge-mark::after`). "Exactly like COMPLETE" overstates it: that badge is green on a
green tint (`.badge.ok`); they share only the shape and the mono capitals. The note the badge opens
repeats "How the figures run" at the chapter's foot (`0390-light-12-notes.png`), so a reader who
misses it loses nothing.

**Severity**: Low.

**Where the fix lives**: The course (`app.css`, and the badge's words in `runtimeStrings`).

### S13. Names and values the lab generates are set in the prose face

**Verdict**: Upheld. In text the figures generate, names and times are sans (the radio labels, the
change lab's bullets, the sort's answers, the eight inspector answers; `1280-light-07-failureExperiment.png`,
`1280-light-05-investigation.png`), while chapter prose chips them in mono, against the header of
`tokens.css` ("Plex Mono for every name, value and line of SQL"). The headings "Rebuilding
daily_sales" and "Which rules filter orders.parquet?" use the display face. It is the clearest
departure from the stated intent, which is why it stands; a name in a sentence is still readable,
which keeps it low.

**Severity**: Low.

**Where the fix lives**: Split. The figures' own strings (`ChangeLab`, `QuestionMap`,
`StorageInspector`, `strings.ts`) are the course's. The radio labels are plain strings drawn by the
platform's `PredictionChallenge` and `FaultInjector`, and section and challenge titles by
`LessonView` and `ChallengeRunner`, so marking names there is a platform change.

### S14. The section rule stops at the prose measure

**Verdict**: Rejected. It is an alignment, not a cut: the rule is the `border-top` of
`.lesson-section > h2`, whose `max-width` is the prose measure, so in every section (measured:
576 px against a 992 px or 802 px section) it ends where the prose under it does, and on a phone it
spans the full width. Preferring a rule at column width is taste.

**Severity**: None (low at most).

**Where the fix lives**: The course's `app.css`, if the author wants it.

### S15. The disabled primary button looks washed, not disabled

**Verdict**: Rejected. The numbers are right (`#78aba3`, 2.6:1), but opacity 0.55 on a filled button is
the usual disabled look, WCAG exempts inactive controls, and beside the enabled "Run tests"
(`1280-light-06-construction.png`) the disabled "Check my prediction"
(`1280-light-fresh-prediction.png`) plainly reads as unavailable. The dark version is the same
convention. A taste finding.

**Severity**: None.

**Where the fix lives**: The course's `app.css`, if the author wants it.

### S16. The dashboard looks like the page rather than like a dashboard, and its tracks imply a scale

**Verdict**: Rejected as a fault. The title sharing the h3 style (`.dashboard-title`) is a design
choice for a deliberately minimal stand-in. The tracks do not imply a round-number axis: Friday's
bar fills its track exactly (`1280-light-02-question.png`), so the track's end reads as the largest
value, and every value is printed beside its bar. The 1.19:1 track is decoration. The chart itself
is sound, as the reviewer says.

**Severity**: None (polish at most).

**Where the fix lives**: The course (`figures.css` `.dashboard`), if wanted.

### S17. The contents list's right-hand note wraps inconsistently on a phone

**Verdict**: Upheld, and it is wider than the reviewer saw. Of 32 rows, 3 put the note below the
title at 375 and 390 (rows 1, 27 and 29), 9 at 360, 23 at 320, 1 at 414 and none from 600 up
(measured). Rows are 52 or 79 px high as a result.

**Severity**: Low.

**Where the fix lives**: The course (`app.css` `.chapter-link`, `.chapter-to-write`).

### S18. The shell header takes two rows on a phone

**Verdict**: Upheld in part. The header is 113 px tall at 414 px and below (61 px at 600) because
the theme picker wraps to a second row (measured). It is not sticky (there is no `position: sticky`
in the stylesheets), so the cost is the top of a page once, and the 44 px controls are deliberate.

**Severity**: Low.

**Where the fix lives**: The course (`App.tsx`, `app.css` `.shell-header`).

### S19. The pager's link breaks across two lines on a phone

**Verdict**: Upheld, with a narrower scope. Measured: "Back to chapters" breaks across two lines at
375, 390, 412, 414 and 430 px (the common iPhone and Android widths) but not at 320 or 360 (the
sentence wraps before the link) or from 480 up. The sentence exists only while the next chapter is
unwritten.

**Severity**: Low.

**Where the fix lives**: The course (`Pager.tsx`, `app.css` `.pager-not-yet`).

### S20. Failure boxes run full width with their content in the left quarter

**Verdict**: Upheld in part. The geometry is right: four 958 px boxes with their content in roughly
the first 250 px (`1280-light-challenge-failing.png`). The chip claim is not a fault: the chips
read as mono chips in light and in dark (`1280-dark-challenge-failing.png`), and a decorative fill
needs no contrast ratio. It is the "what a desktop leaves empty" point the brief asks about, and no
more.

**Severity**: Low.

**Where the fix lives**: The course's `app.css` (`.verdict-failure`, `.verdict-values`); the markup is
the platform's `VerdictView`.

### S21. Small labels come in two faces, and the uppercase ones wrap on a phone

**Verdict**: Upheld in part. There are three faces, not two: mono (`.section-kind`, `.badge`,
`.hints-rung`), the condensed display face (`.choice-heading`, `h5`, `.change-result h4`) and the
text sans (`th`, `.asset-group-label`, `.map-system-name`). The inspector's two heads differ by
role (a label, `.inspector-heading`, 17 px display; a name, `.inspector-asset`, 20 px mono), which
fits "names in mono". The phone wrap is real (`0390-light-07-failureExperiment.png`: "THE QUERIES IN
THE BUILDER'S / CHOICES THAT REBUILD DAILY_SALES"). Polish.

**Severity**: Low.

**Where the fix lives**: The course (`figures.css`, `app.css`; the long labels are in `strings.ts`).

### S22. The four-select grid orphans the fourth control on a tablet

**Verdict**: Upheld. Measured: `.choice-fields` is two by two from 640 to 719 px, three and one from
720 to 933 px (every iPad portrait width included), and four across from 934 px; the orphans are
"Per" and "Orders with a quantity of 0 or less" (`0834-light-06-construction.png`,
`0834-light-10-challenge.png`).

**Severity**: Low.

**Where the fix lives**: The course (`figures.css` `.choice-fields`).

### S23. Inline code chips detach their punctuation

**Verdict**: Rejected. The mechanism is wrong: the lesson source has no space before the punctuation
("`products.parquet`?", "`daily_sales`?" and "`daily_sales`, and" in `invisible-system.prose.ts`).
The gap is only the chip's `padding: 0.05em 0.3em`, 2 to 4 px at 1x (zoom of
`1280-light-03-motivation.png`), which is how inline code normally looks, and the mark still reads
with its clause.

**Severity**: None.

**Where the fix lives**: Nowhere.

### S24. The question sort's columns do not align and squeeze at tablet width

**Verdict**: Upheld in part. At 1280 the third heading wraps and its rule sits a line lower than the
other two; at 834 the columns are about 248 px wide with answers of three to five lines
(`0834-light-08-explanation.png`). The first column being three quarters empty is the lesson and
not a flaw: storage answers one of the eight questions. The phone stacks well.

**Severity**: Low.

**Where the fix lives**: The course (`figures.css` `.question-map`, `.map-column`).

### S25. Two adjoining notes at the end of the change lab look like one

**Verdict**: Upheld in part. They share one rule and fill and sit 16 px apart (`.change-outcome`,
`.change-after-all`, `margin-top: var(--space-4)`), as in `1280-light-07-failureExperiment.png`, but
they read as two boxes and the second opens with a different statement ("Rebuilding daily_sales
suggested..."). Whether it needs a heading is a question about the text more than the styling.

**Severity**: Low.

**Where the fix lives**: The course (`figures.css`; the words are in the lesson prose).

## Faults the reviewer missed

- Control edges are under 3:1: selects and secondary buttons use `--border-strong`, 2.23:1 on the white card in light and 2.07:1 in dark, and the reviewer measured only text; the labels and the select chevron still identify them (`1280-light-06-construction.png`, `1280-dark-06-construction.png`). Low.
- "Text contrast passes AA everywhere measured" is not quite true: `--ok` on `--ok-bg` is 4.43:1 and is used for the 17 px prediction verdict and the 12 px COMPLETE badge, and AA asks 4.5:1 (`1280-light-07-failureExperiment.png`, `1280-light-06-construction.png`). Low.
- A false scroll cue: at 390 px the change lab's "Your query against this week's daily_sales" table overflows its box by 4 px with all four columns visible, yet the page says "Scroll sideways to see every column" and thickens the border, which narrows the box further (`0390-light-07-failureExperiment.png`, measured). Low.
- The challenge task paragraph meets the first select label with no gap (measured 0 px: `.prose > *:last-child { margin-bottom: 0 }`, then `.choice-fields` with no top margin), so the form reads as part of the paragraph (`1280-light-06-construction.png`, `0390-light-10-challenge.png`). Low.
- On a desktop the header's brand and theme picker sit at the window's edges (x = 16 and 1264 at 1280) while the page column starts at x = 144, so the header and the page share no edge (`1280-light-00-front.png`). Low, and arguable.
- The wrapped label of the front page's full-width "Start with Chapter 1" button is left-aligned (`.button` centres its box but sets no `text-align`), so a two-line label looks unbalanced (`0390-light-00-front.png`). Low.
