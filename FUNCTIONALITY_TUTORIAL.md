
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


## Scale and geometry review series

Prepared November 4, 2026 on a local review branch after publishing the existing site.

- Added the Scale and geometry hub with a twelve-question outline and two complete opening drafts.
- Added worked derivations, primary sources, exercises, and reproducible SVG diagrams about radius-dependent SGD steps and normalization placement.
- Prioritized this series in the editorial plan and retained free probability with its rewriting notices.
- Replaced the single-series catalog with independent collections and per-article hub paths. Planned chapters remain visible without broken links.
- The local homepage features the new series. The committed docs tree remains the published release until editorial approval.


## Series publication and personal presentation

Updated November 4, 2026 after publication approval.

- Publish the Scale and geometry hub and first two posts, with ten later chapters clearly marked as planned.
- Use an original compact skull ornament in place of decorative link arrows across the production layout, indexes, and project page. Text labels remain accessible and the mark inherits the theme color.
- Rename the homepage groups Recent writing and Recent projects, remove the affiliation above the name, and let the interests sentence use the available desktop width.
- Keep natural line wrapping on phones. The previous desktop wrap came from an inherited 500-pixel maximum width.
- Rename the two opening source sections Yo twin, go read... while retaining their references and stable source-section anchors.


## Weight decay and momentum review drafts

Prepared November 4, 2026 on a separate local review branch.

- Added parts 3 and 4 with exact radius and angle identities, a momentum-free schedule equivalence, explicit momentum conventions, worked examples, exercises, and primary references.
- Added three reproducible figures and numerical checks comparing independently evolved trajectories and optimizer states.
- Linked the new local drafts from the series hub and chapter navigation. Both articles display Draft for review, and the hub distinguishes two published posts, two review drafts, and eight planned chapters.
- The published docs tree remains unchanged. No new draft content is committed or pushed before review.


## Publish the weight decay and momentum posts

Approved November 4, 2026 after review.

- Publish parts 3 and 4 with their worked derivations, figures, exercises, and checked source references.
- Remove the review-only notices and update the hub and homepage to show four available posts and eight planned chapters.
- Preserve the established occasional orange italics, skull ornaments, and informal source headings.


## Layer geometry and dual norm review drafts

Prepared November 4, 2026 after publication of the first four posts.

- Added parts 5 and 6 with activation perturbation bounds, RMS width factors, dense and lookup semantics, dual support problems, and polar directions.
- Added two reproducible diagrams, worked examples, exercises, and numerical checks for induced norms and duality.
- Preserved occasional italic emphasis in the orange accent and the established source-heading voice.
- Linked the new local drafts from Part 4 and the hub. The local index distinguishes four published posts, two review drafts, and six planned chapters.
- The published docs tree remains at the posts 3 and 4 release. New drafts remain uncommitted and unpushed until review.


## Publish layer geometry and dual norms

Approved November 4, 2026.

- Publish Parts 5 and 6 after review, including their two diagrams and twelve numerical checks.
- Use P: and N: with the respective chapter titles in bottom navigation, retaining skull marks and descriptive assistive labels.
- Update the hub and homepage to show six available posts. Completion and publication of Parts 7 through 12 is authorized after validation.

## Complete Scale and geometry

Published November 4, 2026 with authorization to finish the agreed outline.

- Added Parts 7 through 12 with modular budget allocation, tangent constraints and retractions, angular schedules, learnable scales, shared-gain feasibility, and research controls.
- Added six reproducible diagrams and seventeen numerical checks for the worked examples, finite isotropic teacher evaluations, and attention factorization controls.
- Directly evaluated 45 frozen-feature target ratios. Independent-radius losses match the analytic floor within 1e-12. A joint radius and independent branch multipliers restore exact fitting in this model.
- Made all twelve chapters available in the hub and Writing index, completed neighbor navigation, and updated homepage and editorial status.
- Preserved orange italic emphasis, skull ornaments, P: and N: title links, informal source headings, and the existing free-probability rewriting notices.
- The closing notes distinguish exact local calculations from proposed training experiments.

## Simplify the series introduction

Updated November 4, 2026.

- Remove the long introductory paragraph and publication-status panel from the Scale and geometry hub.
- Remove the series count and completion metadata from the homepage and the completion label from the Writing index.
- Allow a collection to omit its introduction without producing an empty paragraph. Keep the short series question and chapter links.
- Rebuild generated includes, rendered pages, and search data from the corrected sources.

## Remove personal references from research notes

Updated November 4, 2026.

- Remove personal collaborator references from the closing Scale and geometry posts, internal editorial instructions, rendered articles, and search data.
- Preserve the mathematical arguments, primary references, exercises, and chapter navigation.
- Apply the same neutral wording to earlier repository revisions and verify the published history before replacing it.

The editorial plan now maps ten follow-up questions to dossier sources and distinguishes the neighboring width-scaling and training-dynamics sequences. The backlog also includes the stochastic feature-selection calculation and ordinary-network response controls. This is an internal backlog, with no additional public chapters.

## Practical polar, averaging, and norm-budget drafts

Prepared November 4, 2026 for review.

- Add Parts 13 through 15 with worked derivations, four reproducible figures, numerical tables, exercises, and primary references.
- Verify finite polar evaluation, stochastic normalization bias, estimator variance and lag, support defects, and norm envelopes with eighteen numerical checks.
- Extend the local hub and P: and N: chapter navigation with open-ended part labels, preserving orange italics and skull ornaments.
- Mark the new articles as review drafts. Keep the published docs output unchanged and render the local preview externally.

## Publish the practical follow-up posts

Approved November 5, 2026 after review.

- Publish Parts 13 through 15 and their four figures, worked examples, exercises, and eighteen numerical checks.
- Remove review notices and retain the open-ended part labels and title-based P: and N: links.
- Render the complete site afresh so the published output matches the approved sources.


## Residual, width, and normalized-head review drafts

Prepared November 5, 2026 for review after publishing Parts 13 through 15.

- Add Parts 16 through 18 with full derivations, three reproducible figures, numerical examples, exercises, and primary source links.
- Verify the examples with twenty-three checks in tools/check_network_scaling.py. Rebuild their figures with tools/network_scaling_figures.py.
- Extend the local catalog with the Networks, scaling, and feature motion group. Connect Part 15 to Part 16 using title-based P: and N: navigation.
- Keep Draft for review notices on the three new articles. Keep their work uncommitted and unpushed until review, and preserve the published docs tree.
- Review at http://127.0.0.1:8878/blog/scale-geometry-16/index.html and follow the chapter links through Part 18.


## Publish the network geometry posts

Approved November 5, 2026 after review.

- Publish Parts 16 through 18 with their three figures, worked derivations, exercises, and twenty-three numerical checks.
- Remove review notices and preserve the open-ended part labels, orange emphasis, and title-based P: and N: chapter links.
- Render the approved sources into a separate release directory before updating the published docs output.


## Tangent geometry and experimental evidence review drafts

Prepared November 5, 2026 after publication of Parts 16 through 18.

- Add Parts 19 through 21 on the exact tangent spectral oracle, module-specific constraints, and archived matched-step experiments.
- Add three reproducible SVG figures and algebraic checks in tools/check_geometry_evidence.py. Preserve a source-hashed aggregate record in specs/009-tangent-constraints-evidence, outside the rendered reader resources.
- Extend the local hub with Constraints, algorithms, and evidence. Link Part 18 to Part 19 using the accepted title-based navigation.
- Keep Draft for review notices on the three articles. Render the preview externally and leave docs unchanged. The new batch remains uncommitted and unpushed until review.


Review checks for Parts 19 through 21 pass: twenty-five numerical and aggregate checks, two catalog checks, all local links across thirty-six rendered pages, and desktop and phone inspection. The three figures have alternative text, disclosures work, and the published docs tree remains unchanged. Details are in specs/009-tangent-constraints-evidence/validation.md.


## Publish the constraint and evidence posts

Approved November 5, 2026 after review.

- Publish Parts 19 through 21 with their three figures, derivations, exercises, and twenty-five numerical and archived-record checks.
- Remove their review notices while preserving orange italic emphasis, skull ornaments, and P: and N: chapter titles.
- Render the approved site separately before replacing docs and pushing the release.


## Noise, sharpness, and symmetry review drafts

Prepared November 5, 2026 after publication of Parts 19 through 21.

- Add Parts 22 through 24 on the intrinsic-noise model, finite-step sharpness selection, and optimizer-state symmetry, splitting the remaining bundled editorial question into three articles.
- Add three reproducible SVG figures, worked examples, exercises, and twenty-five checks in tools/check_noise_sharpness_symmetry.py.
- Extend the local hub with Noise, sharpness, and symmetry, and link Part 21 to Part 22 using title-based navigation.
- Mark the three articles Draft for review. Keep this batch uncommitted and unpushed until review. Render externally and preserve the published docs tree.


Review checks for Parts 22 through 24 pass: twenty-five mathematical checks, two catalog checks, thirty-nine rendered pages with valid local links, and desktop and phone inspection. Details and source qualifications are in specs/010-noise-sharpness-symmetry/validation.md. Published docs remain unchanged.


## Publish the noise and symmetry posts

Approved November 5, 2026 after review.

- Publish Parts 22 through 24 with their three figures, worked calculations, exercises, and twenty-five mathematical checks.
- Remove review notices and preserve orange italics, skull ornaments, open-ended part labels, and title-based P: and N: links.
- Render the approved site separately before replacing docs and pushing the release.
