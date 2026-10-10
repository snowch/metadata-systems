# Brief AP: the warning at the top of each part

Chapter 1's notebook is now two pages, part 1 and part 2, in two versions: one that runs every cell
when the page opens, and one in which nothing runs until the reader runs it. Each page opens with a
short warning for a reader on a phone. The facts below were measured on 10 October 2026 in
Chromium, on a computer, from a local copy of each site (`docs/notes/notebook-prototype.md`,
"The chapter in two parts"). Write the four warnings, each under its key, following
`docs/style.md` and the writing standard in `AGENTS.md`. At most five sentences each. Do not add
facts. Do not mention a lab, an engine, a simulator, marimo, JupyterLite, Pyodide or WebAssembly.
The reader is "you". British English. No em dashes.

The current warning of the first version, for one page, reads: "This page runs Python in your
browser. The first time you open it, your browser downloads about 17 MB. On a computer, Python
took 10 to 17 seconds to start, and the page used about 1 GB of memory. If your phone runs short of
memory, the browser may reload the page, and a reload loses what you changed or wrote on the page."
Keep its wording wherever the facts below have not changed.

## Slots

- **MARIMO_1** (the first version, part 1). Facts, in this order:
  1. The page runs Python in your browser.
  2. The first time you open it, your browser downloads about 17 MB.
  3. On a computer, Python took 9 to 17 seconds to start, and the page used about 0.8 GB of memory.
  4. If your phone runs short of memory, the browser may reload the page, and a reload loses what
     you changed or wrote on the page.
- **MARIMO_2** (the first version, part 2). Facts, in this order:
  1. The page runs Python in your browser.
  2. Opened on its own the first time, it downloads about 17 MB; opened from part 1's link, in a
     browser that had opened part 1, it downloaded less than 1 MB.
  3. On a computer, Python took 8 to 17 seconds to start, and the page used about 1 GB of memory.
  4. If your phone runs short of memory, the browser may reload the page, and a reload loses what
     you changed or wrote on the page.
- **JUPYTER_1** (the second version, part 1). The current warning of the second version reads:
  "The page runs Python in your browser. The first time you open it, your browser downloads about
  13 MB. On a computer, running every cell took about 10 seconds, and the page used about 440 MB of
  memory. If a phone runs short of memory, the browser may reload the page, and a reload loses
  anything you have not saved." Facts, in this order:
  1. The page runs Python in your browser.
  2. The first time you open it, your browser downloads about 13 MB.
  3. On a computer, running every cell took about 10 seconds, and the page used about 400 MB of
     memory.
  4. If a phone runs short of memory, the browser may reload the page, and a reload loses anything
     you have not saved.
- **JUPYTER_2** (the second version, part 2). Facts, in this order:
  1. The page runs Python in your browser.
  2. Opened on its own the first time, it downloads about 13 MB; opened from part 1's link, in a
     browser that had opened part 1, it downloaded less than 1 MB.
  3. Part 1's link opens this page in a new tab; part 1 stays open in its own tab.
  4. On a computer, running every cell took 10 to 11 seconds, and the page used about 420 MB of
     memory.
  5. If a phone runs short of memory, the browser may reload the page, and a reload loses anything
     you have not saved.
