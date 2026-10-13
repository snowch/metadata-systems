[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 31](chapter_31.ipynb)

# Chapter 32: Metadata for ML and AI

**Objectives**

- Record a forecast trained on `daily_sales` with the fields an experiment tracker keeps.
- Find what the run's record can tell you about the rows the forecast was trained on, and what it cannot.
- Test a guess about those rows against the record's digest.
- Question the requirement "Record the training data of the model."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## A forecast and its record

On Saturday 12 at 09:00 the shop trains a forecast of the next day's revenue. The run reads all the rows `daily_sales` holds then, 5, and takes the mean of the last 3 days.

MLflow is an experiment tracker. It records each training run, the data the run read and the model it made.

As in Chapters 29 to 31, MLflow does not run here. Each cell applies MLflow's rules, as its code states them in the version read, to the shop's run.

The next cell lists the record of the run's input, one field on each row. The fields are the ones MLflow keeps for a dataset a run reads: `name`, `digest`, `source`, `schema` and `profile`, with the context `training`. MLflow keeps one more, `source_type`, which the shop's record leaves out.

    >>> week32 = shop.run_week(["returns"])
    >>> shop.ml.record(week32)
      | field | value
      | name | shop.analytics.daily_sales
      | digest | 60ba54ee
      | source | warehouse://shop-warehouse/shop.analytics.daily_sales
      | schema | ["day", "revenue_pence"]
      | profile | {"num_rows": 5}
      | context | training

`source` names where the data is kept: the warehouse table `shop.analytics.daily_sales`. It holds no rows.

The digest is a short fingerprint of the rows. For a table held as a pandas table, MLflow computes it from the first 10,000 rows, the number of rows and the column names, through MD5, and keeps 8 characters.

The shop computes its digest from the same three things. It is the shop's value, not MLflow's, because MLflow reads the rows with a library the shop does not use.

`profile` holds the number of rows: 5.

The forecast is registered as version 1 of the model `next_day_revenue`. The next cell lists the version. Its `run_id` names the run that made it, so the model leads to the run, and the run to the record of its input.

    >>> shop.ml.version(week32)
      | field | value
      | name | next_day_revenue
      | version | 1
      | run_id | 01a094d8-5280-7ec2-8896-f5b5f297e321
      | source | runs:/01a094d8-5280-7ec2-8896-f5b5f297e321/forecast
      | the forecast, in pence | 13650

On Monday 14 at 09:00, Jo Marsh asks which rows the forecast was trained on.

The record holds no rows: a name, where the data is kept, a digest and a count.

Before you read on, write in the next cell whether `daily_sales`, read on Monday 14 at 09:00, will give the digest the run recorded, and what that would tell you.

    [WRITE] Will daily_sales on Monday 14 at 09:00 give the digest the run recorded?
    [WRITE] ........

    >>> shop.ml.today(week32)
      |  | rows | digest
      | the run's record | 5 | 60ba54ee
      | daily_sales on Monday 14 at 09:00 | 7 | 6b0727dc

The record counts 5 rows and holds the digest `60ba54ee`. `daily_sales` has 7 rows and gives the digest `6b0727dc`.

The digests differ, so `daily_sales` has changed since the run.

Compare this with what you wrote.

Each night's run of `build_daily_sales` adds one row, for the day before, and leaves the other rows as they are. So the rows the run read may still be in `daily_sales`.

The record can test that guess: the same rows give the same digest.

The next cell holds `where`, a condition on the rows of `daily_sales`. As it stands, `day <= '2026-09-13'` keeps all 7.

Change the date so that the condition keeps the rows `daily_sales` held on Saturday 12 at 09:00. Select the cell and press **Run below**.

The check below it computes the digest of the rows your condition keeps, and compares it with the run's.

    >>> where = "day <= '2026-09-13'"

    >>> shop.ml.check(week32, where)
      | test | passes
      | Your rows (7) give the digest `6b0727dc`, not the run's `60ba54ee`; the run read 5 rows. | no

With the date of Friday 11, the check passes: 5 rows give the digest `60ba54ee`, the one the run recorded.

A match is strong evidence, not proof: with 8 characters, other rows could give the same digest, though the chance is small.

The match relied on `daily_sales` only gaining rows. Had a row the run read been changed or deleted since, no condition would give the run's digest, and the record could not show which row changed or what it held.

## What a digest reads

The digest reads the first 10,000 rows, the number of rows and the column names. A row added anywhere changes the number of rows, so it changes the digest.

The next cell takes a table of 10,001 rows made for this cell, and changes one value at a time, in place, by 1 penny.

    >>> shop.ml.cap()
      | change | digest
      | none | b54985ab
      | the first row, plus 1 penny | ebf8f1e4
      | row 10001, the last, plus 1 penny | b54985ab

Changing the first row changes the digest, from `b54985ab` to `ebf8f1e4`. Changing row 10,001, the last, leaves it at `b54985ab`.

A value changed in place after row 10,000 leaves the digest as it was: the number of rows, the column names and the first 10,000 rows are all unchanged.

## The training data

[BOX] The head of the shop's requirement: "Record the training data of the model."

Before you read on, write in the next cell what "record the training data" means to you here.

    [WRITE] What does "record the training data" mean here?
    [WRITE] ........

"Record the training data of the model" could mean three things. Each item says what it needs:

- the snapshot the run read: a version or a time of `daily_sales`, and a table that keeps its earlier states, as the table formats in Chapter 2's closing note do;
- the query that chose the rows: its text and when it ran. The run read every row `daily_sales` held at 09:00 on Saturday 12; the same read on Monday 14 gives 7 rows, not 5;
- the features computed from the rows: the code that computed them and the values it gave, here the revenue of the last 3 days.

This record meets none of the three. It names `daily_sales`, and its digest and count show whether the rows are still as the run read them. MLflow can also keep text with a run, such as a query, which this record does not.

The requirement does not say which it means.

## Before Chapter 33

The run's record held a name, a digest and a count, not the rows. The digest showed that `daily_sales` had changed since the run. A guess about the rows could be tested against it because `daily_sales` only gained rows.

A value changed in place after row 10,000 did not change the digest.

The evaluation of the forecast, where it was used and what it predicted would each need its own record, as would embeddings, vector indexes, retrieval and generated artefacts. None of them is shown here.

Part VII ends here. Chapter 33 asks you to build the whole thing on a second platform you have not seen.

Three questions:

- Which version of the data did your last training run read?
- Could you rebuild that data from what your tracker recorded?
- What does your digest, or your checksum, read, and what does it leave out?

### How this differs from a real platform

- The cells apply MLflow's rules as its code states them in the version read.
- The forecast is a mean of 3 numbers, made so that there is a run to record. A real training run reads far more rows, and its record holds more: settings, measures of how well it did, and the version of its code.
- The shop's record keeps fewer fields than MLflow's: it leaves out `source_type`, and holds `schema` and `profile` in a simpler form of its own.
- The shop's digest follows MLflow's rule for a pandas table, but it is not MLflow's value. For a Spark table, MLflow's digest comes from the query plan and reads no rows.
- In OpenLineage, the run's input would be `daily_sales` as an input dataset, as in Chapter 8. OpenLineage's facet for a dataset's version holds the version as free text, with no meaning defined for it.
- OpenLineage has no facet for training or evaluation. Its facet for a dataset's type lists `MODEL` among its examples, so a run could name the forecast as a dataset it writes; the specification does not define what that means.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 31](chapter_31.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

