// Copyright © 2026 Christopher Snow

// At the foot of a chapter: start the chapter again. A prediction, once committed, stays as the
// record of what the learner expected, so this is the one way to clear it: everything the chapter
// keeps in the browser (predictions, sorts, challenge work, hints) goes, after a second press. The
// shell then mounts the chapter afresh, so every figure reads the cleared state.

import { useState } from "react";

import { LessonStore, type Storage } from "@platform/lesson-runtime";

import { STRINGS } from "../strings";

export function StartAgain({
  storage,
  bookId,
  lessonId,
  onCleared,
}: {
  storage: Storage;
  bookId: string;
  lessonId: string;
  onCleared: () => void;
}) {
  const [confirming, setConfirming] = useState(false);
  const [cleared, setCleared] = useState(false);
  return (
    <section className="start-again" aria-label={STRINGS.startAgain}>
      <p className="start-again-note">{STRINGS.startAgainNote}</p>
      {confirming ? (
        <span className="start-again-confirm" role="group" aria-label={STRINGS.startAgain}>
          <button
            type="button"
            className="button danger"
            onClick={() => {
              new LessonStore(storage, bookId, lessonId).reset();
              setConfirming(false);
              setCleared(true);
              onCleared();
            }}
          >
            {STRINGS.startAgainConfirm}
          </button>
          <button type="button" className="button secondary" onClick={() => setConfirming(false)}>
            {STRINGS.startAgainCancel}
          </button>
        </span>
      ) : (
        <button
          type="button"
          className="button secondary"
          onClick={() => {
            setConfirming(true);
            setCleared(false);
          }}
        >
          {STRINGS.startAgain}
        </button>
      )}
      <p className="start-again-status" role="status">
        {cleared ? STRINGS.startAgainDone : ""}
      </p>
    </section>
  );
}
