// Copyright © 2026 Christopher Snow

// The platform's kinds of thing, before any question: one card per asset the chapter works
// through, each with its kind's mark (Glyph.tsx) and a line on what it is and where it sits.
// Selecting a card shows a small head of its rows, or, for the dashboard, the reporting view
// itself. Nothing is asked, marked or scored: the point is to see what the platform holds
// before investigating it (the author's exploration step), so the Thursday question that
// follows asks a learner who knows what each asset is. The heads and the kind marks come from
// the lab, so they are the same everywhere the chapter shows them.
import { z } from "zod";
import { ASSET_IDS, recordOf, storage, week, type Table } from "@ms/lab";
import { useSlot, type InteractiveProps } from "@platform/lesson-runtime";
import { DataTable } from "../DataTable";
import { Glyph } from "../Glyph";
import { Rich } from "../Rich";
import { withProps } from "../props";
import { useViewStrings } from "../strings";

const Props = z.object({
  /** Each card: the asset, its one-line role, and what its head shows. */
  cards: z
    .array(
      z.object({
        id: z.enum(ASSET_IDS),
        role: z.string().min(1),
      }),
    )
    .min(2),
  /** How many rows a data-bearing card's head shows. */
  head: z.number().int().min(1).max(5).default(3),
});

function head(t: Table, rows: number): Table {
  return { columns: t.columns, rows: t.rows.slice(0, rows) };
}

export const AssetCards = withProps(
  Props,
  function AssetCards({
    data,
    interactive,
    store,
  }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const [open, setOpen] = useSlot<{ id: string } | null>(store, interactive.id);
    const view = storage(week());
    const chosen = open ? data.cards.find((c) => c.id === open.id) : undefined;
    const kinds = {
      file: strings.kindFile,
      table: strings.kindTable,
      dashboard: strings.kindDashboard,
    };
    return (
      <div className="asset-cards" data-open={chosen ? "true" : "false"}>
        <ul className="asset-card-list">
          {data.cards.map((c) => {
            const r = recordOf(view, c.id);
            const selected = chosen?.id === c.id;
            return (
              <li key={c.id} className={selected ? "asset-card is-open" : "asset-card"}>
                <button
                  type="button"
                  className="asset-card-button"
                  aria-pressed={selected}
                  onClick={() => setOpen(selected ? null : { id: c.id })}
                >
                  <Glyph kind={r.kind} />
                  <span className="asset-card-name">{c.id}</span>
                  <span className="asset-card-kind">{kinds[r.kind]}</span>
                </button>
                <p className="asset-card-role">
                  <Rich text={c.role} />
                </p>
                {selected && r.kind !== "dashboard" && (
                  <DataTable
                    table={head(r.content, data.head)}
                    caption={`${c.id} (${strings.rowsCaption.replace(/{count}/, String(data.head))})`}
                  />
                )}
                {selected && r.kind === "dashboard" && (
                  <p className="asset-card-dashboard-note">
                    {r.title}: {strings.valuesCaption.replace(/{count}/, String(r.rows))}
                  </p>
                )}
              </li>
            );
          })}
        </ul>
      </div>
    );
  },
);
