[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 22](chapter_22.ipynb)

# Chapter 23: Metadata at scale

**Objectives**

- Measure the week's metadata.
- Project it to 10,000,000 assets, and find which way of answering a question passes a limit first.
- Delete old events, and find what lineage that loses.
- Question the requirement "Keep lineage for 90 days."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## The week, counted

The shop's metadata system holds the events of one week. The next cell counts what it holds.

    >>> week23 = shop.run_week(["returns"])
    >>> shop.scale.measure(week23)
      | assets | jobs | runs | events | edges by run | edges by job | days | bytes per event
      | 11 | 6 | 34 | 68 | 67 | 14 | 7 | 1492

The week holds 11 assets, 6 jobs, 34 runs, 68 events, 67 edges by run and 14 edges by job, over 7 days. An event takes 1492 bytes on average.

The week's rate is about 0.9 events per asset per day: 68 events, over 7 days, for 11 assets.

The next cell lists, for each dataset, how many of the 14 edges by job a traversal downstream from it follows to the end, and the share of all 14 that is.

    >>> shop.scale.reach(week23)
      | dataset | edges followed | share
      | s3://shop-raw/orders.jsonl | 6 | 0.43
      | warehouse://shop-warehouse/shop.analytics.clean_orders | 4 | 0.29
      | s3://shop-raw/customers.jsonl | 2 | 0.14
      | s3://shop-returns/r-201.json | 2 | 0.14
      | s3://shop-returns/r-202.json | 2 | 0.14
      | s3://shop-returns/r-203.json | 2 | 0.14
      | s3://shop-returns/r-204.json | 2 | 0.14
      | warehouse://shop-warehouse/shop.analytics.daily_sales | 2 | 0.14
      | reporting://shop-reporting/sales_dashboard | 0 | 0.0
      | warehouse://shop-warehouse/shop.analytics.clean_customers | 0 | 0.0
      | warehouse://shop-warehouse/shop.analytics.returns | 0 | 0.0

From `orders.jsonl`, a traversal downstream follows 6 of the 14 edges by job: 0.43, the widest share. From `clean_orders`, it follows 4: 0.29.

The projection below grows the platform from 10 assets to 10,000,000, in powers of ten: 10, 100, 1,000 and so on.

At every size it keeps the week's rates: about 0.9 events per asset per day, the week's number of edges by job per asset, and a widest traversal that follows 0.43 of the edges.

It keeps every event for 90 days, the time the head of the shop's requirement at the end of the chapter names.

It counts the records each of three questions reads, each answered in two ways:

- The latest run of one job: read every stored event, or read the events sorted by job and time.
- One day's events: read every stored event, or read the events stored day by day.
- What is downstream of one asset: follow the traversal to the end, or follow it 4 steps. At each step, each dataset leads to at most 3 edges, so 4 steps follow at most 81 edges.

For each way, the projection gives the first of these sizes at which it reads more than 1,000,000 records.

The limit of 1,000,000 records, the 4 steps and the 3 edges a step are the shop's own choices.

Before you read on, write in the next cell which ways pass that limit first.

    [WRITE] Which ways of answering pass the limit first?
    [WRITE] ........

    >>> shop.scale.first_over(week23)
      | way | first over the limit at
      | latest run: every event | 100000
      | latest run: sorted by job and time | None
      | one day: every event | 100000
      | one day: stored by day | 10000000
      | downstream: to the end | 10000000
      | downstream: 4 steps | None

The two questions that read every stored event pass the limit first, at 100,000 assets: the latest run of one job, and one day's events, each in its way that reads every stored event. The sizes go up in powers of ten, so each passes it somewhere between 10,000 and 100,000 assets.

A structure that lets a question go straight to the records it needs, the way a book's index points to pages, is an **index**. The events sorted by job and time are one.

With that index, the latest run reads 31 records at 10,000,000 assets: about 30 steps down the index, then one record. It never passes the limit.

Storing records in separate parts by a key is a **partition**. Here the key is the day. One day's events read one part, and that way passes the limit only at 10,000,000 assets.

Followed to the end, the traversal downstream passes the limit at 10,000,000 assets. Followed 4 steps, it reads at most 81 edges and never passes it.

Compare this with what you wrote. The next cell lists the projection's numbers at each size.

    >>> shop.scale.project(week23)
      | assets | events a day | events stored | edges | latest run: every event | latest run: sorted by job and time | one day: every event | one day: stored by day | downstream: to the end | downstream: 4 steps
      | 10 | 9 | 810 | 13 | 810 | 11 | 810 | 9 | 6 | 6
      | 100 | 88 | 7920 | 127 | 7920 | 14 | 7920 | 88 | 55 | 55
      | 1000 | 883 | 79470 | 1273 | 79470 | 18 | 79470 | 883 | 547 | 81
      | 10000 | 8831 | 794790 | 12727 | 794790 | 21 | 794790 | 8831 | 5473 | 81
      | 100000 | 88312 | 7948080 | 127273 | 7948080 | 24 | 7948080 | 88312 | 54727 | 81
      | 1000000 | 883117 | 79480530 | 1272727 | 79480530 | 28 | 79480530 | 883117 | 547273 | 81
      | 10000000 | 8831169 | 794805210 | 12727273 | 794805210 | 31 | 794805210 | 8831169 | 5472727 | 81

## Keeping less

At 10,000,000 assets, the projection holds 794,805,210 events.

Deleting events older than a set time is **retention**.

The week holds 7 days of events, so 90 days would delete none of them. The next cell keeps the events no older than 3 days, measured at 09:00 on Monday 14, as a stand-in: 90 days deletes the same way, later.

It lists the edges by run that remain and include `r-201.json`.

The returns desk recorded the return `r-201` on Tuesday 8 at 14:20, and `record_return` read the file `r-201.json`.

    >>> events23 = shop.delivery.week_events(week23)
    >>> kept = shop.scale.retain(events23, 3, "2026-09-14T09:00:00Z")
    >>> found23 = shop.ingest.edges(shop.ingest.objects(shop.ingest.normalise(kept)))
    >>> print(len(events23), "events,", len(kept), "kept")
    >>> shop.scale.lineage_of(found23.by_run, "r-201.json")
      68 events, 28 kept
      []

The output shows 68 events, of which 28 are kept.

No edge by run still includes `r-201.json`, because the run that read the file is no longer in the kept events.

With 90 days, that run's events would be deleted after 14:20 on Monday 7 December.

The next cell reads `r-201`'s row from the table `returns`.

    >>> week23.warehouse.sql("SELECT * FROM returns WHERE return_id = 'r-201'")
      | return_id | order_id | product_id | quantity | returned_at
      | r-201 | 7004 | 2 | 1 | 2026-09-08T14:20:00Z

The row is still in `returns`. Chapter 10's SQL function `returned_quantity(7004, 2)` reads it.

The row is still used. The record of the run that wrote it is gone.

Folding each run's edges into one edge per job, before the events are deleted, is **compaction**. The folded edge keeps how many runs had it, and the first and last time.

The next cell applies compaction to the whole week's events, and lists the edges by job that include `r-201.json`.

    >>> shop.scale.lineage_of(shop.scale.compact(events23), "r-201.json")
      | job | edge | dataset | runs | first | last
      | shop/record_return | reads | s3://shop-returns/r-201.json | 1 | 2026-09-08T14:20:05Z | 2026-09-08T14:20:05Z

After compaction, `r-201.json` appears in one edge. `record_return` reads it, in 1 run, first and last at 14:20:05 on Tuesday 8.

The shop keeps edges by job when it deletes events. The cell deleted nothing: keeping this edge is the shop's rule.

The edge keeps that `record_return` read `r-201.json`, and when. It does not keep which run read the file, or what that run wrote.

## Ninety days

[BOX] The head of the shop's requirement: "Keep lineage for 90 days."

Before you read on, write in the next cell what the requirement means to you here.

    [WRITE] What does "lineage for 90 days" mean here?
    [WRITE] ........

The requirement could mean three things. Each is a question the head of the shop might be asking, with what it needs:

- Can I see the events of the last 90 days? It needs the events kept for 90 days by age: retention.
- Can I see which jobs read and wrote which assets in the last 90 days? It needs edges by job kept for 90 days, folded before the events are deleted: compaction. It keeps jobs, not runs.
- Can I see how every asset still in use was made, however old it is? It needs a record of which assets are still in use, and lineage kept by use, not by age.

The shop records nowhere which assets are in use. With 90 days' retention, the run that wrote `r-201`'s row would be deleted on Monday 7 December, while the row stays in `returns`.

The requirement does not say which it means.

## Before Chapter 24

Kept at the week's rates, the metadata grows to 794,805,210 events at 10,000,000 assets. The ways that read every stored event passed the limit first, at 100,000 assets. The index kept the latest run under the limit at every size, and partitions by day kept one day's events under it until 10,000,000 assets. A traversal limited to 4 steps never passed the limit. Deleting events by age lost the run that wrote a row still in use. Compaction first kept the edge by job showing that `record_return` read `r-201.json`.

Part V ends here. In Chapter 24, the first chapter of Part VI, you build a metadata store: as JSON documents, then as tables, then as an indexed store, then as a graph.

- Which of your metadata system's questions read everything it stores?
- How long does it keep events, and what is kept after?
- Which of your assets depend on lineage older than that?

### How this differs from a real platform

- The projection keeps the week's rates at every size. A real platform's rates differ by asset: some assets change every second, and many never change.
- The projection keeps the widest share, 0.43, and 3 edges a step at every size. A real graph's shape changes as it grows.
- The projection counts the records each question reads. It does not count writes, the work of keeping an index up to date, time, memory or the cost of each read.
- The limit of 1,000,000 records, the 90 days and the 4 steps are the shop's own choices.
- The word compaction means other things in other systems. Apache Kafka's log compaction, for example, keeps at least the last record for each key and removes older ones.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 22](chapter_22.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

