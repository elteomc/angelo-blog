"""Build series and project indexes from the catalog and article metadata."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def esc(value):
    return html.escape(str(value), quote=True)


def field(text, key):
    match = re.search(r'^' + re.escape(key) + r':\s*(.+)$', text, re.M)
    if not match:
        raise ValueError('Missing metadata: ' + key)
    return match.group(1).strip().strip('"')


def chapter_row(item):
    if not item.get('source'):
        return (
            f'<li><div class="planned-chapter"><span class="chapter-number">{item["number"]:02}</span>'
            f'<div><h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p>'
            '<span class="chapter-state">Planned</span></div></div></li>'
        )
    source = ROOT / item['source']
    text = source.read_text()
    url = item['source'].replace('.qmd', '.html')
    return (
        f'<li><a href="{esc(url)}"><span class="chapter-number">{item["number"]:02}</span>'
        f'<div><h3>{esc(field(text, "title"))}</h3><p>{esc(field(text, "description"))}</p></div>'
        '<span class="link-mark" aria-hidden="true"></span></a></li>'
    )


def status_note(collection):
    if not collection.get('status'):
        return ''
    description = collection.get('status_description', '')
    return (
        '<aside class="publication-note" aria-label="Series status">'
        f'<strong>{esc(collection["status"])}</strong><p>{esc(description)}</p></aside>'
    )


def build():
    catalog = json.loads((ROOT / 'content/catalog.json').read_text())
    out = ROOT / '_includes'
    out.mkdir(exist_ok=True)
    writing = (
        '<div class="archive-layout"><header class="archive-header quarto-title-block">'
        '<h1>Writing</h1><p>Mathematics, algorithms, and machine learning.</p></header>'
    )
    for collection in catalog['collections']:
        rows = [chapter_row(item) for item in collection['chapters']]
        available = [row for item, row in zip(collection['chapters'], rows) if item.get('source')]
        title = esc(collection['title'])
        description = esc(collection['description'])
        first_url = collection['chapters'][0]['source'].replace('.qmd', '.html')
        introduction = collection.get('introduction', '')
        introduction_html = f'<p>{esc(introduction)}</p>' if introduction else ''
        series = (
            '<div class="series-layout"><header class="series-header quarto-title-block">'
            f'<a href="blog.html">Writing</a><h1>{title}</h1>{status_note(collection)}'
            f'<p class="series-dek">{description}</p>{introduction_html}'
            f'<a class="start-reading" href="{esc(first_url)}">Start with Part I <span class="link-mark" aria-hidden="true"></span></a></header>'
            '<div class="series-sequence">'
        )
        for group in collection['groups']:
            start = group['start']
            end = start + group['count']
            series += (
                f'<section><div class="list-heading"><h2>{esc(group["title"])}</h2></div>'
                '<ol class="reading-list">' + ''.join(rows[start:end]) + '</ol></section>'
            )
        series += '</div></div>'
        (out / (collection['include'] + '.html')).write_text(series + '\n')
        status = ''
        if collection.get('status'):
            status = f'<p class="publication-status"><strong>{esc(collection["status"])}</strong></p>'
        writing += (
            f'<section class="archive-body"><a class="series-summary" href="{esc(collection["url"])}">'
            f'<h2>{title}</h2>{status}<p>{description}</p></a>'
            '<ol class="reading-list">' + ''.join(available) + '</ol></section>'
        )
    if catalog.get('articles'):
        writing += '<section class="archive-body"><h2>Other writing</h2><ol class="reading-list">'
        for item in catalog['articles']:
            text = (ROOT / item['source']).read_text()
            url = item['source'].replace('.qmd', '.html')
            writing += (
                f'<li><a href="{esc(url)}"><div><h3>{esc(field(text, "title"))}</h3>'
                f'<p>{esc(field(text, "description"))}</p></div></a></li>'
            )
        writing += '</ol></section>'
    writing += '</div>'
    projects = (
        '<div class="projects-index"><header class="quarto-title-block"><h1>Projects</h1>'
        '<p>Experiments, implementations, and the questions they left me with.</p></header>'
    )
    for item in catalog['projects']:
        if not (ROOT / item['url'].replace('.html', '.qmd')).exists():
            raise ValueError('Missing project source: ' + item['url'])
        projects += (
            f'<article class="indexed-project"><div><p class="home-meta">{esc(item["topic"])} '
            f'<span>{esc(item["date"])}</span></p><h2><a href="{esc(item["url"])}">{esc(item["title"])}</a></h2>'
            f'<p>{esc(item["description"])}</p><a class="text-link" href="{esc(item["url"])}">Read the project <span class="link-mark" aria-hidden="true"></span></a>'
            f'</div><a class="index-figure" href="{esc(item["url"])}"><img src="{esc(item["image"])}" '
            f'alt="{esc(item["alt"])}" width="1800" height="756"></a></article>'
        )
    projects += '</div>'
    (out / 'writing.html').write_text(writing + '\n')
    (out / 'projects.html').write_text(projects + '\n')


if __name__ == '__main__':
    build()
