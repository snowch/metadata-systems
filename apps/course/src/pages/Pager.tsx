// Copyright © 2026 Christopher Snow

// The links at the foot of a chapter to the chapter before and the chapter after, among those
// written so far. A chapter before that is a notebook with no page is linked as its notebook.

import { NOTEBOOKS, PLAN, chapterOf, notebookHref } from "@ms/content";
import type { Book } from "@platform/lesson-runtime";

import { chapterHref } from "../route";
import { STRINGS } from "../strings";

export function Pager({ book, lessonId }: { book: Book; lessonId: string }) {
  const ordered = [...book.lessons].sort((a, b) => chapterOf(a) - chapterOf(b));
  const i = ordered.findIndex((l) => l.id === lessonId);
  const lesson = ordered[i];
  const next = i >= 0 ? ordered[i + 1] : undefined;
  const page = i > 0 ? ordered[i - 1] : undefined;
  // The chapter just before this one, if it is a notebook with no page and comes after `page`.
  const before = lesson ? PLAN.find((c) => c.number === chapterOf(lesson) - 1) : undefined;
  const file = before && NOTEBOOKS.get(before.number);
  const previous =
    before && file && (!page || chapterOf(page) < before.number)
      ? { href: notebookHref(import.meta.env.BASE_URL, file), title: before.title }
      : page && { href: chapterHref(page.id), title: page.title };
  return (
    <nav className="pager" aria-label={STRINGS.pagerLabel}>
      {previous ? (
        <a className="pager-link" href={previous.href} rel="prev">
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
