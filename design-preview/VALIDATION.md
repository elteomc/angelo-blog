# Revision 03 validation

Checked 2026-10-18 in the local browser preview.

- All six full draft articles were opened in both directions at a 390-pixel viewport. All twelve views rendered mathematical notation with no MathJax error elements and no page-wide horizontal overflow.
- Home, Writing, and Series were opened in both directions at the same viewport. Each had one primary heading and no page-wide horizontal overflow.
- Part II answer sketches were opened and their mathematical content was rendered.
- Switching from Workshop to Studio retained Part II and its article title.
- All imported local resource paths and section anchors resolved against the snapshot.
- Desktop article, writing-index, and series layouts were visually inspected.

These checks cover the prototype's presentation and navigation. They do not constitute a new mathematical review, a deployment check, or approval to publish the draft series. Equation formatting requires the MathJax CDN. No new numerical experiment was run in this batch.

## Revision 04 checks

- Inspected the project opening in Workshop and Studio on desktop, plus Workshop on a 390px viewport.
- Both project directions fit the 390px viewport without page-wide overflow.
- Verified Studio homepage to project navigation and project direction switching.
- Project image loaded, local resource paths exist, and authored HTML/JavaScript contain no middle-dot separators.
- Preserved existing chapter snapshots and math content. No experiments or public deployment were run.

## Revision 05

Checked all six chapter snapshots for removed figure captions. The project has no report links or evidence section, and the two report files are no longer bundled. The content extractor preserves these omissions on refresh. Browser inspection confirmed the revised project layout and zero figure captions or report links.

## Revision 06

Project headings now name the research questions and decisions. Removed redundant section labels across the project and probability series. Revised generic chapter headings while keeping stable section anchors and matching sidebar titles. heading_overrides.json preserves these edits during content refreshes. Results use the full figure width with two separated columns and smaller numbers. Checked all six chapter heading/anchor pairs, desktop rendering, mobile overflow and chapter II navigation.

## Reading presentation and color themes

- Hide individual article subtitles and the series prerequisites/exercises sidebar using the hidden attribute. Preserve all source text and keep the six series-list descriptions visible.
- Center the series content after hiding the sidebar in both design directions.
- Add Light, Dark and System controls with saved preferences, operating-system fallback and live system-theme updates. Keep scientific figures on light panels for legibility.
- Verified dark article rendering, preference persistence through navigation, all three choices, hidden sidebar, preserved series descriptions and a 390px Studio layout. Changes remain uncommitted.

## Homepage and project discovery, revision 09

- Workshop is the default presentation. Studio remains available through the comparison control, preserving the current route.
- The homepage introduces selected writing and magnetic-PE without duplicating the full chapter index. Existing personal introduction and interests remain available for editorial review.
- Projects has a dedicated index containing the actual magnetic-PE study and comparison figure.
- Main navigation identifies the current section. Project breadcrumbs and the bottom return link lead to the Projects index.
- Added a keyboard skip link and roomier mobile navigation with theme controls.
- Checked homepage, Projects, series and article routes at 320px without page-wide overflow or broken images. Checked project return navigation, Studio comparison, light and dark presentation, and preference persistence.
- This batch remains uncommitted and unpublished.
