// Copyright © 2026 Christopher Snow

import { createOffline } from "../../../offline/client.js";
export type { Manifest, Snapshot } from "../../../offline/client.js";
export const base = new URL(import.meta.env.BASE_URL, window.location.href).href;
export const { supported, manifest, snapshot, register, download, remove } = createOffline(base);
