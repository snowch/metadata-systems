// Copyright © 2026 Christopher Snow

// A JupyterLab extension for the chapter's JupyterLite site: a row of large buttons above every
// notebook's cells. Run all runs every cell, Run below runs the selected cell and every cell below
// it, and Save saves the notebook. On a phone the menus at the top of the page open when tapped but
// their items do nothing, and the toolbar's buttons are 21 pixels tall; these are 44
// (docs/notes/notebook-prototype.md). The labels are in buttons.json, which
// notebook/tests/test_jupyterlite.py checks against the buttons the chapter's texts name.
//
// JupyterLab's own Run All and Run All Below select the last cell and scroll to it, so a reader who
// presses one at the top of a long notebook is taken to its end. These buttons run the same cells
// with the selection kept, and Run all first selects a cell that starts in view: JupyterLab
// scrolls to the selected cell after a run only when it is out of view.

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
  for (const [action, label] of Object.entries(labels)) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ms-Buttons-button";
    button.textContent = label;
    // As the toolbar's buttons do, leave the focus in the notebook, so that its keyboard
    // shortcuts still work after a press.
    button.addEventListener("mousedown", (event) => event.preventDefault());
    button.addEventListener("click", () => {
      Promise.resolve(actions[action](panel, app)).catch((reason) => console.error(label, reason));
    });
    widget.node.append(button);
  }
  return widget;
}

export default {
  id: "ms-notebook-buttons:row",
  description:
    "Adds a row of large Run all, Run below and Save buttons above every notebook's cells.",
  autoStart: true,
  requires: [INotebookTracker],
  activate(app, tracker) {
    const add = (panel) => panel.contentHeader.addWidget(row(app, panel));
    tracker.forEach(add);
    tracker.widgetAdded.connect((_, panel) => add(panel));
  },
};
