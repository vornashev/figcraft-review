"""Pinned collection integrity and importer transformations; no network calls."""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skills

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("design_collections", ROOT / "skills/design_collections.py")
collections = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collections)


class Collections(unittest.TestCase):
    def test_every_import_has_originals_license_provenance_and_readable_local_previews(self):
        expected = {"typeui": 67, "tweakcn": 42, "uipro": 79}
        for origin, count in expected.items():
            folders = sorted((ROOT / "skills/skills").glob(origin + "-*/SKILL.md"))
            self.assertEqual(len(folders), count)
            for entry in folders:
                with self.subTest(name=entry.parent.name):
                    folder = entry.parent
                    skill = skills.read_skill(str(folder), "builtin")
                    self.assertEqual((skill["origin"], skill["category"], skill["group"], skill["mode"]), (origin, "themes", "style", "manual"))
                    self.assertEqual(skill["name"], folder.name)
                    self.assertIn("thumbnail", skill)
                    self.assertTrue((folder / "LICENSE").stat().st_size > 1000)
                    self.assertIn(collections.SOURCES[origin]["sha"], (folder / "ATTRIBUTION.md").read_text(encoding="utf-8"))
                    refs = skills.references(skill)
                    self.assertEqual(len(refs["images"]), 2 if origin == "tweakcn" else 1)
                    for image in refs["images"]:
                        data, kind = skills.reference_image(skill, image["file"])
                        self.assertEqual((data[:4], data[8:12], kind), (b"RIFF", b"WEBP", "image/webp"))
                        self.assertGreater(len(data), 1000)
                    for target in re.findall(r"\]\((references/[^)]+|references\.json)\)", entry.read_text(encoding="utf-8")):
                        self.assertTrue((folder / target).is_file(), target)
                    if origin == "uipro":
                        row = json.loads((folder / "references/style.json").read_text(encoding="utf-8"))
                        self.assertIn(row["Status"], ("active", "supplemental"))
                        self.assertEqual(skill["name"], "uipro-" + row["Style ID"])
                    elif origin == "typeui":
                        self.assertTrue((folder / "references/upstream-SKILL.md").read_text(encoding="utf-8").startswith("---"))
                        self.assertTrue((folder / "references/DESIGN.md").stat().st_size > 100)
                    else:
                        data = json.loads((folder / "references/tokens.json").read_text(encoding="utf-8"))
                        self.assertEqual(set(data["styles"]), {"light", "dark"})

    def test_css_function_commas_and_font_stacks_survive_parsing(self):
        parsed = collections.css_declarations("box-shadow: 1px 2px 3px rgba(0,0,0,0.1), -1px -2px 4px rgba(255,255,255,0.6), border: 1px solid rgba(255,255,255,0.3), font-family: Arial, sans-serif")
        self.assertEqual(parsed["box-shadow"], "1px 2px 3px rgba(0,0,0,0.1), -1px -2px 4px rgba(255,255,255,0.6)")
        self.assertEqual(parsed["border"], "1px solid rgba(255,255,255,0.3)")
        self.assertEqual(parsed["font-family"], "Arial, sans-serif")

    @unittest.skipUnless((ROOT / "sidecar/web/node_modules/typescript").is_dir(), "needs npm --prefix sidecar/web ci")
    def test_preset_reader_accepts_data_and_rejects_expressions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "presets.ts"
            path.write_text('export const defaultPresets: Record<string, ThemePreset> = {example: {label: "Example", styles: {light: {primary: "#000000"}}}};', encoding="utf-8")
            result = subprocess.check_output(["node", str(ROOT / "skills/read_theme_presets.mjs"), str(path)])
            self.assertEqual(json.loads(result)["example"]["styles"]["light"]["primary"], "#000000")
            path.write_text('export const defaultPresets = {example: getTheme()};', encoding="utf-8")
            result = subprocess.run(["node", str(ROOT / "skills/read_theme_presets.mjs"), str(path)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
