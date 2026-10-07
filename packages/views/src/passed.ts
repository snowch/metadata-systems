// Copyright © 2026 Christopher Snow

// Whether the learner's stored work for a challenge passes its tests now. The work is graded
// again on every read, as the runtime grades saved work, so a figure that waits for a pass cannot
// be opened by editing storage: only work that passes opens it.

import type { Lesson } from "@platform/lesson-schema";
import { useStored, type LessonStore } from "@platform/lesson-runtime";

import { grade } from "./grade";

export function usePassed(lesson: Lesson, store: LessonStore, challengeId: string): boolean {
  const stored = useStored(store);
  const challenge = lesson.challenges.find((c) => c.id === challengeId);
  const saved = stored.challenges[challengeId]?.artifact;
  return Boolean(challenge && saved && grade(challenge, saved).passed);
}

/** The challenge's title, for a figure that says which challenge it waits for. */
export function challengeTitle(lesson: Lesson, challengeId: string): string {
  return lesson.challenges.find((c) => c.id === challengeId)?.title ?? challengeId;
}

/** A figure's caption without its closing full stop, for a figure that says which it waits for. */
export function figureCaption(lesson: Lesson, id: string): string {
  const figure = lesson.sections.flatMap((s) => s.interactives).find((x) => x.id === id);
  return (figure?.caption ?? id).replace(/\.$/, "");
}
