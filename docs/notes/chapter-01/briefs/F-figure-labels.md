# Brief F: the labels inside the figures, and the course's frame

Attach: `common.md`, `../facts.md`, `docs/style.md`. Write to `docs/notes/chapter-01/drafts/F.md`.
These strings appear inside the figures and around every page. Keep each one short: a label is a
few words; a template is one sentence. Slots in braces, such as `{time}`, are filled by the page
with a value: keep every slot exactly as written, and use no slot that is not given.

## labNote
The note a reader opens from a figure's badge. Two to four sentences. Facts: the figure runs the
lab: the shop's platform, whose programs are written in SQL and really run over the rows you see,
in your browser, for the week of 7 to 13 September 2026. What the figure shows is worked out from
those rows each time. The lab's clock is the week's own, not real time, and nothing leaves your
browser.

## labels
Write each as `key: text`, one per line:
- badge: the badge's text on a figure that runs the lab (one or two words)
- badgeLabel: the badge's accessible name, with slot {model} for the badge's text
- modelNote: heading at the foot of a chapter over the note on how its figures run (a few words)
- modelVsReality: heading over the note on how the lab differs from a real platform
- modelVsRealityNone: the same heading for a chapter whose figures do not run the lab
- inputs: label in a failed test for what the test was about (one word, such as "For")
- actual: label in a failed test for what the learner's work gave
- expected: label in a failed test for what was expected
- checkPrediction: the button that commits a prediction
- predictAgain: the button that clears it
- yourPrediction: a screen reader's name for the options
- youSaid: template with slot {choice}: what the learner chose
- labFound: template with slot {answer}: what the lab found
- match: one sentence when the prediction matched
- noMatch: one sentence when it did not
- daysCaption: caption of a table comparing each day's total from `orders.parquet` with `daily_sales`
- day: column heading, a day
- addedUp: column heading, the total from `orders.parquet` added up
- same: column heading, whether the two agree
- yes: cell text when they agree
- no: cell text when they differ
- ownerFound: template with slots {asset} and {value}: the warehouse names {value} as the owner of {asset}
- assetsHeading: heading over the list of assets
- objectStorage: group label, with slot {bucket}
- warehouse: group label, with slot {place}
- reporting: group label for the reporting tool
- recordCaption: template with slot {asset}: caption of the table of what storage records about it
- location: row label
- kind: row label
- format: row label
- columns: row label
- rows: row label
- size: row label
- lastModified: row label for a file
- lastAltered: row label for a table
- lastRefreshed: row label for a dashboard
- created: row label
- ownerRole: row label for the warehouse's owning account
- createdBy: row label
- title: row label
- kindFile: value "file"
- kindTable: value "table"
- kindDashboard: value "dashboard"
- columnsCaption: caption of the table of columns and types
- column: column heading
- type: column heading
- rowsCaption: template with slot {count}: caption of the table of an asset's rows
- valuesCaption: caption of the table of values a dashboard shows
- questionsHeading: heading over what storage says about the questions
- q.last-written: the question: when was it last written?
- q.made-from: the question: what is it made from?
- q.computed: the question: how are its numbers worked out?
- q.computed.dashboard: the same question for the dashboard: what does it show?
- q.read-by: the question: what reads it?
- q.worked: the question: did last night's write work?
- q.responsible: the question: who is responsible for it?
- q.unit: the question: in what units are its numbers?
- q.changed: the question: what changed in it this week?
- a.answered: template with slot {time}: storage records the last write, at {time}
- a.columns: template with slot {count}: storage records {count} column names and their types, not what they mean
- a.title: template with slot {title}: the reporting tool records the title, {title}, and nothing about where the values come from
- a.owner-role: template with slot {role}: the warehouse records the owning account, {role}, not a person or a team
- a.creator: template with slot {person}: the reporting tool records who created it, {person}, not who answers for it now
- a.types: template with slots {column} and {type}: storage records {column} as {type}, a number with no unit
- a.time-only: template with slot {time}: storage records the last write, at {time}, not whether a write was due
- a.nothing: storage records nothing that answers this
- builderSql: heading over the learner's query shown as SQL
- builderResult: heading over its result
- resultCaption: template with slot {count}: caption of the result's rows
- keptRows: template with slot {count}: the rules keep {count} rows
- p.unknown-column: template with slots {table} and {column}: {table} has no column called {column}
- p.unknown-table: template with slot {name}: there is no asset called {name}
- p.other: the query cannot run
- noRow: cell text where a query gives no row for a day
- missingRows: template with slots {count} and {ids}: your rules drop {count} rows that clean_orders keeps, orders {ids}
- extraRows: template with slots {count} and {ids}: your rules keep {count} rows that clean_orders does not, orders {ids}
- changeLegend: label over the choice of change
- noChange: the choice with no change
- runWeek: the button that runs the week again with the chosen change
- ranWith: template with slot {change}: the status line once the week has gone through again, saying it went through with {change}
- storageDiffHeading: heading: what storage shows differently
- newAsset: template with slots {asset} and {location}: a new file, {asset}, at {location}
- changedTime: template with slots {asset}, {after} and {before}: {asset} last written at {after}, not {before}
- changedRows: template with slots {asset}, {after} and {before}: {asset} has {after} rows, not {before}
- changedValue: template with slots {asset}, {day}, {after} and {before}: in {asset}, the row for {day} reads {after}, not {before}
- noDiff: storage shows no difference
- yourQueryHeading: heading: your query against the new daily_sales
- usingYours: note that this uses the learner's own query from the construction section
- usingCourse: note that the learner has not built a passing query yet, so this uses the course's
- fitsHeading: heading: every query in the builder's choices that rebuilds daily_sales
- fitsNone: no query in the builder's choices rebuilds it
- describeQuery: template with slots {source}, {keep}, {measure} and {per}: a short phrase describing one query: from {source}, {keep}, add up {measure} per {per}
- place.storage: column heading: storage records it
- place.suggested: column heading: the data suggests it
- place.record: column heading: only a record kept at the time answers it
- e.time: template with slot {time}: last written at {time}
- e.oneQuery: template with slot {query}: one query rebuilds it: {query}
- e.manyQueries: template with slots {count} and {sources}: {count} queries rebuild it, from {sources}
- e.noQuery: no query rebuilds it
- e.readers: template with slot {assets}: {assets} shows the same numbers
- e.noReaders: no other asset shows the same numbers
- e.nightDone: template with slots {time} and {day}: last written at {time}, with a row for {day}
- e.nightMissing: template with slots {time}, {latest} and {expected}: last written at {time}; the latest row is for {latest}, not {expected}
- e.account: template with slot {role}: storage names {role}, an account, not who answers for it
- e.types: template with slots {column} and {type}: {column} is {type}, with no unit
- e.currentOnly: storage keeps only the current rows
- chartLabel: template with slots {title} and {time}: a screen reader's name for the dashboard's chart, giving its title and when it last refreshed
- refreshed: template with slot {time}: last refreshed {time}
- weekdays: the seven weekday names Monday to Sunday, abbreviated to three letters, comma-separated

## shell
Write each as `key: text`, one per line. These frame every page of the site.
- brand: Metadata Systems
- courseTitle: Metadata Systems: From Raw Files to a Working Metadata Platform
- lead: one or two sentences on the front page saying what the course is: you build a small
  metadata system inside a small data platform that really runs in your browser; for each idea you
  predict, build, run, inspect, break and repair it; your work stays in your browser. (This text is
  the one place outside the generalisation that may use the word "metadata", because it is the
  course's subject.)
- chapters: the navigation link to the list of chapters
- skip: skip link
- theme, themeAuto, themeLight, themeDark: the theme picker's label and options
- footer: everything runs in your browser and nothing is sent anywhere
- start: template with slots {number} and {title}: the button to start: Start with Chapter {number}: {title}
- continueWith: template with slots {number} and {title}: Continue with Chapter {number}: {title}
- contents: heading over the list of all chapters
- part: template with slots {number} and {title}: Part {number}: {title}
- chapter: template with slots {number} and {title}: {number}. {title}
- toWrite: shown under a chapter not yet written: still to be written
- progress: template with slots {passed} and {total}: {passed} of {total} challenges complete
- noChallenges: no challenges
- previous, next: the pager's links
- pagerLabel: a screen reader's name for the pager
- notYet: shown on the last chapter written so far: the next chapter is still to be written
- missing: template with slot {path}: there is no page at {path}
- noLesson: template with slot {id}: there is no chapter called {id}
- back: back to the chapters
