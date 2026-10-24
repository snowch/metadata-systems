// Copyright © 2026 Christopher Snow
export function appStatus(
  base: string | URL,
  options?: {
    blocked?: () => string | null;
    workerURL?: URL;
    releaseURL?: URL;
    resize?: () => void;
  },
): { node: HTMLDivElement; open(): void; dispose(): void };
