# Brief CC: the messages the checks print (Chapters 3 and 4)

Two checks print a table of problems in a Jupyter notebook for a data engineer: one row per problem,
with the line number and the asset or the record beside it, and a column `problem` holding one of
the messages below. Each message is a single short sentence that says what is wrong with that row,
in plain British English, with no em dashes, no "error", no "invalid", no exclamation marks, and
nothing that makes the check sound like a person ("I could not", "the check thinks"). Keep every
name in backticks exactly as written. Do not use the words lab, engine, graph, node, edge, lineage,
identity, event.

Write the file once. Do not change it after you reply.

## Facts

Chapter 3's check holds a reader's records against the warehouse and object storage. A record line
has the form: an asset's name, then a column's name if the fact is about a column, then a field, a
colon, and a value (`daily_sales revenue_pence unit: pence`). A description of a column is a line
with the field `means` and a value that is not dots (`........` means not yet written).

Chapter 4's check holds records against a model. A record line has the form: a type, an identifier,
an attribute, a colon, a value (`dataset daily_sales responsible: j.marsh`). A model line has the
form: a type, an attribute, a colon, and what the attribute's value is: `text`, or one or more type
names joined by `or` (`dataset responsible: person or team`). The words type, identifier and
attribute may be used in Chapter 4's messages (keys 6 to 11), not in Chapter 3's (keys 1 to 5).

## Messages

1. **none**: printed in place of the table when a check finds no problems.
2. **unread**: a line of a Chapter 3 record that is not in the form above.
3. **no_asset**: a line names an asset that is neither a table in the warehouse nor a file in object
   storage.
4. **no_column**: a line names a column that the table does not have in the warehouse.
5. **no_description**: a column of the warehouse that has no description in the records.
6. **typed_unread**: a line of a Chapter 4 record that is not in its form.
7. **model_unread**: a line of the model that is not in its form.
8. **no_type**: a record line whose type the model does not define.
9. **no_attribute**: a record line whose attribute the model does not give that type.
10. **no_value_type**: a model line that says an attribute's value is a type the model does not
    define.
11. **no_thing**: a record line whose value should be the identifier of something of a given type
    (or types), and no record describes such a thing with that identifier. The message must contain
    the placeholder `{types}`, exactly as written, where the type names go (it becomes, for
    example, "person or team").

Write each message under `## 1` to `## 11`, as the exact text.
