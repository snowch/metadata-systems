# Styling review: findings

A review of the course site's look, as the brief in `brief.md` asks, from the 83 screenshots in
the scratchpad's `style-review/` folder (phone 390, tablet 834 and desktop 1280; light and dark;
every section after its figures were used, the fresh states, and a failing challenge), read against
`tokens.css`, `app.css` and `figures.css`. Contrast ratios quoted below were computed from the
token values. The words are another review's; this one is about what the page looks like.

Severity: **high** is broken, unreadable or misleading; **medium** noticeably weakens clarity,
hierarchy or consistency; **low** is polish. Most important first.

## Findings

### S1. A table's caption is clipped inside its scroll box on a phone. High

`0390-light-04-prediction.png` and `0390-dark-04-prediction.png`, below the second prediction's
yellow verdict box. The box headed "Scroll sideways to see every column." shows its caption as
"orders.parquet by day compared with daily_sale", cut at the box's right edge with the thick
border running over the missing letters. The caption is an HTML `<caption>` inside the table, so
it scrolls sideways with the rows instead of wrapping in the visible box. Every table in a
`ScrollRegion` will do this once it is wider than the box.

Direction: keep the caption out of the scrolling element, as a heading above the box that wraps to
the figure's width, and leave a visually hidden caption inside for screen readers.

### S2. The 48-row table is drawn in full, and on a wide screen beside an empty column. Medium

`0390-light-05-investigation.png` (the table runs for about 1,500 px with only ORDER_ID,
CUSTOMER_ID and PRODUCT_ID of the seven columns in view), `1280-light-05-investigation.png` and
`0834-light-05-investigation.png` (the asset list fills the top 500 px of the left column; below
it the column is blank for some 2,500 px while the rows run on; at 1280 the ORDERED_AT column is
still clipped at "2026-09-07T08:14" although a third of the figure is empty). The figure's rule
is that anything wider than its box scrolls inside it; nothing says the same of height, so the
section is mostly rows the learner scrolls past to reach the next section.

Direction: cap the rows table at a height (ten or twelve rows) and scroll it inside its box, or
show the first rows with a "show all 48" disclosure; on wide screens let the detail column take the
room the asset list does not use, or make the list sticky so it travels with the rows.

### S3. The fixed "The map" button covers text on a phone, and the footer at every width. Medium

`0390-light-13-foot.png` and `0390-dark-13-foot.png` (the button sits over the copyright line,
hiding "Snow"), `0390-light-04-prediction.png` (over the end of the first verdict box: "The
prediction was co"), `0390-light-05-investigation.png`, `0390-light-10-challenge.png`,
`0390-light-challenge-failing.png` (over the hint's last line), `0834-light-13-foot.png`,
`1280-light-13-foot.png`. The full-page captures put the button at an arbitrary height, but on a
device it permanently occupies about 100 by 44 px of the lower right of a 358 px reading column,
and at the foot of the page nothing can scroll out from under it.

Direction: give the page a bottom padding at least the dock's height so the footer and the last
control clear it; on narrow screens make the toggle smaller (an icon with its label as a tooltip,
or a slimmer pill) or hide it while the reader scrolls down and bring it back on an upward scroll.

### S4. Radio buttons float beside the middle of multi-line labels. Medium

`0390-light-04-prediction.png` (the radio for "yes, because an owner field names whoever is
responsible for the table" sits beside the second of three lines), `0390-light-07-failureExperiment.png`
(the four-line option "the program that writes daily_sales ... from Saturday's row on"; its radio
is level with the third line), `0834-light-04-prediction.png` (two-line options), the same in
dark. The options use `align-items: center`, which reads well for one line and loses the link
between control and label as soon as the label wraps, which on a phone is most of them.

Direction: align the control with the first line of its label (start alignment with a small top
offset, or a two-column grid with the control in the first row).

### S5. Figure cards hold running prose, so the card no longer marks the lab's view. Medium

`1280-light-07-failureExperiment.png` (five paragraphs of chapter prose inside the white card
before the LAB + badge appears), `1280-light-02-question.png` (the dashboard card opens with a
paragraph, then the badge, the chart, then another paragraph), `1280-light-05-investigation.png`,
`1280-light-08-explanation.png`, `1280-light-10-challenge.png`, and the same at every width. The
lead and after prose are set at the same size and measure as the prose outside the card, so the
card's edge, fill and shadow separate nothing: the reader meets page prose on grey, then the same
prose on white, and the badge and caption that should head the figure appear mid-card.

Direction: either move the lead and after prose outside the card, above and below it, so the
card's first element is the badge and caption; or style them as the figure's own instructions
(smaller, muted, or set off as a block) so the shift from chapter to lab is visible.

### S6. The badge-and-caption line changes layout with the caption's length. Medium

`1280-light-02-question.png` (badge and caption side by side: "LAB + The map: the shop's three
systems ..."), `1280-light-04-prediction.png` (badge alone on a line, caption as a paragraph
beneath with a gap), `1280-light-07-failureExperiment.png` and `1280-light-08-explanation.png`
(stacked), `1280-light-10-challenge.png` (both figures inline), the same at 834 and 390. The
figcaption is a wrapping flex row with a 36rem limit, so any caption over about 70 characters
drops below the badge. The same element therefore heads some figures as a labelled caption and
others as a tag marooned over a paragraph.

Direction: choose one arrangement for every figure: either the badge always on its own line, made
to look intended (for instance the caption set as the figure's heading beneath it), or the caption
always beside the badge with a hanging indent (a two-column grid with the badge in the first).

### S7. Tables are framed three ways, and one frame is wider than its table. Medium

`1280-light-04-prediction.png` (the days table ends at about 470 px inside a bordered box that
runs the card's full 955 px, leaving a framed blank to its right), `1280-light-07-failureExperiment.png`
(a 360 px table in the same 955 px box), `1280-light-05-investigation.png` (the record table and
the columns table have no outer border; the rows table below them has one),
`1280-light-06-construction.png` and `1280-light-fresh-construction.png` (the two-column result
table is stretched to the box, so REVENUE starts 525 px right of DAY and the eye travels across
white to join a day to its figure). The same at 834.

Direction: one frame for all tables, shrink-wrapped to the table (an inline box with `max-width:
100%`) so the border means "this is the table's extent"; reserve full width for tables that need
it, and let a narrow table keep its natural width.

### S8. Options, verdicts and generated lists run the card's full width while prose keeps its measure. Medium

`1280-light-04-prediction.png` (option "no, because an owner field names the account that writes
the table, and programs write the tables", 97 characters on one line; the green verdict's first
line is 117 characters), `1280-light-07-failureExperiment.png` (bullets such as "daily_sales was
last written at 2026-09-13 02:30:21 UTC; in the week as it first ran, at 2026-09-14 02:30:21 UTC."
at about 110 characters), `1280-dark-04-prediction.png`. Within one card the eye jumps between a
36rem column and a 60rem one. The verdict is also bold throughout; on a phone
(`0390-light-04-prediction.png`) that is seven lines of bold amber on yellow.

Direction: give options, verdicts and lab-generated lists the prose measure; set the quoted
prediction in regular weight and keep bold for the verdict's last clause.

### S9. Containers inside a card come in eight treatments. Medium

Across `1280-light-06-construction.png`, `1280-light-07-failureExperiment.png`,
`1280-light-08-explanation.png`, `1280-light-fresh-failure.png` and
`1280-light-challenge-failing.png`: the SQL block (sunken fill with a border), the hint (the same
fill, no border), the notes (note fill, accent left rule), the locked-figure note (note fill, grey
left rule), the verdicts (green or yellow fill, no rule), the failures (pink fill, red left rule),
the map's system boxes (page fill, border), the sort's columns (page fill, border, coloured top
rule). All share a 3 px radius, so the differences read as accident rather than role, and inside
the shadowed white card the result is boxes in boxes in boxes. In dark the two sunken fills become
near-black holes in the card (`1280-dark-06-construction.png`).

Direction: name three or four container roles (a data surface, a note, a verdict, a choice) and
give each one fixed recipe of fill, rule and border; apply the recipe everywhere the role appears
and nowhere else.

### S10. The accent and the kind colours overlap in meaning. Medium

`tokens.css`: `--kind-file` is the same value as `--accent` (#0a6658); `--ok` (#1a7f37) is 1.35:1
from the accent, so the correct-verdict green and the link green are not told apart by eye;
`--kind-dashboard` (#8f5300) and `--warn` (#855600) are 1.02:1 apart. On the page,
`1280-light-08-explanation.png`: the sort's three columns take blue (the table kind), amber (warn)
and green (accent), so one brown means "dashboard" in the glyphs and bars
(`1280-light-02-question.png`), "not matched" in the verdict boxes and "the data suggests it" in
the sort; and one green means a file, a link, a section label, and "a record would answer it". In
dark the warn yellow (#facc15) is far more saturated than anything else on the page
(`1280-dark-08-explanation.png`, `1280-dark-04-prediction.png`).

Direction: keep the three kind colours for kinds only, and take the sort columns and the verdicts
off them (distinct quiet hues, or no colour and let the headings carry it); move either the accent
or the file kind to a hue of its own; soften the dark warn toward the amber used in light.

### S11. After a prediction is checked, the chosen option looks unavailable. Medium

`1280-light-04-prediction.png` (both radios greyed; the chosen "no" is a grey dot among grey
rings), `1280-dark-07-failureExperiment.png` (the chosen "one, so the data still points to a
single query" is barely distinguishable from its neighbours), `1280-light-10-challenge.png`. The
disabled state the browser draws says "cannot be used" where the page means "this is what you
committed to". Related: the hover fill on an option (`--bg-sunken`) is near-black in dark and
reads as a selection where none exists (`1280-dark-08-explanation.png`, the last Week option, where
the cursor rested).

Direction: after commitment keep the chosen option visibly chosen (accent ring or filled mark, or
a small "your choice" label) and dim only the others; make the hover fill lighter than the card in
dark, as it is in light.

### S12. The LAB + badge is a button that looks like a tag. Medium

Every figure, for example `1280-light-02-question.png` and `1280-light-06-construction.png`. The
badge toggles a note about the lab's time model, but it is drawn exactly like the COMPLETE badge
beside the challenge heading, which is static; the only affordance is a 12 px "+" that reads as
part of the word, and there is no hover or pressed style in the stylesheet. The brief's own test
applies: a control that does not look like one.

Direction: give the toggle an affordance that the static badge lacks (an underlined label, a
visible disclosure mark with a hover change, or wording such as "Lab notes") and keep the plain
badge for things that are not pressable.

### S13. Names and values the lab generates are set in the prose face. Medium

`1280-light-07-failureExperiment.png` (radio labels "an analyst copies clean_orders every night";
bullets "daily_sales has 6 rows; in the week as it first ran, 7."), `1280-light-08-explanation.png`
("One asset rebuilds it: clean_orders."; "Last written at 2026-09-14 02:30:21 UTC."),
`1280-light-05-investigation.png` (the eight answers: "Storage records the last write, at
2026-09-14 01:00:41 UTC."). In the chapter prose the same names and timestamps are mono chips;
inside the figures they are sans, so the tokens' rule (every name and value in the mono) holds for
half the page. The section and challenge headings "Rebuilding daily_sales", "Recovering the rules
of clean_orders", "Which rules filter orders.parquet?" set the name in the condensed display face.

Direction: mark names and values in generated strings as the prose does (mono, perhaps without the
chip fill inside figures), and decide once whether a heading's name takes the mono.

### S14. The section rule stops at the prose measure. Low

`1280-light-05-investigation.png`, `1280-light-07-failureExperiment.png`, every 1280 and 834
section screenshot. The hairline above each section label runs from 0 to 576 px while the card
beneath runs to 992 px, so the rule looks cut short rather than chosen.

Direction: run the rule across the page column, or drop it and let the whitespace and the accent
label mark the section.

### S15. The disabled primary button looks washed, not disabled. Low

`1280-light-fresh-prediction.png` ("Check my prediction" at 55% opacity: white on roughly
#78aba3, 2.6:1, a pale teal that looks like a mis-set colour). In dark the same recipe gives dark
text on a dull green.

Direction: a disabled style of its own (an outlined button in the muted grey with muted text)
rather than opacity on the filled accent.

### S16. The dashboard looks like the page rather than like a dashboard, and its tracks imply a scale. Low

`1280-light-02-question.png`, `1280-dark-02-question.png`, `0390-light-02-question.png`. The chart
itself is well made: day labels, bars and values align on a grid in tabular numerals. But its
title "Sales, last 7 days" is the page's h3 style in the display face, so the shop's reporting
artefact and the course's own headings look the same; and the seven grey tracks end at a common
right edge, which reads as a fixed axis (0 to some round number) when the longest bar is simply
Friday's 204.24. The track against the white card is 1.19:1, so in light it is barely there.

Direction: frame the dashboard as an object inside the reporting tool (its own surface and header
line, distinct from the page's headings), and either drop the tracks and draw bars from a left
baseline or add a quiet maximum marker so the scale is stated.

### S17. The contents list's right-hand note wraps inconsistently on a phone. Low

`0390-light-00-front.png`, `0390-dark-00-front.png`. "0 of 2 challenges complete" drops under
chapter 1's title; "Still to be written" sits on the right for short titles and drops under long
ones ("27. Build the metadata interface", "29. Airflow, Spark, dbt and Trino"), so the list's right
edge is ragged.

Direction: on narrow screens always stack the note under the title (or always keep it right and
let the title wrap first).

### S18. The shell header takes two rows on a phone. Low

`0390-light-00-front.png`, `0390-dark-00-front.png`. Brand and "Chapters" on one row, "Theme
[Auto]" alone on a second right-aligned row; the header is about 110 px tall before the page
starts.

Direction: a compact theme control (an icon button, or the select without its label) so the three
fit one row, or move the picker to the footer on narrow screens.

### S19. The pager's link breaks across two lines on a phone. Low

`0390-light-13-foot.png`, `0390-dark-13-foot.png`: "The next chapter is still to be written. Back"
then "to chapters" on the next line, right-aligned, so the link is split mid-phrase.

Direction: set the sentence and the link as separate blocks on narrow screens, or keep the link
unbreakable so the break falls before it.

### S20. Failure boxes run full width with their content in the left quarter. Low

`1280-light-challenge-failing.png`, `1280-dark-challenge-failing.png`, `0834-light-challenge-failing.png`.
Four boxes each 958 px wide, their heading and three value chips within about 250 px, leaving a
long pink band; the chips' green-grey fill (`--bg-inset`) on the pink is 1.09:1, so they read as a
different tint rather than as chips.

Direction: cap the box at the prose measure or lay failures out two abreast on wide screens; derive
the chip fill from the box's tint (or use a hairline border instead of a fill) inside tinted boxes.

### S21. Small labels come in two faces, and the uppercase ones wrap on a phone. Low

`1280-light-06-construction.png`: QUESTION, LAB +, COMPLETE and THE CONCEPT are mono; YOUR QUERY,
AS SQL, RESULT, WHAT STORAGE SAYS, the table heads and OBJECT STORAGE are sans; all are small,
uppercase and spaced, so the two families look like one rule applied twice.
`1280-light-05-investigation.png`: the two column heads of the inspector, "Assets in storage"
(display sans, 17 px) and "orders.parquet" (mono, 20 px, bold), differ in face and size at the same
rank. `0390-light-07-failureExperiment.png`: "THE QUERIES IN THE BUILDER'S / CHOICES THAT REBUILD
DAILY_SALES" and "YOUR QUERY AGAINST / THIS WEEK'S DAILY_SALES" wrap to two letter-spaced lines,
which is slow to read.

Direction: one face for structural labels (the mono for the lab's badges only, or the reverse);
give the inspector's two heads the same rank with the asset name in mono inside; keep the h4
labels short enough for one line on a phone or set the long ones in sentence case.

### S22. The four-select grid orphans the fourth control on a tablet. Low

`0834-light-06-construction.png` ("Per" alone on a second row under three selects),
`0834-light-10-challenge.png` ("Orders with a quantity of 0 or less" alone). The `minmax(13rem,
1fr)` grid fits three at 802 px.

Direction: two by two at this width (a minmax that yields two or four columns, never three).

### S23. Inline code chips detach their punctuation. Low

`1280-light-03-motivation.png` ("Can we delete products.parquet ?", "Who should I ask about
daily_sales ?"), `1280-light-11-reflection.png` ("daily_sales , and your four rules"),
`1280-light-05-investigation.png` ("from daily_sales ;"). A space before the mark plus the chip's
side padding leaves a visible gap, so the question mark hangs apart from its clause.

Direction: remove the space in the source where it is there, and reduce the chip's horizontal
padding (or give the chip a hairline border instead of a fill) so the gap closes.

### S24. The question sort's columns do not align and squeeze at tablet width. Low

`1280-light-08-explanation.png`: the third heading "Only a record kept at the time answers it"
wraps, so its rule sits a line lower than the other two; the first column is three quarters
empty. `0834-light-08-explanation.png`: three columns about 230 px wide, answers wrapping to four
or five lines, headings wrapping too.

Direction: let the headings share a height (or make the coloured rule the column's top edge only)
so the rules align; at tablet width fall back to one or two columns.

### S25. Two adjoining notes at the end of the change lab look like one. Low

`1280-light-07-failureExperiment.png`, `0390-light-07-failureExperiment.png`: the change's
outcome box and the summary over all changes sit 16 px apart with the same fill and accent rule,
so the second reads as a continuation of the first rather than a different kind of statement.

Direction: merge them under one surface with an internal heading, or give the summary a heading
(or a different rule) so the step from "this change" to "all three changes" is visible.

## What works

- The three faces in their roles hold up: the condensed display face for headings, Plex Sans for
  prose, Plex Mono with tabular figures for every table, SQL block and asset name. Tables align,
  NULL in purple italic stands out, and the section kicker (accent mono label over a condensed
  h2) gives the ten sections a steady rhythm. Keep these.
- Text contrast passes AA everywhere measured: muted text is 6 to 7:1 on its surfaces in both
  themes, the verdict colours 4.4 to 5.7:1 in light and over 8:1 in dark, the table heads 6:1 and
  8:1.
- The dark theme is a true re-tokenisation, not an inversion: surfaces keep their order (page,
  raised, sunken), hues lighten rather than invert, and every figure reads the same way in both.
- The platform map is the strongest figure: glyph beside name, three layouts that hold at every
  width, arrows that turn with the layout, and the dock panel that repeats it without a redesign.
- The storage inspector's selected state (accent-soft fill with an accent border) and the
  overflow cue on scrolling tables (the thick right edge plus "Scroll sideways to see every
  column.") are clear and consistent wherever they appear.
- On a phone nothing scrolls horizontally, selects and buttons take the full width at 44 px or
  more, SQL wraps rather than clips, and the stacked map and sort columns read well.
- The dashboard's grid of label, bar and value with tabular numerals is the right form for seven
  days; S16 is about its frame and scale, not its marks.
