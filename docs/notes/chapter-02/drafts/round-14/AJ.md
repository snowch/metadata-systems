## promise

You build a small metadata system inside a browser-based data platform

## assumes

The course assumes you can read a short SQL query (a SELECT with a WHERE and a GROUP BY) and that you have used files, database tables and a dashboard. It assumes nothing about metadata or lineage.

## figureCaption

Monday morning's dashboard: revenue per day, 7 to 13 September. Thursday is far lower than the rest. The head of the shop asks why. Chapter 1 starts from that question.

## partsHeading

The course, part by part

## partsLead

The parts come in reading order, and each builds on the last inside the same lab.

## parts

- Why metadata exists: meet a data platform that keeps almost nothing about its data; build its first records; give them a model, then a graph
- Lineage: record what each program makes from what; design the event it emits; meet OpenLineage, an open standard; turn events into a graph
- Deeper lineage: trace columns to their sources; follow a table's changing columns; decide when two names are one asset; record what programs leave behind
- Metadata becomes operational: use the records to check data quality, trace numbers back to rows, say what changes would break, and find where faults entered
- When the simple model breaks: handle events that go missing, repeat, arrive late or contradict each other, and scale the records up to millions of assets
- Building a metadata platform: build the store, the collector, the graph of relations, the query layer and the interface, each against tests
- Real systems: study OpenLineage in practice, see where Airflow, Spark, dbt and Trino get their records, and compare OpenMetadata, DataHub, Apache Atlas and Marquez
- The complete system: take a second, unfamiliar platform and do all of the course's work on it

## partChapters

- one: Chapter {from}
- other: Chapters {from} to {to}

## partCount

- some: {written} of the part's {total} chapters are written and can be read
- none: none of the part's {total} chapters is written yet
