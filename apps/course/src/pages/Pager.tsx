// Copyright © 2026 Christopher Snow

// The links at the foot of a chapter to the chapter before and the chapter after, among those
// written so far.

import { chapterOf } from "@ms/content";
import type { Book } from "@platform/lesson-runtime";

import { chapterHref } from "../route";
import { STRINGS } from "../strings";

export function Pager({ book, lessonId }: { book: Book; lessonId: string }) {
  const ordered = [...book.lessons].sort((a, b) => chapterOf(a) - chapterOf(b));
  const i = ordered.findIndex((l) => l.id === lessonId);
  const previous = i > 0 ? ordered[i - 1] : undefined;
  const next = i >= 0 ? ordered[i + 1] : undefined;
  return (
    <nav className="pager" aria-label={STRINGS.pagerLabel}>
      {previous ? (
        <a className="pager-link" href={chapterHref(previous.id)} rel="prev">
          <span className="meta">{STRINGS.previous}</span>
          <span>{previous.title}</span>
        </a>
      ) : (
        <span />
      )}
      {next ? (
        <a className="pager-link pager-next" href={chapterHref(next.id)} rel="next">
          <span className="meta">{STRINGS.next}</span>
          <span>{next.title}</span>
        </a>
      ) : (
        <p className="pager-not-yet">
          {STRINGS.notYet}. <a href="#/">{STRINGS.back}</a>
        </p>
      )}
    </nav>
  );
}
