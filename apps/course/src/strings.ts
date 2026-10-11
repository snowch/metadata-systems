// Copyright © 2026 Christopher Snow

// The shell's own words, drafted by the prose process from the brief in
// docs/notes/chapter-02/briefs/F-figure-labels.md (CLAUDE.md).

export const STRINGS = {
  brand: "Metadata Systems",
  courseTitle: "Metadata Systems: From Raw Files to a Working Metadata Platform",
  lead: "For each idea you predict, build, run, inspect, break and repair it. Your work stays in your browser.",
  /** The cover's band, the eight parts and the contents by part (brief AJ). */
  cover: {
    promise: "You build a small metadata system inside a browser-based data platform.",
    assumes:
      "The course assumes you can read a short SQL query (a SELECT with a WHERE and a GROUP BY) and that you have used files, database tables and a dashboard. It assumes nothing about metadata or lineage.",
    figureCaption:
      "Monday morning's dashboard: revenue per day, 7 to 13 September. Thursday is far lower than the other days. The head of the shop asks why. Chapter 1 starts from that question.",
    partCount: {
      some: "{written} of the part's {total} chapters are written and can be read",
      none: "none of the part's {total} chapters is written yet",
      noneOne: "the part's chapter is not written yet",
    },
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
    "Each written chapter opens as a notebook, a page where you run the chapter's Python code in your browser; the first time you open one, your browser downloads about 13 MB.",
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
