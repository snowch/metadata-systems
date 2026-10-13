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
// With the toolbar hidden, nothing else on the page shows that Python is busy, and on a phone the
// first run waits several seconds for Python to start. So while a button's work is under way, the
// row's buttons are disabled and the pressed one shows a spinner (style/index.css).
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
// A link in the text to one of the notebook's own headings scrolls the notebook to that heading
// (followLinks, below), where JupyterLab's own handling lands it a screen away in a long notebook.

import { NotebookActions, INotebookTracker } from "@jupyterlab/notebook";
import { Widget } from "@lumino/widgets";
import labels from "./buttons.json";

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

const actions = {
  runAll(panel) {
    const notebook = panel.content;
    notebook.mode = "command";
    const index = cellInView(notebook);
    if (index >= 0) notebook.activeCellIndex = index;
    return NotebookActions.runCells(notebook, notebook.widgets, panel.sessionContext);
  },
  runBelow(panel) {
    const notebook = panel.content;
    const below = notebook.widgets.slice(Math.max(0, notebook.activeCellIndex));
    return NotebookActions.runCells(notebook, below, panel.sessionContext);
  },
  save(panel, app) {
    return app.commands.execute("docmanager:save");
  },
};

/** The row of buttons for one notebook. */
function row(app, panel) {
  const widget = new Widget();
  widget.addClass("ms-Buttons");
  const buttons = [];
  let pointer = "mouse";
  for (const [action, label] of Object.entries(labels)) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ms-Buttons-button";
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
      for (const b of buttons) b.disabled = true;
      button.setAttribute("aria-busy", "true");
      try {
        await actions[action](panel, app);
      } catch (reason) {
        console.error(label, reason);
      } finally {
        button.removeAttribute("aria-busy");
        for (const b of buttons) b.disabled = false;
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
    "Adds a row of large Run all, Run below and Save buttons above every notebook's cells, with arrows to the chapters either side, hides the menu bar and the notebook's toolbar, scrolls to a heading the text links to, and sends the notebooks' earlier names to their chapters.",
  autoStart: true,
  requires: [INotebookTracker],
  activate(app, tracker) {
    followMove(app);
    const add = (panel) => {
      panel.toolbar.setHidden(true);
      followLinks(panel.content);
      const widget = row(app, panel);
      panel.contentHeader.addWidget(widget);
      panel.context.ready
        .then(() => arrows(app, panel, widget))
        .catch((reason) => console.error("arrows", reason));
      // The menu bar's area in Jupyter Notebook's page, which its zen mode hides the same way.
      app.shell.menu?.setHidden(true);
    };
    tracker.forEach(add);
    tracker.widgetAdded.connect((_, panel) => add(panel));
  },
};
