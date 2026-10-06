// Copyright © 2026 Christopher Snow

// The front page: what the course is, the way in (the first chapter, or the first one not
// finished for a reader who has passed a challenge), then every chapter the plan has, by part,
// each linked with its progress or marked as still to be written.

import { PARTS, PLAN, chapterOf } from "@ms/content";
import { LessonStore, verifyCompletion, type Book, type Storage } from "@platform/lesson-runtime";

import { fill } from "../fill";
import { chapterHref } from "../route";
import { STRINGS } from "../strings";

export function ChapterList({ book, storage }: { book: Book; storage: Storage }) {
  const written = new Map(book.lessons.map((l) => [chapterOf(l), l]));
  const completion = new Map(
    book.lessons.map((l) => [
      l.id,
      verifyCompletion(book, l, new LessonStore(storage, book.id, l.id).get()),
    ]),
  );
  const ordered = [...book.lessons].sort((a, b) => chapterOf(a) - chapterOf(b));
  const started = ordered.some((l) => (completion.get(l.id)?.passed ?? 0) > 0);
  const unfinished = ordered.find((l) => {
    const c = completion.get(l.id);
    return c !== undefined && c.total > 0 && c.passed < c.total;
  });
  const next = started ? (unfinished ?? ordered[0]) : ordered[0];
  return (
    <>
      <div className="cover">
        <h1>{STRINGS.courseTitle}</h1>
        <p className="cover-lead">{STRINGS.lead}</p>
        {next && (
          <p className="cover-start">
            <a className="button primary" href={chapterHref(next.id)}>
              {fill(started && unfinished ? STRINGS.continueWith : STRINGS.start, {
                number: chapterOf(next),
                title: next.title,
              })}
            </a>
          </p>
        )}
      </div>
      <h2 className="contents-heading">{STRINGS.contents}</h2>
      {PARTS.map((title, i) => (
        <section key={title} className="part" aria-labelledby={`part-${i + 1}`}>
          <h3 id={`part-${i + 1}`}>{fill(STRINGS.part, { number: i + 1, title })}</h3>
          <ol className="chapter-list">
            {PLAN.filter((c) => c.part === i + 1).map((c) => {
              const lesson = written.get(c.number);
              const label = fill(STRINGS.chapter, { number: c.number, title: c.title });
              if (!lesson)
                return (
                  <li key={c.number} className="chapter-to-write">
                    <span className="chapter-title">{label}</span>
                    <span className="meta">{STRINGS.toWrite}</span>
                  </li>
                );
              const done = completion.get(lesson.id);
              return (
                <li key={c.number}>
                  <a className="chapter-link" href={chapterHref(lesson.id)}>
                    <span className="chapter-title">{label}</span>
                    <span className="meta">
                      {done && done.total > 0
                        ? fill(STRINGS.progress, { passed: done.passed, total: done.total })
                        : STRINGS.noChallenges}
                    </span>
                  </a>
                </li>
              );
            })}
          </ol>
        </section>
      ))}
    </>
  );
}
