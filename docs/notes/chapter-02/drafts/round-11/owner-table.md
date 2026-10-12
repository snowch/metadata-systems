## O1

The shop's requirement begins with the words "Every table must have an owner." The owner the warehouse records shows how far that requirement goes. "Who should I ask about `daily_sales`?" wants a person or a team. The cell below lists the owner of every table in the warehouse.

## O2

The warehouse records `etl_service` as the owner of all three tables, in the column `table_owner` of `information_schema.tables`. The name looks like an account a program logs in as, and the warehouse records nothing more about it.

| What the requirement could mean | What it needs | Does `etl_service` answer it? |
| --- | --- | --- |
| who is responsible for the table | a person | no |
| which team is responsible for it | a team | no |
| which job writes it | a program | no: it names an account, not a program |
| which account controls it in the warehouse | an account | yes |

"Who should I ask about `daily_sales`?" needs the first or the second reading. The requirement as written is met only by the fourth: every table has an owner, and the owner is an account.
