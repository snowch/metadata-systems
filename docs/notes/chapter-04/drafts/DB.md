## A

## A fact the model has no type for

After the merge, the check still refuses this line:

`dataset clean_orders drops: orders with no customer id, and orders with a quantity of 0 or less`

The model gives a dataset no attribute called `drops`. The line is the rule that explains Thursday's low revenue in Chapter 2. The model has no place for it.

You have two choices.

- Leave the model as it is. The check keeps refusing the fact. Anyone who keeps the records to the model loses it.
- Add the line `dataset drops: text` to the model. The check accepts it, as text. Then any dataset can have any text about what it drops. No check can say whether that text is true, or whether the job that writes the table applies that rule.

A model decides which facts the records can hold, and which of those a check can test.

A fact about how an asset is made, such as this one, gets a place of its own in Chapter 6.

## B

## "Each asset has one owner."

The head of the shop's requirement, "Each asset has one owner.", could mean three things, each needing something different in the records:

- **One person to ask about each asset.** The records need `responsible`, a line that names a person, with one value per asset.
- **One team that answers for each asset.** The records need a team for each asset, named directly or as the team of the person named.
- **One owner, however the records spell the owner's name.** The records need identifiers, so that two spellings of one person count once.

In the cell below, write which reading you would require in the shop's place, and why. No reading is marked right or wrong.

## C

Which reading would you require in the shop's place?
........
Why would you require that reading?
........

## D

The next cell reads the records after your two changes and makes the data engineer a team with the identifier `data_engineering`. Then it lists every asset, the values of its `responsible` lines, and a `yes` or `no` for each reading: `one_owner`, `one_person` and `one_team`.

## E

Of the 7 assets, 5 have one owner under `one_owner`: every asset except `orders.jsonl` and `customers.jsonl`. Those two are the files the export writes, and the records do not say who is responsible for them.

Three assets have one person under `one_person`: `products.csv`, with `s.lund`, and `daily_sales` and `sales_dashboard`, both with `j.marsh`. The two cleaned tables name a team.

Five assets have one team under `one_team`: every asset with an owner.

No reading is wrong. The requirement does not say which one it means. Any list meets some readings and not others, so the list should say which ones it meets.

## F

## Before Chapter 5

With a type on each line and an identifier for each person, the records can count people instead of spellings. A check can also find a value that names nothing the records describe. The check rejected the line about what `clean_orders` drops, because the model had no attribute for it. The requirement is met under some readings and not others, and the two files the export writes have no owner under any reading.

The checks could not show whether a record is true. The model checks the form of a value, and whether the value names a known entity. It does not check whether Jo Marsh is really responsible.

The records now point from one entity to another: a dataset to a person, and a person to a team. Chapter 5 follows those references from one entity to the next.

- Take a platform you work on. Which of the three readings of "Each asset has one owner" does its owner field meet, and what would it need in order to meet the others?
- Which record on that platform could a check accept while the record is false? What would a check need in order to test it?
- A person leaves, and their login is given to someone else. Which records would then name the wrong person, and how would you find out?

## G

### How this differs from a real platform

The shop, its people, its staff list and its data are invented for the course.

The record notation and the model notation are the course's own. Real metadata systems each define their own types and attributes. Chapter 31 compares some of them.

The shop uses staff logins as identifiers for people. A login can change, or be given to someone else after a person leaves. The shop's staff list does not record when.
