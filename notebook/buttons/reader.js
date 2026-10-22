// Copyright © 2026 Christopher Snow

// A small reading surface over Jupyter's existing code editors, outputs and Python session.
// Only notebooks explicitly marked ms.reader opt in. Drafts are synchronous and independent of
// notebook autosave, so refresh before the first execution does not lose a reader's changes.
import { NotebookActions } from "@jupyterlab/notebook";
import { Widget } from "@lumino/widgets";
import words from "./reader-words.json";

const prefix = "ms:metadata-systems:code:v1:";
const element = (tag, text, className) => {
  const node = document.createElement(tag);
  if (text) node.textContent = text;
  if (className) node.className = className;
  return node;
};
const button = (text) => {
  const node = element("button", text, "ms-Buttons-button");
  node.type = "button";
  return node;
};

export async function attachReader(panel, state, navigation) {
  const notebook = panel.content;
  panel.addClass("ms-ReaderPanel");
  document.body.classList.add("ms-Reading");
  notebook.addClass("ms-Reader");
  notebook.notebookConfig = {
    ...notebook.notebookConfig,
    windowingMode: "none",
    showEditorForReadOnlyMarkdown: false,
    showHiddenCellsButton: false,
    scrollPastEnd: false,
  };
  navigation.node.replaceChildren();
  navigation.addClass("ms-Reader-nav");
  const entries = [];
  let busy = false;
  let disposed = false;
  const hold = (value) => {
    busy = value;
    for (const entry of entries) {
      entry.run.disabled = value;
      entry.reset.disabled = value;
    }
  };

  async function execute(entry) {
    if (busy || disposed) return;
    hold(true);
    entry.run.setAttribute("aria-busy", "true");
    entry.status.textContent = state.ready ? words.running : words.queued;
    try {
      if (!(await state.startup.ready()) || disposed) {
        if (!disposed) entry.status.textContent = words.startupFailed;
        return;
      }
      entry.status.textContent = words.running;
      // Capture what is actually run, after any edits made while Python was loading.
      const source = entry.cell.model.sharedModel.getSource();
      const outer = notebook.node;
      const top = outer.scrollTop;
      notebook.activeCellIndex = notebook.widgets.indexOf(entry.cell);
      const succeeded = await NotebookActions.runCells(
        notebook,
        [entry.cell],
        panel.sessionContext,
      );
      if (disposed) return;
      outer.scrollTop = top;
      entry.executed = source;
      entry.status.textContent =
        source !== entry.cell.model.sharedModel.getSource()
          ? words.stale
          : succeeded
            ? words.success
            : words.error;
    } catch {
      if (!disposed) entry.status.textContent = words.error;
    } finally {
      entry.run.removeAttribute("aria-busy");
      hold(false);
    }
  }

  for (const cell of notebook.widgets) {
    cell.model.setMetadata("deletable", false);
    const example = cell.model.getMetadata("ms")?.example;
    if (!example) {
      cell.readOnly = true;
      if (cell.model.type === "markdown") cell.rendered = true;
      continue;
    }
    await cell.ready;
    if (panel.isDisposed) return;
    cell.addClass("ms-Example");
    cell.node.dataset.example = example.id;
    const key = `${prefix}${panel.context.path}:${example.id}`;
    const shared = cell.model.sharedModel;
    const controls = new Widget();
    controls.addClass("ms-Example-controls");
    const run = button(words.run);
    const reset = button(words.reset);
    run.dataset.readerAction = "run";
    reset.dataset.readerAction = "reset";
    const saveStatus = element("span", "", "ms-Example-saved");
    saveStatus.setAttribute("role", "status");
    const statusWidget = new Widget();
    statusWidget.addClass("ms-Example-status");
    const status = element("span");
    status.setAttribute("role", "status");
    statusWidget.node.append(status);
    controls.node.append(run, reset, saveStatus);
    cell.layout.insertWidget(0, controls);
    cell.layout.addWidget(statusWidget);
    const entry = { cell, run, reset, status, executed: null };
    entries.push(entry);
    cell.model.outputs.clear();
    cell.model.executionCount = null;
    // A reset is stored too, so an older notebook autosave cannot resurrect a discarded edit.
    try {
      const saved = localStorage.getItem(key);
      shared.setSource(saved ?? example.source);
      saveStatus.textContent = saved === null ? words.noSavedEdits : words.saved;
    } catch {
      saveStatus.textContent = words.saveFailed;
    }
    let previous = shared.getSource();
    const changed = () => {
      const source = shared.getSource();
      if (source === previous) return;
      previous = source;
      try {
        localStorage.setItem(key, source);
        saveStatus.textContent = words.saved;
      } catch {
        saveStatus.textContent = words.saveFailed;
      }
      if (entry.executed !== null) status.textContent = words.stale;
    };
    cell.model.contentChanged.connect(changed);
    panel.disposed.connect(() => cell.model.contentChanged.disconnect(changed));
    const editor = cell.node.querySelector(".cm-content");
    editor?.setAttribute("aria-label", words.editorLabel.replace("{example}", example.title));
    run.addEventListener("click", () => void execute(entry));
    reset.addEventListener("click", () => {
      if (busy) return;
      shared.setSource(example.source);
      cell.model.outputs.clear();
      cell.model.executionCount = null;
      entry.executed = null;
      status.textContent = words.restored;
    });
  }

  const download = button(words.downloadCode);
  download.addEventListener("click", () => {
    const source = entries
      .map(
        ({ cell }) =>
          `# ${cell.model.getMetadata("ms").example.title}\n${cell.model.sharedModel.getSource()}\n`,
      )
      .join("\n");
    const url = URL.createObjectURL(new Blob([source], { type: "text/x-python;charset=utf-8" }));
    const link = element("a");
    link.href = url;
    link.download = panel.context.path.replace(/\.ipynb$/, "-examples.py");
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  navigation.node.append(download);

  // Keep normal editing, text selection and browser navigation. Notebook structural shortcuts
  // and the context menu are not part of this reading surface. Run shortcuts execute one example.
  const shortcut = (event) => {
    if (!panel.node.contains(event.target)) return;
    const cell = event.target.closest?.(".ms-Example");
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey || event.shiftKey)) {
      event.preventDefault();
      event.stopImmediatePropagation();
      const entry = entries.find((item) => item.cell.node === cell);
      if (entry) void execute(entry);
    }
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {
      event.preventDefault();
      event.stopImmediatePropagation();
    }
    // Lumino's global shortcuts listen before notebook bubbling. A window capture guard keeps
    // command-mode keystrokes on prose out of the document editor while retaining browser defaults.
    if (!event.target.closest?.(".cm-editor, input, textarea, button, select, a"))
      event.stopImmediatePropagation();
  };
  const stop = (event) => event.stopPropagation();
  const contextMenu = (event) => {
    if (panel.node.contains(event.target)) event.stopImmediatePropagation();
  };
  // Capture on the panel, ahead of the notebook's own context menu and execution handlers.
  window.addEventListener("keydown", shortcut, true);
  notebook.node.addEventListener("keydown", stop);
  window.addEventListener("contextmenu", contextMenu, true);
  panel.disposed.connect(() => {
    disposed = true;
    document.body.classList.remove("ms-Reading");
    window.removeEventListener("keydown", shortcut, true);
    notebook.node.removeEventListener("keydown", stop);
    window.removeEventListener("contextmenu", contextMenu, true);
  });
}
