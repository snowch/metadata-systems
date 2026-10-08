// Copyright © 2026 Christopher Snow

// On the front page: start the whole course again. Every chapter's stored work goes, after a
// second press; the shell then mounts every page afresh on the cleared state.
import { useState } from "react";
import { resetBook, type Storage } from "@platform/lesson-runtime";
import { STRINGS } from "../strings";

export function StartCourseAgain({
  storage,
  bookId,
  onCleared,
}: {
  storage: Storage;
  bookId: string;
  onCleared: () => void;
}) {
  const [confirming, setConfirming] = useState(false);
  const [cleared, setCleared] = useState(false);
  return (
    <section className="start-again start-course-again" aria-label={STRINGS.startCourseAgain}>
      <p className="start-again-note">{STRINGS.startCourseAgainNote}</p>
      {confirming ? (
        <span className="start-again-confirm" role="group" aria-label={STRINGS.startCourseAgain}>
          <button
            type="button"
            className="button danger"
            onClick={() => {
              resetBook(storage, bookId);
              setConfirming(false);
              setCleared(true);
              onCleared();
            }}
          >
            {STRINGS.startCourseAgainConfirm}
          </button>
          <button type="button" className="button secondary" onClick={() => setConfirming(false)}>
            {STRINGS.startCourseAgainCancel}
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
          {STRINGS.startCourseAgain}
        </button>
      )}
      <p className="start-again-status" role="status">
        {cleared ? STRINGS.startCourseAgainDone : ""}
      </p>
    </section>
  );
}
