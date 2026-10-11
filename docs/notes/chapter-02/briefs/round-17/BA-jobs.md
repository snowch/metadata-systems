# Brief BA: "jobs", where the chapters said "programs"

The author found "programs" is not the word a data engineer uses for the things that run on a data
platform each night. The word is now **job**. Chapters 1 and 2 use it as the everyday word: what
runs each night, reads some data and writes some. Chapter 6 later makes it precise.

Rewrite each numbered string below so it says "job" (or "jobs") where it says "program" (or
"programs"). Follow `docs/style.md` and `AGENTS.md`. British English. No em dashes.

## Facts and rules

- Change only what the new word needs: an article ("a job", "the job"), a verb's agreement, a
  word order that reads badly with "job". Every other word stays as it is.
- Never use "run" as a noun ("a job's run", "the run"): that word belongs to a later chapter.
  "Run" as a verb is fine ("when they are due to run").
- The four nightly jobs are: clean customers, clean orders, daily sales, and the dashboard
  refresh. They all log in to the warehouse as `etl_service`.
- Strings 15 and 16 are labels in a menu, not sentences: keep them short, with no full stop.
- String 17 is a label drawn between two systems on a diagram: keep it short and lower case.
- Keep names in backticks exactly as they are.

## Strings

1. - Say what happens on the platform each night, and what you cannot see of it: the programs, when they are due to run, and any notes.
2. Every night, programs read the files, write the tables and refresh the dashboard.
3. You cannot see the programs, when they are due to run, or any note anybody kept.
4. Each night, in the early hours of the next day, the three files are written again, then programs write the tables and refresh the dashboard.
5. Each is answered by something that happened, or by a decision somebody made: a program that reads a file, a rule somebody chose, a person who took responsibility.
6. The platform holds both sets of numbers and nothing that connects them: no record of which orders `daily_sales` counts, which program decided that, or why.
7. No field describes how it got that way: which program wrote it, what it read, what its rows were yesterday, or who decided its rules.
8. The warehouse answers `etl_service`, the account that all four of the shop's programs log in as.
9. None of the platform's records says which of the two the program reads.
10. The program that writes `daily_sales` is edited, from Saturday's row on, to keep every order that has not been refunded.
11. On the last night the program that writes `daily_sales` fails and writes nothing.
12. The last rule is in the program.
13. No order in the week has a quantity of 0 or less, so the rule never removes a row, and a version of the program without it would have produced the same table.
14. A note of what a program read, written the next morning from the data, is a reconstruction, with the limits shown above.
15. From Saturday, the daily_sales program keeps unrefunded orders
16. The daily_sales program fails on the last night
17. unseen programs move data each night
