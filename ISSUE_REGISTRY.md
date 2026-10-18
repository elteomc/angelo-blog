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
