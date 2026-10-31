import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skills  # noqa: E402


def write(root, name, head, body="Тело скилла."):
    os.makedirs(os.path.join(root, name))
    with open(os.path.join(root, name, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(f"---\n{head}\n---\n\n{body}\n")


class Frontmatter(unittest.TestCase):
    def test_scalars_blocks_and_metadata(self):
        f, body = skills.frontmatter('---\nname: x\ndescription: >-\n  Two\n  lines.\nmetadata:\n  group: style  # a comment\n'
                                     '  preview: "#111111 #222222 · Inter"\n---\n\n# X\nText\n')
        self.assertEqual(f["description"], "Two lines.")
        self.assertEqual(f["metadata"], {"group": "style", "preview": "#111111 #222222 · Inter"})
        self.assertEqual(body, "# X\nText\n")
        self.assertEqual(skills.frontmatter("no frontmatter"), ({}, "no frontmatter"))


class Catalog(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = self.tmp.name
        self.project, self.builtin, self.pendev = (os.path.join(t, d) for d in ("project", "builtin", "pendev"))
        write(self.builtin, "base", "name: base\ndescription: d\nmetadata:\n  group: base\n  mode: always")
        write(self.builtin, "graphite", "name: graphite\ndescription: d\nmetadata:\n  group: style\n  mode: manual\n"
                                        "  title: Graphite\n  summary: тихий\n  preview: \"#1C1D21 #8AA4FF · Inter\"")
        write(self.builtin, "paper", "name: paper\ndescription: d\nmetadata:\n  group: style\n  mode: manual")
        write(self.builtin, "typo", "name: typo\ndescription: Type scales and pairing.\nmetadata:\n  group: quality")
        write(self.project, "graphite", "name: graphite\ndescription: the project's own\nmetadata:\n  group: style\n  mode: manual")
        write(self.pendev, "motion", "name: motion\ndescription: CSS transitions.")
        self.old = skills.sources
        skills.sources = lambda file=None: [("project", self.project), ("builtin", self.builtin), ("pen.dev", self.pendev)]
        skills._cache.clear()

    def tearDown(self):
        skills.sources = self.old
        skills._cache.clear()
        self.tmp.cleanup()

    def test_groups_modes_and_priority(self):
        cat = {s["name"]: s for s in skills.catalog()}
        self.assertEqual([s["name"] for s in skills.catalog()], ["base", "graphite", "paper", "typo", "motion"], "by group")
        self.assertEqual((cat["graphite"]["source"], cat["graphite"]["description"]), ("project", "the project's own"))
        self.assertEqual((cat["typo"]["mode"], cat["motion"]["mode"], cat["motion"]["group"]), ("auto", "manual", "other"),
                         "no mode: auto, except someone else's skills")
        write(self.builtin, "late", "name: late\ndescription: d")
        skills._cache.clear()
        self.assertIn("late", [s["name"] for s in skills.catalog()], "a new folder is picked up")

    def test_a_turn_gets_the_chosen_text_once_and_the_rest_as_a_list(self):
        cat = skills.catalog()
        picked = skills.pick(cat, ["paper", "nope"], ["graphite"])
        self.assertEqual([(s["name"], lv) for s, lv in picked], [("base", "always"), ("paper", "chat"), ("graphite", "message")],
                         "styles from the chat and message are combined; unknown names are skipped")
        sent = {"names": [], "index": ""}
        first = skills.prompt(cat, picked, sent)
        self.assertIn('<skill name="graphite"', first)
        self.assertIn("Тело скилла.", first)
        self.assertIn("- typo — Type scales and pairing.", first)
        self.assertNotIn("motion", first, "manual skills aren't offered")
        again = skills.prompt(cat, picked, sent)
        self.assertNotIn("<skill", again)
        self.assertIn("Продолжай следовать скиллам: base, paper, graphite.", again)
        self.assertNotIn("- typo", again, "the list only when it changed")
        self.assertNotIn("- typo", skills.prompt(cat, picked, {"names": [], "index": ""}, auto=False))
        dropped = skills.prompt(cat, skills.pick(cat), sent)
        self.assertNotIn("Ещё скиллы", dropped, "graphite left the turn but its text is in the session: not listed again")

    def test_task_skills_with_a_reference_follow_the_chats_reference_mode(self):
        write(self.builtin, "landing", "name: landing\ndescription: d\nmetadata:\n  group: task\n  mode: manual")
        with open(os.path.join(self.builtin, "landing", "ref.png"), "wb") as f:
            f.write(b"png")
        with open(os.path.join(self.builtin, "landing", "references.json"), "w", encoding="utf-8") as f:
            f.write('{"images": [{"file": "ref.png"}]}')
        skills._cache.clear()
        cat = skills.catalog()
        picked = skills.pick(cat, [], ["landing"])
        sent = {"names": [], "index": ""}
        first = skills.prompt(cat, picked, sent, auto=False)
        self.assertIn(skills.SOURCES, first)
        self.assertIn("(landing) — чек-лист", first, "checklist by default")
        self.assertIn("— вдохновение", skills.prompt(cat, picked, sent, auto=False, reference="inspire"), "with every turn")
        self.assertIn("— чек-лист", skills.prompt(cat, picked, sent, auto=False, reference="bad"))
        self.assertNotIn(skills.SOURCES, skills.prompt(cat, skills.pick(cat, ["paper"]), {"names": [], "index": ""}, auto=False),
                         "no task skill with a picture: nothing about references")
        landing = next(s for s in cat if s["name"] == "landing")
        landing["mode"] = "auto"
        offered = {"names": [], "index": ""}
        self.assertIn("— реплика", skills.prompt(cat, [], offered, reference="replicate"), "listed for the agent: told once")
        self.assertNotIn(skills.SOURCES, skills.prompt(cat, [], offered, reference="replicate"))

    def test_multiple_themes_reach_the_agent_without_duplicates(self):
        for name in ("hallmark-almanac", "hallmark-arcade"):
            write(self.builtin, name, f"name: {name}\nmetadata:\n  group: style\n  origin: hallmark\n  mode: manual", body=name)
        for name in ("system-a", "system-b"):
            write(self.builtin, name, f"name: {name}\nmetadata:\n  group: system\n  mode: manual")
        skills._cache.clear()
        cat = skills.catalog()
        picked = skills.pick(cat, ["hallmark-almanac", "hallmark-arcade", "system-a"], ["hallmark-arcade", "system-b"])
        self.assertEqual([(s["name"], lv) for s, lv in picked], [
            ("base", "always"), ("hallmark-almanac", "chat"), ("hallmark-arcade", "message"), ("system-b", "message")])
        prompt = skills.prompt(cat, picked, {"names": [], "index": ""})
        for name in ("hallmark-almanac", "hallmark-arcade"):
            self.assertEqual(prompt.count(f'<skill name="{name}"'), 1)

    def test_the_style_library_has_every_source_and_both_groups(self):
        write(self.builtin, "tokyo", "name: tokyo\ndescription: The project's tokens\nmetadata:\n  group: system\n  mode: manual\n"
                                     "  title: Tokyo Night\n  origin: project")
        skills._cache.clear()
        cat = skills.catalog()
        shown, total = skills.styles_index(cat)
        self.assertEqual([s["name"] for s in shown], ["tokyo", "graphite", "paper"], "systems first, only systems and styles")
        self.assertEqual(skills.styles_index(cat, "PROJECT'S own")[0][0]["name"], "graphite", "all words, any case")
        self.assertEqual(skills.styles_index(cat, "", "system")[1], 1)
        self.assertEqual(skills.styles_index(cat, "", limit=1), (shown[:1], 3))
        tokyo = next(s for s in cat if s["name"] == "tokyo")
        self.assertEqual(skills.style_line(tokyo), "- tokyo — Tokyo Night · дизайн-система · project · The project's tokens")
        self.assertTrue(skills.style_text(tokyo).startswith('<skill name="tokyo"'))

    def test_named(self):
        self.assertEqual(skills.named("Read", {"file_path": "/a/better-ui/SKILL.md"}), "better-ui")
        self.assertEqual(skills.named("Skill", {"skill": "figcraft-design:better-ui"}), "better-ui")
        self.assertIsNone(skills.named("Read", {"file_path": "/a/b.md"}))


class Hallmark(unittest.TestCase):
    """skills/hallmark.py: a Hallmark theme as a style skill the catalog reads."""
    THEME = """---
name: Cobalt
slug: cobalt
genre: modern-minimal
paper: light 98.5 250
display: grotesk-sans Familjen Grotesk
accent: cool 256
posture: restrained
keywords: api, sdk
material: cool near-white paper, one cobalt signal
---

# Cobalt

Exact.

## Tokens

```css
:root { --color-paper: oklch(100% 0 0); --color-ink: oklch(0% 0 0); --color-accent: oklch(62.796% 0.25768 29.234);
  --shadow: 0 1px 2px oklch(0% 0 0 / 0.5); }
```

## Build hint

```html
<link href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk">
```
"""

    def test_theme_as_style(self):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills"))
        import hallmark
        with tempfile.TemporaryDirectory() as t:
            with open(os.path.join(t, "cobalt.md"), "w", encoding="utf-8") as f:
                f.write(self.THEME)
            h, text = hallmark.style_skill(os.path.join(t, "cobalt.md"), {"modern-minimal": "# Genre: modern-minimal\n\nPolished.\n\nStamp: `x`."})
            write(t, "hallmark-cobalt", text[4:text.index("\n---\n")], text[text.index("\n---\n") + 5:])
            s = skills.read_skill(os.path.join(t, "hallmark-cobalt"), "builtin")
        self.assertEqual((s["name"], s["title"], s["group"], s["mode"]), ("hallmark-cobalt", "Cobalt", "style", "manual"))
        self.assertEqual(s["summary"], "минимализм, светлый, сдержанный акцент")
        self.assertEqual(s["preview"], {"colors": ["#FFFFFF", "#000000", "#FF0000"], "font": "Familjen Grotesk"})
        self.assertIn("api, sdk", s["description"])
        self.assertIn("0 1px 2px #00000080", text)
        self.assertIn("## Genre: modern-minimal", text)
        self.assertNotIn("Stamp:", text)
        self.assertNotIn("<link", text)
        self.assertNotIn("oklch", text)


if __name__ == "__main__":
    unittest.main()
