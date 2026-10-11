// Copyright © 2026 Christopher Snow

// The front page: a band with what the course is, the way in (Chapter 1's notebook) and what the
// course assumes, beside the shop's dashboard, which shows the question the course starts from;
// then every chapter the plan has, by part, each part one line until it is pressed, the first part
// open. A written chapter is a notebook, and its title opens it (the author, 11 October 2026: the
// course has only the notebook version of each chapter).

import { NOTEBOOKS, PARTS, PLAN, notebookHref } from "@ms/content";

import { fill } from "../fill";
import { STRINGS } from "../strings";
import { Dashboard } from "./Dashboard";

const notebook = (file: string) => notebookHref(import.meta.env.BASE_URL, file);

/** The band at the top: the title, what you do, the way in, what the course assumes, and the
    dashboard with its caption. */
function Cover() {
  const [title, subtitle] = STRINGS.courseTitle.split(/:\s+/, 2);
  const first = PLAN.find((c) => NOTEBOOKS.has(c.number));
  return (
    <section className="cover-hero" aria-labelledby="cover-title">
      <div className="hero-text">
        <h1 id="cover-title">
          {subtitle ? `${title}:` : title}
          {subtitle && <span className="hero-title-sub">{subtitle}</span>}
        </h1>
        <p className="hero-promise">{STRINGS.cover.promise}</p>
        <p className="cover-lead">{STRINGS.lead}</p>
        {first && (
          <p className="cover-start">
            <a
              className="button primary hero-start"
              href={notebook(NOTEBOOKS.get(first.number) as string)}
            >
              {fill(STRINGS.start, { number: first.number, title: first.title })}
            </a>
          </p>
        )}
        <p className="course-assumes">{STRINGS.cover.assumes}</p>
      </div>
      <figure className="interactive hero-figure" id="ix-cover-dashboard" data-kind="dashboard">
        <figcaption>{STRINGS.cover.figureCaption}</figcaption>
        <Dashboard />
      </figure>
    </section>
  );
}

/** The chapters of a part, from the plan. */
const chaptersOf = (part: number) => PLAN.filter((c) => c.part === part);

export function FrontPage() {
  return (
    <>
      <Cover />
      <h2 className="contents-heading">{STRINGS.contents}</h2>
      <p className="contents-note">{STRINGS.contentsNote}</p>
      {PARTS.map((title, i) => {
        const chapters = chaptersOf(i + 1);
        const count = chapters.filter((c) => NOTEBOOKS.has(c.number)).length;
        return (
          <details key={title} className="part" open={i === 0}>
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
                const file = NOTEBOOKS.get(c.number);
                const label = fill(STRINGS.chapter, { number: c.number, title: c.title });
                return file ? (
                  <li key={c.number}>
                    <a className="chapter-link" href={notebook(file)}>
                      <span className="chapter-title">{label}</span>
                    </a>
                  </li>
                ) : (
                  <li key={c.number} className="chapter-to-write">
                    <span className="chapter-title">{label}</span>
                    <span className="meta">{STRINGS.toWrite}</span>
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
