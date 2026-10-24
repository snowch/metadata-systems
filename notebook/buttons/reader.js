// Copyright © 2026 Christopher Snow

// A small reading surface over Jupyter's existing code editors, outputs and Python session.
// Only notebooks explicitly marked ms.reader opt in. Drafts are synchronous and independent of
// notebook autosave, so refresh before the first execution does not lose a reader's changes.
import { NotebookActions } from "@jupyterlab/notebook";
import { CodeCell } from "@jupyterlab/cells";
import { Widget } from "@lumino/widgets";
import words from "./reader-words.json";
import tableWords from "./table-words.json";
import { tableViewer } from "./tables.js";

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
  let tables;
  const inputKey = (entry) =>
    JSON.stringify(
      entries
        .slice(0, entries.indexOf(entry))
        .map((earlier) => [earlier.cell.model.sharedModel.getSource(), earlier.generation]),
    );
  const dependent = panel.context.model.getMetadata("ms")?.dependent;
  const runAll = button(words.runAll);
  runAll.dataset.readerAction = "runAll";
  const progress = element("div", "", "ms-Status ms-Reader-progress");
  progress.setAttribute("role", "status");
  progress.setAttribute("aria-live", "polite");
  progress.hidden = true;
  panel.node.append(progress);
  let hideProgress;
  const report = (text, briefly = 0) => {
    clearTimeout(hideProgress);
    progress.textContent = text;
    progress.hidden = false;
    if (briefly) hideProgress = setTimeout(() => (progress.hidden = true), briefly);
  };
  let busy = false;
  let disposed = false;
  const hold = (value) => {
    busy = value;
    state.busy = value;
    runAll.disabled = value;
    for (const entry of entries) {
      entry.run.disabled = value;
      entry.reset.disabled = value;
      if (entry.below) entry.below.disabled = value;
    }
    tables?.update();
  };

  async function runExample(entry, batch = false) {
    entry.running = true;
    entry.failed = false;
    tables?.update();
    const outer = notebook.node.classList.contains("jp-WindowedPanel-outer")
      ? notebook.node
      : (notebook.node.querySelector(".jp-WindowedPanel-outer") ?? notebook.node);
    const top = outer.scrollTop;
    const view = outer.getBoundingClientRect();
    // Prefer a visible paragraph or cell boundary: a partly visible output can grow within
    // its cell, so anchoring that cell's top would still move the prose below it.
    const candidates = [...outer.querySelectorAll(".jp-RenderedMarkdown > *, .jp-Cell")].filter(
      (node) => {
        const rect = node.getBoundingClientRect();
        return rect.bottom > view.top && rect.top < view.bottom && rect.height > 0;
      },
    );
    const anchor =
      candidates.find((node) => node.getBoundingClientRect().top >= view.top) || candidates[0];
    const offset = anchor?.getBoundingClientRect().top;
    entry.run.setAttribute("aria-busy", "true");
    entry.status.textContent = words.running;
    let scrolled = false;
    const manual = () => {
      scrolled = true;
    };
    const keyScroll = (event) => {
      if (["PageUp", "PageDown", "Home", "End", "ArrowUp", "ArrowDown", " "].includes(event.key))
        manual();
    };
    outer.addEventListener("wheel", manual, { passive: true });
    outer.addEventListener("touchmove", manual, { passive: true });
    window.addEventListener("keydown", keyScroll, true);
    try {
      // Capture what is actually run, after any edits made while Python was loading.
      const source = entry.cell.model.sharedModel.getSource();
      const inputs = inputKey(entry);
      let succeeded;
      if (batch) {
        // The cell API retains native outputs without NotebookActions selecting or scrolling to
        // each cell in turn. The batch deliberately awaits one reply before starting the next.
        if (!panel.sessionContext.session?.kernel) throw Error("Python is unavailable");
        const reply = await CodeCell.execute(entry.cell, panel.sessionContext);
        succeeded = !reply || reply.content.status === "ok";
      } else {
        notebook.activeCellIndex = notebook.widgets.indexOf(entry.cell);
        succeeded = await NotebookActions.runCells(notebook, [entry.cell], panel.sessionContext);
      }
      if (disposed) return false;
      entry.executed = source;
      entry.inputs = inputs;
      entry.succeeded = succeeded;
      entry.failed = !succeeded;
      entry.generation += 1;
      entry.status.textContent =
        source !== entry.cell.model.sharedModel.getSource()
          ? words.stale
          : succeeded
            ? words.success
            : words.error;
      return succeeded;
    } catch {
      entry.succeeded = false;
      entry.failed = true;
      if (!disposed) entry.status.textContent = words.error;
      return false;
    } finally {
      entry.running = false;
      tables?.update();
      if (!disposed && !scrolled) {
        // Preserve the paragraph in view even when new outputs above it change the page height.
        if (document.visibilityState === "visible")
          await new Promise((resolve) => requestAnimationFrame(resolve));
        if (!disposed) {
          outer.scrollTop =
            anchor && offset !== undefined
              ? outer.scrollTop + anchor.getBoundingClientRect().top - offset
              : top;
        }
      }
      outer.removeEventListener("wheel", manual);
      outer.removeEventListener("touchmove", manual);
      window.removeEventListener("keydown", keyScroll, true);
      entry.run.removeAttribute("aria-busy");
    }
  }

  async function execute(entry, fromTable = false) {
    if (busy || disposed) return;
    hold(true);
    entry.running = true;
    entry.failed = false;
    entry.run.setAttribute("aria-busy", "true");
    entry.status.textContent = state.ready ? words.running : words.queued;
    try {
      if (!(await state.startup.ready()) || disposed) {
        entry.failed = true;
        if (!disposed) entry.status.textContent = words.startupFailed;
        return;
      }
      await runExample(entry, fromTable);
    } finally {
      entry.running = false;
      entry.run.removeAttribute("aria-busy");
      hold(false);
    }
  }

  async function runBatch(start = 0, trigger = runAll) {
    if (busy || disposed) return;
    hold(true);
    trigger.setAttribute("aria-busy", "true");
    const subset = entries.slice(start);
    const below = trigger !== runAll;
    const count = (done) =>
      (below ? words.runningBelow : words.runningAll)
        .replace("{done}", done)
        .replace("{total}", subset.length);
    report(state.ready ? count(0) : below ? words.queuedBelow : words.queuedAll);
    try {
      if (!(await state.startup.ready()) || disposed) {
        if (!disposed) report(below ? words.startupFailedBelow : words.startupFailedAll);
        return;
      }
      report(count(0));
      for (let index = 0; index < subset.length; index++) {
        if (disposed) return;
        const entry = subset[index];
        if (!(await runExample(entry, true))) {
          if (!disposed) {
            report(
              (below ? words.belowStopped : words.stopped).replace(
                "{example}",
                entry.cell.model.getMetadata("ms").example.title,
              ),
              10_000,
            );
            for (const skipped of subset.slice(index + 1))
              skipped.status.textContent = words.skipped;
          }
          return;
        }
        report(count(index + 1));
      }
      report(below ? words.belowSucceeded : words.allSucceeded, 5000);
    } finally {
      trigger.removeAttribute("aria-busy");
      hold(false);
    }
  }
  runAll.addEventListener("click", () => void runBatch());

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
    const initialSource = /\(your copy(?: \d+)?\)/.test(panel.context.path)
      ? shared.getSource()
      : example.source;
    const controls = new Widget();
    controls.addClass("ms-Example-controls");
    const run = button(words.run);
    const reset = button(words.reset);
    const below = dependent ? button(words.runBelow) : null;
    if (below) below.dataset.readerAction = "runBelow";
    run.dataset.readerAction = "run";
    reset.dataset.readerAction = "reset";
    const saveStatus = element("span", "", "ms-Example-saved");
    saveStatus.setAttribute("role", "status");
    const statusWidget = new Widget();
    statusWidget.addClass("ms-Example-status");
    const status = element("span");
    status.setAttribute("role", "status");
    statusWidget.node.append(status);
    controls.node.append(run);
    if (below) controls.node.append(below);
    if (example.editable !== false) controls.node.append(reset, saveStatus);
    else cell.readOnly = true;
    cell.layout.insertWidget(0, controls);
    cell.layout.addWidget(statusWidget);
    const entry = {
      cell,
      run,
      reset,
      below,
      status,
      executed: null,
      generation: 0,
      running: false,
    };
    entries.push(entry);
    cell.model.outputs.clear();
    cell.model.executionCount = null;
    // A reset is stored too, so an older notebook autosave cannot resurrect a discarded edit.
    try {
      let saved = localStorage.getItem(key);
      if (saved === null && state.legacyDrafts?.has(example.id)) {
        saved = state.legacyDrafts.get(example.id);
        localStorage.setItem(key, saved);
      }
      if (saved === null && panel.context.path === "chapter_01.ipynb") {
        saved = localStorage.getItem(`${prefix}chapter_01b.ipynb:${example.id}`);
        if (saved !== null) localStorage.setItem(key, saved);
      }
      shared.setSource(saved ?? initialSource);
      saveStatus.textContent = saved === null ? words.noSavedEdits : words.saved;
    } catch {
      shared.setSource(state.legacyDrafts?.get(example.id) ?? initialSource);
      saveStatus.textContent = words.saveFailed;
      cell.node.dataset.unsaved = "true";
    }
    let previous = shared.getSource();
    const changed = () => {
      const source = shared.getSource();
      if (source === previous) return;
      previous = source;
      try {
        localStorage.setItem(key, source);
        saveStatus.textContent = words.saved;
        cell.node.dataset.unsaved = "false";
      } catch {
        saveStatus.textContent = words.saveFailed;
        cell.node.dataset.unsaved = "true";
      }
      if (entry.executed !== null) status.textContent = words.stale;
      if (dependent)
        for (const later of entries.slice(entries.indexOf(entry) + 1))
          if (later.executed !== null) later.status.textContent = words.staleBelow;
      tables?.update();
    };
    cell.model.contentChanged.connect(changed);
    panel.disposed.connect(() => cell.model.contentChanged.disconnect(changed));
    const editor = cell.node.querySelector(".cm-content");
    editor?.setAttribute("aria-label", words.editorLabel.replace("{example}", example.title));
    run.addEventListener("click", () => void execute(entry));
    below?.addEventListener("click", () => void runBatch(entries.indexOf(entry), below));
    reset.addEventListener("click", () => {
      if (busy) return;
      shared.setSource(example.source);
      cell.model.outputs.clear();
      cell.model.executionCount = null;
      entry.executed = null;
      entry.failed = false;
      entry.generation += 1;
      status.textContent = words.restored;
      tables?.update();
    });
  }

  const download = button(words.downloadCode);
  download.dataset.readerAction = "downloadCode";
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
  navigation.node.append(runAll, download);
  download.setAttribute("aria-label", words.downloadCode);
  download.title = words.downloadCode;
  download.replaceChildren(element("span", words.downloadCode, "ms-Download-label"));
  const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  icon.setAttribute("viewBox", "0 0 24 24");
  icon.setAttribute("aria-hidden", "true");
  icon.classList.add("ms-Download-icon");
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("d", "M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5");
  icon.append(path);
  download.append(icon);
  const references = panel.context.model.getMetadata("ms")?.tables;
  if (references?.length) {
    navigation.addClass("ms-Reader-nav-hasTables");
    tables = tableViewer({
      root: notebook.node,
      toolbar: navigation.node,
      scrollElement: notebook.node.classList.contains("jp-WindowedPanel-outer")
        ? notebook.node
        : (notebook.node.querySelector(".jp-WindowedPanel-outer") ?? notebook.node),
      words: tableWords,
      entries: references.map((reference) => {
        const entry = entries.find(
          (item) => item.cell.model.getMetadata("ms").example.id === reference.id,
        );
        return {
          ...reference,
          node: entry.cell.node,
          run: () => execute(entry, true),
          state: () => {
            const kind = (() => {
              if (entry.running) return "running";
              if (entry.failed) return "error";
              if (entry.executed === null) return "empty";
              if (!entry.succeeded) return "error";
              if (entry.executed !== entry.cell.model.sharedModel.getSource()) return "stale";
              const earlierChanged = entries
                .slice(0, entries.indexOf(entry))
                .some(
                  (earlier) =>
                    earlier.executed !== null &&
                    earlier.executed !== earlier.cell.model.sharedModel.getSource(),
                );
              if (dependent && (entry.inputs !== inputKey(entry) || earlierChanged))
                return "upstream";
              return entry.cell.node.querySelector(".jp-OutputArea table") ? "latest" : "noTable";
            })();
            return { kind, busy };
          },
        };
      }),
    });
  }

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
    tables?.dispose();
    clearTimeout(hideProgress);
    progress.remove();
    document.body.classList.toggle(
      "ms-Reading",
      [...document.querySelectorAll(".ms-ReaderPanel")].some((node) => node !== panel.node),
    );
    window.removeEventListener("keydown", shortcut, true);
    notebook.node.removeEventListener("keydown", stop);
    window.removeEventListener("contextmenu", contextMenu, true);
  });
}
