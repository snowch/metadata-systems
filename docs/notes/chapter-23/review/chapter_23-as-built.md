[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 22](chapter_22.ipynb)

# Chapter 23: Metadata at scale

**Objectives**

- Measure the week's metadata.
- Project it to 10,000,000 assets, and find which question costs too much first.
- Delete old events, and find what lineage that loses.
- Question the requirement "Keep lineage for 90 days."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

    <<CODE>> mo.Html(figures.figure(figures.pipeline(shop.run_week(["returns"]), "jobs nightly; functions at any hour"), "The shop's three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table `returns`."))

## The week, counted

The shop's metadata system holds one week of one small shop. The next cell counts what it holds.

    <<CODE>> week23 = shop.run_week(["returns"])
    shop.scale.measure(week23)

The week holds 11 assets, 6 jobs, 34 runs, 68 events, 67 run edges and 14 job edges, over 7 days. An event takes 1492 bytes on average.

The week's rate is about 0.9 events per asset per day: 68 events, over 7 days, for 11 assets.

The next cell lists, for each dataset, how many of the 14 job edges a search downstream from it follows to the end, and the share of all 14 that number is.

    <<CODE>> shop.scale.reach(week23)

From `orders.jsonl`, a search downstream follows 6 of the 14 job edges: 0.43, the widest share. From `clean_orders`, it follows 4: 0.29.

The projection below keeps the week's rates as the platform grows from 10 assets to 10,000,000. Each asset gets the week's events per day. Every event is kept for 90 days. The widest search follows 0.43 of the edges. The projection counts the stored records that three questions read, each in two ways:

- The latest run of one job: read every stored event, or read the events sorted by job and time.
- One day's events: read every stored event, or read the events stored day by day.
- What is downstream of one asset: follow the search to the end, or follow it 4 steps.

For each way, the projection gives the first number of assets at which it reads more than 1,000,000 records. That limit is the shop's own choice.

Before you read on, write in the next cell which question passes that limit first.

    <<CODE>> expected_first = """
    Which question passes the limit first?
    ........
    """

    <<CODE>> shop.scale.first_over(week23)

The two questions that read every stored event pass the limit first, at 100,000 assets: the latest run of one job, and one day's events.

A structure that lets a question go straight to the records it needs, the way a book's index points to pages, is an **index**. With the events sorted by job and time, the latest run reads 31 records at 10,000,000 assets. It never passes the limit.

Storing records in separate parts by a key is a **partition**. Here the key is the day. One day's events read one part, and that question passes the limit only at 10,000,000 assets.

Followed to the end, the search downstream passes the limit at 10,000,000 assets. Followed 4 steps, it never passes it.

Compare this with what you wrote. The next cell lists the projection's numbers at each size.

    <<CODE>> shop.scale.project(week23)

## Keeping less

At 10,000,000 assets, the projection holds 794,805,210 events.

Deleting events older than a set time is **retention**. The next cell keeps the week's events no older than 3 days, measured at 09:00 on Monday 14. Then it lists the run edges that remain and include `r-201.json`.

The returns desk recorded `r-201` on Tuesday 8 at 14:20, and `record_return` read `r-201.json`.

    <<CODE>> events23 = shop.delivery.week_events(week23)
    kept = shop.scale.retain(events23, 3, "2026-09-14T09:00:00Z")
    found23 = shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(kept)))
    print(len(events23), "events,", len(kept), "kept")
    shop.scale.lineage_of(found23.by_run, "r-201.json")

The output shows 68 events, of which 28 are kept. No run edge still includes `r-201.json`, because the run that read it is no longer in the kept events.

`r-201`'s row is still in `returns`. The asset is in use; its lineage is not kept.

Folding each run's edges into one edge per job, before the events are deleted, is **compaction**. The folded edge keeps how many runs had it, and the first and last time. The next cell applies compaction to the whole week's events, and lists the edges that include `r-201.json`.

    <<CODE>> shop.scale.lineage_of(shop.scale.compact(events23), "r-201.json")

After compaction, `r-201.json` appears in one edge: `record_return` reads it, in 1 run, first and last at 14:20:05 on Tuesday 8. That edge stays when the events are deleted.

That job edge keeps that `r-201.json` was read, and when. It does not keep which run read it, or what that run wrote.

## Ninety days

[BOX] The head of the shop's requirement: "Keep lineage for 90 days."

Before you read on, write in the next cell what the requirement means to you here.

    <<CODE>> what_90_days_means = """
    What does "lineage for 90 days" mean here?
    ........
    """

The requirement could mean three things, and each needs something different:

- 90 days of events: retention of events by age.
- 90 days of edges: compaction before retention.
- The lineage of every asset still in use, however old: retention by use, not by age.

Retention by age meets the first meaning. It also lost the lineage of `r-201` while its row was still in use.

Compaction meets the second, at the level of jobs. The third needs to know which assets are still in use.

The requirement does not say which it means.

## Before Chapter 24

The week's metadata, kept at its rates, grows to 794,805,210 events at 10,000,000 assets. The questions that read every stored event passed the limit first, at 100,000 assets. An index and partitions held them off. A search limited to 4 steps never passed the limit. Deleting events by age lost the lineage of a row still in use. Folding each run's edges into job edges first kept that `r-201.json` was read.

Part V ends here. Chapter 24 starts Part VI, where you build the parts of a metadata system that the shop's pages have used so far.

- Which of your metadata system's questions read everything it stores?
- How long does it keep events, and what is kept after?
- Which of your assets depend on lineage older than that?

### How this differs from a real platform

- The projection keeps the week's rates at every size. A real platform's rates differ by asset: some assets change every second, and many never change.
- The projection counts the stored records that each question reads. It does not count time, memory or the cost of each read.
- The limit of 1,000,000 records, the 90 days and the 4 steps are the shop's own choices.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 22](chapter_22.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

