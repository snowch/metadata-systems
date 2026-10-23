// Copyright © 2026 Christopher Snow

// Browser-owned answers are independent of notebook saves, Python kernels and published versions.
// A separate key for each answer prevents edits to different fields in two tabs overwriting one
// another. An explicit empty value is a reset tombstone: legacy import must not resurrect it.
import words from "./answer-words.js";

export const PREFIX = "ms:metadata-systems:answers:v1:";
export const TABLES = ["clean_customers", "clean_orders", "daily_sales"];
export const IDS = [
  ...TABLES.map((table) => `ch01.${table}`),
  "ch02.daily_sales.revision",
  "ch02.clean_orders.revision",
  "ch02.report",
];
const known = (id) => IDS.includes(id);

export function answerStore(storage = () => window.localStorage, events = window) {
  const memory = new Map();
  const pending = new Set();
  const listeners = new Set();
  const emit = () => listeners.forEach((listener) => listener());
  const read = (id) => {
    if (!known(id)) throw new Error("Unknown exercise");
    if (pending.has(id)) return { text: memory.get(id) ?? "", exists: true, saved: false };
    try {
      const text = storage().getItem(PREFIX + id);
      memory.set(id, text);
      return { text: text ?? "", exists: text !== null, saved: true };
    } catch {
      return { text: memory.get(id) ?? "", exists: memory.get(id) != null, saved: false };
    }
  };
  const write = (id, text) => {
    if (!known(id) || typeof text !== "string") throw new Error("Invalid answer");
    memory.set(id, text);
    pending.add(id);
    try {
      storage().setItem(PREFIX + id, text);
      pending.delete(id);
    } catch {
      // Keep the draft available for export and report the failure to the learner.
    }
    events.dispatchEvent(new Event("ms-answers-changed"));
    return !pending.has(id);
  };
  const changed = (event) => {
    if (event.key === null || event.key?.startsWith(PREFIX)) emit();
  };
  events.addEventListener("storage", changed);
  events.addEventListener("ms-answers-changed", emit);
  return {
    read,
    write,
    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    export() {
      const answers = {};
      for (const id of IDS) {
        const answer = read(id);
        if (answer.exists) answers[id] = answer.text;
      }
      return JSON.stringify({ course: "metadata-systems", version: 1, answers }, null, 2);
    },
    import(text) {
      const data = JSON.parse(text);
      if (
        data?.course !== "metadata-systems" ||
        data.version !== 1 ||
        !data.answers ||
        typeof data.answers !== "object" ||
        Array.isArray(data.answers) ||
        Object.entries(data.answers).some(([id, value]) => !known(id) || typeof value !== "string")
      ) {
        throw new Error("Invalid answers file");
      }
      let saved = true;
      for (const [id, value] of Object.entries(data.answers)) {
        if (!read(id).text) saved = write(id, value) && saved;
      }
      return saved;
    },
    dispose() {
      events.removeEventListener("storage", changed);
      events.removeEventListener("ms-answers-changed", emit);
      listeners.clear();
    },
  };
}

// Read old exercise strings as text, never execute a notebook to recover an answer.
export function legacyGuesses(notebook) {
  const answers = {};
  for (const cell of notebook?.cells ?? []) {
    if (cell.cell_type !== "code") continue;
    const source = [].concat(cell.source ?? []).join("");
    const match = /^\s*guesses\s*=\s*(?:r)?(["']{3})([\s\S]*?)\1\s*$/m.exec(source);
    if (!match) continue;
    for (const line of match[2].split("\n")) {
      const row = /^(clean_customers|clean_orders|daily_sales):\s*(.*)$/.exec(line.trim());
      if (row && row[2].trim() && row[2].trim() !== "made from ........ because ........") {
        answers[`ch01.${row[1]}`] = row[2].trim();
      }
    }
  }
  return answers;
}

export async function recoverGuesses(contents, store) {
  if (TABLES.every((table) => store.read(`ch01.${table}`).exists)) return;
  const files = (await contents.get("", { content: true })).content
    .filter((file) => /^chapter_01(?: \(your copy(?: \d+)?\))?\.ipynb$/.test(file.name))
    .sort((a, b) => String(b.last_modified).localeCompare(String(a.last_modified)));
  for (const file of files) {
    const notebook = (await contents.get(file.path ?? file.name, { content: true })).content;
    for (const [id, text] of Object.entries(legacyGuesses(notebook))) {
      if (!store.read(id).exists) store.write(id, text);
    }
  }
}

const element = (tag, text) => {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  return node;
};

function field(root, store, id, label, readonly = false) {
  const wrapper = element("label");
  wrapper.className = "ms-Answer-field";
  wrapper.append(element("span", label));
  const input = element("textarea");
  input.dataset.answer = id;
  input.rows = 4;
  input.readOnly = readonly;
  input.placeholder = readonly
    ? words.empty
    : id.endsWith(".revision")
      ? words.revisionPrompt
      : words.prompt;
  if (id === "ch02.report") input.placeholder = "";
  const status = element("p");
  status.className = "ms-Answer-status";
  status.setAttribute("role", "status");
  status.setAttribute("aria-live", "polite");
  wrapper.append(input);
  root.append(wrapper, status);
  const refresh = () => {
    const answer = store.read(id);
    wrapper.dataset.unsaved = String(!answer.saved);
    if (input.value !== answer.text) input.value = answer.text;
    status.textContent = !answer.saved
      ? words.unsaved
      : readonly && !answer.text
        ? words.empty
        : answer.exists
          ? words.saved
          : "";
  };
  input.addEventListener("input", () => store.write(id, input.value));
  // Notebook keyboard shortcuts must not consume normal editing keys, including spaces and Escape.
  input.addEventListener("keydown", (event) => event.stopPropagation());
  if (!readonly) {
    const reset = element("button", words.reset);
    reset.type = "button";
    reset.addEventListener("click", () => {
      if (window.confirm(words.confirmReset)) store.write(id, "");
    });
    root.append(reset);
  }
  refresh();
  return store.subscribe(refresh);
}

export function mountAnswers(root, kind, store) {
  root.classList.add("ms-Answers");
  const cleanups = [];
  const original = (table, readonly) =>
    cleanups.push(
      field(root, store, `ch01.${table}`, words.original.replace("{table}", table), readonly),
    );
  if (kind === "guesses") TABLES.forEach((table) => original(table, false));
  else if (kind === "daily_sales" || kind === "clean_orders") {
    original(kind, true);
    const link = element("a", words.chapterOne);
    link.href = "?path=chapter_01.ipynb#Your-guesses-about-the-warehouse-tables";
    link.target = "_blank";
    link.rel = "noopener";
    root.append(link);
    cleanups.push(
      field(root, store, `ch02.${kind}.revision`, words.revision.replace("{table}", kind)),
    );
  } else if (kind === "report") cleanups.push(field(root, store, "ch02.report", words.report));
  root.append(element("p", words.local));
  const controls = element("div");
  controls.className = "ms-Answer-controls";
  const status = element("p");
  status.setAttribute("role", "status");
  const download = element("button", words.export);
  download.type = "button";
  download.addEventListener("click", () => {
    try {
      const url = URL.createObjectURL(new Blob([store.export()], { type: "application/json" }));
      const link = element("a");
      link.href = url;
      link.download = "metadata-systems-answers.json";
      root.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch {
      status.textContent = words.exportFailed;
    }
  });
  const upload = element("input");
  upload.type = "file";
  upload.accept = ".json,application/json";
  upload.hidden = true;
  const restore = element("button", words.import);
  restore.type = "button";
  restore.addEventListener("click", () => upload.click());
  upload.addEventListener("change", async () => {
    try {
      const file = upload.files[0];
      if (!file) return;
      status.textContent = store.import(await file.text()) ? words.imported : words.unsaved;
    } catch {
      status.textContent = words.invalid;
    } finally {
      upload.value = "";
    }
  });
  controls.append(download, restore, upload);
  root.append(controls, status);
  return () => cleanups.forEach((dispose) => dispose());
}

// Attach to cell widgets, not Markdown HTML: sanitising or rerendering Markdown cannot erase a
// draft. Jupyter's windowed notebook may detach cells; the observer also handles replacement cells
// when a new published notebook is opened. No kernel is involved.
export async function attachAnswers(app, panel, checked) {
  await panel.context.ready;
  await checked;
  if (!/^chapter_0(?:1b?|2)(?: \(your copy(?: \d+)?\))?\.ipynb$/.test(panel.context.path)) return;
  const store = answerStore();
  try {
    await recoverGuesses(app.serviceManager.contents, store);
  } catch {
    // An unavailable legacy notebook must not prevent new answers. Its saved copy is untouched.
  }
  if (panel.isDisposed) {
    store.dispose();
    return;
  }
  const mounted = new Map();
  const scan = () => {
    const cells = new Set(panel.content.widgets);
    for (const [cell, dispose] of mounted) {
      if (!cells.has(cell)) {
        dispose();
        mounted.delete(cell);
      }
    }
    for (const cell of cells) {
      const kind = cell.model.getMetadata("ms")?.answer;
      if (!["guesses", "daily_sales", "clean_orders", "report"].includes(kind) || mounted.has(cell))
        continue;
      const root = element("section");
      root.dataset.exercise = kind;
      cell.node.append(root);
      const unmount = mountAnswers(root, kind, store);
      mounted.set(cell, () => {
        unmount();
        root.remove();
      });
    }
  };
  const observer = new MutationObserver(scan);
  observer.observe(panel.content.node, { childList: true, subtree: true });
  scan();
  panel.disposed.connect(() => {
    observer.disconnect();
    mounted.forEach((dispose) => dispose());
    store.dispose();
  });
}
