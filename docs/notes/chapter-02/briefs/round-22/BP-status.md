# Brief BP: the words of a status notice under every notebook

Read `BK-common.md` first for the voice (British English, no em dashes, short, plain). This is not
chapter prose: these are the words of a small notice at the foot of the screen, at most about 40
characters each, that tells the reader what Python is doing. A phone reader may wait a minute; the
notice is the only sign that anything is happening. Write each under its own `## BPn` heading,
exactly as shown on the page, with no full stop at the end unless it has two sentences.

## BP1: shown from the moment the page opens until Python is ready
Python is starting in the browser. (The reader can read and scroll meanwhile.)

## BP2: shown for a few seconds once Python is ready
Python is ready.

## BP3: shown when the reader pressed Run all or Run below before Python was ready
Python is still starting; the cells will run as soon as it is ready.

## BP4: shown while the cells run, with two numbers the page fills in
Write it with the placeholders `{done}` and `{total}` exactly as written: how many of the cells
have run out of how many, for example 4 of 15.

## BP5: shown for a few seconds when every cell has run
Every cell has run.
