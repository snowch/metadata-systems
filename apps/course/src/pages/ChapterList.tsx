// Copyright © 2026 Christopher Snow

// The front page: a band with what the course is, the way in (the first chapter, or the first one
// not finished for a reader who has passed a challenge) and what the course assumes, beside a
// real figure from Chapter 2, the shop's dashboard, which shows the question the course starts
// from; then the eight parts in reading order, one line each; then every chapter the plan has, by
// part, each part one line until it is pressed, the part of the chapter the button names already
// open (the author, 8 October 2026: the page was a title, a paragraph and thirty-one lines of
// "still to be written"). A chapter that is a notebook links it: from its line when the chapter has
// no page, at the right of its line when it has one, with one sentence under "Contents" saying what
// a notebook is (content/lessons/notebooks.ts).

import { useMemo } from "react";

import { NOTEBOOKS, PARTS, PLAN, chapterOf, notebookHref } from "@ms/content";
import { Dashboard } from "@ms/views";
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

/** Where the band's button leads: a chapter's page, or its notebook if it has no page. */
interface Start {
  href: string;
  number: number;
  title: string;
}

const notebook = (file: string) => notebookHref(import.meta.env.BASE_URL, file);

/** The dashboard as Chapter 2 shows it, on the week as it first ran. */
const COVER_FIGURE: InteractiveProps["interactive"] = {
  id: "cover-dashboard",
  kind: "dashboard",
  timeModel: "none",
  caption: STRINGS.cover.figureCaption,
  props: {},
};

/**
 * The band at the top: the title, what you do, the way in, what the course assumes, and the
 * dashboard computed from the shop's data, with its caption and no badge, as a chapter shows it.
 */
function Cover({
  book,
  storage,
  first,
  start,
  started,
}: {
  book: Book;
  storage: Storage;
  first: Lesson;
  start: Start;
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
          <a className="button primary hero-start" href={start.href}>
            {fill(started ? STRINGS.continueWith : STRINGS.start, {
              number: start.number,
              title: start.title,
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
      >
        <figcaption>{COVER_FIGURE.caption}</figcaption>
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
  // A reader with challenges left starts at the first chapter that has them; anyone else at the
  // first chapter there is, page or notebook.
  const opening = PLAN.find((c) => written.has(c.number) || NOTEBOOKS.has(c.number));
  const start: Start | undefined =
    started && unfinished
      ? { href: chapterHref(unfinished.id), number: chapterOf(unfinished), title: unfinished.title }
      : opening && {
          href: written.has(opening.number)
            ? chapterHref((written.get(opening.number) as Lesson).id)
            : notebook(NOTEBOOKS.get(opening.number) as string),
          number: opening.number,
          title: opening.title,
        };
  const openPart = start ? (PLAN.find((c) => c.number === start.number)?.part ?? 1) : 1;
  return (
    <>
      {first && start && (
        <Cover
          book={book}
          storage={storage}
          first={first}
          start={start}
          started={started && unfinished !== undefined}
        />
      )}
      <h2 className="contents-heading">{STRINGS.contents}</h2>
      {NOTEBOOKS.size > 0 && <p className="contents-note">{STRINGS.notebooksNote}</p>}
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
                const file = NOTEBOOKS.get(c.number);
                const label = fill(STRINGS.chapter, { number: c.number, title: c.title });
                if (!lesson && file)
                  return (
                    <li key={c.number}>
                      <a className="chapter-link" href={notebook(file)}>
                        <span className="chapter-title">{label}</span>
                        <span className="meta">{STRINGS.notebookNote}</span>
                      </a>
                    </li>
                  );
                if (!lesson)
                  return (
                    <li key={c.number} className="chapter-to-write">
                      <span className="chapter-title">{label}</span>
                      <span className="meta">{STRINGS.toWrite}</span>
                    </li>
                  );
                const done = completion.get(lesson.id);
                // The title opens the page; a chapter that is also a notebook links it at the right
                // of its line. Progress shows only where a chapter has challenges to count.
                return (
                  <li key={c.number} className="chapter-row">
                    <a className="chapter-link" href={chapterHref(lesson.id)}>
                      <span className="chapter-title">{label}</span>
                      {done && done.total > 0 && (
                        <span className="meta">
                          {fill(STRINGS.progress, { passed: done.passed, total: done.total })}
                        </span>
                      )}
                    </a>
                    {file && (
                      <a className="chapter-notebook" href={notebook(file)}>
                        {STRINGS.notebookLink}
                      </a>
                    )}
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
