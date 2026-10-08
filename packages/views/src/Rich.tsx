// Copyright © 2026 Christopher Snow

// A figure's own sentence with its names set as the chapter's prose sets them: a name between
// backticks in a string is drawn in the monospace, as code, and a name the lab holds as an asset
// carries its kind's mark before it (packages/views/src/Glyph.tsx), so a file, a table and a
// dashboard are told apart at a glance wherever a sentence names one. The mark is decoration:
// hidden from a screen reader, and never the only way the kind is told. Where only plain text
// will do (an accessible name, a caption the platform draws), `plain` drops the marks.
import { Fragment } from "react";
import { ASSETS, type AssetId } from "@ms/lab";
import { Glyph } from "./Glyph";

/** Each asset's kind, for any sentence that names one. */
export const ASSET_KINDS = new Map<string, (typeof ASSETS)[AssetId]["kind"]>(
  Object.entries(ASSETS).map(([id, a]) => [id, a.kind]),
);

export function Rich({ text }: { text: string }) {
  return (
    <>
      {text.split("`").map((part, i) =>
        i % 2 === 1 ? (
          <code key={i}>
            {ASSET_KINDS.has(part) && <Glyph kind={ASSET_KINDS.get(part)!} />}
            {part}
          </code>
        ) : (
          <Fragment key={i}>{part}</Fragment>
        ),
      )}
    </>
  );
}

export const plain = (text: string): string => text.replaceAll("`", "");
/** A name, marked for `Rich`. */
export const code = (name: string): string => `\`${name}\``;

/** An option's label, with the asset it names marked before the name, as prose marks one. */
export function LabelledOption({ label }: { label: string }) {
  for (const [name, kind] of ASSET_KINDS) {
    if (label === name)
      return (
        <>
          <Glyph kind={kind} />
          {label}
        </>
      );
    if (label.startsWith(`${name},`))
      return (
        <>
          <Glyph kind={kind} />
          {label}
        </>
      );
  }
  return <>{label}</>;
}
