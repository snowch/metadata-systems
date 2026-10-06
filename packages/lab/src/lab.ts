// Copyright © 2026 Christopher Snow

// The lab as a figure uses it: a week, plain or changed, its storage view and a catalogue for
// queries over what storage holds on Monday morning. Each week is run once and kept, so every
// figure on a page sees the same rows.

import { catalogueOf, type Catalogue } from "./sql";
import type { Table } from "./table";
import { storageView, type StorageRecord } from "./storage";
import { CHANGE_IDS, runWeek, type ChangeId, type Week } from "./shop/week";

const weeks = new Map<string, Week>();
const views = new Map<Week, StorageRecord[]>();

const keyOf = (changes: readonly ChangeId[]) =>
  CHANGE_IDS.filter((c) => changes.includes(c)).join("+") || "plain";

/** The week with these changes made to the shop, run once and kept. */
export function week(changes: readonly ChangeId[] = []): Week {
  const key = keyOf(changes);
  let w = weeks.get(key);
  if (!w) {
    w = runWeek(CHANGE_IDS.filter((c) => changes.includes(c)));
    weeks.set(key, w);
  }
  return w;
}

/** What storage records on Monday morning, for a week. */
export function storage(w: Week = week()): StorageRecord[] {
  let v = views.get(w);
  if (!v) {
    v = storageView(w);
    views.set(w, v);
  }
  return v;
}

/** Every asset's contents by its name, for a query a learner builds. */
export function catalogueFor(w: Week = week()): Catalogue {
  return catalogueOf(Object.fromEntries(w.tables) as Record<string, Table>);
}
