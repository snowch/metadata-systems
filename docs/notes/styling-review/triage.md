# Styling review: what each finding got

The author asked, on 7 October 2026, for a review of the site's overall styling. A reviewer on
another model read 83 screenshots against `tokens.css` (`brief.md`, `findings.md`: 25 findings);
an independent sceptic on a third model tested each one against the screenshots, the stylesheets
and the live preview (`sceptic-brief.md`, `verdicts.md`). The sceptic upheld 21 in whole or in
part, rejected 4, lowered the one high to medium, and found six faults the reviewer missed, two of
them accessibility. The sceptic's verdicts and severities are the ones acted on.

| Finding | Verdict | What was done |
| --- | --- | --- |
| S1, a table's caption clipped in its scroll box on a phone (medium) | upheld | A table's title now sits above its scroll box and wraps to the figure's width; inside the box the caption stays for a screen reader only (`ScrollRegion`'s `title`). |
| S2, the 48 rows beside an empty column (low) | in part | The 48 rows stay: the section sends the learner to find rows in them. On a wide page the list of assets now travels with the detail (sticky). |
| S3, the map's button over the page's foot on a phone (low) | in part | The foot has room below it for the button; a browser test checks no foot text is under it from 320 to 414 pixels. |
| S4, radios beside the middle of long labels (low) | upheld | The radio sits by the label's first line; a one-line label stays centred in its row. |
| S5, chapter prose inside the figure cards (low) | in part | Decided for the learner, as the author asked: a figure's lead and after text now sit on the page, at the prose's measure, and the card holds the caption and the lab's view only, so it always means the lab and always opens with its badge. Done in the course's stylesheet (the card is a layer behind two rows of the figure's grid), so the runtime's markup and reading order are unchanged and no platform change was needed. |
| S6, the badge and caption laid out by the caption's length (medium) | upheld | The badge has its own column and the caption sits beside it at every length, wrapping under itself. |
| S7, tables framed three ways, frames wider than tables (medium) | upheld | Every table's frame now hugs the table; the record and column tables have the same frame; no two-column table is stretched across the figure. |
| S8, verdicts at full width and in bold (low) | in part | A verdict keeps the prose's measure and regular weight, with only "The prediction was correct" or "was not correct" in bold. |
| S9, eight container treatments (low) | in part | The narrower inconsistencies the sceptic named are gone: a prediction's verdict now has the same left rule as a challenge's failures, and every note (the lab's note, a choice's line) the note's rule. |
| S10, the accent and kind colours overlapping (low) | in part | The sort's columns no longer borrow the table kind's blue, the warning's amber and the accent; their headings carry the meaning. The dashboard's brown against the warning's stays, as the sceptic judged it. |
| S11, the chosen option looking unavailable (low) | in part | Once committed, the chosen option is bold and the others muted; the locked options lose the pointer and the hover fill. |
| S12, the LAB badge a button that looks like a tag (low) | in part | The badge takes the accent on hover and focus, and a tinted fill while its note is open. |
| S13, names in figures set in the prose face (low) | upheld | Names in the figures' own sentences (the change lab's results, the sort's evidence, the inspector's answers, two headings) are set as code, as the chapter's prose sets them; the headings that carry names are in sentence case so the names keep their case. Option labels and section titles are drawn by the platform as plain text and stay so. |
| S14, the section rule at the prose measure | rejected | Nothing. |
| S15, the disabled button's look | rejected | Nothing. |
| S16, the dashboard's frame and tracks | rejected | Nothing. |
| S17, the contents list's notes wrapping unevenly on a phone (low) | upheld | On a phone each row's note sits under its title, every row alike. |
| S18, the header in two rows on a phone (low) | in part | On a phone the theme picker's word is kept for screen readers only and the header keeps one row. |
| S19, "Back to chapters" breaking across lines (low) | upheld | The link no longer breaks inside its words. |
| S20, failure boxes the figure's width (low) | in part | A challenge's failures keep the prose's measure. |
| S21, three faces for small labels (low) | in part | Not changed: polish, for a later pass. |
| S22, the fourth select alone on a tablet (low) | upheld | The choices sit two by two, then four across; a browser test holds every row full at eight widths. |
| S23, code chips detaching punctuation | rejected | Nothing. |
| S24, the sort's headings out of line, cramped on a tablet (low) | in part | The headings take the same height, so their rules line up, and the three columns start at 60rem; below it they stack. |
| S25, two adjoining notes reading as one (low) | in part | The summary over all three changes stands further off, with a muted rule, from the note on one change. |

The sceptic's own findings:

| Fault | What was done |
| --- | --- |
| Control edges under 3:1 (selects and secondary buttons) | A new token, `--border-control`, at 3.7:1 in light and 3.2:1 in dark, for every control's edge. |
| The correct-verdict green at 4.43:1 on its tint | `--ok` darkened to 4.92:1. A unit test, `tokens.test.ts`, now computes every text pair at 4.5:1 and every control edge at 3:1, in both themes. |
| A false "scroll sideways" cue on the change lab's table at 390 pixels | The narrow tables' cells are tighter on a phone; the table fits from 360 pixels, and below that the cue is true. |
| No gap between a challenge's task and its first control | The choices have space above them. |
| The header's edges off the page column on a desktop | The header's contents now share the page column's edges. |
| A wrapped button label left-aligned | Button labels are centred. |

The author asked for S5 and S13 to be settled for the best learner experience, and both are done.
Left: S21 (the small labels' three faces), polish for a later pass.
