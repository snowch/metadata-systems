// Copyright © 2026 Christopher Snow

// The shell's own words, drafted by the prose process from the brief in
// docs/notes/chapter-01/briefs/F-figure-labels.md (CLAUDE.md).

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
  continueWith: "Continue with Chapter {number}: {title}",
  contents: "Contents",
  part: "Part {number}: {title}",
  chapter: "{number}. {title}",
  toWrite: "Still to be written",
  progress: "{passed} of {total} challenges complete",
  noChallenges: "No challenges",
  previous: "Previous",
  next: "Next",
  pagerLabel: "Previous and next chapter",
  notYet: "The next chapter is still to be written",
  // The chapter-wide start again, drafted from docs/notes/chapter-01/briefs/revision/N.
  startAgain: "Start this chapter again",
  startAgainNote:
    "The chapter keeps your predictions, sorts and challenge work in your browser. Starting again clears them all, and cannot be undone.",
  startAgainConfirm: "Clear everything in this chapter",
  startAgainCancel: "Keep my work",
  startAgainDone: "This chapter's work is cleared.",
  // The link at the top of a chapter to the start-again control at its foot.
  startAgainTop: "Start this chapter again",
  // The course-wide start again, on the front page: clears every chapter's work.
  startCourseAgain: "Start the course again",
  startCourseAgainNote:
    "Every chapter keeps your predictions, sorts and challenge work in your browser. Starting the course again clears them all, in every chapter, and cannot be undone.",
  startCourseAgainConfirm: "Clear all my work in every chapter",
  startCourseAgainCancel: "Keep my work",
  startCourseAgainDone: "All your work is cleared.",
  missing: "There is no page at {path}.",
  noLesson: "There is no chapter called {id}.",
  back: "Back to chapters",
};
