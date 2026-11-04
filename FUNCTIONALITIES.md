# Functionalities

## Free probability series

Added 2026-10-17.

- Six complete Quarto articles cover spectra and freeness, cumulants, additive convolution, Haar-unitary experiments, multiplicative convolution, and covariance products.
- A series landing page gives prerequisites, a reading order, and links to each worked example.
- Articles contain previous and next navigation, primary references, and expandable exercise answers.
- Reproducible numerical figures and generated result tables use a fixed seed. The experiment script checks matrix unitarity, mixed moments, covariance zero mass, and product moments.
- Long equations and result tables scroll within the article on narrow screens. Theme file paths and the dark-theme footer declaration are corrected so full builds succeed.
- The homepage and blog listing link directly to the complete series.
- EDITORIAL_PLAN.md records a minimum of two publications per week and a proposed six-post release queue.

## Reproduction

Run `uv sync --frozen`, then `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run python tools/free_probability_figures.py`, then `quarto render`.

The script writes figures and check results to `assets/free-probability/` and the two result-table includes beside their articles. Published resource files include the experiment script and the result JSON.

## Isolated design comparison

Added 2026-10-18.

- `design-preview/` provides Workshop and Studio directions with identical homepage and article-opening content.
- A review toolbar switches direction and page while preserving the selected context.
- Original SVG illustrations, compact article metadata, a desktop contents column, and responsive compositions are included.
- The preview is dependency-free and separate from the existing rendered site. It does not implement full articles, publication pages, or mathematical interaction.
- Four views were checked at a 390-pixel viewport with no page-wide horizontal overflow. Desktop homepage and article layouts were visually reviewed.

## Design comparison revision 02

- Replaces decorative homepage imagery and slogans with direct personal copy and the existing Part II pairing figure.
- Workshop places the introduction above the writing. Studio uses a separate profile column beside the work and places article contents on the left.
- Narrow screens place the Studio personal-interest section after the work. The pairing diagram can scroll locally to preserve label legibility.
- Preview asset URLs are versioned to avoid stale styles and scripts during review. No existing blog pages are replaced.

## Design comparison revision 03

- Adds a writing index and a series overview with ordered chapter groups, prerequisites, and experiment resources.
- Replaces shortened article samples with snapshots of all six existing full drafts, including mathematical typesetting, native answer disclosures, and previous and next chapter navigation.
- Direction switching retains the selected route and chapter. Article contents indicate the current section.
- Adds a refresh tool that reads the existing rendered pages without modifying their sources.
- Twelve phone article views and six phone overview views passed overflow checks. All article views rendered mathematical notation without error elements. Functional controls and local resource links were checked.
- Existing blog pages, release status, and repository commits remain unchanged. The preview depends on the MathJax CDN for equation formatting.

## Design preview revision 04

Added October 18, 2026. Uncommitted local preview.

- Added a magnetic-PE project case study in both design directions, linked from the homepage.
- Uses the actual matched-width comparison figure, clearly separates historical test results from current validation results, and includes the negative charge-selection pilot.
- Bundles the two current research reports and records provenance in design-preview/PROJECT_SOURCES.md.
- Replaces middle-dot metadata separators with spacing and separate lines. Mathematical notation is preserved.
- Verified desktop presentation, 390px layout, project navigation, direction switching and local resource paths.

## Design preview revision 05

- Removed visible figure captions from both homepages, the project case study and all six free-probability chapter snapshots. Kept image alternative text.
- Removed experiment-record navigation, report downloads and the bundled magnetic-PE Markdown reports. Removed the series record links and chapter IV reproduction section from the preview.
- Rewrote project copy from the author’s perspective, using direct descriptions of decisions and findings.
- Updated the chapter extractor so refreshes preserve the caption and record-section omissions.
- Verified chapter snapshots and browser presentation. Everything remains uncommitted.

## Design preview revision 06

- Replaced generic project headings with the approved alternatives, including A negative follow-up and One graph is not enough.
- Removed redundant orange section labels and chapter-navigation labels.
- Reviewed all six probability chapters and replaced generic headings with specific mathematical topics. Preserved anchors and synchronized navigation labels.
- Added persistent heading overrides to the content extractor.
- Spread result summaries across the full plot width in two columns, with smaller type and a central gap.
- Verified chapter headings and anchors, desktop rendering and a 390px project layout. No commits or deployment.

## Reading presentation and color themes

- Hide individual article subtitles and the series prerequisites/exercises sidebar using the hidden attribute. Preserve all source text and keep the six series-list descriptions visible.
- Center the series content after hiding the sidebar in both design directions.
- Add Light, Dark and System controls with saved preferences, operating-system fallback and live system-theme updates. Keep scientific figures on light panels for legibility.
- Verified dark article rendering, preference persistence through navigation, all three choices, hidden sidebar, preserved series descriptions and a 390px Studio layout. Changes remain uncommitted.

## Mathematical review before commit

Reviewed the six chapters, their worked examples and exercise answers. Reproduced all figure-script assertions and matched the saved numerical output exactly. Browser checks found zero MathJax errors in every chapter. See design-preview/MATH_REVIEW.md for scope and evidence.

## Homepage and project discovery, revision 09

- Workshop is the default presentation. Studio remains available through the comparison control, preserving the current route.
- The homepage introduces selected writing and magnetic-PE without duplicating the full chapter index. Existing personal introduction and interests remain available for editorial review.
- Projects has a dedicated index containing the actual magnetic-PE study and comparison figure.
- Main navigation identifies the current section. Project breadcrumbs and the bottom return link lead to the Projects index.
- Added a keyboard skip link and roomier mobile navigation with theme controls.
- Checked homepage, Projects, series and article routes at 320px without page-wide overflow or broken images. Checked project return navigation, Studio comparison, light and dark presentation, and preference persistence.
- This batch remains uncommitted and unpublished.

Projects index refinement: removed the secondary status line beneath the project description. Status remains on the project detail page. Uncommitted.

## Workshop Quarto core migration

- Replaced the original website shell with a shared Workshop HTML template and presentation assets. Production pages use real URLs and do not depend on the comparison router.
- Added native homepage, Writing index, series page, Projects index and magnetic-PE case study. Existing article, About, Notes and CV URLs remain available.
- Catalog-driven indexes support project entries, ordered series groups and standalone article sources. Article prose and math remain in Quarto sources.
- Light, Dark and System persist across routes. Hidden article subtitles and figure captions preserve source content. Answers use native details elements.
- Added post-render checks for missing files, broken fragment links, duplicate IDs and h1 counts. Normalized output doctypes to keep browsers in standards mode.
- Validated all 14 rendered pages. Browser checks covered 11 primary routes at 320px, zero math errors across all six chapters, theme persistence and answer expansion. The link checker also rejected a deliberate broken-link fixture.
- Studio remains in design-preview. Local Quarto review is at port 8877. No commit, push or deployment.
- See WORKSHOP.md for authoring and maintenance instructions.

### Writing endings

Parts IV and V finish with Exercises and their answer sketches. Parts I, II, III, and VI finish with Further reading. The loose closing paragraph after Part IV’s exercises has been removed, with no additional exercises.


## Working-draft publication notices

Added November 4, 2026.

- The six existing free-probability articles retain their prose and display a bold In process of rewriting... notice directly below the title.
- The series hub and Writing index identify the same unfinished status.
- Article notices use rewrite-notice metadata and the shared template, with theme-aware presentation.
- The current website is rendered afresh before publication so the committed output matches the Workshop sources.

External preview builds exclude the existing docs tree from resource discovery to prevent duplicated output assets.
