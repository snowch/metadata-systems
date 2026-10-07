// Copyright © 2026 Christopher Snow

// The metadata course as a book the platform's runtime can render: its lessons, the figures they
// name, the challenge editor, the grader, and the note for the one model its figures run, the
// lab. The runtime's own words are kept, except where this course names its model and its tests
// differently.

import type { ComponentType } from "react";

import type { Lesson } from "@platform/lesson-schema";
import {
  DEFAULT_STRINGS,
  type Book,
  type InteractiveProps,
  type Strings,
} from "@platform/lesson-runtime";

import { ChoiceEditor } from "./ChoiceEditor";
import { ChangeLab } from "./figures/ChangeLab";
import { Dashboard } from "./figures/Dashboard";
import { LabPrediction } from "./figures/LabPrediction";
import { PlatformMap } from "./figures/PlatformMap";
import { QuestionMap } from "./figures/QuestionMap";
import { StorageInspector } from "./figures/StorageInspector";
import { grade } from "./grade";
import { DEFAULT_VIEW_STRINGS, type ViewStrings } from "./strings";

/** The figures a lesson may name, by kind. */
export const INTERACTIVES: Readonly<Record<string, ComponentType<InteractiveProps>>> = {
  "platform-map": PlatformMap,
  dashboard: Dashboard,
  "lab-prediction": LabPrediction,
  "storage-inspector": StorageInspector,
  "change-lab": ChangeLab,
  "question-map": QuestionMap,
};

/**
 * The figures that take the learner's commitment before the lab answers: a prediction, a change
 * run after a prediction, and a sort. Each must ask for a belief the learner can already hold, and
 * the chapter's notes say why it does (CLAUDE.md, "Interaction is the explanation").
 */
export const PREDICTION_KINDS: readonly string[] = ["lab-prediction", "change-lab", "question-map"];

/** The models this course's figures run, by the name a lesson gives. */
export const MODELS = ["lab"] as const;

export function runtimeStrings(v: ViewStrings = DEFAULT_VIEW_STRINGS): Strings {
  return {
    ...DEFAULT_STRINGS,
    lesson: {
      ...DEFAULT_STRINGS.lesson,
      modelNote: v.modelNote,
      modelVsReality: v.modelVsReality,
      modelVsRealityNoSimulator: v.modelVsRealityNone,
      timeModel: { lab: v.badge },
      badgeLabel: v.badgeLabel,
    },
    challenge: {
      ...DEFAULT_STRINGS.challenge,
      inputs: v.inputs,
      actual: v.actual,
      expected: v.expected,
    },
  };
}

export const COURSE_TITLE = "Metadata Systems: From Raw Files to a Working Metadata Platform";

export function createBook(
  lessons: readonly Lesson[],
  interactives: Readonly<Record<string, ComponentType<InteractiveProps>>> = INTERACTIVES,
): Book {
  return {
    id: "ms",
    title: COURSE_TITLE,
    lessons,
    interactives,
    ChallengeEditor: ChoiceEditor,
    grade: (challenge, artifact) => grade(challenge, artifact),
    timeModelNotes: { lab: DEFAULT_VIEW_STRINGS.labNote },
  };
}
