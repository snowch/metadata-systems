# App status delivery evidence

Issue: https://github.com/snowch/metadata-systems/issues/2

The contents, chapters and Jupyter file browser now offer App status. Version discovery and
verified offline completeness are independent. Update prepares a replacement; Later preserves
the current page, and Restart to update is a separate guarded action. No other tab is reloaded.

## Build and migration

The release contract and cache migration are documented in [authoring](../../authoring.md#app-status-and-release-identity).
Root and notebook `release.json` have the same `{schema: 1, commit, build}` values. HTML embeds
its own commit and build. Checks bypass HTTP and worker caches and never query GitHub main.
Assembly rejects mismatched source commits between HTML entry points. Reassembling the same
production directory twice produced identical release and offline manifest identities.

Existing manifest versions, code-save keys, exercise-answer keys and notebook storage remain
unchanged. Pending snapshots are verified again after focus/reopen, including eviction repair.
Existing complete snapshots are retained for pinned open clients. Explicit removal deletes only
this course's offline caches, not its answer/notebook stores or another project's caches/workers.

Measured local production artifact (before committing, so screenshots show the base source
commit; clean CI builds embed their own commit):

| Asset | Bytes | Gzip bytes |
| --- | ---: | ---: |
| Front JavaScript | 251,727 | 79,820 |
| Front stylesheet | 29,772 | 7,615 |
| Explicit offline payload, 628 files | 38,821,784 | Not a compressed archive |

The total includes chapters, Python, wheels, fonts and runtime assets. The installed course
worker manages that payload separately. UI size and progress come from the generated manifest
and actual verified bytes, not the shared mockup's simulated figures.

## Commands and results

- `npm run check`: passed formatting, copyright, licences, types, 47 Vitest tests, Node tests,
  203 Python tests, prose checks, production front build and 20 browser checks. Two existing
  viewport-specific browser checks were skipped as designed.
- `PATH=/workspace/offline-venv/bin:$PATH notebook/jupyterlite/build.sh /tmp/app-status-production-lite`:
  passed all 33 notebook executions and reader-ID checks; built the real runtime and 21 licensed
  wheels. After the last shared UI changes, rebuilt `notebook/buttons` and copied its generated
  federation files/configuration into the assembled test artifact.
- `node scripts/build-offline.mjs /tmp/app-status-accepted`: assembled the measured payload.
- `node scripts/offline-smoke.mjs /tmp/app-status-accepted`: passed actual persistent-browser
  cancellation/resume, fresh launch with empty HTTP cache and no network, old/deep links,
  Jupyter file browser, real Python in previously unvisited chapters, checksum rejection,
  storage failure, pending-update eviction/repair, defer/restart, activation failure/retry,
  busy/unsaved/composition guards, work becoming unsafe during asynchronous restart,
  separate online-only update, multi-tab release pins, missing-pinned-asset rejection,
  saved-notebook retention and confirmed removal preserving user and sibling-project storage.
- `node notebook/jupyterlite/reader-smoke.mjs /tmp/app-status-accepted-reader`: passed release,
  answer recovery, publication replacement, Chapter 1b redirect, table viewer, execution,
  persistence, shared Python navigation and autosave checks. A separate copy prevents test
  fixture mutations from interfering with the offline suite.
- `node notebook/jupyterlite/download-smoke.mjs /tmp/app-status-production-reader`: passed actual
  streamed Python-byte progress, delayed startup, queued runs and answer retention.
- Focused `checkRelease` browser run: passed phone touch opening, reduced motion, Escape/focus
  restoration, malformed metadata, failed checks, offline uncertainty and an aborted stale
  response. Separate phone/desktop light/dark screenshots are below.

The offline test constructs a second actual assembled artifact with a changed required asset,
then downloads and verifies it through the real worker. Both retain the same real source commit,
so the test also verifies that `build` detects asset changes a commit-only comparison misses.
The test logs both content-derived build identities. No download progress or execution is
simulated; HTTP/storage/eviction failures are deliberately injected.

## Independent review

Learner words were drafted separately by `prose_edits` from checked implementation facts.
`proximity_sceptic` reviewed source and actual browser logs independently. Findings about release
pinning, restart lifecycle, pending-only downloads and operation-specific feedback were fixed.
The final source review, including pending-eviction repair and file-browser entry points, found
no remaining critical issues. The reviewer did not independently rerun browser tests.

## Screenshots

Before: [phone](before-390.png), [desktop](before-1280.png).

After: [phone](after-390.png), [desktop](after-1280.png),
[phone dark](after-dark-390.png), [desktop dark](after-dark-1280.png).
