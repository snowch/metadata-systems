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

A second regression fills all six written-answer fields through the UI, saves old notebook copies
in JupyterLite's IndexedDB, and closes the browser process. It changes the served Chapter 1 and 2
files, restarts the same browser profile, verifies that the new prose appears, and checks every
answer, including Chapter 1 originals displayed read-only in Chapter 2. This passed in Chromium;
it has not reproduced the reported loss and does not establish the cause on the reader's device.

## Published commit indicator

The reader header shows the first seven characters of the Git commit stamped into its HTML,
linked to that commit on GitHub. A network-only comparison with `jupyterlite/release.json`
shows a tick for the same deployed commit, a cross for a different deployed commit, and a
question mark when the check fails. It checks on opening, each minute while visible, and when
focus, visibility or connectivity returns. The comparison is with the deployed site, not the
main branch while a deployment may still be building. It never reloads the reader or changes
saved work. `release.json` is excluded from the offline snapshot and its request uses the
existing offline-download cache bypass, so a saved release cannot certify itself as current.

## Applying an update from a chapter

The commit line offers **Update and reload** when a newer deployed commit is detected. It checks
the release over the network again on click. If a downloaded snapshot exists, it uses the same
client as the home page (`offline/client.js`): cross-tab locking, resumable downloads, file lengths
and SHA-256 checks, then the existing atomic snapshot switch. Without a downloaded snapshot it
reloads the online reader without downloading the full course. Cache and answer keys are unchanged.

Activation is explicit. Both worker wrappers intercept the pinned upstream install handler, whose
precache list is empty and whose default handler unconditionally calls `skipWaiting`. Their new
activation message calls `skipWaiting`, then a claim acknowledgement makes reload wait for the
new controller. The helper selects only the expected course worker, retaining other projects'
registrations. It never closes or reloads another tab. A course-scoped BroadcastChannel announces
that a verified update is ready; other chapters and the home page offer **Reload to update**.

Running code disables the action. A failed answer/code save blocks reload and names the export
controls; execution started during download also defers reload. Download cancellation or failure
does not publish a partial snapshot. The button reports percentage progress, and only the chosen
tab reloads after successful activation. Saved text/code remains in browser storage; Python restarts.

A waiting worker also exposes **Reload to update** when the HTML's commit already matches the
server. Retrying a complete snapshot keeps its existing previous-version fallback, so a repeated
update does not discard assets still used by another tab.
