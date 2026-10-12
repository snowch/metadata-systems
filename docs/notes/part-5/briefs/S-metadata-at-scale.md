# Brief S: Chapter 23, "Metadata at scale"

Read `docs/notes/part-5/briefs/common.md` first, and `docs/style.md`. Their rules hold here.

Terms this chapter introduces, in bold, and nowhere before the slot named: **index** and
**partition** (slot E), **retention** (slot F), **compaction** (slot G). Terms already introduced,
which you may use: delivery, deduplication, idempotent, event time, arrival time, precedence, alias,
entity resolution.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Measure the week's metadata.
- Project it to ten million assets, and find which question costs too much first.
- Delete old events, and find what lineage that loses.
- Question the requirement "Keep lineage for 90 days."

### Slot B: under the heading `## The week, counted`

- The shop's metadata system holds one week of one small shop. The next cell counts what it holds.

### Slot C: after that cell

- 11 assets, 6 jobs, 34 runs, 68 events, 67 edges run by run, 14 edges job by job, 7 days. An event
  takes 1492 bytes on average.
- That is about 0.9 events per asset per day: 68 events, over 7 days, for 11 assets.
- The next cell lists, for each dataset, how many of the 14 job edges a search downstream from it
  follows, to the end, and what share of all 14 that is.

### Slot D: after that cell

- From `orders.jsonl`, 6 of the 14 edges: 0.43, the widest. From `clean_orders`, 4: 0.29.
- The next cell's model keeps the week's rates as the platform grows from 10 assets to 10,000,000: each
  asset with the week's events per day, every event kept for 90 days, and the widest search following
  0.43 of the edges. It counts the stored records three questions read, each two ways (write them as
  a Markdown list):
  - the latest run of one job: reading every stored event, or with the events sorted by job and time;
  - one day's events: reading every stored event, or with the events stored day by day;
  - what is downstream of one asset: followed to the end, or followed 4 steps.
- For each way, it gives the first number of assets at which it reads more than 1,000,000 records.
  That limit is the shop's own choice.
- Before you read on, write in the next cell which question passes that limit first.

### Slot DD: the text inside that cell

One question, then `........` on its own line: which question passes the limit first? Plain text.

### Slot E: after that cell

- The two that read every stored event pass it first, at 100,000 assets: the latest run, and one
  day's events.
- A structure that lets a question go straight to the records it needs, as a book's index points to
  pages, is an **index**: with the events sorted by job and time, the latest run reads 31 records at
  10,000,000 assets and never passes the limit.
- Storing records in separate parts by a key, here the day, is a **partition**: one day's events read
  one part, and pass the limit only at 10,000,000 assets.
- Followed to the end, the search downstream passes it at 10,000,000; followed 4 steps, never.
- Compare this with what you wrote. The next cell lists the model's numbers at each size.

### Slot F: after that cell, under the heading `## Keeping less`

- At 10,000,000 assets the model stores 794,805,210 events.
- Deleting records older than a set time is **retention**. The next cell keeps the week's events no
  older than 3 days at 09:00 on Monday 14, and lists the run edges left that name `r-201.json`.
- The returns desk recorded `r-201` on Tuesday 8 at 14:20, and `record_return` read its object.

### Slot G: after that cell

- The cell prints 68 events, 28 kept. No run edge names `r-201.json`: the run that read it is gone.
- `r-201`'s row is still in `returns`. The asset is in use; its lineage is not kept.
- Folding each run's edges into one edge per job, with how many runs had it and the first and last
  time, before deleting the events, is **compaction**. The next cell folds the whole week's events
  that way and lists the edges that name `r-201.json`.

### Slot H: after that cell

- One edge: `record_return` reads `r-201.json`, in 1 run, first and last at 14:20:05 on Tuesday 8. It
  stays when the events are deleted.
- The job edge keeps that the object was read, and when. It does not keep which run, or what that run
  wrote.

### Slot RH: the heading of the requirement's section

Exactly `## Ninety days`. A box holding the requirement comes after this heading.

### Slot I: after the box (do not quote the requirement again)

- Before you read on, write in the next cell what "lineage for 90 days" means to you here.

### Slot II: the text inside that cell

One question, then `........` on its own line: what does "lineage for 90 days" mean here? Plain text.

### Slot J: after that cell

- It could mean three things, each needing something different. Write them as a Markdown list:
  - 90 days of events: retention of events by age;
  - 90 days of edges: compaction before retention;
  - the lineage of every asset still in use, however old: retention by use, not by age.
- Retention by age met the first and lost `r-201`'s lineage while its row was in use. Compaction met
  the second at the level of jobs. The third needs to know which assets are still in use.
- The requirement does not say which it means.

### Slot Z: the closing (a heading `## Before Chapter 24`, a summary, a lead, three questions)

- Summary: the week's metadata, kept at its rates, grows to hundreds of millions of events at ten
  million assets. The questions that read every stored event passed the limit first, at 100,000
  assets; an index and partitions held them off, and a search limited to 4 steps never passed it.
  Deleting events by age lost the lineage of a row still in use; folding runs into job edges first
  kept that the object was read.
- Part V ends here. Chapter 24 starts Part VI, where you build the parts of a metadata system that
  the shop's pages have used so far.
- Three questions, as a list: Which of your metadata system's questions read everything it stores?
  How long does it keep events, and what is kept after? Which of your assets depend on lineage older
  than that?

Then a heading `### How this differs from a real platform` and a list:

- The model keeps the week's rates at every size. A real platform's rates differ by asset: some
  assets change every second, many never.
- The model counts stored records read. It does not count time, memory or the cost of each read.
- The limit of 1,000,000 records, the 90 days and the 4 steps are the shop's own choices.
