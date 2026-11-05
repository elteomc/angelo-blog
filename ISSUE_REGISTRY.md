# Issue registry

## FP-001: incomplete introductory article

Found 2026-10-17. The free probability introduction contains empty closing sections, an undefined B_1 in its first example, and malformed mathematical table markup. Status: resolved in the six-part series. The introduction now defines both matrix choices, uses valid display mathematics, and ends with completed calculations, references, and exercises. Render verification is recorded in the series validation note.

## FP-002: theme paths resolve outside the project

Found 2026-10-17 during a full Quarto build. Leading slashes on the two SCSS theme files are interpreted as filesystem-root paths and produce missing-theme warnings. Status: resolved by using project-relative theme paths.

## FP-003: internal planning documents enter the site build

Found 2026-10-17 during a full Quarto build. Default document discovery attempts to publish internal Markdown records. Status: resolved by explicitly rendering root Quarto pages and article index files.

## FP-004: invalid SCSS footer declarations

Found 2026-10-17 after resolving the theme paths. The dark theme contains a bare top-level footer declaration, so Sass compilation fails. Status: resolved by restoring the missing variable marker. Full-build validation passed.

## FP-005: mathematical displays overflow phone-width pages

Found 2026-10-17 in the browser at 390 pixels. Long displays expand the document beyond the viewport despite the existing overflow rule. Status: resolved with block-level scrolling equation containers and responsive wrappers around wide result tables. The articles are checked at a 390-pixel viewport.

## Resolved: stale design-preview assets

Found and resolved 2026-10-18. Reloading the revised HTML could retain the prior stylesheet and template-selection script from browser cache. Versioned preview asset URLs now load the matching revision. Verified by inspecting the two-column Studio homepage after reload.

## Resolved: missing design-preview theme controls

The original Quarto site retained light and dark configuration, but the isolated preview had no theme control. Added a shared Light, Dark and System selector with persistent preference and theme palettes for Workshop and Studio. Verified navigation persistence and mobile layout.

## Workshop migration integration issues

- Initial render required generated includes before Quarto discovered project inputs. Keep generated includes in the project and refresh them before rendering.
- Custom layout headings were moved by Quarto title-block processing. Disable that processing for the shared template.
- Minimal HTML flattened collapsed callouts. Use native details elements for exercise answers.
- The rendered document omitted its doctype and entered browser quirks mode. Restore the standard doctype in a post-render validation step.
- Homepage project-index link matched the singular project route during conversion. Correct the explicit index target.

Workshop migration issues above are resolved and verified in the final 14-page build. Quarto canonicalization requires explicit quarto-title-block classes on the intended heading containers. Native details replace flattened callouts. The post-render checker restores the doctype and enforces internal-link integrity. Internal experiment JSON is excluded from output resources.


## PUB-001: published assets enter an external preview build twice

Found November 4, 2026 while preparing the current site for publication. Rendering to an external output directory lets existing docs assets enter resource discovery and creates a redundant docs/assets subtree inside the new output. Status: resolved. The committed docs tree is excluded from project resources. A fresh 14-page render passed all local-link checks and contains no nested docs tree.


## PUB-002: series navigation and discovery assume free probability

Found November 4, 2026 while preparing a second series. The article template sends every series label to free-probability.html and says All six chapters. The catalog generator also fixes the Writing index and hub to that series. Status: resolved in the local review branch. Collections now own hub metadata, ordered chapters, and planned entries. Article hub paths are explicit, and all existing chapter URLs are preserved. Regression tests cover separate collection indexes and unwritten chapter handling.


## PUB-003: inherited asset prefix is rebased for new chapter folders

Found November 4, 2026 in the first new-series render. New articles relying only on the blog folder metadata receive a three-level prefix instead of the required two-level prefix, breaking navigation and shared assets. Status: resolved. New articles explicitly set site-root to ../../. The full 17-page render passes all local links, and header and sidebar hub targets were checked for all eight articles.

## PUB-004: planned chapter HTML is misparsed during inclusion

Found November 4, 2026 in the first new-series hub render. The generated planned-chapter markup triggers unclosed-div warnings when included as Markdown. Status: resolved. The new hub includes its generated fragment inside a raw HTML block. The complete render has no unclosed-div warnings and the hub contains two linked drafts plus ten unlinked planned entries.


## PUB-005: image captions do not provide rendered alternative text

Found November 4, 2026 in the new draft output. The two diagram descriptions written as image captions are omitted from the rendered img alternative text by the current rendering path. Status: resolved. Both diagrams set explicit fig-alt attributes, and browser inspection confirms their full alternative text and successful loading.


## UI-001: homepage interest text wraps prematurely on desktop

Found November 4, 2026 during publication review. The inherited plain-intro interest rule caps the sentence at 500 pixels even when the homepage has enough width for one line. Status: resolved. The homepage interest sentence uses the full desktop width and stays on one line at desktop sizes. Browser checks confirm normal wrapping and no page overflow at 390 pixels.


## UI-002: cached Workshop stylesheet hides the latest presentation

Found November 4, 2026 during browser verification. Reloading the changed HTML retained the prior stylesheet, so the skull ornaments were invisible and the interest sentence still used the old width cap. The rendered CSS already contained the correct rules. Status: resolved. The shared stylesheet URL now carries a release version. Browser inspection confirms the skull mask loads and the interest line uses the corrected width.


## CHECK-001: experiment aggregate check uses an incorrect precision constant

Found November 5, 2026 while checking the new experiment article. A hand-entered full-precision expectation for the four-head mean differs from the saved aggregate, although both round to the correct displayed value. Status: resolved. Verify the displayed six-decimal value against the independently recomputed paired mean. Raw seed differences and their full-precision aggregate remain checked separately.


## UI-003: attention figure footnote clips in the rendered image

Found November 5, 2026 during desktop review of Part 20. A long single-line figure footnote is clipped in the embedded rendering. Status: resolved by shortening the annotation while retaining its exact-example and no-training scope. The article carries the full assumptions beside the figure.


## UI-004: moment-rotation annotation overlaps its curve

Found November 5, 2026 during desktop review of Part 24. The point annotation touches the descending curve. Status: resolved by placing the annotation above the selected point, with the value unchanged.
