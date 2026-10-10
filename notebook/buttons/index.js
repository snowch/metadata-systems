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

export default {
  id: "ms-notebook-buttons:row",
  description:
    "Adds a row of large Run all, Run below and Save buttons above every notebook's cells, and hides the menu bar and the notebook's toolbar.",
  autoStart: true,
  requires: [INotebookTracker],
  activate(app, tracker) {
    const add = (panel) => {
      panel.toolbar.setHidden(true);
      panel.contentHeader.addWidget(row(app, panel));
      // The menu bar's area in Jupyter Notebook's page, which its zen mode hides the same way.
      app.shell.menu?.setHidden(true);
    };
    tracker.forEach(add);
    tracker.widgetAdded.connect((_, panel) => add(panel));
  },
};
