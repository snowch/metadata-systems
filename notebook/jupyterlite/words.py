# Copyright © 2026 Christopher Snow

"""The few sentences that differ in the JupyterLite version, because Jupyter runs cells differently.

Everything else the reader sees comes from the marimo notebooks, notebook/chapter_01_part_1.py and
_part_2.py. Each entry here replaces one paragraph there (`MARIMO` names what it replaces) or follows
one (`AFTER`). Haiku drafted them from brief AN (docs/notes/chapter-01/briefs/round-15/), from facts
checked on the built page, and the warnings from brief AP (round-16/); RUN_FIRST is the first two
sentences of HOW_TO, for part 2.
"""

# The warning at the top of each part: what was measured for this version.
WARNING = {
    1: (
        "The page runs Python in your browser. The first time you open it, your browser downloads "
        "about 13 MB. On a computer, running every cell took about 10 seconds, and the page used "
        "about 400 MB of memory. If a phone runs short of memory, the browser may reload the page, "
        "and a reload loses anything you have not saved."
    ),
    2: (
        "The page runs Python in your browser, and the first time you open it on its own, your "
        "browser downloads about 13 MB. Measured on a computer, the page downloaded less than 1 MB "
        "when opened from part 1's link, in a browser that had opened part 1. Part 1's link opens "
        "this page in a new tab, and part 1 stays open in its own tab. On a computer, running every "
        "cell took 10 to 11 seconds, and the page used about 420 MB of memory. If a phone runs short "
        "of memory, the browser may reload the page, and a reload loses anything you have not saved."
    ),
}

# How to run a cell, in place of part 1's paragraph.
HOW_TO = (
    "Nothing on the page runs until you run it. Run every cell first: choose Run, then Run All Cells, "
    "in the menu bar at the top. To run one cell, select it and press Shift+Enter, or press the run "
    "button, a triangle, in the toolbar. A cell does not run again when a cell it uses changes. After "
    "you change a cell, run the cells below it too. Select the cell below the one you changed, then "
    "choose Run, then Run Selected Cell and All Below. To keep your changes, save the notebook: choose "
    "File, then Save Notebook, or press Ctrl+S (Cmd+S on a Mac). After a reload, the page shows your "
    "saved copy. That copy stays in this browser and is shown instead of the chapter, even after the "
    "chapter is updated."
)

# Part 2's reader has read HOW_TO in part 1; nothing on part 2 shows until it runs.
RUN_FIRST = (
    "Nothing on the page runs until you run it. Run every cell first: choose Run, then Run All Cells, "
    "in the menu bar at the top."
)

# Before the cell that reads the day's row, in place of the marimo notebook's lead.
THURSDAY_ROW = (
    "The cell below reads the row for the same day from `daily_sales`. The day is the one set in the "
    "code cell above. If you change the day there, run the cell below too, because it does not run "
    "again by itself."
)

# Before the menu of changes, in place of the marimo notebook's lead.
CHANGES = (
    "Choose a change from the menu below. Then select the first cell below the menu. In the menu bar "
    "at the top, choose Run, then Run Selected Cell and All Below. The cells below show the platform "
    "on Monday morning, after the week ran with the change you chose. The cells above the menu keep "
    "showing the week as it ran."
)

#: The marimo notebooks' sentences these replace, found by their exact text.
MARIMO = {
    "HOW_TO": (
        "The boxes of code with numbered lines are cells you can run. To run a cell, press its run "
        "button. The run button is a triangle at the top right of the cell. You can also press "
        "Ctrl+Enter (Cmd+Enter on a Mac) while you type in the cell. On a computer, the run button "
        "appears when the pointer is over the cell. On a phone, the run button is always there. When "
        "you run a cell, the cells that use its results run again. Nothing you change is saved. "
        "Reloading the page shows the chapter as it was published."
    ),
    "THURSDAY_ROW": (
        "The cell below reads the row for the same day from `daily_sales`. That is the day set in "
        "the cell above, which you may have changed."
    ),
    "CHANGES": (
        "The cells below show the platform on Monday morning, after the week ran with the option "
        "you choose. The cells above the menu keep showing the week as it ran."
    ),
}

#: The marimo notebooks' sentences these follow: RUN_FIRST ends part 2's opening paragraph.
AFTER = {
    "RUN_FIRST": "The head of the shop has sent you one line: \"Thursday's revenue looks wrong.\"",
}
