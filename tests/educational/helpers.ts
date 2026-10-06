// Copyright © 2026 Christopher Snow

// Shared helpers for the educational tests: the chapter page, its challenges, and the words the
// page uses, taken from the same modules the app renders from, so a wording change moves both.

import { expect, type Locator, type Page } from "@playwright/test";

import { LESSONS } from "@ms/content";
import { DEFAULT_VIEW_STRINGS as V, format, runtimeStrings } from "@ms/views";

export const S = runtimeStrings();
export { V, format, LESSONS };

export const CHAPTER = LESSONS[0]!;

export function challengeData(id: string, lesson = CHAPTER) {
  const c = lesson.challenges.find((x) => x.id === id);
  if (!c) throw new Error(`no challenge ${id}`);
  return c;
}

export async function openChapter(page: Page, id = CHAPTER.id): Promise<void> {
  await page.goto(`#/chapter/${id}`);
  await expect(page.locator("section.lesson-section")).toHaveCount(10);
  await page.evaluate(async () => {
    await document.fonts.ready;
  });
}

/** A challenge's section on the page. */
export const challenge = (page: Page, id: string): Locator =>
  page.locator(`section.challenge[data-challenge="${id}"]`);
export const status = (c: Locator): Locator => c.locator(".challenge-status");

/** Sets each of a challenge's fields to the given answer, through its select. */
export async function choose(
  section: Locator,
  answers: Readonly<Record<string, string>>,
  id: string,
  lesson = CHAPTER,
) {
  const c = challengeData(id, lesson);
  for (const f of c.fields) {
    const value = answers[f.id];
    if (value === undefined) continue;
    await section.getByLabel(f.label, { exact: true }).selectOption(value);
  }
}

export async function runTests(c: Locator): Promise<void> {
  await c.getByRole("button", { name: S.challenge.run }).click();
}

/** Passes a challenge through the page with its reference, and waits for the badge. */
export async function pass(page: Page, id: string, lesson = CHAPTER): Promise<void> {
  const c = challengeData(id, lesson);
  const section = challenge(page, id);
  await choose(section, c.reference.answers ?? {}, id, lesson);
  await runTests(section);
  await expect(section.locator(".challenge-complete")).toBeVisible();
}

/** A figure's props as the lesson gives them, for the labels a test clicks. */
export function figureProps(id: string, lesson = CHAPTER): Record<string, unknown> {
  const x = lesson.sections.flatMap((s) => s.interactives).find((i) => i.id === id);
  if (!x) throw new Error(`no figure ${id}`);
  return (x.props ?? {}) as Record<string, unknown>;
}

export const storageKey = (id = CHAPTER.id) => `ms:v1:${id}`;
