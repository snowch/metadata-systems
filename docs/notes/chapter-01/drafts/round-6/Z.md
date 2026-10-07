## roleLabels

Experiment

Inspect

Reference

## roleBadgeLabel

What this figure asks of you is {role}.

## roleNotes

You commit first, to a prediction, a choice or a query you build. Then you act, and the lab's evidence answers. What you take away is what the evidence shows beside what you expected.

This is an instrument: it shows what the platform holds, and answers no question by itself. Use it on the question the page has just asked, and look for the evidence that question needs.

You have what you were told about the platform, kept to hand. It asks nothing of you.

## wCaption

Decide which asset you would inspect first to find where Thursday's total became 51.50, and what you would look for there.

## wQuestion

Thursday's orders in `orders.parquet` add up to 205.50. `daily_sales` and the dashboard both show 51.50. Somewhere between them, the total changed. Which asset would you inspect first to find where, and what would you look for there?

## wOptions

- orders.parquet; for the orders that make up Thursday's 205.50
- clean_orders; to set its Thursday orders beside the raw ones
- daily_sales; for how its 51.50 was worked out
- the dashboard; for where its 51.50 comes from

## wCommit

I'll start here

## wMine

You will start with {choice}.

## wAfter

- `orders.parquet` keeps one row per order, with its price, quantity and status. It shows what Thursday's 205.50 is made of, and not which orders `daily_sales` counts.
- `clean_orders` keeps one row per order too, with the same columns as `orders.parquet`. Set beside it, it shows which orders the two hold differently.
- `daily_sales` keeps one row per day: the day and its revenue. It shows 51.50, and not which orders make it up.
- The dashboard keeps the values it shows, one per day. It shows 51.50, and nothing about orders.

## wNext

The inspector below opens on it. Look there first, then at any other asset.

## inspectorCaption

Inspect what storage records about each asset, starting with the one you chose.

## inspectorLead

The inspector is your instrument for the question above: where could Thursday's difference have entered?

Choose an asset from the list. It shows what storage records about it. That includes its record, what storage says about eight questions, its columns and their types, and its rows.

It asks every asset the same eight questions.

Then try one of these:

- find the rows of `orders.parquet` that make Thursday's total differ from `daily_sales`;
- add up `clean_orders` per day and compare each total with `daily_sales`;
- read which orders `daily_sales` counts and why it counts only those;
- see what the dashboard draws and when it last refreshed.

## p2ExplainEnd

Now there is a difference to explain.

First, where to look: the next section starts there.
