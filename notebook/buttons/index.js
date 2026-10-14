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
// says what Python is doing, from the moment the page opens: starting, ready, or how many cells
// have run (its words are in status.json).
//
// At the row's right end, an arrow to the chapter before and one to the chapter after. The row
// stays in view while the cells scroll, and the links the chapter's text gives are at its top and
// its end only. The chapters are the site's files named chapter_NN.ipynb, so a new chapter gains its
// arrows when its file is added. Each arrow is a link that opens its chapter in a new tab, as the
// text's links do; their names are the text's links' own words. Between them, a link to the course's
// contents, which opens in a new tab too. Below 500 pixels the arrows show without their chapters'
// numbers, below 600 the contents link shows as an icon, and below 390 not at all, so that the row
// fits 360 pixels (style/index.css); the chapter's text links to the contents at its top and end.
//
// As the page opens, Python is started on the chapter's hidden setup cells (warmUp, below), so that
// on a slow phone the reader does not wait for it after pressing Run all.
//
// A link in the text to one of the notebook's own headings scrolls the notebook to that heading
// (followLinks, below), where JupyterLab's own handling lands it a screen away in a long notebook.

import { NotebookActions, INotebookTracker } from "@jupyterlab/notebook";
import { Widget } from "@lumino/widgets";
import labels from "./buttons.json";
import words from "./status.json";

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

/** A notice at the foot of the screen that says what Python is doing: starting, ready, how many
    cells have run. On a phone Python takes most of a minute to start, and a press of Run all before
    then waits for it; without the notice, the page looks stuck. It is a status for screen readers
    too, and lets taps through to the page beneath it. */
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
      node.textContent = text;
      node.classList.toggle("ms-Status-busy", busy);
      node.hidden = false;
      if (briefly) timer = setTimeout(() => (node.hidden = true), 3000);
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
  state.runs += 1;
  try {
    const promise = start();
    // The cells the action runs: every code cell, or those from the selected one down.
    const from = state.lastAction === "runAll" ? 0 : Math.max(0, before);
    total = notebook.widgets.slice(from).filter(counted).length;
    if (!state.ready) state.notice.show(words.waiting, { busy: true });
    else
      state.notice.show(words.running.replace("{done}", 0).replace("{total}", total), {
        busy: true,
      });
    await promise;
    state.ready = true;
    state.notice.show(words.done, { briefly: true });
  } finally {
    NotebookActions.executed.disconnect(count);
  }
}

/** The row of buttons for one notebook. */
function row(app, panel, state) {
  const widget = new Widget();
  widget.addClass("ms-Buttons");
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
  const own = CHAPTER.exec(panel.context.path);
  if (!own) return;
  const listing = await app.serviceManager.contents.get("", { content: true });
  const chapters = listing.content
    .map((file) => file.name)
    .filter((name) => CHAPTER.test(name))
    .sort();
  const at = chapters.indexOf(panel.context.path);
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
    link.target = "_blank";
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

// The notebooks' names until 11 October 2026, when the two parts of Chapter 1 became Chapters 1 and
// 2, and the names they have now.
/** Starts Python on the chapter's setup as the page opens. Python starts in the browser when the
    notebook opens, but the setup cells (installing the shop's package, the imports and the shop's
    week) wait for Run all, and on a slow phone they take most of a minute. This sends their code
    to Python as soon as it is up, silently: no cell runs, nothing is printed and no cell's count
    changes. When the reader presses Run all, the setup cells run again, now in a moment, and a
    press before the warm-up ends waits for it; a press before Python is even up runs the setup
    itself, and the warm-up stands aside. A notebook without marked setup cells (one a
    reader saved before the mark existed) is left as it is. */
async function warmUp(panel, state) {
  state.notice.show(words.starting, { busy: true });
  await panel.context.ready;
  await panel.sessionContext.ready;
  const kernel = panel.sessionContext.session?.kernel;
  if (!kernel) return state.notice.hide();
  const code = panel.content.widgets
    .filter((cell) => cell.model.type === "code" && cell.model.getMetadata("ms")?.setup)
    .map((cell) => cell.model.sharedModel.getSource())
    .join("\n\n");
  await kernel.info;
  // A run the reader started before Python was up queued its cells first, and they do the setup
  // themselves: the warm-up would only repeat it after them.
  if (code && !state.runs)
    await kernel.requestExecute({ code, silent: true, store_history: false }).done;
  state.ready = true;
  // Once the reader has run anything, the notice is the run's.
  if (!state.runs) state.notice.show(words.ready, { briefly: true });
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

export default {
  id: "ms-notebook-buttons:row",
  description:
    "Adds a row of large Run all, Run below and Save buttons above every notebook's cells, with arrows to the chapters either side, hides the menu bar and the notebook's toolbar, starts Python on the chapter's setup as it opens, scrolls to a heading the text links to, and sends the notebooks' earlier names to their chapters.",
  autoStart: true,
  requires: [INotebookTracker],
  activate(app, tracker) {
    followMove(app);
    const add = (panel) => {
      panel.toolbar.setHidden(true);
      followLinks(panel.content);
      const state = { notice: notice(panel), ready: false, runs: 0, lastAction: null };
      states.set(panel, state);
      const widget = row(app, panel, state);
      panel.contentHeader.addWidget(widget);
      panel.context.ready
        .then(() => arrows(app, panel, widget))
        .catch((reason) => console.error("arrows", reason));
      warmUp(panel, state).catch((reason) => {
        state.ready = true;
        state.notice.hide();
        console.error("warm-up", reason);
      });
      // The menu bar's area in Jupyter Notebook's page, which its zen mode hides the same way.
      app.shell.menu?.setHidden(true);
    };
    tracker.forEach(add);
    tracker.widgetAdded.connect((_, panel) => add(panel));
  },
};
