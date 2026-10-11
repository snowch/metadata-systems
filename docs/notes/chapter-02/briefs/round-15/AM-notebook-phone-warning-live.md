# Brief AM: the phone warning, corrected from the published page

Brief AL's warning was written from measurements on this machine. The notebook is now published,
and measuring the published page changed two facts. Redraft only the slot below, following
`docs/style.md` and the writing standard in `AGENTS.md`. Do not add facts. Do not mention a lab, an
engine, a simulator, marimo, Pyodide or WebAssembly. British English. No em dashes.

## The draft being corrected

> This page runs Python in your browser. The first time you open it, your browser downloads up to
> about 32 MB. On a computer, Python took 10 to 15 seconds to start, and the page used about 1 GB of
> memory. If your phone runs short of memory, the browser may reload the page, and a reload loses
> what you changed or wrote on the page.

## What changed

- The first visit downloads about 17 MB, not "up to about 32 MB": the site's host compresses the
  files as it sends them (measured on the published page, 10 October 2026: 17.1 MB).
- On a computer, Python took 10 to 17 seconds to start, not 10 to 15: on the published page it
  includes the download.

## Slot

- **phone_warning**: the same four facts, in this order, at most four sentences:
  1. The page runs Python in your browser.
  2. The first time you open it, your browser downloads about 17 MB.
  3. On a computer, Python took 10 to 17 seconds to start, and the page used about 1 GB of memory.
  4. If a phone runs short of memory, the browser may reload the page, and a reload loses what you
     changed or wrote on the page.
