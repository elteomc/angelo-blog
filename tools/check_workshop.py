"""Normalize document mode and validate the rendered site's local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import os
import sys

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.duplicates = []
        self.headings = 0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.duplicates.append(attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.headings += 1
        key = 'href' if tag in ('a', 'link') else 'src' if tag in ('img', 'script') else None
        if key and attrs.get(key):
            self.links.append(attrs[key])

root = Path(os.environ.get('QUARTO_PROJECT_OUTPUT_DIR', 'docs')).resolve()
pages = {}
for file in root.rglob('*.html'):
    text = file.read_text()
    if not text.lstrip().lower().startswith('<!doctype html>'):
        text = '<!doctype html>\n' + text
        file.write_text(text)
    pages[file] = Page(text)
errors = []
for file, page in pages.items():
    for duplicate in page.duplicates:
        errors.append(f'{file.relative_to(root)}: duplicate ID {duplicate}')
    if page.headings != 1:
        errors.append(f'{file.relative_to(root)}: expected one h1, found {page.headings}')
    for link in page.links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc:
            continue
        path = unquote(parsed.path)
        target = ((root / path.lstrip('/')) if path.startswith('/') else (file.parent / path)).resolve() if path else file
        if target.is_dir():
            target /= 'index.html'
        if not target.exists():
            errors.append(f'{file.relative_to(root)}: missing {link}')
        elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
            errors.append(f'{file.relative_to(root)}: missing anchor {link}')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f'Validated {len(pages)} HTML pages, headings, local links and assets in {root}')
