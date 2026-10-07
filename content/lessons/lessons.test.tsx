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

import { optionForCount, runProbe, sumReconstructions, week, type ChangeId } from "@ms/lab";
import {
  INTERACTIVES,
  MODELS,
  PREDICTION_KINDS,
  createBook,
  grade,
  labAnswer,
  runtimeStrings,
} from "@ms/views";
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

  type Option = { value: string; label: string; range?: [number, number]; means?: string[] };
  const word = (label: string) =>
    new RegExp(`\\b${label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`, "i");

  it("gives no prediction's answer in the text a learner reads before committing", () => {
    for (const l of LESSONS)
      for (const s of l.sections)
        for (const x of s.interactives) {
          if (x.kind !== "lab-prediction") continue;
          const p = x.props as {
            question: string;
            probe: Parameters<typeof runProbe>[0];
            options: Option[];
          };
          const answer = labAnswer(runProbe(p.probe, week()), p.options);
          expect(answer, `${l.id}: ${x.id} has an option for the lab's answer`).toBeDefined();
          const label = p.options.find((o) => o.value === answer)?.label ?? "";
          for (const text of [x.lead ?? "", p.question, x.after ?? "", x.caption])
            expect(text, `${l.id}: ${x.id}`).not.toMatch(word(label));
        }
  });

  it("questions a requirement without showing what the platform records before it is asked", () => {
    // A requirement figure (CLAUDE.md, "Question the requirement"): the platform's record answers
    // some of the requirement's readings and not others, and nothing the learner reads before the
    // second press names that record.
    for (const l of LESSONS)
      for (const s of l.sections)
        for (const x of s.interactives) {
          if (x.kind !== "requirement") continue;
          const p = x.props as {
            requirement: string;
            question: string;
            probe: Parameters<typeof runProbe>[0];
            options: (Option & { short: string; asks: string })[];
            undecided: { label: string };
            text: { mine: string; undecided: string; meanings: string };
          };
          const found = runProbe(p.probe, week());
          if (found.kind !== "owner-kind") throw new Error(`${x.id}: an owner probe`);
          const answered = p.options.filter((o) => o.means?.includes(found.answer));
          expect(answered.length, `${x.id}: some reading is answered`).toBeGreaterThan(0);
          expect(answered.length, `${x.id}: some reading is not`).toBeLessThan(p.options.length);
          const before = [
            x.lead ?? "",
            x.caption,
            x.after ?? "",
            p.requirement,
            p.question,
            p.undecided.label,
            ...Object.values(p.text),
            ...p.options.flatMap((o) => [o.label, o.short, o.asks]),
          ].filter((t) => t !== p.text["explain" as keyof typeof p.text]);
          for (const text of before) expect(text, `${x.id}`).not.toContain(found.value ?? "");
        }
  });

  it("checks an explanation only against a choice the chapter offers, after the learner's work", () => {
    // A hypothesis check reads the choice of a hypothesis figure earlier in the same chapter, with
    // the same explanations; it waits for a challenge; its rows support some explanations and
    // rule out others; and neither figure names what the left-out rows have in common, which a
    // later challenge asks the learner to find.
    for (const l of LESSONS) {
      const figures = l.sections.flatMap((s) => s.interactives);
      figures.forEach((x, i) => {
        if (x.kind !== "hypothesis-check") return;
        const p = x.props as {
          of: string;
          requires: string;
          options: Option[];
          probe: Parameters<typeof runProbe>[0];
          text: Record<string, string>;
        };
        const choice = figures.findIndex((f) => f.id === p.of);
        expect(choice, `${x.id}: ${p.of} comes first`).toBeGreaterThanOrEqual(0);
        expect(choice, `${x.id}: ${p.of} comes first`).toBeLessThan(i);
        const asked = figures[choice]?.props as { options: Option[]; question: string };
        expect(p.options.map((o) => o.value)).toEqual(asked.options.map((o) => o.value));
        expect(l.challenges.map((c) => c.id)).toContain(p.requires);
        const found = runProbe(p.probe, week());
        if (found.kind !== "day-gap") throw new Error(`${x.id}: a day-gap probe`);
        const supported = p.options.filter((o) =>
          o.means?.some((m) => found.answer.includes(m as never)),
        );
        expect(supported.length, `${x.id}: some explanation holds`).toBeGreaterThan(0);
        expect(supported.length, `${x.id}: some is ruled out`).toBeLessThan(p.options.length);
        for (const text of [asked.question, ...Object.values(p.text), x.caption])
          expect(text, x.id).not.toMatch(/customer id/i);
      });
    }
  });

  it("says in its chapter's notes which requirement the chapter questions, or why none", () => {
    // Every chapter's notes have a "Requirements" section: it names each requirement figure, or,
    // in a chapter with none, says why none fits (CLAUDE.md, "Question the requirement").
    const missing: string[] = [];
    for (const l of LESSONS) {
      const notes = readFileSync(
        `docs/notes/chapter-${String(chapterOf(l)).padStart(2, "0")}.md`,
        "utf8",
      );
      const section = notes.split("\n## Requirements\n")[1]?.split("\n## ")[0]?.trim() ?? "";
      if (!section) missing.push(`${l.id}: no "Requirements" section`);
      for (const s of l.sections)
        for (const x of s.interactives)
          if (x.kind === "requirement" && !section.includes(`\`${x.id}\``))
            missing.push(`${l.id}: ${x.id}`);
    }
    expect(missing).toEqual([]);
  });

  it("gives every count prediction ranges that do not overlap, one holding the lab's count", () => {
    const disjoint = (options: Option[]) => {
      const ranges = options
        .map((o): [number, number] => o.range ?? [-1, -1])
        .sort((a, b) => a[0] - b[0]);
      return ranges.every((r, i) => r[0] <= r[1] && (i === 0 || (ranges[i - 1]?.[1] ?? 0) < r[0]));
    };
    for (const l of LESSONS)
      for (const s of l.sections)
        for (const x of s.interactives) {
          if (x.kind === "change-lab") {
            const p = x.props as {
              changes: { id: ChangeId }[];
              target?: string;
              prediction: { options: Option[] };
            };
            expect(disjoint(p.prediction.options), `${l.id}: ${x.id}`).toBe(true);
            for (const c of p.changes) {
              const fits = sumReconstructions(week([c.id]), "daily_sales", "covers").length;
              expect(optionForCount(fits, p.prediction.options), `${x.id}: ${c.id}`).toBeDefined();
            }
          }
          if (x.kind === "lab-prediction") {
            const p = x.props as { options: Option[] };
            if (p.options.some((o) => o.range)) expect(disjoint(p.options), x.id).toBe(true);
          }
        }
  });

  it("answers the eight questions in its chapter's notes for every prediction", () => {
    // Each figure that takes a commitment has a block in the notes' "Predictions" section, with
    // an answer to each question CLAUDE.md asks of a prediction ("Interaction is the
    // explanation"), so a prediction cannot go in without its author having asked them.
    const LABELS = [
      "Objective",
      "Known before",
      "Hypotheses",
      "Told apart by",
      "Gives nothing away",
      "If wrong",
      "Next question",
      "A belief, not a guess",
    ];
    const missing: string[] = [];
    for (const l of LESSONS) {
      const notes = readFileSync(
        `docs/notes/chapter-${String(chapterOf(l)).padStart(2, "0")}.md`,
        "utf8",
      );
      const section = notes.split("\n## Predictions\n")[1]?.split("\n## ")[0] ?? "";
      for (const s of l.sections)
        for (const x of s.interactives) {
          if (!PREDICTION_KINDS.includes(x.kind)) continue;
          const block = section.split(`\n### \`${x.id}\`\n`)[1]?.split("\n### ")[0];
          if (block === undefined) missing.push(`${l.id}: ${x.id} has no block`);
          for (const label of LABELS)
            if (block !== undefined && !new RegExp(`\\*\\*${label}:\\*\\* \\S`).test(block))
              missing.push(`${l.id}: ${x.id} does not answer "${label}"`);
        }
    }
    expect(missing).toEqual([]);
  });

  it("gives every prediction at least two options, each an explanation that picks one answer", () => {
    for (const l of LESSONS)
      for (const s of l.sections)
        for (const x of s.interactives) {
          if (x.kind !== "lab-prediction") continue;
          const p = x.props as { options: Option[] };
          expect(p.options.length, x.id).toBeGreaterThanOrEqual(2);
          // An option stands for answers or for counts, never for nothing.
          for (const o of p.options)
            expect(o.means ?? o.range, `${x.id}: ${o.value}`).toBeDefined();
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
