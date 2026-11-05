# Local review validation

Original local review checked November 4, 2026. That review kept the published docs tree unchanged.

## Numerical checks

All eighteen checks in tools/check_practical_followups.py pass. They cover classical cubic and quintic scalar maps, their local error formulas, rectangular Gram evaluation against independent SVD evaluation, rank and zero conventions, finite support values, norm overshoot, exact stochastic bias, exhaustive small-batch enumeration against binomial sums, EMA variance and trend lag, tracking identities, exact and approximate support-error bounds, vector and matrix norm envelopes, conditional-gradient equivalence, exposure products, step-range counterexamples, and coupled versus decoupled updates.

The finite polar table uses the input spectrum (1, 0.1, 0.001, 0), Frobenius initialization, and cubic stages 0, 5, 10, 20, and 24. The largest active-mode error at stage 10 is approximately 0.94267149 while the optimal-support fraction is approximately 0.999143804. This difference is intentional.

The stochastic table uses exact binomial probability sums. At batch sizes 1, 2, 4, 16, 64, and 256, expected unit descent proposals are approximately 0.5, 0.125, -0.367188, -0.190026, -0.688311, and -0.933480. Ties return zero. No Monte Carlo sampling or neural-network training is used.

The norm-envelope example uses proposal 1, rate 0.1, and decay 0.5. At step 20, the zero initialization gives 1.2830281552 and the initialization of five gives 3.0754577672. The initial-coefficient half-life is 13.513407334 updates.

The two existing collection tests also pass. Four SVG figures reproduce from tools/practical_followup_figures.py.

## Source checks

The Polar Express v5 was checked against its primary text, especially Sections 1.2, 2, and 3, Appendix G, and Appendix J. The article explains the elementary classical recurrence and gives the scope of the interval-based minimax construction. It does not implement that paper's coefficient schedule or reproduce a GPU benchmark.

Training Deep Learning Models with Norm-Constrained LMOs v2 was checked for the averaging order, Section 3's SCG and uSCG updates, the decay reparameterization, and the assumptions accompanying stochastic analysis. The displayed estimator identities and norm bounds are derived directly with explicit initialization and coefficient conditions. Old Optimizer, New Norm v2 supplies the companion support-direction context.

## Render and browser checks

A full external Quarto build renders thirty pages without warnings. The post-render checker finds no broken local links or fragments, missing assets, duplicate IDs, or h1-count errors. A separate audit checks all fifteen chapter neighbors, all fifteen hub links, exactly three draft notices, and open-ended part labels. Internal checks and review records stay outside the reader output.

Desktop browser inspection gives 61, 74, and 80 mathematical containers for Parts 13, 14, and 15, with zero math error elements. All four figures load and have nonempty alternative text. Figures, tables, and the dark reading presentation were visually inspected.

At a 390 by 844 viewport, all three drafts have zero math errors, loaded images, correct title-based P: and N: links, and no page-wide horizontal overflow. All three answer disclosures open. The previous link from Part 15 reaches Part 14. The temporary viewport override is reset before the test tab is closed.

Published docs have no diff. The local hub includes the new fourth group. The new articles remain marked Draft for review, and the removed personal references and publication-count panels are absent.


## Publication approval

Angelo approved publication of the three actual drafts on November 5, 2026. Review notices are removed, publication dates use November 5, and the approved sources are rendered into a separate release directory before replacing docs. The eighteen numerical checks and collection checks pass for the release. Publication is followed by live deployment verification.
