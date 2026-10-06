// Copyright © 2026 Christopher Snow

// A challenge built from choices: one select per field, and below them the query the choices
// mean, as SQL, run on Monday's storage. The learner builds, runs and inspects in one place; the
// tests are the runtime's "Run tests".

import { useId, useMemo } from "react";

import { catalogueFor, cleanSql, runOver, sumSql, week } from "@ms/lab";
import type { ChallengeEditorProps } from "@platform/lesson-runtime";

import { answersOf, cleanChoiceOf, sumChoiceOf } from "./choices";
import { DataTable } from "./DataTable";
import { problemText } from "./grade";
import { format, useViewStrings } from "./strings";

export function ChoiceEditor({ challenge, artifact, onChange }: ChallengeEditorProps) {
  const strings = useViewStrings();
  const id = useId();
  const answers = answersOf(challenge, artifact);
  const grader = challenge.tests.kind === "answers" ? challenge.tests.grader : "";
  const sql = useMemo(() => {
    if (grader === "reproduces") {
      const c = sumChoiceOf(answers);
      return c ? sumSql(c) : undefined;
    }
    const c = cleanChoiceOf(answers);
    return c ? cleanSql(c) : undefined;
  }, [grader, answers]);
  const outcome = useMemo(() => (sql ? runOver(sql, catalogueFor(week())) : undefined), [sql]);
  const set = (field: string, value: string) =>
    onChange({ ...artifact, answers: { ...(artifact.answers ?? {}), [field]: value } });

  return (
    <div className="choice-editor">
      <div className="choice-fields">
        {challenge.fields.map((f) => (
          // The label is a sibling of the select, not its parent, so the select's accessible
          // name is the field's label alone, not the label followed by the chosen option.
          <div key={f.id} className="choice-field">
            <label className="choice-label" htmlFor={`${id}-${f.id}`}>
              {f.label}
            </label>
            <select
              id={`${id}-${f.id}`}
              value={answers[f.id] ?? ""}
              onChange={(e) => set(f.id, e.target.value)}
            >
              {(f.options ?? []).map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>
      {sql && (
        <div className="choice-result">
          <h4 className="choice-heading">{strings.builderSql}</h4>
          <pre className="sql">
            <code>{sql}</code>
          </pre>
          <h4 className="choice-heading">{strings.builderResult}</h4>
          {outcome && "problem" in outcome ? (
            <p className="query-problem" role="status">
              {problemText(outcome.problem, strings)}
            </p>
          ) : outcome && grader === "same-rows" ? (
            <>
              <p role="status">{format(strings.keptRows, { count: outcome.table.rows.length })}</p>
              <details className="choice-rows">
                <summary>
                  {format(strings.rowsCaption, { count: outcome.table.rows.length })}
                </summary>
                <DataTable
                  table={outcome.table}
                  caption={format(strings.rowsCaption, { count: outcome.table.rows.length })}
                />
              </details>
            </>
          ) : outcome ? (
            <DataTable
              table={outcome.table}
              caption={format(strings.resultCaption, { count: outcome.table.rows.length })}
            />
          ) : null}
        </div>
      )}
    </div>
  );
}
