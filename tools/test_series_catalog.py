from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import json
import re

ROOT = Path(__file__).resolve().parents[1]


class SeriesCatalogTest(unittest.TestCase):
    def test_writing_index_keeps_two_collections_separate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'tools').mkdir()
            (root / 'content').mkdir()
            shutil.copy(ROOT / 'tools/build_workshop.py', root / 'tools/build_workshop.py')
            collections = []
            for slug, title in [('free-probability', 'Free probability'), ('scale-geometry', 'Scale and geometry')]:
                source = f'blog/{slug}-1/index.qmd'
                target = root / source
                target.parent.mkdir(parents=True)
                target.write_text(f'---\ntitle: "{title} opening"\ndescription: "A worked example"\n---\n')
                collections.append({
                    'id': slug,
                    'title': title,
                    'url': f'{slug}.html',
                    'include': 'series' if slug == 'free-probability' else slug,
                    'description': f'{title} description',
                    'introduction': 'Start with a question.',
                    'status': 'Draft for review',
                    'chapters': [{'number': 1, 'source': source}],
                    'groups': [{'title': 'Opening', 'start': 0, 'count': 1}],
                })
            catalog = {'collections': collections, 'projects': [], 'articles': []}
            (root / 'content/catalog.json').write_text(json.dumps(catalog))
            result = subprocess.run(['python3', str(root / 'tools/build_workshop.py')], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            writing = (root / '_includes/writing.html').read_text()
            self.assertIn('href="scale-geometry.html"', writing)
            self.assertIn('href="free-probability.html"', writing)
            scale = (root / '_includes/scale-geometry.html').read_text()
            self.assertIn('Scale and geometry opening', scale)
            self.assertNotIn('Free probability opening', scale)

    def test_unwritten_chapter_is_visible_but_never_linked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'tools').mkdir()
            (root / 'content').mkdir()
            shutil.copy(ROOT / 'tools/build_workshop.py', root / 'tools/build_workshop.py')
            source = root / 'blog/opening/index.qmd'
            source.parent.mkdir(parents=True)
            source.write_text('---\ntitle: "Opening"\ndescription: "A complete draft"\n---\n')
            collection = {
                'id': 'scale-geometry', 'title': 'Scale and geometry',
                'url': 'scale-geometry.html', 'include': 'scale-geometry',
                'description': 'One question at a time.', 'introduction': 'A series.',
                'chapters': [
                    {'number': 1, 'source': 'blog/opening/index.qmd'},
                    {'number': 2, 'title': 'An unwritten question', 'description': 'A planned argument'},
                ],
                'groups': [{'title': 'Opening questions', 'start': 0, 'count': 2}],
            }
            (root / 'content/catalog.json').write_text(json.dumps({
                'collections': [collection], 'projects': [], 'articles': [],
            }))
            result = subprocess.run(['python3', str(root / 'tools/build_workshop.py')], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            hub = (root / '_includes/scale-geometry.html').read_text()
            self.assertIn('An unwritten question', hub)
            self.assertIn('Planned', hub)
            anchors = re.findall(r'<a\b[^>]*>.*?</a>', hub, flags=re.S)
            self.assertTrue(all('An unwritten question' not in anchor for anchor in anchors))
            self.assertNotIn('An unwritten question', (root / '_includes/writing.html').read_text())


if __name__ == '__main__':
    unittest.main()
