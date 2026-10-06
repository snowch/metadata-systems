// Copyright © 2026 Christopher Snow

// The course shell: header, routes, footer. Chapters render through the platform's runtime with
// this course's book; the shell knows nothing about metadata.

import { useMemo } from "react";

import { LESSONS } from "@ms/content";
import { createBook, runtimeStrings } from "@ms/views";
import { browserStorage, LessonView } from "@platform/lesson-runtime";

import { fill } from "./fill";
import { ChapterList } from "./pages/ChapterList";
import { Pager } from "./pages/Pager";
import { chapterHref, useRoute } from "./route";
import { STRINGS } from "./strings";
import { useTheme, type Theme } from "./theme";

export function App() {
  const route = useRoute();
  const [theme, setTheme] = useTheme();
  const storage = useMemo(() => browserStorage(), []);
  const book = useMemo(() => createBook(LESSONS), []);
  const strings = useMemo(() => runtimeStrings(), []);

  let page: React.ReactNode;
  if (route.kind === "list") page = <ChapterList book={book} storage={storage} />;
  else if (route.kind === "chapter") {
    const lesson = book.lessons.find((l) => l.id === route.id);
    page = lesson ? (
      <>
        <LessonView
          key={lesson.id}
          book={book}
          lesson={lesson}
          storage={storage}
          lessonHref={chapterHref}
          strings={strings}
        />
        <Pager book={book} lessonId={lesson.id} />
      </>
    ) : (
      <>
        <h1>{fill(STRINGS.noLesson, { id: route.id })}</h1>
        <p>
          <a href="#/">{STRINGS.back}</a>
        </p>
      </>
    );
  } else {
    page = (
      <>
        <h1>{fill(STRINGS.missing, { path: route.path })}</h1>
        <p>
          <a href="#/">{STRINGS.back}</a>
        </p>
      </>
    );
  }

  return (
    <>
      <a className="skip-link" href="#main">
        {STRINGS.skip}
      </a>
      <header className="shell-header">
        <a className="brand" href="#/">
          {STRINGS.brand}
        </a>
        <nav aria-label={STRINGS.chapters}>
          <a href="#/" aria-current={route.kind === "list" ? "page" : undefined}>
            {STRINGS.chapters}
          </a>
        </nav>
        <label className="theme-picker">
          <span>{STRINGS.theme}</span>
          <select value={theme} onChange={(e) => setTheme(e.target.value as Theme)}>
            <option value="auto">{STRINGS.themeAuto}</option>
            <option value="light">{STRINGS.themeLight}</option>
            <option value="dark">{STRINGS.themeDark}</option>
          </select>
        </label>
      </header>
      <main id="main" className="shell-main" tabIndex={-1}>
        {page}
      </main>
      <footer className="shell-footer">
        <p>{STRINGS.footer}</p>
        <p className="copyright">{STRINGS.copyright}</p>
      </footer>
    </>
  );
}
