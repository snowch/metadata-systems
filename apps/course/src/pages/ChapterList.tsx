// Copyright © 2026 Christopher Snow

// The front page: a band with what the course is, the way in (the first chapter, or the first one
// not finished for a reader who has passed a challenge) and what the course assumes, beside a
// real figure from Chapter 1, the shop's dashboard, which shows the question the course starts
// from; then the eight parts in reading order, one line each; then every chapter the plan has, by
// part, each part one line until it is pressed, the part of the chapter the button names already
// open (the author, 8 October 2026: the page was a title, a paragraph and thirty-one lines of
// "still to be written").

import { useMemo } from "react";

import { PARTS, PLAN, chapterOf } from "@ms/content";
import { DEFAULT_VIEW_STRINGS, Dashboard } from "@ms/views";
import {
  LessonStore,
  verifyCompletion,
  type Book,
  type InteractiveProps,
  type Storage,
} from "@platform/lesson-runtime";

import { fill } from "../fill";
import { chapterHref } from "../route";
import { STRINGS } from "../strings";

type Lesson = Book["lessons"][number];

/** The dashboard as Chapter 1 shows it: a reference, on the week as it first ran. */
const COVER_FIGURE: InteractiveProps["interactive"] = {
  id: "cover-dashboard",
  kind: "dashboard",
  timeModel: "lab",
  role: "reference",
  caption: STRINGS.cover.figureCaption,
  props: {},
};

/**
 * The band at the top: the title, what you do, the way in, what the course assumes, and the
 * dashboard live from the lab, with the lab's mark and a plain badge, as a chapter shows it.
 */
function Cover({
  book,
  storage,
  first,
  next,
  started,
}: {
  book: Book;
  storage: Storage;
  first: Lesson;
  next: Lesson;
  started: boolean;
}) {
  const store = useMemo(() => new LessonStore(storage, book.id, first.id), [storage, book, first]);
  const [title, subtitle] = STRINGS.courseTitle.split(/:\s+/, 2);
  return (
    <section className="cover-hero" aria-labelledby="cover-title">
      <div className="hero-text">
        <h1 id="cover-title">
          {subtitle ? `${title}:` : title}
          {subtitle && <span className="hero-title-sub">{subtitle}</span>}
        </h1>
        <p className="hero-promise">{STRINGS.cover.promise}</p>
        <p className="cover-lead">{STRINGS.lead}</p>
        <p className="cover-start">
          <a className="button primary hero-start" href={chapterHref(next.id)}>
            {fill(started ? STRINGS.continueWith : STRINGS.start, {
              number: chapterOf(next),
              title: next.title,
            })}
          </a>
        </p>
        <p className="course-assumes">{STRINGS.cover.assumes}</p>
      </div>
      <figure
        className="interactive hero-figure"
        id={`ix-${COVER_FIGURE.id}`}
        data-kind={COVER_FIGURE.kind}
        data-time-model={COVER_FIGURE.timeModel}
        data-role={COVER_FIGURE.role}
      >
        <figcaption>
          <span className="badge time-model">{DEFAULT_VIEW_STRINGS.roles["reference"]}</span>{" "}
          {COVER_FIGURE.caption}
        </figcaption>
        <Dashboard lesson={first} interactive={COVER_FIGURE} store={store} />
      </figure>
    </section>
  );
}

/** The chapters of a part, from the plan. */
const chaptersOf = (part: number) => PLAN.filter((c) => c.part === part);

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
  const first = ordered[0];
  const next = started ? (unfinished ?? first) : first;
  const openPart = next ? (PLAN.find((c) => c.number === chapterOf(next))?.part ?? 1) : 1;
  return (
    <>
      {first && next && (
        <Cover
          book={book}
          storage={storage}
          first={first}
          next={next}
          started={started && unfinished !== undefined}
        />
      )}
      <h2 className="contents-heading">{STRINGS.contents}</h2>
      {PARTS.map((title, i) => {
        const chapters = chaptersOf(i + 1);
        const count = chapters.filter((c) => written.has(c.number)).length;
        return (
          <details key={title} className="part" open={i + 1 === openPart}>
            <summary>
              <span className="part-heading">{fill(STRINGS.part, { number: i + 1, title })}</span>
              <span className="meta">
                {count > 0
                  ? fill(STRINGS.cover.partCount.some, { written: count, total: chapters.length })
                  : chapters.length === 1
                    ? STRINGS.cover.partCount.noneOne
                    : fill(STRINGS.cover.partCount.none, { total: chapters.length })}
              </span>
            </summary>
            <ol className="chapter-list">
              {chapters.map((c) => {
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
          </details>
        );
      })}
    </>
  );
}
