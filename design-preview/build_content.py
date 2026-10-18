"""Refresh preview content from the existing rendered drafts."""
import argparse
import json
import re
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('site_root', type=Path)
args = parser.parse_args()
root = args.site_root.resolve()
output = Path(__file__).resolve().parent
headings = json.loads((output / 'heading_overrides.json').read_text())
chapters = []
for number in range(1, 7):
    source = root / f'blog/free-prob-{number}/index.qmd'
    text = source.read_text()
    def field(name):
        match = re.search(rf'^{name}:\s*"?([^\n]+?)"?\s*$', text, re.M)
        return match.group(1) if match else ''
    rendered = root / f'docs/blog/free-prob-{number}/index.html'
    soup = BeautifulSoup(rendered.read_text(), 'html.parser')
    main = soup.select_one('main#quarto-document-content')
    main.select_one('header').decompose()
    for p in list(main.find_all('p')):
        if p.get_text().startswith('The complete series') or p.get_text().startswith('Previous:'):
            p.decompose()
    for element in main.select('.anchorjs-link, .code-copy-button, figcaption, #reproduce-the-figures'):
        element.decompose()
    for callout in main.select('.callout'):
        body = callout.select_one('.callout-body')
        if body is not None:
            details = soup.new_tag('details', attrs={'class': 'answer-sketch'})
            summary = soup.new_tag('summary')
            summary.string = 'Answer sketches'
            details.append(summary)
            for child in list(body.contents):
                details.append(child.extract())
            callout.replace_with(details)
    for a in main.find_all('a', href=True):
        href = a['href']
        match = re.search(r'blog/free-prob-(\d)/index.html', href)
        if match:
            a['href'] = f'?page=article&chapter={match.group(1)}'
            a['data-chapter'] = match.group(1)
        elif 'free-probability.html' in href:
            a['href'] = '?page=series'
            a['data-series'] = ''
        elif href.startswith('../../assets/free-probability/'):
            a['href'] = 'assets/' + Path(href).name
        elif href.startswith('../../tools/'):
            a['href'] = 'resources/' + Path(href).name
        if a.find('img'):
            a['target'] = '_blank'
            a['rel'] = 'noopener'
            a['class'] = ['figure-link']
            a['aria-label'] = 'Open figure at full size in a new tab'
    for img in main.find_all('img', src=True):
        img['src'] = 'assets/' + Path(img['src']).name
        img['loading'] = 'lazy'
    for heading in main.select('section.level2 > h2'):
        title = heading.get_text(' ', strip=True)
        if title in headings:
            heading.string = headings[title]
    toc = [{'id': h.parent.get('id'), 'title': h.get_text(' ', strip=True)} for h in main.select('section.level2 > h2')]
    chapters.append({'number': number, 'title': field('title').split(': ', 1)[-1][0].upper() + field('title').split(': ', 1)[-1][1:], 'subtitle': field('subtitle'), 'description': field('description'), 'date': field('date-modified') or field('date'), 'toc': toc, 'html': main.decode_contents()})
(output / 'assets').mkdir(exist_ok=True)
for file in (root / 'assets/free-probability').iterdir():
    if file.suffix in {'.svg', '.json'}:
        shutil.copy2(file, output / 'assets' / file.name)
(output / 'resources').mkdir(exist_ok=True)
shutil.copy2(root / 'tools/free_probability_figures.py', output / 'resources/free_probability_figures.py')
(output / 'chapters.js').write_text('window.previewChapters = ' + json.dumps(chapters, ensure_ascii=False) + '\n')
print(f'Extracted {len(chapters)} existing drafts without changing their sources')
