# Review validation

Checked November 4, 2026.

## Published baseline

Posts 3 and 4 were approved and pushed in 41852d9aa8a2e88844461679d5bad44fe9c4f698. GitHub Pages reports a successful build for that commit. The published hub identifies four available posts, and the approved articles no longer carry review-only notices.

## Mathematical evidence

- Twelve new numerical checks pass, covering the Frobenius-versus-spectral activation example, a nonzero-mean input second moment, RMS width factors and attaining inputs, lookup semantics, and the moving-input cross term.
- Matrix support checks cover rectangular polar factors, Frobenius and nuclear budgets, the printed diagonal examples, rank-deficient and zero gradients, reciprocal dual scaling, columnwise embedding duality, and the squared-norm model and finite-step overshoot example.
- Support constructions are checked for feasibility and attainment. Independently sampled feasible matrices are also tested against the support bounds.
- The nine decay and momentum checks, two catalog regression checks, and earlier scale-geometry numerical checks still pass.
- Primary sources were read at the cited locations: Modular Duality Sections 3.1 through 3.3, Proposition 1, and Section 4.1, the modular-norm paper's module and scaling conventions, and Boyd and Vandenberghe Section 9.4 and Appendix A.1.6.

## Presentation

- Complete preview render: 21 pages pass headings, assets, local links, and fragment checks.
- Browser checks found 61 MathJax containers in Part 5 and 87 in Part 6, with zero math error elements.
- Both diagrams load with explicit alternative text and were visually inspected.
- Both posts were checked at 390 pixels without page-wide overflow. Temporary test viewport overrides were reset before closing the test tab.
- The embedding lookup derivation expands successfully and has no math errors.
- Each article retains the source-heading voice and occasional italic phrases. Browser inspection confirms their orange accent color in dark mode, rgb(233, 161, 126).
- The local hub distinguishes four published posts, two review drafts, and six planned chapters. Chapter navigation continues from Part 4 to Part 5 to Part 6, with no link to unwritten Part 7.

## Publication boundary

The new drafts are uncommitted on codex/scale-geometry-posts-5-6. HEAD and the saved origin/main remain at the posts 3 and 4 release. The published docs tree is unchanged, and no new draft files were pushed. git diff --check passes.

## Review links

- Part 5: http://127.0.0.1:8878/blog/scale-geometry-5/index.html
- Part 6: http://127.0.0.1:8878/blog/scale-geometry-6/index.html
- Hub: http://127.0.0.1:8878/scale-geometry.html

The preview server serves /tmp/angelo-scale-geometry-review. Both new drafts are left open in review tabs.


## Publication approval

Angelo reviewed and approved Parts 5 and 6. Remove the review notices, publish matching sources and docs, and use the requested P: and N: bottom-navigation labels. Earlier publication-boundary statements record the initial review stage.
