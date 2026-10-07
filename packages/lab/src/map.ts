// Copyright © 2026 Christopher Snow

// The platform as a newcomer is shown it on the first morning: its systems, in the order data
// moves through them each night, the assets each holds, and the direction in which programs move
// data from one system to another. It says nothing about which asset is made from which. Chapter
// 1 shows that storage cannot tell that, so the map must not tell it either; a later chapter's map
// shows what the learner's own records add.

import { ASSETS, type AssetId, type AssetKind, type StorageSystem } from "./shop/assets";
import { PROGRAMS, PROGRAM_IDS } from "./shop/programs";
import type { Week } from "./shop/week";
import { storage } from "./lab";

export interface MapSystem {
  readonly system: StorageSystem;
  readonly assets: readonly { readonly id: AssetId; readonly kind: AssetKind }[];
}

/** Programs move data from one system to another; which program, and which asset, is not said. */
export interface MapFlow {
  readonly from: StorageSystem;
  readonly to: StorageSystem;
}

export interface PlatformMap {
  /** In the order data moves through them: a system nothing flows into comes first. */
  readonly systems: readonly MapSystem[];
  readonly flows: readonly MapFlow[];
}

export function platformMap(w: Week): PlatformMap {
  const flows: MapFlow[] = [];
  for (const id of PROGRAM_IDS) {
    const to = ASSETS[PROGRAMS[id].writes].system;
    for (const read of PROGRAMS[id].reads) {
      const from = ASSETS[read].system;
      if (from !== to && !flows.some((f) => f.from === from && f.to === to))
        flows.push({ from, to });
    }
  }
  const held = new Map<StorageSystem, { id: AssetId; kind: AssetKind }[]>();
  for (const r of storage(w))
    held.set(r.system, [...(held.get(r.system) ?? []), { id: r.asset, kind: r.kind }]);
  // Order the systems by the flows: take, each time, one that nothing left flows into.
  const left = [...held.keys()];
  const order: StorageSystem[] = [];
  while (left.length) {
    const next =
      left.find((s) => !flows.some((f) => f.to === s && left.includes(f.from) && f.from !== s)) ??
      left[0]!;
    order.push(next);
    left.splice(left.indexOf(next), 1);
  }
  return {
    systems: order.map((system) => ({ system, assets: held.get(system) ?? [] })),
    flows,
  };
}

/** How many assets of a kind the map holds. */
export interface KindCount {
  readonly kind: AssetKind;
  readonly count: number;
}

/** What the map counts under its systems: its assets by kind, in the order it shows them, and all. */
export function mapTally(m: PlatformMap): {
  readonly kinds: readonly KindCount[];
  readonly total: number;
} {
  const kinds: { kind: AssetKind; count: number }[] = [];
  for (const s of m.systems)
    for (const a of s.assets) {
      const k = kinds.find((c) => c.kind === a.kind);
      if (k) k.count += 1;
      else kinds.push({ kind: a.kind, count: 1 });
    }
  return { kinds, total: kinds.reduce((n, k) => n + k.count, 0) };
}
