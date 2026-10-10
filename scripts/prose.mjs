#!/usr/bin/env node
// Copyright © 2026 Christopher Snow
//
// The prose regression check: fails on known-bad learner-facing phrases. The writing standard
// (AGENTS.md, "The writing standard") rejects whole classes of wording; this script is the
// narrow, deterministic backstop for phrases that actually appeared and were actually rejected.
// It is not a style judge: short sentences, passive constructions, "nothing" and metaphor are
// fine in themselves, and this script does not flag them. When a review finds a new failure,
// add its phrase to PROHIBITED below with a comment naming the rule it enforces.
//
// Run: node scripts/prose.mjs        (also: npm run check:prose)
// Exits non-zero when any prohibited phrase is found; prints file, rule and the offending line.

import { readFileSync } from "node:fs";
import { join } from "node:path";

/** Each prohibited phrase: what it is, and the standard's rule it breaks. */
const PROHIBITED = [
  // Rule 1: pseudo-profound aphorisms. Explain the activity instead.
  {
    phrase: "A wrong belief, once tested, tells you something",
    rule: "a pseudo-profound aphorism (rule 1): explain the activity, do not aphorise it",
  },
  // Rule 2: artificially dramatic fragments used as openers.
  {
    phrase: "One thing to take away",
    rule: "a dramatic fragment opener (rule 2): write a complete, direct sentence",
  },
  {
    phrase: "Three words to keep apart",
    rule: "a dramatic fragment opener (rule 2): name the distinction in a complete sentence",
  },
  // Rule 4: personification. Name what the metadata does or does not hold.
  {
    phrase: "The data might.",
    rule: "a personifying fragment (rule 4): say what the data can or cannot show",
  },
  // Rule 9: formulaic closing slogans.
  {
    phrase: "current state is not history",
    rule: "a closing slogan (rule 9): state the conclusion plainly, once, where it belongs",
  },
  // Rule 4: personification. "Nothing" as the subject of "says" names no metadata and no system;
  // name what does not show the answer. Found in p2UndecidedLine and an option label.
  {
    phrase: "Nothing so far says",
    rule: "personification (rule 4): name what does not show it - the page, the metadata, the record",
  },
  // Rule 12: curriculum narration and over-signposting. Found in the chapter review of Oct 2026.
  {
    phrase: "This chapter works through",
    rule: "curriculum narration (rule 12): advance the argument, do not describe its order",
  },
  {
    phrase: "The one-sentence version",
    rule: "a redundant summary layer (rule 13): state the conclusion once, where it belongs",
  },
  {
    phrase: "What this chapter established",
    rule: "summary scaffolding (rule 13): repeats conclusions the reader has just met",
  },
  {
    phrase: "Notice what this table",
    rule: "reader direction (rule 12): make the point instead of directing attention to it",
  },
  {
    phrase: "deserves its own moment",
    rule: "narrating the structure (rule 12): teach the subject, not the lesson's shape",
  },
  {
    phrase: "The general principle:",
    rule: "a formulaic transition (rule 13): the explanation must do the work, not the label",
  },
  {
    phrase: "The conclusion is structural, not incidental",
    rule: "rhetorical emphasis (rule 13): authoritative-sounding framing that adds no information",
  },
  // No lab on the page (CLAUDE.md): a figure is a diagram or a figure of the shop's data, and
  // nothing a learner reads names a lab or says what computes a figure. The trailing space and
  // punctuation keep "the label" and "the labour" clear of the check.
  ...["the lab ", "the lab's", "the lab.", "the lab,", "the lab;", "the lab:", "the lab)"].flatMap(
    (phrase) => [
      { phrase, rule: "no lab on the page: the page never names what computes a figure" },
      {
        phrase: phrase[0].toUpperCase() + phrase.slice(1),
        rule: "no lab on the page: the page never names what computes a figure",
      },
    ],
  ),
  {
    phrase: "Metadata Lab",
    rule: "no lab on the page: the page never names what computes a figure",
  },
];

/**
 * The learner-facing sources: chapter prose, labels and structure, the figures' own strings, and
 * the app's strings. Every string literal in these files is scanned. Excluded: tests and docs
 * (they quote and teach the standard, and quote bad phrasing on purpose); the platform packages
 * (platform/), whose strings the course replaces through runtimeStrings() where they are
 * learner-facing, and which are synced from snowch/learning-platform, never edited here; and
 * code identifiers.
 */
const FILES = [
  "content/lessons/invisible-system.prose.ts",
  "content/lessons/invisible-system.labels.ts",
  "content/lessons/invisible-system.ts",
  "packages/views/src/strings.ts",
  "apps/course/src/strings.ts",
];

/** Every string literal in a TypeScript source file, one per line of the file it came from. */
function* stringsOf(source) {
  let line = 1;
  let inString = false;
  let quote = "";
  let startLine = 1;
  let current = "";
  for (let i = 0; i < source.length; i++) {
    const c = source[i];
    if (c === "\n") line++;
    if (inString) {
      if (c === "\\") {
        current += c + (source[i + 1] ?? "");
        i++;
        continue;
      }
      if (c === quote) {
        yield { text: current, line: startLine };
        inString = false;
        current = "";
      } else current += c;
    } else if (c === "/" && source[i + 1] === "/") {
      // A line comment: an apostrophe in one ("a platform's state") is not a string's start.
      while (i < source.length && source[i] !== "\n") i++;
      line++;
    } else if (c === "/" && source[i + 1] === "*") {
      const end = source.indexOf("*/", i + 2);
      const stop = end === -1 ? source.length : end + 2;
      for (; i < stop; i++) if (source[i] === "\n") line++;
      i--;
    } else if (c === '"' || c === "'") {
      inString = true;
      quote = c;
      startLine = line;
      current = "";
    }
  }
}

// An optional argument gives the repository root to scan (the tests use a temporary one).
const ROOT = process.argv[2] ?? process.cwd();

const problems = [];
for (const file of FILES) {
  const source = readFileSync(join(ROOT, file), "utf8");
  for (const { text, line } of stringsOf(source)) {
    for (const { phrase, rule } of PROHIBITED) {
      if (text.includes(phrase)) {
        problems.push({ file, line, phrase, rule, text });
      }
    }
  }
}

if (problems.length > 0) {
  for (const p of problems) {
    console.error(`${p.file}:${p.line}: ${p.rule}`);
    console.error(`  found: "${p.phrase}"`);
    console.error(`  in:   ${p.text.slice(0, 120)}${p.text.length > 120 ? "…" : ""}`);
  }
  console.error(`\n${problems.length} prohibited phrase${problems.length === 1 ? "" : "s"} found.`);
  process.exit(1);
}
console.log("prose check: no prohibited phrases.");
