# Brief CD: the warning boxes of Chapters 3 and 4

Each chapter opens with a warning box: one sentence always shown, then a section the reader opens,
labelled "Time and memory", with the measurements. Chapter 2's box reads, as a model of the form
(not to be copied for its numbers):

> The page runs Python in your browser, and the first time you open it on its own your browser
> downloads about 13 MB.
>
> (Time and memory) The page downloaded less than 1 MB when opened from Chapter 1's link, in a
> browser that had opened Chapter 1 (measured on a computer). Chapter 1's link opens this page in a
> new tab. Chapter 1 stays open in its own tab and keeps its own memory. On a phone, closing
> Chapter 1 leaves more memory for this page.
>
> Running every cell took 10 to 12 seconds, and the page used about 420 MB of memory. If a phone
> runs short of memory, the browser may reload the page, and a reload loses anything you have not
> saved.

Write in British English, no em dashes. Do not use "lab", "engine", "Jupyter" or "Pyodide".

Write the file once. Do not change it after you reply.

## Facts (measured on a computer, 12 October 2026)

- Chapter 3, opened on its own the first time: the browser downloads about 13 MB (the same files as
  Chapter 2).
- Chapter 3, opened from Chapter 2's link, in a browser that had opened and run Chapter 2: it
  downloaded less than 1 MB. Chapter 2's link opens it in a new tab; Chapter 2 stays open in its own
  tab and keeps its own memory; on a phone, closing Chapter 2 leaves more memory for Chapter 3.
- Chapter 3: running every cell took 9 to 11 seconds, and the page used about 420 MB of memory.
- Chapter 4: the same facts, with Chapter 3 in place of Chapter 2: about 13 MB on its own; less than
  1 MB from Chapter 3's link; a new tab; 9 to 11 seconds; about 410 MB of memory.
- For both: if a phone runs short of memory, the browser may reload the page, and a reload loses
  anything you have not saved.

## Slots

Keep these phrases word for word: "downloads about 13 MB", "running every cell took 9 to 11
seconds", "a reload loses anything you have not saved", and in each chapter "the page downloaded
less than 1 MB when opened from Chapter N's link" with N the chapter before.

A. **ch3_line**: Chapter 3's always-shown sentence.

B. **ch3_details**: Chapter 3's details, in the order of Chapter 2's: the link, the new tab and its
memory, then the time and memory, then the reload.

C. **ch4_line**: Chapter 4's always-shown sentence.

D. **ch4_details**: Chapter 4's details, in the same order.

Write the slots under `## A` to `## D`, each the exact text to place.
