"""Real design-system bundles: local assets, provenance and chat/message prompt delivery."""
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skills

ROOT = Path(__file__).resolve().parent.parent / 'skills/skills'


class DesignSystems(unittest.TestCase):
    def setUp(self):
        self.cat = [skills.read_skill(str(p), 'builtin') for p in sorted(ROOT.glob('design-*'))]

    def test_every_system_has_local_specifications_and_two_loadable_previews(self):
        self.assertEqual(len(self.cat), 7)
        for skill in self.cat:
            with self.subTest(skill=skill['name']):
                folder = Path(skill['dir'])
                self.assertEqual(skill['category'], 'design-systems')
                self.assertEqual(skill['mode'], 'manual')
                self.assertIn('thumbnail', skill)
                self.assertLess(len(skills.body(skill)), skills.MAX_BODY)
                for target in re.findall(r'\]\((references/[^)]+|references\.json|ATTRIBUTION\.md)\)', skills.body(skill)):
                    self.assertTrue((folder / target).is_file(), target)
                refs = skills.references(skill)
                self.assertEqual(len(refs['images']), 2)
                for image in refs['images']:
                    data, kind = skills.reference_image(skill, image['file'])
                    self.assertEqual((data[:4], data[8:12], kind), (b'RIFF', b'WEBP', 'image/webp'))
                    self.assertGreater(len(data), 5000)
                tokens = json.loads((folder / 'references/tokens.json').read_text())
                self.assertEqual(set(tokens['themes']), {'light', 'dark'})
                for theme in tokens['themes'].values():
                    for key in tokens['roles'].values():
                        self.assertIn(key, theme)
                        self.assertNotIn('var(', theme[key])
                for source in tokens['sourceFiles']:
                    self.assertEqual(hashlib.sha256((folder / source['file']).read_bytes()).hexdigest(), source['sha256'])
                self.assertTrue(any('LICENSE' in source['file'] for source in tokens['sourceFiles']))
                self.assertTrue((folder / 'assets/fonts/LICENSE').is_file())

    def test_every_selected_skill_delivers_its_local_workflow_at_both_levels(self):
        for skill in self.cat:
            for level in ('chat', 'message'):
                with self.subTest(skill=skill['name'], level=level):
                    picked = skills.pick(self.cat, [skill['name']] if level == 'chat' else [], [skill['name']] if level == 'message' else [])
                    self.assertEqual([(s['name'], lv) for s, lv in picked], [(skill['name'], level)])
                    sent = {'names': [], 'index': ''}
                    prompt = skills.prompt(self.cat, picked, sent, auto=False)
                    self.assertIn(f'<skill name="{skill["name"]}" path="{skill["path"]}">', prompt)
                    self.assertIn('references/tokens.json', prompt)
                    self.assertIn('references/components.md', prompt)
                    self.assertIn('references/foundations.md', prompt)
                    self.assertIn('Скиллы к этому ходу', prompt)
                    self.assertNotIn('<skill', skills.prompt(self.cat, picked, sent, auto=False))

    def test_message_override_is_temporary_and_component_libraries_can_accompany_it(self):
        picked = skills.pick(self.cat, ['design-material-3'], ['design-carbon', 'design-shadcn-ui'])
        self.assertEqual([(s['name'], lv) for s, lv in picked], [('design-carbon', 'message'), ('design-shadcn-ui', 'message')])
        next_turn = skills.pick(self.cat, ['design-material-3'], [])
        self.assertEqual([(s['name'], lv) for s, lv in next_turn], [('design-material-3', 'chat')])


if __name__ == '__main__':
    unittest.main()
