// @vitest-environment jsdom
// Copyright © 2026 Christopher Snow

// Every chapter in the course, checked as content: it parses, its challenges can be completed
// with their references and not with their starting points, it uses no term before the chapter
// that introduces it (including chapters not yet written), every figure it names exists, runs a
// model the book has and says what it asks of the learner, it states no prediction's answer before
// the learner commits, and the whole page renders.

import { readFileSync } from "node:fs";

import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { optionForCount, runProbe, sumReconstructions, week, type ChangeId } from "@ms/lab";
import {
  DEFAULT_VIEW_STRINGS,
  INTERACTIVES,
  MODELS,
  PREDICTION_KINDS,
  ROLES,
  createBook,
  grade,
  labAnswer,
  runtimeStrings,
} from "@ms/views";
import { LessonView, memoryStorage } from "@platform/lesson-runtime";
import { learnerText, modelProblems, termPattern, termProblems } from "@platform/lesson-schema";

import { STRINGS } from "../../apps/course/src/strings";
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

  it("uses none of the commonest forms of filler", () => {
    // CLAUDE.md, "Silence is preferable to filler": a sentence the learner would not miss goes.
    // Only reading applies that test; this is a backstop for the forms the author named.
    const FILLER = [
      /\byou have (what you need|everything)\b/i,
      /\beverything (is )?in place\b/i,
      /\bnow you can (begin|start)\b/i,
      /\bwhere things get interesting\b/i,
      /\basks nothing of you\b/i,
      /\bkept to hand\b/i,
      /\b(is|are) (quietly )?waiting\b/i,
      /\bquietly\b/i,
      /\byou (have been|were) told\b/i,
      /\b(as )?you already know\b/i,
      /\blet's\b/i,
    ];
    const strings = (v: unknown): string[] =>
      typeof v === "string"
        ? [v]
        : v && typeof v === "object"
          ? Object.values(v).flatMap(strings)
          : [];
    const texts = [
      ...LESSONS.flatMap((l) => learnerText(l)),
      ...strings(DEFAULT_VIEW_STRINGS),
      ...strings(runtimeStrings()),
      ...strings(STRINGS),
    ];
    const found = texts.flatMap((t) =>
      FILLER.filter((f) => f.test(t)).map((f) => `${String(f)}: ${t.slice(0, 80)}`),
    );
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

  it("names only figures the book has, running only models the book declares", () => {
    for (const l of LESSONS)
      for (const s of l.sections)
        for (const x of s.interactives)
          if (x.kind !== "challenge") expect(Object.keys(INTERACTIVES)).toContain(x.kind);
    expect(modelProblems(LESSONS, [...MODELS])).toEqual([]);
    // The lab is explained once, where Chapter 1 first names it: no model note repeats it behind
    // every badge or at the foot of every page.
    expect(book.timeModelNotes).toEqual({});
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

  it("states a prediction's result below it only in a figure that waits for its answer", () => {
    // A figure below a prediction can be in view while the learner is still choosing, so it states
    // what the prediction found only once the answer is committed: it waits for the prediction, or
    // for a figure that waits for it. Captions, leads, after-texts, tasks and the sections' own
    // prose show at once, so none of them states it.
    for (const l of LESSONS) {
      const placed = l.sections.flatMap((s) => s.interactives.map((x) => ({ s, x })));
      const waits = (id: string) =>
        (placed.find((f) => f.x.id === id)?.x.props as { waits?: string } | undefined)?.waits;
      const waitsFor = (id: string, earlier: string): boolean => {
        const w = waits(id);
        return w !== undefined && (w === earlier || waitsFor(w, earlier));
      };
      placed.forEach(({ x }, i) => {
        const w = waits(x.id);
        if (w === undefined) return;
        const at = placed.findIndex((f) => f.x.id === w);
        expect(at, `${x.id} waits for an earlier figure`).toBeGreaterThanOrEqual(0);
        expect(at, `${x.id} waits for an earlier figure`).toBeLessThan(i);
        expect(PREDICTION_KINDS, `${x.id} waits for an answer`).toContain(placed[at]?.x.kind);
      });
      placed.forEach(({ s, x }, i) => {
        if (x.kind !== "lab-prediction") return;
        const found = runProbe(
          (x.props as { probe: Parameters<typeof runProbe>[0] }).probe,
          week(),
        );
        if (found.kind !== "day-total") return;
        const result = found.checks.find((c) => c.key === found.day)?.actual;
        expect(result, x.id).toBeTruthy();
        const below = placed.slice(i + 1).map((f) => f.x);
        const tasks = below
          .filter((f) => f.kind === "challenge")
          .map((f) => l.challenges.find((c) => c.id === f.props["challengeId"])?.task ?? "");
        const atOnce = [
          ...l.sections.slice(l.sections.indexOf(s)).map((t) => t.prose),
          ...below.flatMap((f) => [f.caption, f.lead ?? "", f.after ?? ""]),
          ...tasks,
        ];
        for (const text of atOnce) expect(text, x.id).not.toContain(result);
        for (const f of below)
          if (JSON.stringify(f.props).includes(result ?? ""))
            expect(waitsFor(f.id, x.id), `${f.id} states what ${x.id} found`).toBe(true);
      });
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
    // A hypothesis check reads the choice of a decision figure earlier in the same chapter, with
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

  it("gives every figure a role, and its block in the chapter's notes, in the page's order", () => {
    // CLAUDE.md, "Experiments, instruments and explanations": a figure says what it asks of the
    // learner, and the notes' "Figures" section says why it is on the page. An experiment answers
    // twelve questions, or names the experiment it completes; an instrument or a reference answers
    // two. A figure that takes a commitment is an experiment.
    const EXPERIMENT = [
      "Objective",
      "Known before",
      "Driving question",
      "The action",
      "Why the action",
      "Evidence",
      "Consequence",
      "Predictable",
      "Gives nothing away",
      "Not knowing",
      "Next question",
      "An experiment",
    ];
    const OTHER = ["Serves", "Why now"];
    const answers = (block: string, label: string) =>
      new RegExp(`\\*\\*${label}:\\*\\* \\S`).test(block);
    const missing: string[] = [];
    for (const l of LESSONS) {
      const notes = readFileSync(
        `docs/notes/chapter-${String(chapterOf(l)).padStart(2, "0")}.md`,
        "utf8",
      );
      const section = notes.split("\n## Figures\n")[1]?.split("\n## ")[0] ?? "";
      const blocks = new Map(
        section
          .split("\n### `")
          .slice(1)
          .map((b) => [b.slice(0, b.indexOf("`")), b] as const),
      );
      const figures = l.sections.flatMap((s) => s.interactives);
      expect([...blocks.keys()], `${l.id}: the notes' figures, in order`).toEqual(
        figures.map((x) => x.id),
      );
      for (const x of figures) {
        const role = x.role;
        if (role === undefined || !(ROLES as readonly string[]).includes(role)) {
          missing.push(`${l.id}: ${x.id} has no role`);
          continue;
        }
        if (PREDICTION_KINDS.includes(x.kind) && role !== "experiment")
          missing.push(`${l.id}: ${x.id} takes a commitment, so it is an experiment`);
        const block = blocks.get(x.id) ?? "";
        if (!block.includes(`\n- **Role:** ${role}\n`))
          missing.push(`${l.id}: ${x.id}'s notes do not give its role, ${role}`);
        const part = /\*\*Part of:\*\* `([^`]+)`/.exec(block)?.[1];
        if (part !== undefined) {
          const whole = figures.find((f) => f.id === part);
          if (role !== "experiment" || whole?.role !== "experiment" || whole === x)
            missing.push(`${l.id}: ${x.id} is part of ${part}, which is no other experiment`);
          continue;
        }
        for (const label of role === "experiment" ? EXPERIMENT : OTHER)
          if (!answers(block, label)) missing.push(`${l.id}: ${x.id} does not answer "${label}"`);
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
