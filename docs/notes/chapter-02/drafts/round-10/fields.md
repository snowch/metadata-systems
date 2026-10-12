## E

Everything the three systems showed describes each asset as it is this morning. None of it describes how the asset got that way: which job wrote it, what it read, what its rows were yesterday, or who decided its rules. The platform records the current state of each asset and none of its history.

## H

## Why each system records what it does about an asset

## P

Each system records what it does about an asset because its own work needs it. The warehouse keeps column names and types so that it can run a query. Object storage keeps a file's key so that it can serve the file. The reporting tool keeps the values so that it can draw the chart. In the shop's platform, a system records what its own work needs and nothing more. The questions you want answered are not its work.

## O

The warehouse's owner shows how far that goes. "Who should I ask about `daily_sales`?" wants a person or a team. The requirement is: "Every table must have an owner." The warehouse records `etl_service` as the owner of all three tables, in the column `table_owner` of `information_schema.tables`. The name looks like an account a program logs in as, and the warehouse records nothing more about it. The column is called `table_owner`, but the question it answers is which account controls the table. The requirement is met as written, and your question is not.
