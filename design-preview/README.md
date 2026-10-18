# Design study 03

Two isolated visual directions with a homepage, writing index, series overview, and all six existing free-probability drafts. The toolbar retains the current route and chapter when switching directions.

Workshop uses a spacious introduction and a right-hand article contents column. Studio places a compact profile beside the work and uses left-hand contents and prerequisites. Both use the same content.

## This revision

- The Writing navigation opens a dedicated index. Chapter rows follow reading order rather than draft timestamps.
- The series page groups chapters into foundations, addition, and multiplication, with prerequisites and experiment resources.
- All chapter links open the corresponding full draft. Previous and next links retain the chosen direction.
- Answer sketches use native expandable details. Article figures open at full size in another tab.
- Article contents indicate the section being read. Wide mathematics, code, and tables remain contained on narrow screens.
- The text and mathematical claims are taken from the existing rendered drafts. This is a design review, not a new content approval.

## Running and refreshing

Run a static HTTP server from this directory and open `index.html`. No JavaScript build step is required. Article math uses the same MathJax 4 CDN endpoint as the existing site, so equation formatting requires network access. A readable error notice appears if the script fails to load.

To refresh the imported drafts after rendering the main site, run `python3 build_content.py /absolute/path/to/angelo-blog`. The refresh tool requires Beautiful Soup 4. It copies the article bodies and existing SVG assets into this preview, converts answer callouts to native details, and rewrites internal chapter links. It does not modify the original drafts. Run the tool only after rendering the intended source revisions.

The preview includes a snapshot of the existing experiment script and numerical checks for resource links. Running that script is outside the preview workflow.

## Review boundary

This directory is not wired into public navigation or copied to `docs/` by this batch. Before a future public Quarto build, explicitly exclude design studies and verify output. Publication and notebook pages, new project case studies, dark mode, video, and interactive mathematics remain later phases.

The original decorative homepage diagrams and slogans remain removed. The pairing figure comes from Part II. All six articles remain drafts. No content is labeled as an original publication or a released series.

Commit only after explicit review and approval. Preserve unrelated uncommitted work.

## Revision 04

Open `?direction=workshop&page=project&revision=4` or switch to Studio. The project case study replaces the homepage placeholder with magnetic-PE research. Reports and the real comparison figure are bundled locally. See PROJECT_SOURCES.md for provenance. Metadata uses spacing and separate lines instead of middle-dot separators.

## Revision 05

Figure captions are omitted across the preview, including all six chapter snapshots. Image alternative text remains available to screen readers. Experiment reports and record links are removed from the reader-facing pages, and project copy uses the author’s perspective. Open with revision=5.

## Revision 06

Project headings now name the research questions and decisions. Removed redundant section labels across the project and probability series. Revised generic chapter headings while keeping stable section anchors and matching sidebar titles. heading_overrides.json preserves these edits during content refreshes. Results use the full figure width with two separated columns and smaller numbers. Checked all six chapter heading/anchor pairs, desktop rendering, mobile overflow and chapter II navigation.

## Revision 09

Open `?page=home&revision=9` for the Workshop homepage or `?page=projects&revision=9` for the project index. Studio remains available through Compare Studio. Shared navigation keeps the current direction and theme.
