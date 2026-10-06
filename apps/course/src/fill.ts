// Copyright © 2026 Christopher Snow

/** Fills `{slot}`s in one of the shell's templates. */
export function fill(template: string, slots: Readonly<Record<string, string | number>>): string {
  return template.replace(/\{(\w+)\}/g, (whole, key: string) => {
    const v = slots[key];
    return v === undefined ? whole : String(v);
  });
}
