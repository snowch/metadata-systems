# Brief FC: the messages the comparison with code prints (Chapter 6)

A cell compares the lines that record what each job reads and writes with the job's code, and
prints one row per difference, with the job, the line it concerns, and a column `problem` holding one
of the messages below. Each is one short sentence in plain British English, with no em dashes, no
"error", "invalid" or exclamation marks, nothing that makes the comparison sound like a person.
Words: a "line" is one line of the records; a job's "code" is its file in the repository; "reads"
and "writes" are the attributes. Do not use lineage, run (as a noun), event, lab, engine.

Write the file once. Do not change it after you reply.

## Messages

1. **none**: printed in place of the table when every line agrees with the code and the code reads
   and writes nothing that no line records.
2. **no_code**: lines name a job that has no code in the repository.
3. **not_in_code_reads**: a line says the job reads something; the job's code does not read it.
4. **not_in_code_writes**: a line says the job writes something; the job's code does not write it.
5. **not_said_reads**: the job's code reads something; no line says so.
6. **not_said_writes**: the job's code writes something; no line says so.

Write each under `## 1` to `## 6`, as the exact text.
