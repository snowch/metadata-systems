## hCaption

Choose the explanation you will test for the difference on Thursday.

## hQuestion

Thursday's `orders.parquet` rows add up to 205.50, but `daily_sales` holds 51.50. Which explanation will you test?

## hOptions

- left: some of Thursday's orders are not counted in daily_sales
- lower: Thursday's orders are counted, but at lower values
- moved: some of Thursday's orders are counted on another day

## hCommit

Test this explanation

## hMine

You will test {choice}.

## hTest

Read Thursday's rows in the inspector below. In the next section, the query builder adds up an asset's rows and compares each day with `daily_sales`. Once your query rebuilds `daily_sales`, a check at the end of that section reads the rows and says which explanations they support.

## inspectorFirstTask

Test the explanation you chose; find the rows of `orders.parquet` that make Thursday's total differ from `daily_sales`.

## cCaption

Check the explanation you chose against Thursday's rows.

## cMine

You chose to test {choice}.

## cNone

You did not choose an explanation to test.

## cButton

Read Thursday's rows and show which explanations they support

## cHeadings

- explanation: The explanation
- supported: Whether Thursday's rows support it

## cLab

Of Thursday's {orders} orders in `orders.parquet`, {kept} are among the rows your query keeps, each at the same price and quantity and on the same day. The other {left} are not, and together they are worth {leftTotal}, the whole difference.

## cExplain

The rows support one explanation. Some of Thursday's orders are not counted.

They rule out the other two. No order is counted at a lower value, and none on another day.

If you chose another explanation, the rows have ruled it out. The first explanation you test need not be the right one.

The rows do not say why those orders were left out. Ask: what do they have in common?

The challenge at the end of this chapter asks which rows the cleaning keeps.

## reflectionThursday

Back to Thursday. The three orders your check found left out are the three with no customer id. Every setting of the rules that passes drops orders with no customer id.
