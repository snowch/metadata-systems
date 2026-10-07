## prediction

Before you open storage, answer two questions.

The first gives you a requirement the shop has set. It asks what you would store to meet it. Then it shows what the requirement could mean and what the shop's warehouse holds.

The second asks what you expect the data to show. Each of its options is an explanation of how the platform works, and the lab checks it.

For each, choose an option, then press the button below it.

## p1Caption

Choose what you would store to meet a requirement, see what it could mean, then see what the shop's warehouse holds.

## requirementLabel

Requirement

## p1Question

Suppose you write the program that writes `daily_sales` every night. What would you store as the owner of `daily_sales`?

## p1Undecided

nothing yet; ask what the owner is for

## p1Commit

Show what this means

## p1MineUndecided

You would ask what the owner is for before storing anything.

## p1Meanings

Each of the four choices meets the requirement as written. Each puts an owner on the table and answers a different question about `daily_sales`. The requirement does not say which question the owner must answer, so it does not say which to store.

## p1Asks

- person: Who is responsible for `daily_sales`?
- team: Which team is responsible for `daily_sales`?
- program: Which program writes `daily_sales`?
- account: Which account controls `daily_sales` in the warehouse?

## p1Short

- person: a person
- team: a team
- program: the program that writes it
- account: an account that programs log in as

## p1Headings

- asks: the question the owner would answer
- store: what you would store for it
- answers: whether the warehouse's owner answers it

## p1Lab

The warehouse records `{value}` as the owner of `daily_sales` and an owner for {owned} of its {tables} tables.

## p1Explain

The warehouse records `etl_service` as the owner of all three tables. `etl_service` is the account all four of the shop's programs log in as. The lab tells you this; storage does not.

Every table has an owner, so the warehouse meets the requirement as written.

The warehouse defines "owner" as the account that controls the table. Of the four questions in the table above, `etl_service` answers only the last.

The requirement did not say which meaning it wanted. The name of a field does not say which question the field answers.

"Who should I ask about `daily_sales`?" is one of the questions at the start of this chapter. It needs a person or a team. The warehouse's owner names neither.

Before you decide what to store, ask whoever set the requirement what the owner is for.

## modelVsRealityOwner

In a real database, a table's owner is an account too. In PostgreSQL, for example, a new table's owner is normally the account that created it. Only the owner (or a superuser) may change or drop the table or let other accounts use it. The lab's warehouse records the owning account and models no such rights.
