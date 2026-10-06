// Copyright © 2026 Christopher Snow

// The course's chapters, in order. Each chapter is a module in this directory; adding one here is
// what publishes it. Every chapter is parsed when the app starts, so an invalid chapter fails
// fast with its problems listed, and the content tests parse the same list.

import { parseLesson, type Lesson, type LessonInput } from "@platform/lesson-schema";

import { invisibleSystem } from "./invisible-system";

const INPUTS: readonly LessonInput[] = [invisibleSystem];

export const LESSONS: readonly Lesson[] = INPUTS.map(parseLesson).sort(
  (a, b) => a.module - b.module || a.order - b.order,
);

export function lessonById(id: string): Lesson | undefined {
  return LESSONS.find((l) => l.id === id);
}

export { PARTS, PLAN, TERMS, chapterOf, type PlannedChapter } from "./plan";
