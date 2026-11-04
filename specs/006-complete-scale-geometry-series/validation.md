# Completion validation

Checked November 4, 2026.

## Mathematical examples

The existing scale checks pass. All 40 unit checks pass across collection behavior (2), decay and momentum (9), layer geometry and duality (12), and final-series examples (17).

The new checks cover weighted modular support bounds, the printed three-budget example, sphere and Stiefel projections and retractions, the projected-polar counterexample, oblique singular values, actual fixed-norm angles, conditional one-step schedule matching, coordinate SGD under reciprocal scale changes, effective-map differentials, positive-gain reconstruction, two-branch energy ratios, scalar fitting floors, finite-design controls, attention factorization, the scalar attention escape, and rotary restrictions.

The frozen teacher uses seed 1126, four-dimensional inputs at the eight equally weighted points plus and minus twice each coordinate vector, and 45 target norm ratios from 0.25 to 3. The maximum discrepancy between direct evaluated loss and the analytic floor is 4.440892098500626e-16. Maximum group loss is 4.930380657631324e-32. Maximum independent-multiplier loss is 6.162975822039155e-33. The script checks both individual radii and the joint radius. These are direct evaluations of specified representatives, with no training claim.

See frozen-teacher-results.json for the complete record and WORKSHOP.md for reproduction commands.

## Primary source checks

- Scalable Optimization in the Modular Norm, Sections 2.2 and 3, and Modular Duality, Sections 3.4 and 4.2, support the composition and weighted-maximum discussion. Alternative support calculations are derived directly in Part 7.
- Modular Manifolds distinguishes constraints, tangent geometry, and return maps. Part 8 states its column-Stiefel convention and derives its displayed identities.
- Hyperball v2, Section 2 and Sections 4.1 and 4.2, supplies the wrapper and the separate expressivity and stationary assumptions. The iid isotropic Gaussian and infinite-history assumptions are explicit in Part 9.
- Hyperball May Not Be a Free Lunch v1, Sections 2 through 4, supports angle-aware comparisons in its tested settings. No universal trajectory equality or reproduction of its training results is claimed.
- Learnable Multipliers v1, Sections 2 and 4.1 and Appendix C, supports multiplier placement and redundant-symmetry discussion. The branch criterion and fitting floor are self-contained calculations with joint-direction credit.
- RoFormer v5, Section 3.2, supplies the rotary operators that restrict basis changes. Fantastic Pretraining Optimizers v3, Sections 3 and 4, supports tuned and completed-budget comparisons.

## Render and browser checks

A full external Quarto render completed all 27 pages without warnings. The post-render checker found no missing local assets, broken local links or fragments, duplicate IDs, or incorrect h1 counts.

A separate release audit checked all twelve chapter neighbors and their visible P: and N: labels, all twelve hub and archive links, the completed homepage count, absence of review notices in the new series, and all six preserved free-probability rewriting notices. Internal numerical records and check scripts are not bundled in the reader output.

All six new article figures were visually inspected at the default desktop width. Their images loaded and had nonempty alternative text. Browser math-container counts for Parts 7 through 12 were 42, 58, 44, 53, 61, and 37, with zero error elements on each page.

All six articles were also checked at a 390 by 844 viewport. Each had zero math errors, loaded images, correct footer titles, and no page-wide horizontal overflow. Clicking Part 12's P: link opened Part 11. The temporary viewport override was reset to 1280 pixels before closing the test tab.

Publication uses the validated external output, with the previous generated docs tree backed up before replacement. The final publication commit and Pages build are verified after pushing.
