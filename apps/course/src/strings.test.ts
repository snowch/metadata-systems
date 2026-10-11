// Copyright © 2026 Christopher Snow

// The front page's words use none of the commonest forms of filler (CLAUDE.md, "Silence is
// preferable to filler"): a backstop for the forms the author named; only reading applies the rule.
// notebook/tests/test_words.py holds the notebooks to the same list.

import { describe, expect, it } from "vitest";

import { STRINGS } from "./strings";

describe("the front page's words", () => {
  it("use none of the commonest forms of filler", () => {
    const FILLER = [
      /\byou have (what you need|everything)\b/i,
      /\beverything (is )?in place\b/i,
      /\bnow you can (begin|start)\b/i,
      /\bwhere things get interesting\b/i,
      /\basks nothing of you\b/i,
      /\bkept to hand\b/i,
      /\b(is|are) (quietly )?waiting\b/i,
      /\bquietly\b/i,
      /\byou (have been|were) told\b/i,
      /\b(as )?you already know\b/i,
      /\blet's\b/i,
    ];
    const strings = (v: unknown): string[] =>
      typeof v === "string"
        ? [v]
        : v && typeof v === "object"
          ? Object.values(v).flatMap(strings)
          : [];
    const found = strings(STRINGS).flatMap((t) =>
      FILLER.filter((f) => f.test(t)).map((f) => `${String(f)}: ${t.slice(0, 80)}`),
    );
    expect(found).toEqual([]);
  });
});
