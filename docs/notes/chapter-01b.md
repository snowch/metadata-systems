# Chapter 1b: The shop and its platform

This comparison view is generated from Chapter 1's source by `build_reader` in
`notebook/jupyterlite/build_ipynb.py`. The shop, diagrams, examples and answer boxes are the same.
The heading, navigation and running/saving instructions adapt to the reader controls. Four file
and warehouse descriptions use short introductions and labelled bullets, held in `reader.json`;
the build requires their headings to match Chapter 1. They retain the original facts, field
meanings and code instructions. The original chapter remains available beside the comparison
on the contents page.

## Requirements

This view questions no additional metadata requirement. It compares the reading experience of
per-example Run and Reset controls with the existing notebook controls on the same material.
Chapter 1's learning objectives and the requirements described in its notes still apply.

## Originality

The comparison uses the course's own bicycle shop and the same examples as Chapter 1. It does
not reproduce another project's course or interface copy. Reader instructions and descriptions
were drafted by the separate prose agent from checked implementation and data facts.

## Reader implementation

`ms.reader` notebook metadata opts in. Prose and setup are read-only and cells cannot be deleted.
Windowing is disabled so reading and keyboard navigation use the complete document. Native code
editors, output rendering, answer fields and Python startup/retry are reused. Each example runs
only itself after hidden setup is ready. All six Chapter 1 examples are independent of the other
visible cells. Future dependent examples will need explicit prerequisites rather than implicitly
replaying arbitrary learner code.

Run all executes current examples sequentially, stops on the first error and marks later results
as skipped. It reuses Jupyter's cell execution/output API without selecting each cell. A live
progress notice floats outside the document so it cannot shift the reader's place. Execution
restores the visible document anchor after outputs resize, while respecting wheel/touch scrolling.
Code edits and answers remain available during execution; Run and Reset controls share one lock.

The shared platform diagram uses original file, table, dashboard and job symbols with a single
key. Connectors indicate the known order of systems, not asset-level dependencies. Its container
query stacks cards based on the diagram's available width and font size, including landscape and
split views where a viewport-only breakpoint left the old diagram cramped.

Code drafts use a synchronous localStorage key per notebook and stable example identifier,
independent of notebook autosave and published versions. A failed write retains the live code
and reports that it is not saved. Download code exports the live examples. Reset restores the
published source and clears only that example's output; it does not restart Python. A refresh
restores code and clears outputs so old results cannot be mistaken for a new execution. The
comparison's code drafts are separate from Chapter 1's notebook saves. Its answer boxes use the
same answer keys as Chapters 1 and 2. Offline download updates/removal leave all learner data.
