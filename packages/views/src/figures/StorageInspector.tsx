// Copyright © 2026 Christopher Snow

// Everything storage holds: the seven assets, grouped by the system that holds them; for the one
// chosen, exactly what its system records, what storage says about each of the chapter's eight
// questions, its columns and its rows. The answers come from the lab's storage view, so a question
// storage cannot answer says so because no field holds the answer. The questions come before the
// rows, which can be long and, on a phone, wide.

import { z } from "zod";

import {
  ASSET_IDS,
  CHANGE_IDS,
  QUESTION_IDS,
  storage,
  storageAnswer,
  typeName,
  week,
  type AssetId,
  type QuestionId,
  type StorageRecord,
} from "@ms/lab";
import { useSlot, type InteractiveProps } from "@platform/lesson-runtime";
import { StateInspector } from "@platform/primitives";

import { DataTable } from "../DataTable";
import { Glyph } from "../Glyph";
import { withProps } from "../props";
import { Rich } from "../Rich";
import { showSize, showTime } from "../show";
import { format, useViewStrings, type ViewStrings } from "../strings";

const Props = z.object({
  initial: z.enum(ASSET_IDS).default("orders.parquet"),
  changes: z.array(z.enum(CHANGE_IDS)).default([]),
});

function groupLabel(r: StorageRecord, strings: ViewStrings): string {
  if (r.system === "object-storage")
    return format(strings.objectStorage, { bucket: r.location.split("/")[2] ?? "" });
  if (r.system === "warehouse")
    return format(strings.warehouse, { place: r.location.split(".").slice(0, 2).join(".") });
  return strings.reporting;
}

function recordRows(r: StorageRecord, strings: ViewStrings) {
  const kind = {
    file: strings.kindFile,
    table: strings.kindTable,
    dashboard: strings.kindDashboard,
  }[r.kind];
  const written =
    r.system === "object-storage"
      ? strings.lastModified
      : r.system === "warehouse"
        ? strings.lastAltered
        : strings.lastRefreshed;
  const rows: { key: string; name: string; text: string }[] = [
    { key: "location", name: strings.location, text: r.location },
    { key: "kind", name: strings.kind, text: kind },
  ];
  if (r.title) rows.push({ key: "title", name: strings.title, text: r.title });
  if (r.kind === "file") rows.push({ key: "format", name: strings.format, text: "Parquet" });
  rows.push({ key: "columns", name: strings.columns, text: String(r.columns.length) });
  rows.push({ key: "rows", name: strings.rows, text: String(r.rows) });
  if (r.sizeBytes !== undefined)
    rows.push({ key: "size", name: strings.size, text: showSize(r.sizeBytes) });
  if (r.created) rows.push({ key: "created", name: strings.created, text: showTime(r.created) });
  rows.push({ key: "written", name: written, text: showTime(r.lastWritten) });
  if (r.ownerRole) rows.push({ key: "owner", name: strings.ownerRole, text: r.ownerRole });
  if (r.createdBy) rows.push({ key: "creator", name: strings.createdBy, text: r.createdBy });
  return rows;
}

function answerText(r: StorageRecord, q: QuestionId, strings: ViewStrings): string {
  const a = storageAnswer(q, r);
  const template = strings.a[a.kind] ?? "";
  switch (a.kind) {
    case "answered":
    case "time-only":
      return format(template, { time: showTime(a.time) });
    case "columns":
      return template;
    case "title":
      return format(template, { title: a.title });
    case "owner-role":
      return format(template, { role: a.role });
    case "creator":
      return format(template, { person: a.person });
    case "types":
      return format(template, { column: a.column, type: a.type });
    default:
      return template;
  }
}

export const StorageInspector = withProps(
  Props,
  function StorageInspector({
    data,
    interactive,
    store,
  }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const view = storage(week(data.changes));
    const [chosen, setChosen] = useSlot<AssetId>(store, interactive.id);
    const current = view.find((r) => r.asset === (chosen ?? data.initial)) ?? view[0];
    const groups = new Map<string, StorageRecord[]>();
    for (const r of view)
      groups.set(groupLabel(r, strings), [...(groups.get(groupLabel(r, strings)) ?? []), r]);
    if (!current) return null;
    return (
      <div className="inspector">
        <nav className="inspector-assets" aria-label={strings.assetsHeading}>
          <h4 className="inspector-heading">{strings.assetsHeading}</h4>
          {[...groups].map(([label, records]) => (
            <div key={label} className="asset-group">
              <p className="asset-group-label">{label}</p>
              <ul>
                {records.map((r) => (
                  <li key={r.asset}>
                    <button
                      type="button"
                      className="asset-button"
                      aria-pressed={r.asset === current.asset}
                      onClick={() => setChosen(r.asset)}
                    >
                      <Glyph kind={r.kind} />
                      <span>{r.asset}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
        <div className="inspector-detail">
          <h4 className="inspector-asset">
            <Glyph kind={current.kind} /> <span>{current.asset}</span>
          </h4>
          <StateInspector
            className="record-table"
            caption={format(strings.recordCaption, { asset: current.asset })}
            headings={[strings.field, strings.recorded]}
            rows={recordRows(current, strings).map((x) => ({
              key: x.key,
              name: x.name,
              cells: [{ text: x.text }],
            }))}
          />
          <section className="inspector-questions" aria-label={strings.questionsHeading}>
            <h5>{strings.questionsHeading}</h5>
            <dl>
              {QUESTION_IDS.map((q) => (
                <div key={q} className="question-answer">
                  <dt>{strings.q[q]}</dt>
                  <dd>
                    <Rich text={answerText(current, q, strings)} />
                  </dd>
                </div>
              ))}
            </dl>
          </section>
          <StateInspector
            className="columns-table"
            caption={strings.columnsCaption}
            headings={[strings.column, strings.type]}
            rows={current.columns.map((c) => ({
              key: c.name,
              name: c.name,
              cells: [{ text: typeName(c.type) }],
            }))}
          />
          <DataTable
            table={current.content}
            caption={
              current.kind === "dashboard"
                ? strings.valuesCaption
                : format(strings.rowsCaption, { count: current.rows })
            }
          />
        </div>
      </div>
    );
  },
);
