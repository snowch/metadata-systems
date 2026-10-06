// @vitest-environment jsdom
// Copyright © 2026 Christopher Snow

// Every chapter in the course, checked as content: it parses, its challenges can be completed
// with their references and not with their starting points, it uses no term before the chapter
// that introduces it (including chapters not yet written), every figure it names exists and
// runs a model the book has, it states no prediction's answer before the learner commits, and
// the whole page renders.

import { readFileSync } from "node:fs";

import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { runProbe, week } from "@ms/lab";
import { INTERACTIVES, MODELS, createBook, grade, runtimeStrings } from "@ms/views";
import { LessonView, memoryStorage } from "@platform/lesson-runtime";
import { learnerText, modelProblems, termPattern, termProblems } from "@platform/lesson-schema";

import { LESSONS, PLAN, TERMS, chapterOf } from "./index";

const book = createBook(LESSONS);

describe("the course's chapters", () => {
  it("has at least one chapter, each with ten sections and an originality note", () => {
    expect(LESSONS.length).toBeGreaterThan(0);
    for (const l of LESSONS) {
      expect(l.sections).toHaveLength(10);
      expect(l.originalityNote.howThisDiffers.length).toBeGreaterThan(40);
    }
  });

  it("places each chapter where the plan does, introducing the plan's terms", () => {
    for (const l of LESSONS) {
      const planned = PLAN.find((c) => c.number === chapterOf(l));
      expect(planned, l.id).toBeDefined();
      expect(l.module).toBe(planned?.part);
      expect(l.title).toBe(planned?.title);
      expect([...l.introduces].sort()).toEqual([...(planned?.introduces ?? [])].sort());
    }
  });

  it("uses no term before the chapter that introduces it, written or not", () => {
    expect(termProblems(LESSONS)).toEqual([]);
    const found: string[] = [];
    for (const l of LESSONS) {
      const exempt = new Set(l.termExemptions.map((e) => e.term.toLowerCase()));
      for (const [term, home] of TERMS) {
        if (home <= chapterOf(l) || exempt.has(term.toLowerCase())) continue;
        const re = termPattern(term);
        for (const text of learnerText(l)) {
          const m = re.exec(text);
          if (m)
            found.push(
              `${l.id} uses "${m[0]}" (Chapter ${home}): ${text.slice(Math.max(0, m.index - 30), m.index + 30)}`,
            );
        }
      }
    }
    expect(found).toEqual([]);
  });

  it("keeps the plan's list of chapters and terms in step with docs/plan.md", () => {
    // Vitest runs from the repository root, as the check script does.
    const plan = readFileSync("docs/plan.md", "utf8");
    for (const c of PLAN) {
      const row = plan.split("\n").find((line) => line.startsWith(`| ${c.number} | ${c.title} |`));
      expect(row, `chapter ${c.number} in docs/plan.md`).toBeDefined();
      if (c.introduces.length && c.number !== 24) {
        const cells = (row ?? "").split("|").map((x) => x.trim());
        expect(cells[cells.length - 2], `chapter ${c.number}'s terms`).toBe(
          c.introduces.join(", "),
        );
      }
    }
  });

  it("names only figures the book has, running only models the book has notes for", () => {
    for (const l of LESSONS)
      for (const s of l.sections)
        for (const x of s.interactives)
          if (x.kind !== "challenge") expect(Object.keys(INTERACTIVES)).toContain(x.kind);
    expect(modelProblems(LESSONS, [...MODELS])).toEqual([]);
    for (const m of MODELS) expect(book.timeModelNotes[m]).toBeTruthy();
  });

  it("gives no prediction's answer in the text a learner reads before committing", () => {
    for (const l of LESSONS)
      for (const s of l.sections)
        for (const x of s.interactives) {
          if (x.kind !== "lab-prediction") continue;
          const p = x.props as {
            question: string;
            probe: Parameters<typeof runProbe>[0];
            options: { value: string; label: string }[];
          };
          const answer = runProbe(p.probe, week()).answer;
          const label = p.options.find((o) => o.value === answer)?.label ?? answer;
          for (const text of [x.lead ?? "", p.question, x.after ?? "", x.caption])
            expect(text.toLowerCase(), `${l.id}: ${x.id}`).not.toContain(label.toLowerCase());
        }
  });

  for (const lesson of LESSONS) {
    describe(lesson.id, () => {
      for (const c of lesson.challenges) {
        it(`${c.id}: the reference passes and the starting point does not`, () => {
          const passing = grade(c, c.reference);
          expect(passing.blocked).toBeUndefined();
          expect(passing.failures).toEqual([]);
          expect(passing.passed).toBe(true);
          expect(grade(c, c.initial).passed).toBe(false);
        });
      }

      it("renders every section and figure without a problem note", () => {
        const { container } = render(
          <LessonView
            book={book}
            lesson={lesson}
            storage={memoryStorage()}
            strings={runtimeStrings()}
          />,
        );
        expect(container.querySelectorAll("section.lesson-section")).toHaveLength(10);
        const figures = lesson.sections.flatMap((s) => s.interactives);
        expect(container.querySelectorAll("figure.interactive")).toHaveLength(figures.length);
        const problems = [
          ...container.querySelectorAll(".interactive-problem, .interactive-missing"),
        ].map((e) => e.textContent);
        expect(problems).toEqual([]);
      });
    });
  }
});
