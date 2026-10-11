1. Say what happens on the platform each night, and what you cannot see of it: the jobs, when they are due to run, and any notes.
2. Every night, jobs read the files, write the tables and refresh the dashboard.
3. You cannot see the jobs, when they are due to run, or any note anybody kept.
4. Each night, in the early hours of the next day, the three files are written again, then jobs write the tables and refresh the dashboard.
5. Each is answered by something that happened, or by a decision somebody made: a job that reads a file, a rule somebody chose, a person who took responsibility.
6. The platform holds both sets of numbers and nothing that connects them: no record of which orders `daily_sales` counts, which job decided that, or why.
7. No field describes how it got that way: which job wrote it, what it read, what its rows were yesterday, or who decided its rules.
8. The warehouse answers `etl_service`, the account that all four of the shop's jobs log in as.
9. None of the platform's records says which of the two the job reads.
10. The job that writes `daily_sales` is edited, from Saturday's row on, to keep every order that has not been refunded.
11. On the last night the job that writes `daily_sales` fails and writes nothing.
12. The last rule is in the job.
13. No order in the week has a quantity of 0 or less, so the rule never removes a row, and a version of the job without it would have produced the same table.
14. A note of what a job read, written the next morning from the data, is a reconstruction, with the limits shown above.
15. From Saturday, the daily_sales job keeps unrefunded orders
16. The daily_sales job fails on the last night
17. unseen jobs move data each night
