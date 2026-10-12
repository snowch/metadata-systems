# Brief: Chapter 2, the first sentence of "What each system records about assets, and why"

Read `docs/style.md` first; its rules hold. The current sentence, "Each system records what it does
about an asset because its own work needs it.", is ambiguous: "what it does" reads as the system's
activity, when it means the things the system records.

## Facts

- Each of the shop's systems records about an asset the things its own work needs, and records them
  because its work needs them.
- The sentences that follow give the examples (the warehouse keeps column names and types so that it
  can run a query; object storage keeps a file's key so that it can serve the file; the reporting
  tool keeps the values so that it can draw the chart), and then: "In the shop's platform, a system
  records what its own work needs and nothing more." So the new sentence must not say "and nothing
  more", which comes later.
- One sentence. No "metadata", no "field", no "what it does".

## Output

Write the file `docs/notes/chapter-02/drafts/round-13/first-sentence.md` holding only the sentence.
