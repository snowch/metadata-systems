# Revision brief P28: Chapter 28, Build the metadata interface

Read `rev-common.md` first. Redraft these slots: A, B, D, F, Z. Terms: none new.

## A

A list of four objectives:

- Build a page for one asset from the shop's versions of the pieces Chapters 24 to 27 built, and
  from the shop's other records.
- Write the page's run history, and find which run a first version leaves out.
- Choose the page's sections, and see what the page leaves out.
- Question the requirement "The asset page must show everything about an asset."

## B

- Keep the heading `### A page for one asset`.
- The page is made of sections. A list, each section with where its rows come from:
  - `description`: the store (Chapter 24), which holds Chapter 4's lines;
  - `owner`: the three owners' sources (Chapter 27);
  - `runs`: the collector's file (Chapter 25);
  - `upstream` and `downstream`: the lineage graph and the queries (Chapters 26 and 27);
  - `columns`: the warehouse;
  - `freshness`: Chapter 13's measure.
- The pieces from Chapters 24 to 27 are the shop's own versions, not your code.
- The week is Chapter 27's, with Monday's failed run of `build_daily_sales`.
- You write one section's rows, `run_history(asset)`, and the list of sections.
- `shop.interface.runs()` gives every run in the collector's file: its program, state, start, end,
  and the datasets it wrote. `shop.interface.writers(asset)` gives the programs the lineage graph
  records writing the asset.
- The next cell lists the programs that write `daily_sales`: one, `build_daily_sales`.
- Keep: "The file holds 41 runs in all."

## D

- Keep: "The check finds 6 runs, and not Monday's."
- Monday's run failed and wrote nothing, so a run history built from what each run wrote leaves it
  out.
- Compare this with what you wrote.
- Change `run_history` so that it keeps the runs of the programs that write the asset, from
  `shop.interface.writers(asset)`. Select the cell and press **Run below**.
- Keep: "The check finds 7 runs, the `FAIL` among them."
- Keep the heading `### The sections`.
- Jo Marsh opens this page on Monday morning to find out why `daily_sales` ends on Saturday 12.
- The next cell holds the page's sections as a list, `sections`. As it stands, it has `description`,
  `owner` and `runs`.
- `description` holds Chapter 4's lines, which name the person responsible; `owner` puts that person
  beside the other two owners.
- The cell after it draws the page for `daily_sales`, and ends with the sections the page leaves
  out: `upstream`, `downstream`, `columns` and `freshness`. A name that is not one of the seven is
  listed as one the page cannot draw.
- Add the sections Jo Marsh's question needs, from the seven names. Select the cell and press
  **Run below**.

## F

- "Everything" could mean three things, and each needs something different. A list:
  - every section the shop can draw: all seven names in the list. That meets this reading, and
    shows nothing more about the asset than the sections themselves hold.
  - everything a person asking about the asset needs: the sections that answer their question. Who
    to ask about `daily_sales` needs `owner`; why its latest day is Saturday 12 needs `runs` and
    `freshness`.
  - the asset's whole history: every run and every earlier value, which grows every night. No list
    of sections meets it: `runs` holds this week's 7 runs, and `description` holds one record for
    each asset.
- The page's last line names which of the seven sections are not drawn. It cannot show what a drawn
  section leaves out, such as an earlier value or why a run failed.
- The page meets a reading only through the sections chosen for it.
- The requirement does not say which it means.

## Z

- Keep the heading `### Before Chapter 29`.
- The page took its sections from the shop's versions of the pieces Chapters 24 to 27 built, and
  from the warehouse and Chapter 13's measure.
- A run history built from what each run wrote left out Monday's failed run, which wrote nothing.
  Built from the programs that write the asset, it held all 7 runs.
- That history is complete only for programs the graph records writing the asset. A program whose
  every run failed would write nothing, so the graph would hold no edge from it to the asset, and
  `writers` would not list it.
- The page named the sections it left out, but not what a drawn section leaves out.
- Part VI ends here. Chapter 29 starts Part VII, where real producers and a real consumer of
  OpenLineage events meet the shop's own collector.
- Three questions, as a list:
  - Which runs does your catalogue's history of an asset leave out?
  - Which sections of your asset pages does anyone read?
  - What does your asset page not show, and does it say so?
- Keep the heading `### How this differs from a real platform`, then a list:
  - The shop's page is drawn in these cells, for one asset at a time, from a file read whole. A real
    catalogue's page reads a store that changes as events arrive.
  - The shop's failed run sends a `FAIL` with no output (Chapter 8). That is the shop's choice: in
    the OpenLineage specification, any run event may list outputs, a `FAIL` among them, and none
    must.
