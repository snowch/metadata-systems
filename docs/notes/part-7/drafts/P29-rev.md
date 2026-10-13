## A

- See the names a real producer, Airflow's OpenLineage provider, would give the shop's nightly jobs.
- Send the week's events, with Part V's faults, through Marquez's rules and through your collector, and compare what each stores.
- Change the order in which the events reach both, and find which differences that removes.
- Question the requirement "Use the reference consumer."

## B

### A real producer

Each real producer follows its own rules for the names, run ids and facets it sends. Each real consumer follows its own rules for what it does with a repeated or a late event.

None of these systems runs on this page. Each cell applies a system's rule, as its code states it at the commit read, to the shop's week.

Airflow runs tasks on a schedule. A Dag is Airflow's name for a set of tasks it runs together. Airflow's OpenLineage provider is a package that sends an OpenLineage event as each task starts and ends.

Suppose the shop's four nightly jobs ran as tasks of one Dag, `shop_nightly`, each task named for its job, and sent their events through the provider, version 2.20.3.

The provider names each task's job `{dag_id}.{task_id}`. It takes the job's namespace from its settings, and uses `default` when none is set.

The next cell lists the shop's four nightly jobs as the shop names them and as the provider would, with the parent the provider gives each.

## C

Every name differs: the namespace is `default`, not `shop`, and the job is `shop_nightly.build_daily_sales`, not `build_daily_sales`.

The shop's lineage would take the provider's four jobs as four new programs. Chapter 12 compared names this way, and Chapter 22 joined two names of one dataset with an alias.

The next cell shows the `START` of the run of `build_daily_sales` early on Friday 11. It is the shop's own event with the provider's names, `producer`, `parent` and `jobType` put in. These differ from the shop's own event:

- `producer` is the provider's address;
- the facet `parent` names the Dag's run, in the job `default/shop_nightly`;
- the facet `jobType` gives `AIRFLOW`, `BATCH` and `TASK`;
- the shop's job facet `sourceCodeLocation`, the version of the job's code, is gone: the provider's own job facets do not include it.

The datasets keep the shop's names. Which datasets a real task reports depends on its operator, so here they are the shop's assumption.

The cell after it runs Chapter 8's check on the event.

## D

The event breaks none of the rules Chapter 8's check tests.

### The reference consumer

OpenLineage's own README calls Marquez "the reference implementation of the OpenLineage API".

Marquez's rules for a run's events, as its code states them:

- it refuses an event with no `eventTime`;
- it stores every event it takes as a row; its table of events has no uniqueness rule, so an event that arrives twice is two rows;
- for each event with a type, it writes a state row and sets the run's current state from that event, in the order it takes the events, without comparing their times;
- `START` gives the state `RUNNING`, `COMPLETE` gives `COMPLETED`, `ABORT` gives `ABORTED` and `FAIL` gives `FAILED`; `RUNNING` and `OTHER`, the specification's other two types, give `RUNNING`, as does any type it does not know;
- `COMPLETE`, `ABORT` or `FAIL` moves the run's end time to the event's own time.

The two cells after the next one send Chapter 25's arrivals, Part V's faults included, to your collector (the shop's versions of your three pieces from Chapter 25) and through Marquez's rules, in the order the events arrived.

The run of `build_daily_sales` early on Friday 11 has a `START` with the event time 02:30:00 and a `COMPLETE` with the event time 02:30:21. The `START` arrived at 02:31:03, after the `COMPLETE`.

Before you read on, write in the next cell which state Marquez's rules give that run once all the week's events have arrived.

## DD

Which state will Marquez's rules give the run early on Friday 11, once all the events have arrived?
........

## E

Friday 11: your collector's state is `COMPLETE`. By Marquez's rules, the state is `RUNNING`. The late `START` was the last of the run's events taken, so it set the state.

Compare this with what you wrote.

Thursday 10: the run's `COMPLETE` was sent again with a new event time, a retry. Your collector dropped the retry and kept the end at 02:30:21. Marquez's rules stored 3 event rows for the run and moved its end to 02:30:52.

Saturday 12: the same `COMPLETE` of `remove_return` arrived twice, a repeat. Your collector stored 2 events for the run; Marquez's rules stored 3 rows.

Over the week, both refused the developer's event with no `eventTime`. Your collector stored 68 events, and Marquez's rules stored 70.

The next cell holds `order`, the order in which the events reach Marquez's rules and your collector: `"arrival"`.

Change it to `"event time"`: a buffer then holds the week's events and sends them sorted by their event time, Chapter 20's rule. Select the cell and press **Run below**.

The check below it tests whether Friday 11's run is in the same state in both.

## F

With `"event time"`, the check passes: the run early on Friday 11 is `COMPLETED` by Marquez's rules and `COMPLETE` in your collector.

The run early on Thursday 10 still ends at 02:30:52 by Marquez's rules: sorting does not drop a retry. Saturday's repeat is still 3 rows.

Putting events in order and dropping retries and repeats are two separate steps.

The buffer here sorted the whole week before sending anything. A real buffer can hold events only for a while, and an event later than that still arrives out of order.

## H

"Use the reference consumer" could mean three things. Each item says what it needs:

- use Marquez, the consumer the OpenLineage project names as its reference implementation: it needs a Marquez to send the events to. By the rules above, the shop would then hold Friday 11's run as `RUNNING` unless the events are sorted first, and a retry would move a run's end;
- use a consumer that does what the OpenLineage specification requires of a consumer: it needs the specification to say what a consumer does with a repeated, late or out-of-order event. It says nothing about these, so it cannot choose between Marquez's rules and your collector;
- check your own consumer against the reference: it needs a rule for which is right where the two differ. For Friday 11's late `START`, the specification does not say what a consumer does.

The requirement does not say which it means.

## Z

### Before Chapter 30

The provider gave the shop's jobs new names in a new namespace, so its events would start new programs in the shop's lineage.

By Marquez's rules, a late `START` left a finished run `RUNNING`, and a retry moved the run's end. Your collector kept `COMPLETE` and the first end time.

Sorting the events by event time fixed the state, not the retry.

Chapter 30 looks at where four systems' metadata comes from: Airflow, Spark, dbt and Trino.

Three questions:

- Which consumer takes your events, and in what order does it apply them?
- What does it do with an event it has taken before?
- Which of your jobs would a new scheduler rename?

### How this differs from a real platform

- The cells apply Marquez's rules as its code states them at commit `180f37b` (12 April 2026, version 0.51.2-SNAPSHOT). Marquez also keeps versions of jobs and datasets, facets and more, which the cells leave out.
- The provider was read from Airflow's main branch, where its version reads 2.20.3; only a release candidate of that version is tagged.
- A real task's events carry more than the event shown: the run facets `airflow` and `processing_engine`, and a `root` inside `parent`. The Dag's own run also sends events, as a job named `shop_nightly`.
- The run ids are the shop's own, made from the values the provider uses.
- In the documents read (Marquez's README, its changelog, its docs and its API description), none says what Marquez does with a repeated, late or out-of-order event. The rules here are its code's.
- The OpenLineage specification asks a producer to send one `START` and one of `COMPLETE`, `ABORT` or `FAIL` for each run. It says nothing about what a consumer does with a repeat or a late event.
