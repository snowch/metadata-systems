## titles.explanation

What each system needs to record

## explanation

Object storage keeps the location, size and last-modified time of every file. The warehouse keeps each table's column names, their types, its row count and the account that owns it. The reporting tool keeps the dashboard title, its values and its last refresh time.

Each system records only what it needs for its own work. The warehouse must know the columns and types to run a query. Object storage must know the file size to serve it. None of them ask: what does this number mean, or who is answerable for it?

The platform is full of questions that the data cannot answer. What does a revenue figure represent? Who wrote the program that computed it? Did last night's work succeed? What does a cancelled order mean? Storage did not need to know. So it did not record the answers. Some systems do keep records you were not shown: the reporting tool keeps the query behind its chart, and something keeps the programs and their timetable. You will see them in later chapters.

## mapCaption

Each question about `daily_sales` sits in one column: where storage records the answer, where the data suggests it, or where only a record kept at the time can answer it.

## mapLead

The lab places each question in one of three columns: storage records it; the data suggests it because a query rebuilds the asset or another asset shows the same numbers; or only a record kept at the time answers it.

The lab finds each place by running storage and trying queries in the query builder, not from a list.

## mapAfter

The middle column shows answers the data hints at. The failure experiment proved it: the evidence can change when an analyst adds a copy, when a program is edited, or when a night's work fails.

## titles.generalisation

Data and the records around it

## generalisation

The right-hand column holds questions no amount of data answers: who is answerable for each asset, what unit a number uses, what rows were deleted.

The middle column holds answers the data suggests. They can be ambiguous. They can be impossible to tell apart. They can be misleading.

Records about assets and about the platform, written down and kept separate from the data itself, are called **metadata**. A platform needs three kinds: what each asset is (its meaning, the units it uses, who is answerable for it); what happened (what programs ran, when they ran, whether they worked); and what was made from what. The rest of this course builds a system that keeps all three, starting with the first records in the next chapter.

## map2Caption

Each question about `daily_sales` with the analyst's copy in storage: the data can now suggest two sources.

## map2Lead

The figure runs the week with the analyst's copy in storage. Look at the middle column for "What is it made from?".

## map2After

With the analyst's copy present, two different queries give the same result. The data cannot tell which one `daily_sales` was built from.
