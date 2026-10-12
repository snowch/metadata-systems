REVIEW OF CHAPTER 5, "Metadata as a graph" (first read, 12 October 2026)

I read it as a learner who has done Chapters 1 to 4. Findings are ranked, most serious first. Each is marked blocking or minor. Quotes are exact. No finding contains an exercise's answer.

BLOCKING

1. The opening continuity is wrong, and "Before anything changes" points at nothing.
   - Where: "Jo Marsh's question", paragraph 1.
   - Quote: "Jo Marsh, in finance, replies to the list of owners you sent at the end of Chapter 4. Jo wants daily revenue to count orders that have no customer id. Jo's meaning of a day's revenue already says so (Chapter 3). Before anything changes, Jo asks:"
   - Problem:
     - Chapter 4's requirement came from the head of the shop ("Each asset has one owner. Send me the list."). The reader only wrote, in a free-text cell, what they would send the head. Nothing was sent, and Jo was not the recipient.
     - "Before anything changes" promises a change that never comes in this chapter.
     - "Jo wants" and "Jo's meaning already says so" say the same thing twice.
     - Chapter 3 does support "already says so": Jo's meaning gave 20550 for Thursday against 5150 in the table. But the new "Jo wants" adds nothing the reader did not already know.
   - Direction: make the first sentence true of Chapter 4 (a reply from the head, or Jo writing separately). Say what Jo is trying to do, or cut the clause. Drop "Before anything changes".

2. The page does not use Jo's purpose, and it never pays off the reader's own commitment.
   - Where: the whole chapter, especially the requirement section and "Before Chapter 6".
   - Quotes: "Jo wants daily revenue to count orders that have no customer id." and "What would you send Jo Marsh?"
   - Problem:
     - The opening gives the reason for the request, which is the best evidence for which "related" Jo meant. The requirement section never returns to it. Chapter 3 told the reader that `clean_orders` drops those orders, and the chapter never says which reading of "related" would let Jo find where they go. The reader's "What would you send Jo Marsh?" is never answered. Chapter 4's version ended with "A list you send should say which reading it meets, and for which assets." Chapter 5 has no such ending. The "question the requirement" structure (commit, readings, what the platform records, which readings it meets) stops before the last step.
     - The reader also cannot tell what to send Jo now, or which readings the graph does and does not meet for Jo's purpose.
   - Direction: after the readings, connect them to Jo's stated purpose. Say what the reader could honestly send Jo (the responsible person and team, the columns, and that "made from" and "read by" cannot be answered). Make clear which reading would serve a person asking about orders with no customer id. This does not mark any reading wrong.

3. "The records as Chapter 4 left them" is false.
   - Where: the paragraph before the records cell, and the `#` comment in the cell.
   - Quotes: "The records cell holds the records as Chapter 4 left them, with the two spellings merged into `j.marsh` and `s.lund`, and the data engineer as a team with the identifier `data_engineering`." and "# The records as Chapter 4 left them: two spellings merged, the data engineer a team".
   - Problem:
     - Chapter 4's records held `dataset clean_orders drops: orders with no customer id`. Chapter 5's cell silently omits it. That line is the only record of the rule behind Jo's concern. Chapter 4 left it refused by the check, or accepted if the reader added `drops` to the model.
     - Chapter 4 let the reader choose team or person for the data engineer. Chapter 5 fixes it as a team without saying the choice has been made for them. The sentence does say "as a team", so the choice is disclosed, but not as a choice.
     - A reader who made the model accept `drops` in Chapter 4 will not find that line here.
   - Direction: either keep the `drops` line (the model then needs the attribute, and the graph is unchanged because the value is text), or say plainly that it is left out and why. Say the data engineer's type is the shop's choice here, as in Chapter 4's default.

4. The page contradicts itself about the readings and about what the graph answers.
   - Where: "Show everything related to `daily_sales`."
   - Quotes: "It could mean four things. Each needs a different kind of edge:", then "what reads `daily_sales`: the same kind of edge, the other way;", then "The graph holds the third reading, who is responsible." and "Following every edge answers none of the four readings, because it mixes owners, teams and columns."
   - Problem:
     - Reading 2 needs the same kind of edge as reading 1, so "each needs a different kind" is false.
     - "The graph holds the third reading" and "answers none of the four" conflict. The all-edges result from `daily_sales` does contain the responsible person and the team. It also contains the dashboard and the columns, so it fails to answer cleanly. The flat "none" overstates.
   - Direction: say that the all-edges walk contains the answer to reading three mixed with other nodes. Fix "each needs a different kind".

5. The closing generalisation is wider than the evidence.
   - Where: after the `clean_customers` traversal, and in "Before Chapter 6".
   - Quotes: "Following every edge returns what shares an owner with the start, here `clean_customers`." and "Following every edge, both ways, returned the assets that share an owner with the start."
   - Problem:
     - The `daily_sales` result is not "assets that share an owner". It is the owner, the owner's team, two columns and a dashboard, and only the dashboard shares an owner.
     - From a column or a person, the same walk would return different kinds of node.
     - "Owner" is also a word Chapter 4 split carefully (the head's "owner" against `responsible`, a person against a team), and here it stands for `responsible`.
     - "A reader asking for everything related could take that result for what `clean_customers` is made from." That reader is hypothetical. No one in the chapter claimed it.
   - Direction: state what the two results showed (the nodes joined by `responsible` to the same node), not a rule for all starts. Use "responsible" rather than "owner". Drop or replace the hypothetical reader.

6. Both predictions can be read off what sits directly above them, and the second also asks for a cause with the effect.
   - Where: "The next cell draws the graph" with its alt text, then "Following edges".
   - Quotes: the drawing's alt text, "The drawing has 3 parts: daily_sales, its 2 columns and sales_dashboard, joined through j.marsh and finance; ...", then "Which nodes will graph.traverse("daily_sales") reach, and why is each one reached?"
   - Problem:
     - The alt text (and the drawing) names exactly the five nodes the second prediction asks for. The first prediction is answered by the prose plus the arrows. The notes admit "Predictable: yes, from the drawing."
     - A text label is given before the prediction, which breaks "no caption, label or text gives away a prediction's answer".
     - The second cell asks "which" and "why" at once. The cause for the dashboard is requested before the reader has the result that shows it. The belief worth testing is "a dashboard that reads the table will show up", and the reader never has to commit to it.
   - Direction:
     - Keep the alt text to what the drawing shows (the type layers, the count of parts) without listing which nodes are joined.
     - Ask first which nodes. Then, after the result, ask why the dashboard is there, or move the "why" to after the table.
     - Consider a prediction that can be wrong, for example whether the dashboard will appear, or what a walk from `j.marsh` reaches.

7. The chapter's central claim is asserted, not shown, and "You choose" is false of the page.
   - Where: "Following edges" and the closing.
   - Quotes: "You choose which kinds of edge it follows, and the direction for each.", "Which nodes come back depends on the kinds of edge followed, and on the direction each is followed in." and "A traversal answers a question only when it follows the edges that the question means."
   - Problem:
     - The reader never chooses anything. All three traversals are fixed, and the notes confirm no cell is meant to change. Only the first uses `out`; `"in"` is never run anywhere.
     - So "depends on the direction" is told, not shown. This is the chapter's main lesson.
     - The loop (predict, build, run, inspect, explain, change, run again) has no build or change step.
     - The objective "Turn the records into connections" is done by `shop.graph`, not by the reader.
     - A reader who wants to see direction matter must invent the experiment.
   - Direction:
     - Invite one or two edits to the traversal cell, for example following `responsible` the other way from `j.marsh`, or only `of`. Ask what comes back before it runs.
     - That would show direction mattering and show a question answered by the right kinds of edge.
     - Also say how the reader asks (edit the dictionary, press **Run below**), and that the dictionary maps an edge label to a direction.

8. Reading 1 sets out the data model Chapter 6 reverses, and a closing question is answered by the page.
   - Where: the four readings, and "Before Chapter 6".
   - Quotes: "what `daily_sales` is made from: an edge between datasets, from `daily_sales` to whatever makes it;" and "What would a record have to say for a graph to show that one dataset is made from another?"
   - Problem:
     - The plan says Chapter 6 gets there through jobs: "records what each job reads and writes". The graph has job nodes, with `reads` and `writes`, not dataset-to-dataset edges. The page states as a need something the course then does differently.
     - The third closing question is answered by reading 1 in the same chapter.
   - Direction: state the need without choosing the shape of the edge (a record that says what produced `daily_sales` and from what). Leave the final question open.

MINOR

9. One idea has several names, and "owner" slips back in.
   - Where: objectives, "The records as a graph", edge table.
   - Quotes: objectives "Turn the records into connections", "carries the line's attribute as its label", the edge table's header `edge` (it holds the label), "A traversal given no kinds", "a team ... the team responsible", "share an owner".
   - Problem: connection, edge, label, attribute and kind all appear for related things. "Edge" is both a link and the column header for its label. "Owner" and "the list of owners" return after Chapter 4 separated the head's "owner" from `responsible`.
   - Direction: pick one word for the label (attribute, as in the records) and one for "kinds". Use "edges" instead of "connections" in the objectives. Say "responsible" or "responsible person", not "owner". The edge column's name is a design choice for the course to change in the engine.

10. The path notation and the dictionary argument are not explained.
    - Where: "Following edges".
    - Quotes: "daily_sales -responsible-> j.marsh <-responsible- sales_dashboard" and "the number of edges it walked".
    - Problem:
      - `<-label-` is never explained. It first appears in the second result, so a reader must infer that the arrow shows the direction the edge was walked relative to its own arrow.
      - The `steps` column is introduced as "the number of edges it walked".
      - The first dictionary `{"responsible": "out", "team": "out"}` is never explained as label-to-direction.
      - "The path it took" is the shortest path found. This data never has two, but the claim is general.
    - Direction: one sentence on the notation where it first matters, and one on the dictionary.

11. Prose repeats what the table shows.
    - Where: several places.
    - Quotes: "There are 12: 4 datasets (`daily_sales`, `clean_customers`, `clean_orders`, `products.csv`), 2 columns, the dashboard, 2 people and 3 teams.", "The traversal reaches `j.marsh` by 1 edge and `finance` by 2 edges. `j.marsh` is who is responsible for `daily_sales`, and `finance` is that person's team." and "The traversal reaches 5 nodes: `j.marsh`, the 2 columns, `sales_dashboard` and `finance`."
    - Problem: each sentence restates the output just above, so the reader would not miss it. The node breakdown is correct (4+2+1+2+3 = 12), but the table already shows it.
    - Direction: keep the count and the non-obvious fact (`orders.jsonl` and `customers.jsonl` are not nodes). Cut the lists that duplicate the table.

12. Some phrasing is awkward or loose.
    - Quotes:
      - "It draws each part of the graph that edges join on its own." (unclear, and "parts" is not defined)
      - "Walking from one node along its edges, from node to node, is a **traversal**." (repeats "node")
      - "A traversal answers a question only when it follows the edges that the question means." (the question "means")
      - "Which nodes come back depends on ..."
      - "The cell reaches `data_engineering`, then `clean_orders`, which it reaches through the team responsible for both."
    - Direction: use plain nouns, for example "each group of nodes joined by edges is drawn on its own" and "the edges the question needs".

13. The model's role in building the graph is not stated.
    - Where: "The records as a graph".
    - Quote: "Each line whose value is the identifier of another entity becomes an edge."
    - Problem:
      - The engine decides this from the model, not from the value alone. An attribute the model types as text is never an edge, and a value naming no entity makes none.
      - `shop.graph(records, model)` takes the model without the page saying why.
      - Identifiers are also unique across types in the engine: it raises an error if one name belongs to two nodes. That is a shop choice, unstated.
    - Direction: one sentence that the model says which attributes name entities. Mention the uniqueness choice in the closing note.

14. The "How this differs from a real platform" note says nothing about real platforms.
    - Where: final section.
    - Quote: "The shop, its people and its data are invented for the course. The notation, the model and the traversals are the course's own. The graph is made from the records each time the cell runs."
    - Problem: it is mostly about the repository. CLAUDE.md asks the note to say where the shop's platform differs from a real one. Examples of such differences: how real catalogues store relationships, edges with their own properties, several paths between two nodes where the shop shows one, and the shop deriving every edge from one attribute type.
    - Direction: say what a real system differs in, checked against `docs/sources.md`, or say the course makes no comparison here.

15. The platform figure and its caption do no work in this chapter.
    - Where: after "Jo Marsh's question".
    - Quotes: "The three systems, in the order data moves through them each night." and "The shop's three systems and what each holds."
    - Problem: the sentence is a fragment. The chapter never uses the systems. The notes give the figure's role as "Jo's question is about one of them", but nothing on the page connects the two. (I cannot see the figure.)
    - Direction: tie it to one thing the reader needs (where `daily_sales` sits), or drop the figure's introduction here.

16. Names are inconsistent between prose and tables.
    - Where: prose against the nodes, edges and drawing.
    - Problem: the prose says `products.csv` while the node and edge tables show `s3://shop-raw/products.csv`. The first mention does not say which is meant.
    - Direction: say once that `products.csv` is short for the key.

17. The record line numbers skip without explanation.
    - Where: the records output.
    - Quote: "18 | team | data_engineering ... 20 | column | daily_sales.day | of | daily_sales".
    - Problem: lines 1 and 19 are `#` notes, so the numbers run 2, 3 ... 18, 20, 21. Chapter 4's output began at 1 with no gap, so a reader may think lines were lost.
    - Direction: one clause that `#` notes count as lines.

18. The closing section is unclear about who does what and ends on a summary the page has already made.
    - Where: "Before Chapter 6".
    - Quote: "Chapter 6 gives you the jobs' code and records what each job reads and writes, so that the graph holds what is made from what."
    - Problem: it is unclear who records ("gives you ... and records"). The first paragraph mostly restates the section above.
    - Direction: say who writes the lines in Chapter 6. Compress the summary to what the experiments showed and could not show.

What I read and could not check
- I read: `docs/notes/chapter-03/review/brief.md`, Chapter 5 as built, Chapter 4 after review, `CLAUDE.md` (both copies, as given), `AGENTS.md`, `docs/prompts/review-learner-facing-prose.md`, the source `notebook/chapter_05.py` and `notebook/shop/graph.py`, `docs/notes/chapter-05.md`, the plan's Chapter 5 and 6 decision, and extracts of Chapter 2 and Chapter 3's as-built page.
- I checked the counts against the records and the engine code, and they hold: 12 nodes, 9 edges (5 `responsible`, 2 `of`, 2 `team`), 3 parts, and the steps and paths in all three traversals.
- I did not run the notebook or see the drawing. I judged it from its alt text and the engine code, so I could not check layout, legibility, colours or the dark theme.
- I did not check the timing and memory figures ("9 to 12 seconds", "about 400 MB"). The notes say local runs measured 8.3 to 8.7 s. A test pins "9 to 12 seconds" for the other chapters too, but I did not confirm that for Chapter 5.
- I did not independently verify that the dashboard reads `daily_sales`, or that `clean_orders` is made from `orders.jsonl` alone. I relied on Chapter 2's text ("clean_orders is made from orders.jsonl by four rules"), and on `shop/week.py` having `build_clean_orders` read only the raw orders file.
- I did not read Chapter 1 or the full Chapter 3 or Chapter 4 in detail beyond what bears on Chapter 5's continuity, and I did not read `docs/style.md` or `docs/sources.md`.
