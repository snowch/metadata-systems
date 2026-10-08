// Copyright © 2026 Christopher Snow

// The metadata course as a book the platform's runtime can render: its lessons, the figures they
// name, the challenge editor, the grader, the one model its figures run, the lab, and a note for
// each role a figure can have. The runtime's own words are kept, except where this
// course names its model, its roles and its tests differently.

import type { ComponentType } from "react";

import type { Lesson } from "@platform/lesson-schema";
import {
  DEFAULT_STRINGS,
  type Book,
  type InteractiveProps,
  type Strings,
} from "@platform/lesson-runtime";

import { ChoiceEditor } from "./ChoiceEditor";
import { Glyph } from "./Glyph";
import { ASSET_KINDS } from "./Rich";
import { ChangeLab } from "./figures/ChangeLab";
import { AssetCards } from "./figures/AssetCards";
import { Dashboard } from "./figures/Dashboard";
import { Decision, HypothesisCheck } from "./figures/HypothesisLab";
import { LabPrediction } from "./figures/LabPrediction";
import { PlatformMap } from "./figures/PlatformMap";
import { QuestionMap } from "./figures/QuestionMap";
import { RequirementLab } from "./figures/RequirementLab";
import { StorageInspector } from "./figures/StorageInspector";
import { WeekTimeline } from "./figures/WeekTimeline";
import { grade } from "./grade";
import { DEFAULT_VIEW_STRINGS, type ViewStrings } from "./strings";

/** The figures a lesson may name, by kind. */
export const INTERACTIVES: Readonly<Record<string, ComponentType<InteractiveProps>>> = {
  "platform-map": PlatformMap,
  "asset-cards": AssetCards,
  "week-timeline": WeekTimeline,
  dashboard: Dashboard,
  "lab-prediction": LabPrediction,
  requirement: RequirementLab,
  decision: Decision,
  "hypothesis-check": HypothesisCheck,
  "storage-inspector": StorageInspector,
  "change-lab": ChangeLab,
  "question-map": QuestionMap,
};

/**
 * The figures that take the learner's commitment before the lab answers: a prediction, a change
 * run after a prediction, and a sort. Each must ask for a belief the learner can already hold, and
 * the chapter's notes say why it does (CLAUDE.md, "Interaction is the explanation").
 */
export const PREDICTION_KINDS: readonly string[] = [
  "lab-prediction",
  "requirement",
  "decision",
  "change-lab",
  "question-map",
];

/** The models this course's figures run, by the name a lesson gives. */
export const MODELS = ["lab"] as const;

/**
 * What a figure asks of the learner, which its badge names (CLAUDE.md, "Experiments, instruments
 * and explanations"): an experiment, an instrument to inspect with, or a reference.
 */
export const ROLES = ["experiment", "inspect", "reference"] as const;

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
      role: v.roles,
      roleBadgeLabel: v.roleBadgeLabel,
    },
    // A name the lab holds as an asset carries its kind's mark before it in prose, as Rich draws
    // it in the figures' own sentences. The mark is decoration; the words are the same.
    code: ({ children }) => {
      const name = typeof children === "string" ? children : String(children ?? "");
      const kind = ASSET_KINDS.get(name);
      return kind ? (
        <code>
          <Glyph kind={kind} />
          {name}
        </code>
      ) : (
        <code>{children}</code>
      );
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
    // No note on the lab: Chapter 1 explains it in its own prose, where it first names it, so no
    // badge and no foot of a page says it again.
    timeModelNotes: {},
    roleNotes: DEFAULT_VIEW_STRINGS.roleNotes,
  };
}
