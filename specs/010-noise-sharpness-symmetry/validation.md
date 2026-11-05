# Local review validation

Checked November 5, 2026. Parts 19 through 21 are published at 9980af1. Parts 22 through 24 remain uncommitted local review drafts.

## Numerical checks

All twenty-five checks in tools/check_noise_sharpness_symmetry.py pass. The nine noise checks cover sampled-loss gradients and covariance, homogeneity, exact finite-step fourth moments, the normalization Hessian's Itô contraction, unit-norm balance, an independent RK4 comparison with the constant-trace solution, the reciprocal effective rate, half-life, initialization scaling, equal-trace directional differences, and the deterministic radius kick omitted by the SDE. Some checks cover several linked identities in one test.

Eight sharpness checks verify the polynomial loss gradient against finite differences, equatorial Hessian eigenvalues and radial scaling, the exact spherical step and longitude formula, normal linearization and even-in-height drift, the finite decay and no-decay controls, the exact-minimizer exception, the gradient-flow time change, and the sign of the published slow-flow chain rule.

The declared 3000-update float64 valley calculation begins at equatorial curvature 2.6602684919277424. It ends near 1.436125999 with decay and 2.657075731 without decay. Its decayed normal coordinate remains below 0.037 in absolute value. Both controls use the same initial weight vector. These are finite evaluations of an explicit loss, with no neural-network training or generalization measurement.

Eight optimizer-state checks cover covector and displacement transformations, a general mobility transformation, multi-step gradient-EMA scale covariance, moment and damping scaling, the realizable two-dimensional moment example, full-matrix EMA rotation covariance, lost correlations in diagonal storage, translation equivariance versus horizontality, and the positional-operator boundary for attention rotations. The relative diagonal-moment discrepancy at 45 degrees is 0.4974573030771096. The full-matrix control is zero to floating-point tolerance.

The two existing catalog checks pass. Three SVG figures reproduce from tools/noise_sharpness_symmetry_figures.py. The radius figure evaluates a closed ODE solution. The valley figure reports only its declared finite horizon and plots curvature at the corresponding equatorial minimizer. The moment figure is a state-level algebraic comparison. A point annotation was moved above its curve and visually rechecked.

## Source pass

Intrinsic Learning Rate v1 was checked for Theorem 5.1, the fourth-power radius reparametrization in Equations 9 through 12, and the separate Fast Equilibrium Conjecture. The article uses the independently derived reciprocal relation between Gamma and the effective directional rate, avoiding the nearby v1 prose reversal. It states sampled-loss symmetry, covariance, initialization, and iteration-time conventions explicitly.

Normalization Sharpness Reduction v3 was checked for Assumptions 4.5 and 4.6, Equation 3, Theorem 4.7, the perturbed initialization, and the exact-minimizer exception. The source's local tracking theorem remains distinct from the independent polynomial-on-the-sphere demonstration. Neither is presented as a universal generalization claim.

The Exponential Learning Rate v3 source and existing dossier were checked for scale covariance, gradient-flow time change, and optimizer-state conventions. The new article states its own decoupled update and does not silently substitute the paper's coupled momentum convention.

Dead-Direction Conditioners v1 was checked for its architectural actions and scalar and matrix rotation moments in Section 3.2. The article relies on the narrow orthogonal-conjugation argument. It explicitly separates equivariance from horizontality rather than endorsing broad claims that every coordinatewise update fails every symmetry action. Its translation counterexample and positional-operator qualification are checked directly.

## Render and browser inspection

A full external Quarto render builds thirty-nine pages without warnings. The checker validates local links, fragments, assets, heading counts, and duplicate IDs. A separate audit verifies all twenty-four chapter neighbors and hub links, exactly three review notices, and the seventh hub group. Removed personal references, completion text, and count panels remain absent. Internal tools and specs are not copied into reader resources.

Desktop inspection at 1280 by 712 gives 87, 65, and 56 mathematical containers in Parts 22, 23, and 24, with no math errors. All three figures load with alternative text. The article openings, figures, formulas, and orange italic emphasis were visually inspected. The final moment annotation is clear of its curve.

At 390 by 844, all three drafts have zero math errors, loaded images, working answer disclosures, and no page-wide horizontal overflow. P: and N: chapter titles and assistive labels are correct. The previous link from Part 24 reaches Part 23. The temporary viewport is reset and its test tab closed.

Live Parts 19 through 21 match the approved docs HTML byte for byte, have no draft notices, and appear on the public hub. Part 22 is absent from the public hub. Local main and origin/main match. Published docs have no diff after this batch. The three new drafts remain uncommitted and unpushed for review.


## Publication approval

Angelo approved the actual Parts 22 through 24 on November 5, 2026. Remove their review notices, rerun the mathematical and catalog checks, and render the approved sources into a separate release directory before replacing docs. Verify the live site after publication.
