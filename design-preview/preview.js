const params = new URLSearchParams(location.search);
const direction = params.get('direction') === 'studio' ? 'studio' : 'workshop';
const page = ['home', 'writing', 'series', 'article', 'project'].includes(params.get('page')) ? params.get('page') : 'home';
const requestedChapter = Number(params.get('chapter'));
const chapterNumber = Number.isInteger(requestedChapter) && requestedChapter >= 1 && requestedChapter <= 6 ? requestedChapter : 1;
const chapters = window.previewChapters;
const chapter = chapters[chapterNumber - 1];
const url = (targetPage, targetDirection = direction, targetChapter = chapterNumber) => `?direction=${targetDirection}&page=${targetPage}&chapter=${targetChapter}&revision=8`;
const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[char]));
const chapterRows = items => items.map(item => `<li><a data-chapter="${item.number}" href="${url('article', direction, item.number)}"><span class="chapter-number">${String(item.number).padStart(2, '0')}</span><div><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.description)}</p></div><span class="entry-open" aria-hidden="true">↗</span></a></li>`).join('');
document.body.dataset.direction = direction;
document.body.dataset.page = page;
const main = document.querySelector('#main');
if (page === 'home') {
  main.append(document.querySelector(`#${direction === 'studio' ? 'studio-home' : 'home'}-template`).content.cloneNode(true));
} else if (page === 'project') {
  main.innerHTML = window.projectWriting;
} else if (page === 'writing') {
  main.innerHTML = `<div class="archive-layout"><header class="archive-header"><p class="eyebrow">Writing</p><h1>Notes on what<br>I’m learning.</h1><p>Mathematics, algorithms, and machine learning.</p></header><section class="archive-body"><a class="series-summary" href="${url('series')}"><span class="label">Six draft chapters</span><h2>Free probability</h2><p>From the geometry of a matrix sum to covariance products.</p><span class="text-link">About the series ↗</span></a><div class="list-heading"><h2>Chapters</h2><span>In reading order</span></div><ol class="reading-list">${chapterRows(chapters)}</ol></section></div>`;
} else if (page === 'series') {
  main.innerHTML = `<div class="series-layout"><header class="series-header"><a class="eyebrow" href="${url('writing')}">Writing / Series</a><p class="chapter">Six chapters <span>Drafts for review</span></p><h1>Free probability</h1><p class="series-dek">Knowing the eigenvalues of two matrices does not determine the eigenvalues of their sum or product.</p><p>This series studies what happens when their eigenvectors are randomly oriented, then develops the tools that make the limiting calculations possible.</p><a class="start-reading" href="${url('article', direction, 1)}">Start with Part I <span aria-hidden="true">↗</span></a></header><aside class="series-prerequisites" hidden><h2>Before reading</h2><p>Linear algebra, basic probability, and comfort with power series.</p><p>Parts III and VI use a little complex analysis. Transform conventions and inversion formulas are introduced along the way.</p><h2>Exercises</h2><p>Each chapter has exercises with answer sketches. Try a calculation before opening its answer.</p></aside><div class="series-sequence"><section><div class="list-heading"><h2>Freeness and cumulants</h2><span>Parts I & II</span></div><ol class="reading-list">${chapterRows(chapters.slice(0,2))}</ol></section><section><div class="list-heading"><h2>Adding matrices</h2><span>Parts III & IV</span></div><ol class="reading-list" start="3">${chapterRows(chapters.slice(2,4))}</ol></section><section><div class="list-heading"><h2>Multiplying matrices</h2><span>Parts V & VI</span></div><ol class="reading-list" start="5">${chapterRows(chapters.slice(4,6))}</ol></section></div></div>`;
} else {
  const previous = chapterNumber > 1 ? `<a class="previous-chapter" href="${url('article', direction, chapterNumber-1)}"><span>Previous: Part ${chapterNumber-1}</span><strong>${escapeHtml(chapters[chapterNumber-2].title)}</strong></a>` : '';
  const next = chapterNumber < 6 ? `<a class="next-chapter" href="${url('article', direction, chapterNumber+1)}"><span>Next: Part ${chapterNumber+1}</span><strong>${escapeHtml(chapters[chapterNumber].title)}</strong></a>` : `<a class="next-chapter" href="${url('series')}"><span>All six chapters</span><strong>Return to the series</strong></a>`;
  main.innerHTML = `<div class="article-layout"><article><header class="article-header"><a class="eyebrow" href="${url('series')}">Free probability / Part ${chapterNumber} of 6</a><h1>${escapeHtml(chapter.title)}</h1><p class="dek" hidden>${escapeHtml(chapter.subtitle)}</p><div class="article-meta"><span>Angelo Farfan</span><span>Draft for review</span></div></header><div class="article-body full-draft">${chapter.html}<nav class="chapter-navigation" aria-label="Chapter navigation">${previous}${next}</nav></div></article><aside class="contents"><nav aria-label="On this page">${chapter.toc.map(section=>`<a href="#${escapeHtml(section.id)}">${escapeHtml(section.title)}</a>`).join('')}</nav><a class="back-to-series" href="${url('series')}">All six chapters ↗</a></aside></div>`;
  window.MathJax = {startup: {typeset: true}, options: {enableMenu: false}};
  const mathScript = document.createElement('script');
  mathScript.src = 'https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js';
  mathScript.async = true;
  mathScript.onerror = () => {
    const notice = document.createElement('p');
    notice.className = 'math-notice';
    notice.textContent = 'Equation formatting could not load. Mathematical notation is shown in source form.';
    document.querySelector('.article-body').prepend(notice);
  };
  document.head.append(mathScript);
}
document.querySelectorAll('[data-direction]').forEach(a => {
  a.href = url(page, a.dataset.direction);
  if (a.dataset.direction === direction) a.setAttribute('aria-current', 'true');
});
document.querySelectorAll('[data-page]').forEach(a => {
  a.href = url(a.dataset.page);
  if (a.dataset.page === page) a.setAttribute('aria-current', 'page');
});
document.querySelectorAll('[data-project]').forEach(a => a.href = url('project'));
document.querySelectorAll('[data-home]').forEach(a => a.href = url('home'));
document.querySelectorAll('[data-article]').forEach(a => a.href = url('article', direction, 1));
document.querySelectorAll('[data-series]').forEach(a => a.href = url('series'));
document.querySelectorAll('[data-writing]').forEach(a => a.href = url('writing'));
document.querySelectorAll('[data-chapter]').forEach(a => a.href = url('article', direction, Number(a.dataset.chapter)));
for (const section of ['projects', 'about']) {
  document.querySelectorAll(`[data-${section}]`).forEach(a => a.href = `${url('home')}#${section}`);
}
if (page === 'article') {
  const sectionLinks = [...document.querySelectorAll('.contents nav a')];
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        sectionLinks.forEach(link => {
          if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      }
    }
  }, {rootMargin: '-10% 0px -65% 0px'});
  document.querySelectorAll('.full-draft section.level2').forEach(section => observer.observe(section));
}
document.title = `Angelo Farfan: ${direction === 'studio' ? 'Studio' : 'Workshop'}, ${page === 'article' ? chapter.title : page[0].toUpperCase()+page.slice(1)}`;
