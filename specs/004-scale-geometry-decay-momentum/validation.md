# Review validation

Checked November 4, 2026.

## Drafts and evidence

- Part 3 is approximately 1,540 source words, including equations and metadata. It derives the radius recurrence, an exact no-momentum schedule equivalence, and a separately qualified frozen-statistic equilibrium calculation.
- Part 4 is approximately 1,700 source words. It states a decoupled, unscaled-gradient buffer convention, derives the radial and tangent geometry, and includes the exact transformed-buffer calculation in an expandable section.
- Nine numerical checks pass. They cover numerical differentiation, the printed examples and exercise answers, variable-schedule equivalence across 60 minibatches, radius recurrence, angle quadrants, nonzero momentum-state transport, the changed-memory clock transformation, and a coupled-versus-decoupled control.
- The decay figure evolves the two coordinate systems independently. Predictions agree within 1e-12 in the 24-step worked example.
- Primary source locations checked: van Laarhoven Sections 2 through 4, Li and Arora Definition 1.2 and Sections 2.1 through 2.3, Loshchilov and Hutter Section 2 and Algorithm 1, Kosson and collaborators Sections 2 and 3.1 and Appendices C and L, and the Intrinsic Learning Rate paper's Theorem 5.1 and Conjecture 5.3.
- No optimizer benchmark or network-training result is claimed or reproduced. The figures illustrate the explicitly defined toy calculations.

## Rendering

- Complete preview render: 19 pages pass heading, asset, local-link, and anchor checks.
- The two existing catalog regression checks and earlier scale-geometry numerical checks still pass.
- Both articles display Draft for review, retain the Yo twin, go read... source heading, and link to the correct series hub.
- Navigation continues from Part 2 to Part 3 to Part 4. Part 4 has no link to the unwritten Part 5.
- The hub identifies two published posts, two new review drafts, and eight planned chapters.
- Browser checks found 88 MathJax containers in Part 3 and 101 in the final Part 4, with zero math error elements.
- Both posts were inspected at a 390-pixel viewport without page-wide overflow. Figures load with explicit alternative text.
- The three new figures were visually inspected. The expandable momentum derivation opens correctly and has no math errors.
- Temporary viewport overrides were reset after the phone checks. The Part 3 review screenshot is at desktop width.

## Publication boundary

- All draft work is uncommitted on codex/scale-geometry-posts-3-4.
- HEAD and the saved origin/main both remain f7f742de33f67a8375bfa80394909311e130ae64.
- The published docs tree has no changes. No push or deployment was performed.
- git diff --check passes.

## Review links

- Part 3: http://127.0.0.1:8878/blog/scale-geometry-3/index.html
- Part 4: http://127.0.0.1:8878/blog/scale-geometry-4/index.html
- Hub: http://127.0.0.1:8878/scale-geometry.html

The preview server serves /tmp/angelo-scale-geometry-review. Both articles are left open as review tabs.


## Publication approval

Angelo reviewed and approved publication of posts 3 and 4. Remove their review-only notices and update the public hub and homepage to identify four available posts. Retain the recorded mathematical and rendering checks above as the initial review evidence. Publish matching sources and rendered docs together.
