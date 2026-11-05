# Local review validation

Checked November 5, 2026. Parts 13 through 15 are published at e681763. Parts 16 through 18 remain uncommitted local review drafts.

## Mathematical checks

All twenty-three checks in tools/check_network_scaling.py pass. Independent checks include finite differences against composite and loss derivatives, polynomial coefficients against residual derivatives, product formulas against heterogeneous residual recursions, finite sums against the closed curvature bound, scalar Taylor remainders, and the averaged periodic-convolution estimate.

Width examples verify equal operator norms with different feature action, single-example gradient alignment, exact cancellation with moving features, all four rows of the square-width table, rectangular rate conversions against direct matrix action, partial polar support, and fixed versus scaled stabilized-sign denominators. No neural-network training is run.

Normalized-head checks compare the Jacobian with finite differences, attain its spectral sensitivity using an explicit rank-one witness, verify row orthogonality and scale-invariant projection margins, evaluate packed orthogonal rotations and both angle observables directly, and check tangent support and polar retraction. The finite angle bound is tested at its tangent-ball equality case and over a grid of displacements. Fifty seeded moving-feature examples satisfy the finite bound. Separate checks require the product cross term, verify stabilized radial and transverse eigenvalues, and cover the one-dimensional exception.

The existing two catalog tests pass. Three SVG figures reproduce from tools/network_scaling_figures.py, using the same style as the preceding articles. The scalar residual limit is 0.0129814290265578. At plane angle 0.01, head sensitivities 100 and 1000 give approximately 45.0 and 84.3 degree rotations. These are exact constructed examples rather than empirical training outcomes.

## Sources and scope

The modular norm dossier was checked for the second-order composition rule, residual depth calculation, loss chain rule, and convolution assumptions. Pinned primary v1 was checked for Proposition 4, Proposition 5, and the module and normalization context.

The spectral-condition dossier and primary v2 were checked for single-example alignment and the separate non-cancellation step. Extending muP v1, Section 4.1, supports the conditional proposal-norm quotient, without endorsing every optimizer-specific claim. Tensor Programs V v2, Appendix B.3, confirms that a non-negligible stabilizer can require width scaling. The toy stabilized sign update remains explicitly distinct from a full Adam rule.

The November 4 normalized-module reaudit was checked for the local witness, finite moving-input bound, orthogonal construction, and its limitations. No claims about the frequency of worst-case directions or final training loss are inferred.

## Build and browser checks

A full external Quarto build renders thirty-three pages without warnings. The checker validates headings, local links, fragments, assets, and duplicate IDs. A separate audit verifies all eighteen chapter neighbors and hub entries, precisely three Draft for review notices, and the five-group hub. Removed personal references and publication-count panels remain absent.

Desktop inspection at the default 1280 by 712 viewport gives 92, 68, and 90 MathJax containers in Parts 16, 17, and 18, with no math errors. All three SVG images load and have alternative text. The figures, displayed mathematics, and accepted dark reading layout were visually inspected. The orange italic emphasis remains in place.

At a 390 by 844 viewport, all three drafts have loaded images, zero math errors, and no page-wide horizontal overflow. Each answer disclosure opens. Footer links retain their visible P: and N: titles and descriptive assistive labels. The temporary viewport is reset and the phone test tab is closed.

The live HTML for Parts 13 through 15 exactly matches the approved docs files, without draft notices. The public hub includes those articles and excludes Part 16. Local main and origin/main match. The published docs tree has no diff, and no new draft has been committed or pushed.


## Publication approval

Angelo approved publication of the actual Parts 16 through 18 on November 5, 2026. Remove their review notices, rerun the twenty-three numerical checks and catalog checks, and render the approved site into a separate release directory before replacing docs. Live deployment verification follows publication.
