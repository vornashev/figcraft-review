"""Importer checks without contacting OpenDesign."""
import importlib.util
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("opendesign_import", Path(__file__).resolve().parent.parent / "skills/opendesign.py")
od = importlib.util.module_from_spec(spec)
spec.loader.exec_module(od)


def bundle(files):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    return output.getvalue()


class Importer(unittest.TestCase):
    def test_catalog_preserves_entities_and_rejects_duplicates_and_unsafe_slugs(self):
        article = '<article data-prompt-card data-slug="example" data-category="apps" data-style="Soft" data-name="A &amp; B"><p>A useful flow.</p><textarea data-card-raw>Task &amp; content</textarea></article>'
        row = od.parse_catalog(article)[0]
        self.assertEqual((row["name"], row["prompt"], row["summary"]), ("A & B", "Task & content", "A useful flow."))
        for invalid in (article + article, article.replace('data-slug="example"', 'data-slug="../outside"'), "no catalog"):
            with self.assertRaises(ValueError):
                od.parse_catalog(invalid)

    def test_bundle_resources_survive_adaptation(self):
        image = b"RIFF0000WEBPimage"
        prompt = "Original task\n\n## Content\nPreserve supplied content.\n"
        data = bundle({"prompt.txt": prompt, "reference.webp": image, "README.txt": "Source instructions", "fonts/license.txt": "Font license"})
        entry = {"slug": "example", "name": "Example", "summary": "Complete a specific workflow.", "category": "apps", "style": "Soft"}
        with tempfile.TemporaryDirectory() as root:
            folder = od.write_skill(entry, data, Path(root))
            self.assertEqual((folder / "assets/reference.webp").read_bytes(), image)
            self.assertEqual((folder / "references/prompt.md").read_text(), prompt)
            self.assertEqual((folder / "references/source-bundle.txt").read_text(), "Source instructions")
            self.assertEqual((folder / "assets/upstream/fonts/license.txt").read_text(), "Font license")
            refs = json.loads((folder / "references.json").read_text())
            self.assertTrue((folder / refs["images"][0]["file"]).is_file())
            self.assertIn("references/prompt.md", (folder / "SKILL.md").read_text())
            self.assertNotIn("Inspect", (folder / "SKILL.md").read_text(), "the picture is not read by default")
            text = (folder / "SKILL.md").read_text()
            (folder / "SKILL.md").write_text(text.replace("checklist by default", "old adapter"))
            self.assertEqual(od.rewrite_adapters(Path(root)), 1)
            self.assertEqual((folder / "SKILL.md").read_text(), text, "the adapter is rewritten, the frontmatter kept")

    def test_bundle_rejects_missing_images_invalid_images_and_path_traversal(self):
        for files in ({"prompt.txt": "task"}, {"prompt.txt": "task", "reference.webp": b"not an image"},
                      {"prompt.txt": "task", "reference.webp": b"RIFF0000WEBPimage", "../secret": "bad"}):
            with self.assertRaises(ValueError):
                od.unpack(bundle(files))


if __name__ == "__main__":
    unittest.main()
