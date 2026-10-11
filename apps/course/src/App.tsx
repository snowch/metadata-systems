// Copyright © 2026 Christopher Snow

// The course shell: header, the front page, footer. Every chapter is a notebook in the site's
// JupyterLite pages, which the front page links; the shell knows nothing about metadata. An
// address of a chapter's former page (#/chapter/<id>) leads to the chapter's notebook.

import { useEffect } from "react";

import { CHAPTER_PAGES, NOTEBOOKS, notebookHref } from "@ms/content";

import { fill } from "./fill";
import { FrontPage } from "./pages/FrontPage";
import { useRoute } from "./route";
import { STRINGS } from "./strings";
import { useTheme, type Theme } from "./theme";

export function App() {
  const route = useRoute();
  const [theme, setTheme] = useTheme();
  const file =
    route.kind === "chapter" ? NOTEBOOKS.get(CHAPTER_PAGES.get(route.id) ?? 0) : undefined;
  useEffect(() => {
    if (file) window.location.replace(notebookHref(import.meta.env.BASE_URL, file));
  }, [file]);

  let page: React.ReactNode;
  if (route.kind === "list") page = <FrontPage />;
  else if (file) page = null;
  else
    page = (
      <>
        <h1>{fill(STRINGS.missing, { path: route.kind === "chapter" ? route.id : route.path })}</h1>
        <p>
          <a href="#/">{STRINGS.back}</a>
        </p>
      </>
    );

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
