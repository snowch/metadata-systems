// Copyright © 2026 Christopher Snow

// A JupyterLab extension for the chapter's JupyterLite site: a row of large buttons above every
// notebook's cells, in place of the menu bar and the notebook's toolbar, which it hides. Run all
// runs every cell, Run below runs the selected cell and every cell below it, and Save saves the
// notebook. On a phone the menus' items do nothing when tapped, and the toolbar's buttons are 21
// pixels tall; these are 44 (docs/notes/notebook-prototype.md). The labels are in buttons.json,
// which notebook/tests/test_jupyterlite.py checks against the buttons the chapter's texts name.
//
// JupyterLab's own Run All and Run All Below select the last cell and scroll to it, so a reader who
// presses one at the top of a long notebook is taken to its end. These buttons run the same cells
// with the selection kept, and Run all first selects a cell that starts in view: JupyterLab
// scrolls to the selected cell after a run only when it is out of view.
//
// With the toolbar hidden, nothing else on the page shows that Python is busy, and on a phone Python
// takes most of a minute to start. So while a run is under way, Run all and Run below are disabled
// (Save stays usable) and the pressed one shows a spinner; and a notice at the foot of the screen
// counts the cells that have run. A separate row below the controls reports Python startup,
// slow loading and failures, with an in-place retry (its words are in status.json).
//
// At the row's right end, an arrow to the chapter before and one to the chapter after. The row
// stays in view while the cells scroll, and the links the chapter's text gives are at its top and
// its end only. The chapters are the site's files named chapter_NN.ipynb, so a new chapter gains its
// arrows when its file is added. Chapter links open within the running page, preserving its Python worker.
// Modifier clicks still open independent tabs. Contents opens a chapter picker. Below 500 pixels the arrows show without their chapters'
// numbers, below 600 the contents link shows as an icon, and below 390 not at all, so that the row
// fits 360 pixels (style/index.css); the chapter's text links to the contents at its top and end.
//
// As the page opens, Python is started on the chapter's hidden setup cells (warmUp, below), so that
// on a slow phone the reader does not wait for it after pressing Run all.
//
// As a chapter opens, the published chapter is opened in place of a copy the reader saved before it
// was updated (update, below); a copy with changes of the reader's is kept under another name.
//
// A link in the text to one of the notebook's own headings scrolls the notebook to that heading
// (followLinks, below), where JupyterLab's own handling lands it a screen away in a long notebook.

import { DocumentManager, IDocumentManager } from "@jupyterlab/docmanager";
import { PageConfig, URLExt } from "@jupyterlab/coreutils";
import { NotebookActions, INotebookTracker } from "@jupyterlab/notebook";
import { Widget } from "@lumino/widgets";
import labels from "./buttons.json";
import words from "./status.json";
import { attachAnswers } from "./answers.js";
import { createStartup } from "./startup.js";
import { courseWorker } from "./service-worker.js";
import { attachReader } from "./reader.js";

// How much of a cell must show for JupyterLab not to scroll to it, in pixels: its notebook's
// scroll-down threshold, half a cell margin and one line.
const SHOWN = 28;

/** The index of the first cell that starts in view, or -1 if none does. */
function cellInView(notebook) {
  const view = notebook.node.getBoundingClientRect();
  return notebook.widgets.findIndex((cell) => {
    const { top } = cell.node.getBoundingClientRect();
    return top >= view.top && top <= view.bottom - SHOWN;
  });
}

/** Each notebook panel's state: its notice, whether Python is ready, and the last run asked for. */
const states = new WeakMap();

const actions = {
  runAll(panel) {
    states.get(panel).lastAction = "runAll";
    const notebook = panel.content;
    notebook.mode = "command";
    const index = cellInView(notebook);
    if (index >= 0) notebook.activeCellIndex = index;
    return NotebookActions.runCells(notebook, notebook.widgets, panel.sessionContext);
  },
  runBelow(panel) {
    states.get(panel).lastAction = "runBelow";
    const notebook = panel.content;
    const below = notebook.widgets.slice(Math.max(0, notebook.activeCellIndex));
    return NotebookActions.runCells(notebook, below, panel.sessionContext);
  },
  save(panel, app) {
    return app.commands.execute("docmanager:save");
  },
};

/** A notice at the foot of the screen counts completed cells. A queued run waits for startup;
    the separate startup row remains visible.
    It is a status for screen readers too, and lets taps through to the page beneath it. */
function notice(panel) {
  const node = document.createElement("div");
  node.className = "ms-Status";
  node.setAttribute("role", "status");
  node.setAttribute("aria-live", "polite");
  node.hidden = true;
  panel.node.append(node);
  let timer;
  return {
    show(text, { busy = false, briefly = false } = {}) {
      clearTimeout(timer);
      node.replaceChildren(...[].concat(text));
      node.classList.toggle("ms-Status-busy", busy);
      node.hidden = false;
      if (briefly)
        timer = setTimeout(() => (node.hidden = true), briefly === true ? 3000 : briefly);
    },
    hide() {
      clearTimeout(timer);
      node.hidden = true;
    },
  };
}

/** A cell the notice counts: a code cell the reader sees, not one of the hidden setup cells. */
const counted = (cell) => cell.model.type === "code" && !cell.model.getMetadata("ms")?.setup;

/** Runs cells with the notice counting them: a press before Python is ready says the cells will
    run when it is. */
async function run(panel, state, start) {
  const notebook = panel.content;
  const before = notebook.activeCellIndex;
  let done = 0;
  let total = 0;
  const count = (_, { notebook: ran, cell }) => {
    if (ran !== notebook || !counted(cell)) return;
    done += 1;
    state.notice.show(words.running.replace("{done}", done).replace("{total}", total), {
      busy: true,
    });
  };
  NotebookActions.executed.connect(count);
  try {
    // A run waits for the check for a newer chapter, which may replace the notebook's cells.
    await state.checked;
    if (!state.ready) {
      state.notice.show(words.waiting, { busy: true });
      if (!(await state.startup.ready())) {
        state.notice.hide();
        return;
      }
    }
    const promise = start();
    // The cells the action runs: every code cell, or those from the selected one down.
    const from = state.lastAction === "runAll" ? 0 : Math.max(0, before);
    total = notebook.widgets.slice(from).filter(counted).length;
    state.notice.show(words.running.replace("{done}", 0).replace("{total}", total), {
      busy: true,
    });
    const succeeded = await promise;
    state.notice.show(succeeded ? words.done : words.runFailed, {
      briefly: !succeeded ? 10_000 : true,
    });
  } finally {
    NotebookActions.executed.disconnect(count);
  }
}

/** The row of buttons for one notebook. */
function row(app, panel, state) {
  const widget = new Widget();
  widget.addClass("ms-Buttons");
  // The comparison view attaches its per-example controls after the published notebook is ready.
  if (CHAPTER.test(panel.context.path) || panel.context.path === "chapter_01b.ipynb") return widget;
  const buttons = [];
  let pointer = "mouse";
  for (const [action, label] of Object.entries(labels)) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ms-Buttons-button";
    button.dataset.action = action;
    button.textContent = label;
    button.addEventListener("pointerdown", (event) => {
      pointer = event.pointerType;
    });
    // As the toolbar's buttons do, a mouse press leaves the focus in the notebook, so that its
    // keyboard shortcuts still work; a touch is left to the browser.
    button.addEventListener("mousedown", (event) => {
      if (pointer === "mouse") event.preventDefault();
    });
    button.addEventListener("click", async () => {
      // A run disables the two run buttons, since a second run would collide with it; Save stays
      // usable. Saving disables only itself.
      const runs = action !== "save";
      const held = runs ? buttons.filter((b) => b.dataset.action !== "save") : [button];
      for (const b of held) b.disabled = true;
      button.setAttribute("aria-busy", "true");
      try {
        if (runs) await run(panel, state, () => actions[action](panel, app));
        else await actions[action](panel, app);
      } catch (reason) {
        if (runs) state.notice.show(words.runFailed, { briefly: 10_000 });
        console.error(label, reason);
      } finally {
        button.removeAttribute("aria-busy");
        for (const b of held) b.disabled = false;
      }
    });
    buttons.push(button);
    widget.node.append(button);
  }
  return widget;
}

const CHAPTER = /^chapter_(\d\d)\.ipynb$/;

/** Arrows to the chapters either side of the panel's, added to the row when the site's files are
    listed. */
async function arrows(app, panel, widget) {
  const path = panel.context.path
    .replace(/ \(your copy(?: \d+)?\)/, "")
    .replace("chapter_01b.ipynb", "chapter_01.ipynb");
  const own = CHAPTER.exec(path);
  if (!own) return;
  const listing = await app.serviceManager.contents.get("", { content: true });
  const chapters = listing.content
    .map((file) => file.name)
    .filter((name) => CHAPTER.test(name))
    .sort();
  const at = chapters.indexOf(path);
  const links = [
    [chapters[at - 1], "Previous", "\u2039"],
    [chapters[at + 1], "Next", "\u203a"],
  ];
  for (const [name, which, arrow] of links) {
    if (at < 0 || !name) continue;
    const number = Number(CHAPTER.exec(name)[1]);
    const link = document.createElement("a");
    link.className = `ms-Buttons-link ms-Buttons-${which.toLowerCase()}`;
    link.href = `${window.location.pathname}?path=${encodeURIComponent(name)}`;
    const sign = document.createElement("span");
    sign.className = "ms-Buttons-arrow";
    sign.textContent = arrow;
    const label = document.createElement("span");
    label.className = "ms-Buttons-number";
    label.textContent = String(number);
    link.append(...(which === "Next" ? [label, sign] : [sign, label]));
    link.setAttribute("aria-label", `${which}: Chapter ${number}`);
    link.title = `${which}: Chapter ${number}`;
    widget.node.append(link);
    if (which === "Previous") widget.node.append(contents());
  }
  if (!widget.node.querySelector(".ms-Buttons-contents")) {
    widget.node.querySelector(".ms-Buttons-next")?.before(contents());
  }
}

/** A link to the course's contents, for the place between the arrows. The site's notebooks open at
    notebooks/index.html inside the site, which the course's front page holds at jupyterlite/ (the
    deploy workflow), so the contents are two folders up. Its name is the text's own link's. */
function contents() {
  const link = document.createElement("a");
  link.className = "ms-Buttons-link ms-Buttons-contents";
  link.href = new URL("../../", window.location.href).href;
  link.target = "_blank";
  // The word on a wide screen, and on a narrower one a list's three lines (style/index.css).
  const text = document.createElement("span");
  text.className = "ms-Buttons-contents-text";
  text.textContent = "Contents";
  const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  icon.setAttribute("class", "ms-Buttons-contents-icon");
  icon.setAttribute("viewBox", "0 0 18 18");
  icon.setAttribute("aria-hidden", "true");
  for (const y of [4, 9, 14]) {
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    for (const [k, v] of Object.entries({ x1: 2, x2: 16, y1: y, y2: y })) line.setAttribute(k, v);
    icon.append(line);
  }
  link.append(text, icon);
  link.setAttribute("aria-label", "Back to contents");
  link.title = "Back to contents";
  return link;
}

/** Starts Python, then prepares the chapter. Retry replaces the worker in the existing session;
    it never reloads the page or discards notebook edits. The service worker reports actual
    runtime bytes; kernel readiness and chapter preparation remain separate stages. */
async function warmUp(app, panel, state, { retry, active, preparing, signal }) {
  await panel.context.ready;
  await state.checked;
  if (!active()) return;
  if (retry) {
    const name =
      panel.sessionContext.session?.kernel?.name ||
      panel.context.model.getMetadata("kernelspec")?.name;
    if (!name) throw new Error("No Python kernel configured");
    const previous = panel.sessionContext.session?.kernel?.id;
    await panel.sessionContext.changeKernel({ name });
    // JupyterLite 0.8.6 starts a new worker but does not shut down the replaced one.
    if (previous && previous !== panel.sessionContext.session?.kernel?.id)
      await app.serviceManager.kernels.shutdown(previous);
  } else {
    await panel.sessionContext.ready;
  }
  if (!active()) return;
  const kernel = panel.sessionContext.session?.kernel;
  if (!kernel) throw new Error("Python did not start");
  let died;
  let aborted;
  const dead = new Promise((_, reject) => {
    aborted = () => reject(new Error("Startup cancelled"));
    signal.addEventListener("abort", aborted, { once: true });
    died = (_, status) => {
      if (status === "dead") reject(new Error("Python stopped during startup"));
    };
    kernel.statusChanged.connect(died);
    died(null, kernel.status);
  });
  try {
    await Promise.race([kernel.info, dead]);
    if (!active()) return;
    preparing();
    const code =
      (state.reused ? "%reset -f\n" : "") +
      panel.content.widgets
        .filter((cell) => cell.model.type === "code" && cell.model.getMetadata("ms")?.setup)
        .map((cell) => cell.model.sharedModel.getSource())
        .join("\n\n");
    if (code) {
      const reply = await Promise.race([
        kernel.requestExecute({ code, silent: true, store_history: false }).done,
        dead,
      ]);
      if (reply.content.status !== "ok") throw new Error("Chapter setup failed");
    }
  } finally {
    kernel.statusChanged.disconnect(died);
    signal.removeEventListener("abort", aborted);
  }
}

/** Startup stays below the controls, leaving the chapter and its answer fields usable. It has
    its own status region so a chapter-update notice or queued run cannot erase a failure. */
function startup(app, panel, state) {
  const widget = new Widget();
  widget.addClass("ms-Startup");
  const body = document.createElement("div");
  body.className = "ms-Startup-content";
  const status = document.createElement("div");
  status.setAttribute("role", "status");
  status.setAttribute("aria-live", "polite");
  status.setAttribute("aria-atomic", "true");
  const message = document.createElement("div");
  const detail = document.createElement("div");
  detail.className = "ms-Startup-detail";
  const progress = document.createElement("progress");
  progress.className = "ms-Startup-progress";
  progress.max = 100;
  progress.hidden = true;
  status.append(message, progress, detail);
  const retry = document.createElement("button");
  retry.type = "button";
  retry.className = "ms-Startup-retry";
  retry.textContent = words.retry;
  retry.hidden = true;
  const elapsedTimer = document.createElement("div");
  elapsedTimer.className = "ms-Startup-detail";
  elapsedTimer.setAttribute("role", "timer");
  elapsedTimer.setAttribute("aria-live", "off");
  elapsedTimer.hidden = true;
  body.append(status, elapsedTimer, retry);
  widget.node.append(body);
  panel.contentHeader.addWidget(widget);
  // Lumino lays out the header using each widget's explicit limits. Observe the content so
  // wrapped messages at phone widths reserve their height instead of covering the notebook.
  const size = new ResizeObserver(() => {
    if (widget.isHidden || panel.isDisposed) return;
    const height = `${Math.ceil(body.getBoundingClientRect().height)}px`;
    widget.node.style.minHeight = height;
    widget.node.style.maxHeight = height;
    panel.contentHeader.fit();
  });
  size.observe(body);
  const controller = createStartup({
    start: (attempt) => warmUp(app, panel, state, attempt),
    render({ phase, slow, stalled, download, elapsed }) {
      if (panel.isDisposed) return;
      state.ready = phase === "ready" || phase === "hidden";
      widget.setHidden(phase === "hidden");
      widget.node.dataset.phase = phase;
      widget.node.classList.toggle("ms-Startup-busy", phase === "loading" || phase === "preparing");
      const text =
        phase === "loading" && download
          ? download.percent === 100
            ? words.runtimeDownloaded
            : words.downloadingRuntime.replace("{percent}", download.percent)
          : words[phase] || "";
      if (message.textContent !== text) message.textContent = text;
      elapsedTimer.hidden = elapsed === undefined || (phase !== "loading" && phase !== "preparing");
      elapsedTimer.textContent = elapsedTimer.hidden
        ? ""
        : words.elapsed.replace("{seconds}", elapsed);
      progress.hidden = phase !== "loading" || !download || download.percent === 100;
      if (download) {
        progress.value = download.percent;
        progress.setAttribute("aria-label", message.textContent);
        widget.node.dataset.percent = String(download.percent);
      } else delete widget.node.dataset.percent;
      const detailText =
        phase === "loading" || phase === "preparing"
          ? stalled
            ? words.stalled
            : slow
              ? words.slow
              : ""
          : "";
      if (detail.textContent !== detailText) detail.textContent = detailText;
      detail.hidden = !detail.textContent;
      retry.hidden =
        phase !== "failed" && !((phase === "loading" || phase === "preparing") && stalled);
    },
  });
  const downloadMessage = (event) => {
    if (
      event.data?.type === "MS_PYTHON_DOWNLOAD" &&
      event.source?.scriptURL &&
      new URL(event.source.scriptURL).origin === window.location.origin
    )
      controller.download(event.data);
  };
  navigator.serviceWorker?.addEventListener("message", downloadMessage);
  retry.addEventListener("click", () => {
    // Remove focus from the button before hiding it; a keyboard user keeps focus in this region.
    widget.node.tabIndex = -1;
    widget.node.focus();
    void controller.begin(true);
  });
  panel.disposed.connect(() => {
    controller.dispose();
    navigator.serviceWorker?.removeEventListener("message", downloadMessage);
    size.disconnect();
  });
  return controller;
}

/** A heading's address in a link, as JupyterLab writes it: its words with each space a hyphen. */
const anchor = (text) =>
  text
    .replace(/\u00b6$/, "")
    .trim()
    .replace(/ /g, "-");

/** Links in the text to a heading of the same notebook (Chapter 2's to its stages). JupyterLab
    scrolls to one by its estimate of the height of the cells it has not drawn, so in a long
    notebook the heading lands far from the top of the view, and not twice in the same place. This
    finds the heading's cell from the notebook's own text, scrolls to it, and, as the cells around it
    are drawn and change height, moves the view until the heading stays just below its top. */
function followLinks(notebook) {
  notebook.node.addEventListener(
    "click",
    (event) => {
      const link = event.target.closest?.('.jp-RenderedMarkdown a[href^="#"]');
      if (!link) return;
      const id = decodeURIComponent(link.getAttribute("href").slice(1));
      const index = notebook.widgets.findIndex(
        (cell) =>
          cell.model.type === "markdown" &&
          cell.model.sharedModel
            .getSource()
            .split("\n")
            .some((line) => /^#{1,6} /.test(line) && anchor(line.replace(/^#{1,6} /, "")) === id),
      );
      if (index < 0) return;
      event.preventDefault();
      event.stopPropagation();
      goTo(notebook, index, id).catch((reason) => console.error("link", reason));
    },
    true,
  );
}

async function goTo(notebook, index, id) {
  const outer = notebook.node.classList.contains("jp-WindowedPanel-outer")
    ? notebook.node
    : (notebook.node.querySelector(".jp-WindowedPanel-outer") ?? notebook.node);
  const pause = () => new Promise((resolve) => setTimeout(resolve, 80));
  await notebook.scrollToItem(index, "start");
  let still = 0;
  for (let i = 0; i < 40 && still < 3; i += 1) {
    await pause();
    const cell = notebook.widgets[index];
    const heading = [...cell.node.querySelectorAll("h1, h2, h3, h4, h5, h6")].find(
      (h) => anchor(h.textContent) === id,
    );
    if (!heading) {
      await notebook.scrollToItem(index, "start");
      continue;
    }
    const off = heading.getBoundingClientRect().top - outer.getBoundingClientRect().top - 8;
    if (Math.abs(off) <= 2) still += 1;
    else {
      still = 0;
      outer.scrollTop += off;
    }
  }
}

/** The notebook's cells as one text, as the build hashes them (build_ipynb.py, cells_text). */
const sourcesOf = (cells) =>
  cells.map((cell) => `${cell.cell_type}\n${[].concat(cell.source).join("")}\0`).join("");

/** The first 16 hexadecimal digits of a text's SHA-256, as the build writes them. */
async function digest(text) {
  const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return Array.from(new Uint8Array(bytes), (b) => b.toString(16).padStart(2, "0"))
    .join("")
    .slice(0, 16);
}

/** A name for the reader's copy that no file has yet: "chapter_02 (your copy).ipynb", then
    "chapter_02 (your copy 2).ipynb", and so on. */
async function freeName(contents, path) {
  const stem = path.replace(/\.ipynb$/, "");
  for (let n = 1; ; n += 1) {
    const name = `${stem} (your copy${n > 1 ? ` ${n}` : ""}).ipynb`;
    const taken = await contents.get(name, { content: false }).then(
      () => true,
      () => false,
    );
    if (!taken) return name;
  }
}

/** Opens the published chapter when it is newer than the one the page shows. JupyterLite keeps a
    notebook the reader saved in the browser (autosave included), and shows that copy instead of the
    published chapter, even after the chapter is updated; a browser may also hold the published
    file for a while. So, as the notebook opens, this fetches the published chapter, past the
    browser's cache, and compares the versions the build stamps in both (build_ipynb.py, stamp). If
    they differ, the reader's copy is set aside and the published chapter is opened in its place.
    A copy in which the reader changed any cell, or one saved before the stamp existed, is kept
    first under another name, and the notice says which; a copy with no change of the reader's is
    only outputs, which a run makes again. */
async function update(app, panel, state) {
  await panel.context.ready;
  const path = panel.context.path;
  if (!CHAPTER.test(path) && path !== "chapter_01b.ipynb") return;
  const response = await fetch(URLExt.join(PageConfig.getBaseUrl(), "files", path), {
    cache: "no-cache",
  });
  if (!response.ok) return;
  const publishedNotebook = await response.json();
  const published = publishedNotebook.metadata?.ms?.version;
  const open = panel.context.model.getMetadata("ms")?.version;
  if (!published || published === open) return;
  const contents = app.serviceManager.contents;
  const storage = await contents.defaultDrive.storage;
  const saved = await storage?.getItem(path);
  let copy = null;
  if (saved?.content?.cells) {
    const own = saved.content.metadata?.ms?.sources;
    if (own !== (await digest(sourcesOf(saved.content.cells)))) {
      copy = await freeName(contents, path);
      await contents.save(copy, { type: "notebook", format: "json", content: saved.content });
    }
    // Import code from the previous notebook UI before replacing its document. Existing reader
    // drafts take precedence; the archived notebook remains available as an additional backup.
    if (publishedNotebook.metadata?.ms?.reader && !saved.content.metadata?.ms?.reader) {
      state.legacyDrafts = new Map();
      for (const cell of publishedNotebook.cells) {
        const example = cell.metadata?.ms?.example;
        if (!example || example.editable === false) continue;
        const old = saved.content.cells.find(
          (item) => item.id === cell.id && item.cell_type === "code",
        );
        if (!old) continue;
        const source = [].concat(old.source).join("");
        if (source === example.source) continue;
        state.legacyDrafts.set(example.id, source);
        try {
          const key = `ms:metadata-systems:code:v1:${path}:${example.id}`;
          if (localStorage.getItem(key) === null) localStorage.setItem(key, source);
        } catch {
          /* The live draft and archived notebook remain exportable if storage is full. */
        }
      }
    }
    await contents.delete(path);
  }
  await panel.context.revert();
  const shown = copy ? 10_000 : 5_000;
  if (copy) {
    // The copy's name is a link that opens it in a new tab, as the arrows open their chapters.
    const link = document.createElement("a");
    link.href = `${window.location.pathname}?path=${encodeURIComponent(copy)}`;
    link.target = "_blank";
    link.rel = "noopener";
    link.textContent = copy;
    const [before, after] = words.kept.split("{copy}");
    state.notice.show([before, link, after], { briefly: shown });
  } else state.notice.show(words.updated, { briefly: shown });
}

const MOVED = {
  "chapter_01_part_1.ipynb": "chapter_01.ipynb",
  "chapter_01_part_2.ipynb": "chapter_02.ipynb",
};

/** Sends a page opened at an earlier name to the chapter's name, unless the reader saved a copy
    under the earlier name: JupyterLite keeps that copy in the browser, and it opens as before. */
function followMove(app) {
  const params = new URLSearchParams(window.location.search);
  const moved = MOVED[params.get("path")];
  if (!moved) return;
  app.serviceManager.contents.get(params.get("path"), { content: false }).catch(() => {
    params.set("path", moved);
    window.location.replace(`${window.location.pathname}?${params}`);
  });
}

const rowPlugin = {
  id: "ms-notebook-buttons:row",
  description:
    "Run and reset examples, autosave code locally, track Python loading and navigate chapters with the existing notebook editors and outputs.",
  autoStart: true,
  requires: [INotebookTracker, IDocumentManager],
  activate(app, tracker, initialDocuments) {
    // Reader drafts and answers save independently of the notebook file.
    initialDocuments.autosave = false;
    followMove(app);
    let navigating = false;
    let reused = false;
    const documents = new DocumentManager({
      registry: app.docRegistry,
      manager: app.serviceManager,
      opener: {
        open: (widget) => {
          const previous = app.shell.currentWidget;
          if (previous && previous !== widget) previous.parent = null;
          app.shell.add(widget, "main");
          widget.activate();
        },
      },
    });
    documents.autosave = false;
    const navigate = async (path, history = true) => {
      if (navigating) return;
      const previous = app.shell.currentWidget;
      if (!previous || previous.context.path === path) return;
      navigating = true;
      try {
        const state = states.get(previous);
        if (!(await state.startup.ready())) return;
        const kernel = previous.sessionContext.session.kernel;
        while (kernel.status !== "idle" || state.busy) {
          if (previous.isDisposed || kernel.status === "dead") return;
          await new Promise((resolve) => setTimeout(resolve, 100));
        }
        previous.sessionContext.kernelPreference = {
          ...previous.sessionContext.kernelPreference,
          shutdownOnDispose: false,
        };
        reused = true;
        const panel = documents.open(
          path,
          "default",
          { id: kernel.id },
          {},
          { shutdownOnDispose: false },
        );
        if (!panel) throw new Error("Could not open chapter");
        await panel.context.ready;
        await states.get(panel).surface;
        await states.get(panel).startup.ready();
        previous.dispose();
        if (history)
          window.history.pushState(
            {},
            "",
            `${window.location.pathname}?path=${encodeURIComponent(path)}`,
          );
        panel.content.node.scrollTop = 0;
      } catch (error) {
        console.error("chapter navigation", error);
      } finally {
        reused = false;
        navigating = false;
      }
    };
    const chapterContents = document.createElement("dialog");
    chapterContents.className = "ms-ChapterContents";
    chapterContents.setAttribute("aria-label", "Contents");
    const closeContents = document.createElement("button");
    closeContents.textContent = "Close contents";
    closeContents.addEventListener("click", () => chapterContents.close());
    const courseHome = contents();
    courseHome.className = "ms-CourseHome";
    courseHome.textContent = "Course home and offline downloads (new tab)";
    chapterContents.append(closeContents, courseHome);
    document.body.append(chapterContents);
    let contentsLoaded = false;
    const showContents = async () => {
      chapterContents.showModal();
      if (contentsLoaded) return;
      const listing = await app.serviceManager.contents.get("", { content: true });
      for (const file of listing.content
        .filter((file) => CHAPTER.test(file.name))
        .sort((a, b) => a.name.localeCompare(b.name))) {
        const link = document.createElement("a");
        link.href = `${window.location.pathname}?path=${encodeURIComponent(file.name)}`;
        link.textContent = `Chapter ${Number(CHAPTER.exec(file.name)[1])}`;
        chapterContents.append(link);
        void app.serviceManager.contents
          .get(file.name, { content: true })
          .then((model) => {
            const heading = model.content.cells
              .flatMap((cell) => [].concat(cell.source).join("").split("\n"))
              .find((line) => line.startsWith("# "));
            if (heading) link.textContent = heading.slice(2);
          })
          .catch(console.error);
      }
      contentsLoaded = true;
    };
    window.addEventListener(
      "click",
      (event) => {
        if (
          event.defaultPrevented ||
          event.button !== 0 ||
          event.ctrlKey ||
          event.metaKey ||
          event.shiftKey ||
          event.altKey
        )
          return;
        const link = event.target.closest?.("a[href]");
        if (
          !link ||
          link.classList.contains("ms-CourseHome") ||
          link.getAttribute("href").startsWith("#")
        )
          return;
        const url = new URL(link.href, window.location.href);
        if (
          url.origin === window.location.origin &&
          (link.classList.contains("ms-Buttons-contents") ||
            url.href === new URL("../../", window.location.href).href)
        ) {
          event.preventDefault();
          event.stopImmediatePropagation();
          void showContents().catch(console.error);
          return;
        }
        const path =
          url.searchParams.get("path") ||
          (link.closest(".jp-RenderedMarkdown") && url.origin === window.location.origin
            ? url.pathname.split("/").at(-1)
            : null);
        if (
          url.origin !== window.location.origin ||
          (!link.closest(".jp-RenderedMarkdown") && url.pathname !== window.location.pathname) ||
          !/^chapter_\d\d[b]?\.ipynb$/.test(path || "")
        )
          return;
        event.preventDefault();
        event.stopImmediatePropagation();
        chapterContents.close();
        link.setAttribute("aria-busy", "true");
        void navigate(path).finally(() => link.removeAttribute("aria-busy"));
      },
      true,
    );
    window.addEventListener("popstate", () => {
      const path = new URLSearchParams(window.location.search).get("path");
      if (/^chapter_\d\d[b]?\.ipynb$/.test(path || "")) void navigate(path, false);
    });
    const add = (panel) => {
      panel.toolbar.setHidden(true);
      followLinks(panel.content);
      const state = {
        notice: notice(panel),
        ready: false,
        lastAction: null,
        reused,
      };
      state.checked = update(app, panel, state).catch((reason) => console.error("update", reason));
      attachAnswers(app, panel, state.checked).catch((reason) => console.error("answers", reason));
      states.set(panel, state);
      const widget = row(app, panel, state);
      panel.contentHeader.addWidget(widget);
      state.surface = panel.context.ready
        .then(async () => {
          await state.checked;
          if (panel.context.model.getMetadata("ms")?.reader)
            await attachReader(panel, state, widget);
          app.shell.fit();
          await arrows(app, panel, widget);
        })
        .catch((reason) => console.error("arrows", reason));
      state.startup = startup(app, panel, state);
      void state.startup.begin();
      // The menu bar's area in Jupyter Notebook's page, which its zen mode hides the same way.
      app.shell.menu?.setHidden(true);
    };
    tracker.forEach(add);
    tracker.widgetAdded.connect((_, panel) => add(panel));
    tracker.currentChanged.connect((_, panel) => {
      document.body.classList.toggle(
        "ms-Reading",
        !!app.shell.currentWidget?.hasClass("ms-ReaderPanel"),
      );
      app.shell.fit();
    });
  },
};

export default [rowPlugin, courseWorker];
