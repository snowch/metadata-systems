[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 31](chapter_31.ipynb)

# Chapter 32: Metadata for ML and AI

**Objectives**

- Record a forecast trained on `daily_sales` with the fields an experiment tracker keeps.
- Find what the run's record can tell you about the rows the forecast was trained on, and what it cannot.
- Test a guess about those rows against the record's digest.
- Question the requirement "Record the training data of the model."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## A forecast and its record

On Saturday 12 at 09:00 the shop trains a forecast of the next day's revenue: the mean of the last 3 days in `daily_sales`. It comes to 13650 pence.

The run is recorded with the fields MLflow, an experiment tracker, keeps for a run's input: its `name`, `digest`, `source`, `schema` and `profile`, and the context `training`.

The forecast is registered as version 1 of `next_day_revenue`, and the version names the run that made it.

The next cell lists the record of the run's input, one field on each row.

    >>> week32 = shop.run_week(["returns"])
    >>> shop.ml.record(week32)
      | field | value
      | name | shop.analytics.daily_sales
      | digest | 60ba54ee
      | source | warehouse://shop-warehouse/shop.analytics.daily_sales
      | schema | ["day", "revenue_pence"]
      | profile | {"num_rows": 5}
      | context | training

The digest is a short fingerprint of the rows. MLflow computes it from the first 10,000 rows, the number of rows and the column names, through MD5, and keeps 8 characters.

The shop computes its digest the same way from its own rows. It is the shop's value, not MLflow's, because MLflow reads the rows with a library the shop does not use.

The profile holds the number of rows: 5.

On Monday 14 at 09:00, Jo Marsh asks which rows the forecast was trained on.

Before you read on, write in the next cell whether the run's record can tell you.

    [WRITE] Can the run's record tell you which rows the forecast was trained on?
    [WRITE] ........

    >>> shop.ml.today(week32)
      |  | rows | digest
      | the run's record | 5 | 60ba54ee
      | daily_sales on Monday 14 at 09:00 | 7 | 6b0727dc

The cell above sets the run's record beside `daily_sales` on Monday 14 at 09:00. The record has 5 rows and the digest `60ba54ee`. The table has 7 rows and the digest `6b0727dc`.

The record lists no rows. It holds a name, a digest and a count. The digests differ, so the table has changed since the run.

Compare this with what you wrote.

Each night's run of `build_daily_sales` adds one row, for the day before, and leaves the other rows as they are. So the rows the forecast read may still be in the table.

The record can test that guess: the right rows give the same digest.

The next cell holds `where`, a condition on the rows of `daily_sales`. As it stands, `day <= '2026-09-13'` keeps all 7.

Change the date so that the condition keeps the rows the table held on Saturday 12 at 09:00. Select the cell and press **Run below**. The check below it computes the digest of the rows your condition keeps.

    >>> where = "day <= '2026-09-13'"

    >>> shop.ml.check(week32, where)
      | test | passes
      | Your rows (7) give the digest `6b0727dc`, not the run's `60ba54ee`. | no

With the date of Friday 11, the check passes: 5 rows give the digest `60ba54ee`, the one the run recorded.

A match is strong evidence, not proof: with 8 characters, other rows could give the same digest, though the chance is small.

## What a digest reads

The digest reads only the first 10,000 rows, with the row count.

The next cell takes a table of 10,001 rows made for this cell, and changes one row at a time by 1 penny.

    >>> shop.ml.cap()
      | change | digest
      | none | b54985ab
      | the first row, plus 1 penny | ebf8f1e4
      | row 10001, the last, plus 1 penny | b54985ab

Changing the first row changes the digest, from `b54985ab` to `ebf8f1e4`. Changing row 10,001, the last, leaves it at `b54985ab`.

A digest shows a change only within the rows it reads.

## The training data

[BOX] The head of the shop's requirement: "Record the training data of the model."

Before you read on, write in the next cell what "record the training data" means to you here.

    [WRITE] What does "record the training data" mean here?
    [WRITE] ........

It could mean three things. Each item says what it needs:

- the snapshot the forecast read: a version or a time of the table, and a table that keeps its earlier states, as the table formats in Chapter 2's closing note do;
- the query that chose the rows: its text and when it ran. The same text run on Monday reads 7 rows, not 5;
- the features computed from the rows: the code that computed them and the values it gave, here the last 3 days' revenue.

The tracker's record meets a narrower reading: which table, and whether it has changed since. The requirement does not say which it means.

## Before Chapter 33

The run's record held a name, a digest and a count, not the rows. The digest showed the table had changed since the run, and a guess about the rows could be tested against it.

A digest that reads the first 10,000 rows did not change when a later row did.

The page could not show the evaluation of the forecast, where it was used, or what it predicted: each would need its own record.

Part VII ends here. Chapter 33 asks you to build the whole thing on a second platform you have not seen.

Ask three questions:

- Which version of the data did your last training run read?
- Could you rebuild that data from what your tracker recorded?
- What does your digest, or your checksum, read, and what does it leave out?

### How this differs from a real platform

- The forecast is a mean of 3 numbers, made so that there is a run to record. A real training run reads far more rows, and its record holds more: settings, measures of how well it did, and the version of its code.
- The shop's digest follows MLflow's rule, but it is not MLflow's value.
- OpenLineage has no facet for training or evaluation. A dataset's type may be `MODEL`, so the forecast can be named as a dataset a run writes.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 31](chapter_31.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

