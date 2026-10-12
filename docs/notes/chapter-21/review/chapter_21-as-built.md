[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 20](chapter_20.ipynb) · [Next: Chapter 22](chapter_22.ipynb)

# Chapter 21: Conflicting metadata

**Objectives**

- Read what three sources claim about one table, and when each claim was sent.
- Find why "the newest claim wins" shows a claim that nobody has changed for weeks.
- Try three other rules for choosing, and keep track of where each claim came from.
- Question the requirement "Show the correct owner."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

    <<CODE>> mo.Html(figures.figure(figures.pipeline(shop.run_week(["returns"]), "jobs nightly; functions at any hour"), "The shop's three systems with the returns desk on Monday morning: object storage holds three return files, and the warehouse holds the table `returns`."))

## Three sources

The shop's metadata system takes what other systems hold about `daily_sales` from three sources.

- The warehouse: its catalogue, read every night at 03:30. Its owner is the account that created the table, `etl_service` (Chapter 2). Its columns are the table's columns.
- Your records (Chapters 3 and 4), sent when they change. You last changed them on Monday 14 at 16:40, and they name `j.marsh` as responsible.
- The team sheet: a spreadsheet of owners and columns that the engineer who built the platform wrote before the shop opened. Nobody has edited it since 28 August. It is imported every night at 04:00, and each import sends every row again.

Each source's statement about one attribute is a claim. Each claim keeps two times: when it was sent (`sent`), and when its source's content last changed (`as of`).

The next cell lists the claims the shop's metadata system holds at 18:00 on Monday 14.

    <<CODE>> held = shop.claims.claims("2026-09-14T18:00:00Z")
    held

There are five claims. Three are about the owner: `etl_service`, `j.marsh` and `data team`. Two are about the columns: `day, revenue_pence` from the warehouse, and `day, revenue` from the team sheet.

The team sheet's claims were sent at 04:00 on Monday 14, and are as of 28 August.

One rule for choosing: the claim sent most recently wins. The next cell shows its choice.

    <<CODE>> shop.claims.resolve(held, "newest")

At 18:00 on Monday 14, the owner is `j.marsh`, from your records, sent at 16:40. The columns are `day, revenue`, from the team sheet: its import at 04:00 is newer than the warehouse's read at 03:30. `daily_sales` has no column `revenue`.

Overnight, the warehouse's catalogue is read again at 03:30, and the team sheet is imported again at 04:00. Nobody changes anything.

Before you read on, write in the next cell what this rule will show as the owner at 09:00 on Tuesday 15.

    <<CODE>> expected_tuesday = """
    What owner will the rule show on Tuesday at 09:00?
    ........
    """

    <<CODE>> tuesday = shop.claims.claims("2026-09-15T09:00:00Z")
    shop.claims.resolve(tuesday, "newest")

At 09:00 on Tuesday 15, the owner is `data team`, from the team sheet. Its import at 04:00 is now the most recent claim. The columns are still `day, revenue`.

The rule took the claim sent last. The team sheet's content is the oldest of the three: 28 August.

Compare this with what you wrote.

When sources disagree, the rule for which claim counts is called **precedence**.

## Other rules

Change `"newest"` to `"as of"` in the cell, select it and press **Run below**. The claim whose source changed most recently wins: the owner is `etl_service` and the columns are `day, revenue_pence`, both from the warehouse. The warehouse's content changes every night, at 02:30:21, when the night's work writes `daily_sales`. The warehouse's owner does not change.

Change it to `"ranked"` and press **Run below**. Each attribute has its own order of sources. For the owner, your records come first, then the team sheet, then the warehouse. For the columns, the warehouse comes first. The owner is `j.marsh` and the columns are `day, revenue_pence`.

Change it to `"all"` and press **Run below**. Every claim is kept, with its source and its two times: five rows.

`ranked` is the shop's own choice of order. It holds only while each source keeps the role the shop gave it.

## The correct owner

[BOX] The head of the shop's requirement: "Show the correct owner."

Before you read on, write in the next cell what "correct" means to you here, and which owner you would show.

    <<CODE>> what_correct_means = """
    What does "correct" mean here?
    ........
    
    Which owner would you show?
    ........
    """

"Correct" could mean three things, each needing something different.

- the newest claim: the time each claim was sent;
- the claim from the source trusted most for owners: an order of sources for each attribute;
- every claim, with where it came from: all of them kept, with their sources and times.

On Tuesday at 09:00, the three give, in that order: `data team`; `j.marsh`; all three owners.

"Owner" is the word Chapter 2 used. The word can mean a person responsible, a team, or the account that controls the table. `j.marsh` names a person, `data team` a team, and `etl_service` an account. A rule that keeps one claim also keeps one meaning.

The requirement does not say which one it means.

## Before Chapter 22

Three sources made five claims about `daily_sales`. The newest claim was the most recently sent, so a nightly import of an unchanged sheet replaced the owner and kept a column the table does not have. Ordering by the time a source last changed gave the warehouse's account, because its content changes every night. An order of sources for each attribute gave `j.marsh` and the warehouse's columns. Keeping every claim with its source left the choice to you.

Chapter 22 asks when references from different systems name the same asset.

- Which of your platform's sources resend everything on a schedule?
- Which source would you trust for an owner, and which for a schema?
- Where does your metadata system record where each value came from?

### How this differs from a real platform

- The shop's sources, their times and the team sheet are invented for the course.
- The shop keeps the latest claim of each source for each attribute. A real system may keep every claim it has received, with its history.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 20](chapter_20.ipynb) · [Next: Chapter 22](chapter_22.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

