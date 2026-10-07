// Copyright © 2026 Christopher Snow

// A figure's own sentence with its names set as the chapter's prose sets them: a name between
// backticks in a string is drawn in the monospace, as code. Where only plain text will do (an
// accessible name, a caption the platform draws), `plain` drops the marks.

import { Fragment } from "react";

export function Rich({ text }: { text: string }) {
  return (
    <>
      {text
        .split("`")
        .map((part, i) =>
          i % 2 === 1 ? <code key={i}>{part}</code> : <Fragment key={i}>{part}</Fragment>,
        )}
    </>
  );
}

export const plain = (text: string): string => text.replaceAll("`", "");

/** A name, marked for `Rich`. */
export const code = (name: string): string => `\`${name}\``;
