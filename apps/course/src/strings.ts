// Copyright © 2026 Christopher Snow

// The shell's own words, drafted by the prose process from the brief in
// docs/notes/chapter-02/briefs/F-figure-labels.md (CLAUDE.md).

export const STRINGS = {
  offline: {
    title: "Use the course offline",
    intro:
      "Download the full course to open, reload and run every chapter offline. You need an internet connection for the download.",
    size: "Full course: {size} MB",
    download: "Download full course",
    update: "Download update",
    cancel: "Cancel download",
    remove: "Remove downloaded course",
    progress: "Downloaded {done} of {total} MB",
    progressLabel: "Course download progress",
    ready: "The full course is saved in this browser and ready to use offline.",
    offlineReady:
      "You are offline. You can open, reload and run every chapter from the downloaded course.",
    incomplete:
      "The full course is not available offline. Reconnect to the internet and complete the download.",
    updateAvailable: "A course update is available. Download it to update your offline copy.",
    updated:
      "Course update downloaded. Reload open chapters to use it. Your answers and notebook edits are kept.",
    cancelled:
      "Download cancelled. You can resume it later. Any complete version downloaded earlier remains available.",
    failed:
      "Could not complete the download. Check your connection and available browser storage, then try again. Any complete version downloaded earlier remains available.",
    unsupported:
      "This browser cannot download the course for offline use. You can use the course while online.",
    storageNote:
      "Removing the download keeps your answers and saved notebooks. Your browser may clear stored site data, including downloads and answers. Export your answers to keep a separate copy.",
  },
  brand: "Metadata Systems",
  courseTitle: "Metadata Systems: From Raw Files to a Working Metadata Platform",
  lead: "You predict outcomes, build a metadata system, inspect its results, then break and repair it. Your work stays in your browser.",
  /** The cover's band, the eight parts and the contents by part (brief AJ). */
  cover: {
    promise: "You build a small metadata system inside a browser-based data platform.",
    assumes:
      "The course assumes you can read a short SQL query (a SELECT with a WHERE and a GROUP BY) and that you have used files, database tables and a dashboard. It assumes nothing about metadata or lineage.",
    figureCaption:
      "Monday morning's dashboard: revenue per day, 7 to 13 September. Thursday is far lower than the other days. The head of the shop asks why. Chapter 1 starts from that question.",
  },
  chapters: "Chapters",
  skip: "Skip to main content",
  theme: "Theme",
  themeAuto: "Auto",
  themeLight: "Light",
  themeDark: "Dark",
  footer: "Everything runs in your browser. Nothing is sent anywhere.",
  copyright: "© 2026 Christopher Snow",
  start: "Start with Chapter {number}: {title}",
  contents: "Contents",
  // Under "Contents": what opening a chapter does (brief AY).
  contentsNote:
    "Each chapter opens as a notebook, a page where you run the chapter's Python code in your browser; the first time you open one, your browser downloads about 13 MB.",
  part: "Part {number}: {title}",
  chapter: "{number}. {title}",
  toWrite: "Still to be written",
  // The dashboard in the band, worded as the chapters' figures had it (brief F).
  refreshed: "Last refreshed {time}.",
  chartLabel: "{title}, last refreshed {time}.",
  weekdays: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] as readonly string[],
  missing: "There is no page at {path}.",
  back: "Back to chapters",
};
