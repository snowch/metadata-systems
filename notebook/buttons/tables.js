// Copyright © 2026 Christopher Snow

// An evidence view over existing outputs. Opening a table never runs Python or changes a cell.
// Copy text and table structure rather than moving Jupyter's live output or copying active HTML.
function copyTable(source) {
  const table = document.createElement("table");
  for (const row of source.rows) {
    const copy = table.insertRow();
    for (const cell of row.cells) {
      const value = document.createElement(cell.tagName.toLowerCase());
      value.textContent = cell.textContent;
      for (const attr of ["colspan", "rowspan", "scope"])
        if (cell.hasAttribute(attr)) value.setAttribute(attr, cell.getAttribute(attr));
      copy.append(value);
    }
  }
  return table;
}

export function tableViewer({ root, toolbar, entries, words, scrollElement }) {
  const make = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const button = (text) => {
    const node = make("button", text, "ms-Buttons-button");
    node.type = "button";
    return node;
  };
  const trigger = button(words.button);
  trigger.dataset.readerAction = "tables";
  trigger.setAttribute("aria-haspopup", "dialog");
  const dialog = make("dialog", "", "ms-Tables jp-ThemedContainer");
  dialog.setAttribute("aria-label", words.title);
  const header = make("div", "", "ms-Tables-header");
  header.append(make("h2", words.title));
  const close = button(words.close);
  close.addEventListener("click", () => dialog.close());
  header.append(close);
  const label = make("label", words.choose, "ms-Tables-label");
  const select = make("select");
  label.append(select);
  const status = make("p", "", "ms-Tables-status");
  status.setAttribute("role", "status");
  const output = make("div", "", "ms-Tables-output");
  output.tabIndex = 0;
  output.setAttribute("role", "region");
  output.setAttribute("aria-label", words.tableArea);
  const run = button(words.run);
  run.dataset.readerAction = "runTable";
  const scrollHint = make("p", words.scrollHint, "ms-Tables-scrollHint");
  scrollHint.hidden = true;
  dialog.append(header, label, status, output, scrollHint, run);
  document.body.append(dialog);
  toolbar.append(trigger);
  let opener;
  let readingPosition;
  let readingAnchor;
  let readingOffset;
  let frame;
  let disposed = false;
  let displayed = "";
  let originalTables = [];
  let originalText = [];
  const options = entries.map((entry) => {
    const option = make("option", entry.title);
    option.value = entry.id;
    select.append(option);
    return option;
  });
  const refresh = () => {
    if (disposed || !dialog.open) return;
    entries.forEach((entry, index) => {
      const { kind } = entry.state();
      const suffix =
        kind === "empty"
          ? words.notRunLabel
          : kind === "stale" || kind === "upstream"
            ? words.staleLabel
            : kind === "noTable"
              ? words.noTableLabel
              : kind === "error"
                ? words.errorLabel
                : kind === "running"
                  ? words.runningLabel
                  : words.latestLabel;
      options[index].textContent = `${entry.title} (${suffix})`;
    });
    const entry = entries.find((item) => item.id === select.value);
    if (!entry) return;
    const current = entry.state();
    const message = words[current.kind];
    status.textContent =
      current.busy && current.kind !== "running" ? `${message} ${words.busy}` : message;
    run.disabled = current.busy;
    run.setAttribute("aria-busy", String(current.kind === "running"));
    const tables = ["latest", "stale", "upstream"].includes(current.kind)
      ? [...entry.node.querySelectorAll(".jp-OutputArea table")]
      : [];
    // Preserve horizontal and vertical table scroll while an unrelated output changes.
    if (
      displayed !== entry.id ||
      tables.length !== originalTables.length ||
      tables.some(
        (table, index) =>
          table !== originalTables[index] || table.textContent !== originalText[index],
      )
    ) {
      displayed = entry.id;
      originalTables = tables;
      originalText = tables.map((table) => table.textContent);
      output.replaceChildren(...tables.map(copyTable));
      output.scrollTop = 0;
      output.scrollLeft = 0;
    }
    output.hidden = !tables.length;
    scrollHint.hidden = !tables.length || output.scrollWidth <= output.clientWidth + 1;
  };
  const update = () => {
    if (disposed || !dialog.open || frame) return;
    frame = requestAnimationFrame(() => {
      frame = null;
      refresh();
    });
  };
  const open = (id, from) => {
    if (disposed) return;
    if (id && entries.some((entry) => entry.id === id)) select.value = id;
    if (!dialog.open) {
      opener = from;
      readingPosition = scrollElement.scrollTop;
      const view = scrollElement.getBoundingClientRect();
      const visible = [...root.querySelectorAll(".jp-RenderedMarkdown > *, .jp-Cell")].filter(
        (node) => {
          const rect = node.getBoundingClientRect();
          return rect.height > 0 && rect.bottom > view.top && rect.top < view.bottom;
        },
      );
      readingAnchor =
        visible.find((node) => node.getBoundingClientRect().top >= view.top) ?? visible[0];
      readingOffset = readingAnchor?.getBoundingClientRect().top;
      dialog.showModal();
    }
    refresh();
    select.focus({ preventScroll: true });
  };
  trigger.addEventListener("click", () => open(null, trigger));
  select.addEventListener("change", refresh);
  run.addEventListener("click", async () => {
    const entry = entries.find((item) => item.id === select.value);
    if (!entry || entry.state().busy) return;
    const running = entry.run();
    refresh();
    try {
      await running;
    } finally {
      update();
    }
  });
  dialog.addEventListener("close", () => {
    scrollElement.scrollTop = readingAnchor?.isConnected
      ? scrollElement.scrollTop + readingAnchor.getBoundingClientRect().top - readingOffset
      : readingPosition;
    if (opener?.isConnected) opener.focus({ preventScroll: true });
  });
  const follow = (event) => {
    const link = event.target.closest?.('a[href^="#ms-table-"]');
    if (!link || !root.contains(link)) return;
    const id = link.getAttribute("href").slice("#ms-table-".length);
    if (!entries.some((entry) => entry.id === id)) return;
    event.preventDefault();
    event.stopPropagation();
    open(id, link);
  };
  root.addEventListener("click", follow);
  const observer = new MutationObserver(update);
  observer.observe(root, { subtree: true, childList: true, characterData: true });
  const resize = new ResizeObserver(update);
  resize.observe(output);
  return {
    update,
    dispose() {
      disposed = true;
      observer.disconnect();
      resize.disconnect();
      cancelAnimationFrame(frame);
      root.removeEventListener("click", follow);
      if (dialog.open) dialog.close();
      dialog.remove();
      trigger.remove();
    },
  };
}
