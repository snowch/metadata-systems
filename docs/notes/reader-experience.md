# Course reader

All 33 published chapters use the reading surface introduced in the Chapter 1b comparison.
Chapter 1b is no longer generated or listed. Its old URL redirects to Chapter 1 before Jupyter
opens a document. Chapter 1 imports existing 1b code drafts if it has no canonical draft for
that example. Exercise answers already use the shared Chapter 1 keys.

## Controls and execution

Run all executes the current examples sequentially and stops at the first error. Each example
has Run and Reset; Chapters 2 onward also have Run below, which executes that example and every
following example. Learners run all first to establish prerequisites, then run below after an
edit. There is no automatic replay of earlier learner code or side effects. Editing or resetting
an earlier example marks previously executed later results as stale. Skipped results are labelled
so a previous output cannot be mistaken for a new execution.

Prose and generated display helpers remain read-only. Hidden setup executes before examples.
The existing Python computations, example order, exercise checks and output renderers are retained.
Reader buttons replace the running/saving instructions only; exercise callouts retain their content.
Field inventories use labelled bullets where the facts are parallel; explanations remain prose.

## Persistence and migration

Draft keys are per notebook and example. Chapter 1 keeps the six identifiers from 1b. From
23 October 2026, all chapters use permanent reader IDs marked on their source decorators.
Previously those IDs came from notebook positions, so inserting prose could orphan or misassign
a draft. The initial permanent IDs retain all current keys; new builds reject missing or duplicate
IDs. A refresh restores drafts but clears outputs. Earlier positional keys are not deleted or
blindly reassigned, because a key without its original notebook version can be ambiguous.
Download code exports the live examples even when local storage fails. Existing notebook code
edits are imported before a legacy document is replaced, without overwriting a reader draft.
An archived notebook remains as a second backup; storage failures retain an exportable live draft.
Opening an archived reader copy retains the code actually stored in that copy.

Answer keys do not change. Chapter 1 explicitly asks learners to write guesses before Chapter 2,
which recalls the original daily_sales and clean_orders answers read-only beside evidence and
provides separate revision fields. Export answers remains a separate backup from Download code.

## Python progress

A course service worker streams the main runtime response and reports decoded bytes received.
The build records the actual WASM file size, so compressed HTTP length headers cannot distort
percentages. Intermediate reports are throttled with a trailing update so a paused connection
still reports the last bytes received. Cancellation reaches the underlying reader. A truncated
response never reports completion. Kernel startup and chapter preparation remain separate stages.

Standalone builds use a wrapper around JupyterLite's filesystem/stdin worker. Complete-course
builds retain the existing offline worker and add the same streaming helper to its cached and
network responses. Course download/update requests bypass normal runtime progress handling.
If service workers are unavailable, the existing loading stages, slow guidance and Retry remain.

## Validation

Build-time CPython execution checks every chapter. Browser checks run the chapter examples and
exercise edits through Run below, preserve answers/drafts and archive legacy edits. A throttled
HTTP test verifies intermediate download percentages with real service workers. Unit checks cover
compressed length handling, truncated streams, cancellation and superseded startup attempts.


The published-update browser regression changes the release version and notebook cell IDs,
inserts an explanation, then reloads the reader. It checks both a code edit and an exercise answer,
and verifies that every existing local-storage entry remains intact. Builder tests separately
insert prose and code before existing examples to catch any regression to positional save keys.
