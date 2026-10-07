# Brief Q: Sections 7 and 8, what each system keeps, the sorting, and metadata

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/round-2/Q.md`.

## explanation

Section 7's prose. It keeps the old text and adds one fact. The old text said: "Each system that
holds data keeps some information about its own assets. Object storage keeps each file's location,
its size and when it was last modified. The warehouse keeps each table's column names and types,
its row count, its size, when it was created and when it was last altered, and the name of the
account that owns it. The reporting tool keeps the dashboard's title, who created it and when,
when it last refreshed and its values. These are the lab's choices of what each kind of system
keeps. Each field is one the system uses for its own work. The warehouse uses column names and
types to run a query. Object storage uses a file's location to serve it. The reporting tool uses
the values to draw its chart. None of the three keeps what your questions asked about who is
responsible for an asset, what made it, what reads it or what changed in it. The programs, and
when each is due to run, exist. This page has not shown them yet. Later chapters do." The fact to
add, straight after what object storage keeps:

- A Parquet file carries its own column names, their types and its row count, written inside the
  file after its rows. That is where the inspector found a file's columns.

Change nothing else.

## mapLead

Shown above the figure that sorts the questions. It replaces the old text, which called the
figure a map. The old text said: "The map lists the eight questions about `daily_sales`. For each
question, choose the group that can answer it, then check your sorting. The three groups are:
Storage records it. The data suggests it. Only a record kept at the time answers it. A question
goes with the data when a query rebuilds the asset, when another asset shows the same numbers, or
when the last-written time and the latest row fit a write that worked. After you check, the lab
places each question itself, by reading storage and trying every query the builder offers. You can
run the map again on each change from the failure experiment." Facts:

- The figure lists the eight questions about `daily_sales`. Do not call it a map.
- For each question, choose the group that can answer it, then check your sorting.
- The three groups, as a Markdown list, with these headings exactly: Storage records it. The data
  suggests it. Only a record kept at the time answers it.
- A question goes with the data when a query rebuilds the asset, when another asset shows the
  same numbers, or when the last-written time and the latest row fit a write that worked.
- After you check, the lab places each question itself, by reading storage and trying every query
  the builder offers.
- You can then choose any change from the failure experiment, and the lab places the questions
  again for that week.

## generalisation

Section 8's prose. It keeps most of the old text. The old text said: "Once you have checked your
sorting, look at the questions in the group "Only a record kept at the time answers it". The map
tags each with the kind of record that would answer it. There are three kinds of record: [a list
of three]. The groups say what can answer a question now. The kinds say what record would answer
it for certain. The two sortings need not line up. One column in the data names people:
`updated_by` in `products.parquet` says who last edited each product's row. That is a fact about
a product, not a record of who is responsible for the file. After the edit to the program, two
questions about what made `daily_sales` left the data's group. Records about the assets and the
platform, written down and kept apart from the data itself, are called **metadata**. What storage
keeps (names, types, row counts, sizes, times, an owner's name) is metadata too: the part each
system keeps for its own work. The questions only a record answers need the rest, and nobody keeps
it unless somebody decides to. The rest of this course builds a system that keeps all three
kinds."

Change these, and keep the rest, the list of three kinds included, as it was:

- "The map tags each" becomes: the lab tags each. The figure is not a map.
- The definition of metadata changes. Facts, in this order:
  - Information about an asset or about the platform is called **metadata** (keep the word in
    bold): what an asset is, where it came from, who is responsible for it, what its numbers mean,
    how it is made, and how it relates to other assets.
  - Metadata can live inside the system that holds the data, as the warehouse's column names and
    types do; next to the data, inside the same file, as a Parquet file's own column names and
    types do; or in a system of its own.
  - What storage keeps (names, types, row counts, sizes, times, an owner's name) is metadata too:
    the part each system keeps for its own work.
  - The questions only a record answers need the rest.
- Do not say metadata is kept apart from the data.
- Drop "and nobody keeps it unless somebody decides to": the chapter says it once, at its end.
- Keep the last sentence: the rest of this course builds a system that keeps all three kinds.
