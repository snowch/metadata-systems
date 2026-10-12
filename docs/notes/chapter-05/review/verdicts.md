# Chapter 5: the sceptic's verdicts

An independent sceptic, on a model other than the one that wrote the chapter, attacked each finding
in `findings.md` against the as-built page, Chapter 4, `notebook/chapter_05.py` and
`notebook/shop/graph.py`, and ran the engine once (finding 13). Its report, in summary:

| Finding | Verdict | What holds |
| --- | --- | --- |
| 1 | partly | "Before anything changes" points at nothing; Jo replies to a list the reader never sent. Not blocking. |
| 2 | upheld | Jo's purpose (orders with no customer id) is never returned to; what to send Jo is never answered; the last step of questioning the requirement is missing. |
| 3 | partly | The `drops` line is left out while the page says "as Chapter 4 left them". The team choice is disclosed. |
| 4 | partly | "Each needs a different kind of edge" is contradicted by reading 2. "Answers none" is blunt, not contradictory. |
| 5 | partly | "Returned the assets that share an owner" is wrong for the walk from `daily_sales`. |
| 6 | partly | The first prediction is a trace of arrows; the second asks which and why together. The alt text must describe the drawing. Not blocking. |
| 7 | upheld | "You choose which kinds of edge it follows" is never exercised; `in` is never run; no change-and-run-again step. |
| 8 | partly | Reading 1's "edge between datasets" contradicts Chapter 6's shape (through jobs). Closing question 3 is not answered by it. |
| 9 | partly | Minor. |
| 10 | partly | The `<-label-` form has no gloss. Minor. |
| 11 | partly | Two sentences restate the table. Minor. |
| 12 | partly | "Each part of the graph that edges join on its own" is awkward. Minor. |
| 13 | rejected | The engine builds a graph where one name has two types; only `traverse` from it raises. |
| 14 | upheld | The reality note says nothing about how a real platform differs. |
| 15 | rejected | The platform figure is a course-wide convention, identical in Chapter 4. |
| 16 | partly | `products.csv` against `s3://shop-raw/products.csv`: a course-wide habit. Minor. |
| 17 | partly | The `#` lines are counted, as in Chapter 4's first records cell. Very minor. |
| 18 | partly | "Chapter 6 ... records what each job reads and writes" makes the chapter the actor; the reader records them. |

## Acted on

2, 3, 4, 5, 7, 8, 14 and 18, and the cheap parts of 1, 6, 10 and 11. The rest stand, with the
sceptic's reasons.
