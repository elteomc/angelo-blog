"""Build index fragments from the content catalog and article metadata."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'content/catalog.json').read_text())
out = ROOT / '_includes'
out.mkdir(exist_ok=True)
def esc(value):
    return html.escape(str(value), quote=True)
def field(text, key):
    match = re.search(r'^' + key + r':\s*(.+)$', text, re.M)
    if not match:
        raise ValueError('Missing metadata: ' + key)
    return match.group(1).strip().strip('"')
rows = []
for item in catalog['series']:
    source = ROOT / item['source']
    text = source.read_text()
    url = item['source'].replace('.qmd', '.html')
    rows.append(f'<li><a href="{esc(url)}"><span class="chapter-number">{item["number"]:02}</span><div><h3>{esc(field(text, "title"))}</h3><p>{esc(field(text, "description"))}</p></div><span aria-hidden="true">↗</span></a></li>')
listing = '<ol class="reading-list">' + ''.join(rows) + '</ol>'
series = '<div class="series-layout"><header class="series-header quarto-title-block"><a href="blog.html">Writing</a><h1>Free probability</h1><p class="series-dek">Knowing the eigenvalues of two matrices does not determine the eigenvalues of their sum or product.</p><p>This series studies what happens when their eigenvectors are randomly oriented, then develops the tools that make the limiting calculations possible.</p><a class="start-reading" href="blog/free-prob-1/index.html">Start with Part I ↗</a></header><div class="series-sequence">'
for group in catalog['series_groups']:
    label, start, count = esc(group['title']), group['start'], group['count']
    series += '<section><div class="list-heading"><h2>' + label + '</h2></div><ol class="reading-list">' + ''.join(rows[start:start+count]) + '</ol></section>'
series += '</div></div>'
writing = '<div class="archive-layout"><header class="archive-header quarto-title-block"><h1>Writing</h1><p>Mathematics, algorithms, and machine learning.</p></header><section class="archive-body"><a class="series-summary" href="free-probability.html"><h2>Free probability</h2><p>From the geometry of a matrix sum to covariance products.</p></a>' + listing + '</section></div>'
if catalog.get('articles'):
    standalone = '<section class="archive-body"><h2>Other writing</h2><ol class="reading-list">'
    for item in catalog['articles']:
        text = (ROOT / item['source']).read_text()
        url = item['source'].replace('.qmd', '.html')
        standalone += f'<li><a href="{esc(url)}"><div><h3>{esc(field(text, "title"))}</h3><p>{esc(field(text, "description"))}</p></div></a></li>'
    standalone += '</ol></section>'
    writing = writing[:-6] + standalone + '</div>'
projects = '<div class="projects-index"><header class="quarto-title-block"><h1>Projects</h1><p>Experiments, implementations, and the questions they left me with.</p></header>'
for item in catalog['projects']:
    if not (ROOT / item['url'].replace('.html','.qmd')).exists():
        raise ValueError('Missing project source: ' + item['url'])
    projects += f'<article class="indexed-project"><div><p class="home-meta">{esc(item["topic"])} <span>{esc(item["date"])}</span></p><h2><a href="{esc(item["url"])}">{esc(item["title"])}</a></h2><p>{esc(item["description"])}</p><a class="text-link" href="{esc(item["url"])}">Read the project ↗</a></div><a class="index-figure" href="{esc(item["url"])}"><img src="{esc(item["image"])}" alt="{esc(item["alt"])}" width="1800" height="756"></a></article>'
projects += '</div>'
for name, content in [('series',series), ('writing',writing), ('projects',projects)]:
    (out / (name + '.html')).write_text(content + '\n')
