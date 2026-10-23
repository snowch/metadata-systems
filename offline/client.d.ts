// Copyright © 2026 Christopher Snow

export type Manifest = {
  version: string;
  bytes: number;
  files: { path: string; size: number; sha256: string }[];
};
export type Snapshot = { ready: boolean; version?: string; hasDownload?: boolean };

export function createOffline(base: string): {
  supported(): boolean;
  manifest(networkOnly?: boolean): Promise<Manifest | null>;
  snapshot(): Promise<Snapshot>;
  register(): Promise<void>;
  download(value: Manifest, signal: AbortSignal, progress: (bytes: number) => void): Promise<void>;
  remove(): Promise<void>;
};
