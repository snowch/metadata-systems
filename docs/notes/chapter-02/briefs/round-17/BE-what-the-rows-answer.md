# Brief BE: what the rows can and cannot answer

The paragraph under the four questions in "Questions the platform cannot answer" reads awkwardly
(the author): "The rows answer part of the first question: whether the total differs. The full
answers come from what happened, or from a decision that someone made: a job that reads a file, a
rule that a person chose, a person who took responsibility. The rows a table holds today hold
neither." Its list mixes kinds of thing, does not say which answers which question, and "hold
neither" points back at two vague nouns.

Write one paragraph of two or three short sentences that replaces it. Follow `docs/style.md` and
`AGENTS.md`. British English. No em dashes. The reader is "you", a data engineer. Keep names in
backticks exactly as written. Do not use the words "metadata", "lineage" or "event", and never use
"run" as a noun.

## The four questions, just above the paragraph

- Is Thursday's total wrong, and since when?
- Can we delete `products.csv`? Does anything still read it?
- If the checkout renames a column in `orders.jsonl`, what stops working?
- Who should I ask about `daily_sales`?

## Facts

1. The rows can show one thing: whether Thursday's total differs from Thursday's orders.
2. The other answers depend on what the jobs do (which files they read, which rules they apply) and
   on what people decided and took on (who is responsible for `daily_sales`).
3. The rows a table holds today record none of that.

Say which kind of answer each question needs, concretely, in the order of the questions. No
abstract nouns standing in for the answers ("what happened", "a decision"), no "somebody" or
"someone", and no sentence that sums up.

## Slot

- **rows_answer**: the paragraph.
