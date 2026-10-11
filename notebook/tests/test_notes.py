# Copyright © 2026 Christopher Snow

"""Every written chapter keeps notes beside it: what it questions, and how its example is its own.

A chapter is written when its notebook exists. Its notes, `docs/notes/chapter-NN.md`, carry a
section "Requirements" (the requirement the chapter questions, or why none) and a section
"Originality" (the obvious textbook or vendor example for its topic, and how this chapter's
differs). Each is written in the same commit as the chapter.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WRITTEN = sorted(
    int(m.group(1))
    for path in (ROOT / "notebook").glob("chapter_*.py")
    if (m := re.fullmatch(r"chapter_(\d\d)\.py", path.name))
)


def section(text: str, heading: str) -> str:
    """The body of a `## heading` section, up to the next `## ` heading."""
    m = re.search(rf"^## {heading}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


class Notes(unittest.TestCase):
    def test_some_chapters_are_written(self):
        self.assertEqual(WRITTEN[:2], [1, 2])

    def test_every_written_chapter_has_its_requirements_and_originality(self):
        for n in WRITTEN:
            with self.subTest(chapter=n):
                path = ROOT / "docs" / "notes" / f"chapter-{n:02d}.md"
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                for heading in ("Requirements", "Originality"):
                    body = section(text, heading)
                    self.assertGreater(len(body.split()), 10, f"{path.name}: {heading}")


if __name__ == "__main__":
    unittest.main()
