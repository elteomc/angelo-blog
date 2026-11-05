# Local review validation

Checked November 5, 2026. Parts 25 through 27 are published at f6387f5. Parts 28 through 30 remain uncommitted local review drafts.

## Mathematical checks

All twenty-six checks in tools/check_stability_central_flows.py pass, together with the two existing catalog checks. The new work evaluates explicit low-dimensional formulas and a two-variable recurrence. It runs no neural-network training or paper experiment reproduction.

Eight stability checks cover scalar quadratic multipliers, eigencoordinate reconstruction, unexcited and nonpositive modes, hidden unstable-mode growth during initially falling loss, exact flow versus Euler amplification, the segment-integral counterexample, a finite-difference top-eigenvalue derivative, and opposite signs of progressive sharpness drift.

Nine feedback checks cover gradients and Hessians against finite differences, both derivatives of the mixed cubic term, the exact two-cycle and loss, the two-step return map in trajectory order, its multipliers and nearby attraction, the stated 400-update trajectory, the invariant unexcited axis, and the distinction between coordinate curvature and full sharpness.

Nine central-flow checks cover exact frozen-window centering and PSD covariance, the averaged cubic gradient correction, outward and inward scalar complementarity, contact time and interior dynamics, fluctuation loss, projected velocity and center-loss descent, critical-basis rotations and off-diagonal covariance, insufficient static support conditions, and a PSD response with nonunique covariance solutions.

The independent polynomial has rate one, parameters a=b=1, gamma=0.2, target y=1.1, and initial state (0.001,0.4). Its cycle is (plus or minus 0.2,1), with loss 0.041, center loss 0.001, and full instantaneous sharpness 2.0219544457. Both two-step multiplier moduli are 0.84. At update 400, the recorded state is within 2e-13 of the positive cycle point. The loss initially equals 0.0490007, reaches a minimum near 1.6561e-7 and a maximum near 0.05108465, then approaches its cycle value. These are finite evaluations of a local polynomial that is unbounded below globally.

The constrained center's contact time is 9.7295507453 and its boundary variance is 0.04. The flow curves begin on the axis at (0,0.4), while the discrete example retains its initial nonzero oscillating component. The figure preserves the onset mismatch rather than fitting it away. The internal example record contains these values and six verified source-dossier hashes.

## Source and claim checks

The focused primary pass checked Edge of Stability v3 for the fixed-quadratic boundary, full-batch empirical characterization, progressive sharpening, and Appendix A exceptions. A starting Hessian does not certify curvature along a finite step. Exact unexcited states are excluded from an unconditional divergence claim.

Self-Stabilization v2 was checked for the eigenvalue derivative in Lemma 2, the cubic feedback in Section 4, the assumptions and finite horizon in Section 5.3, and the open sharpening question in Section 8.3. The new two-cycle is established directly and is not presented as an application of that paper's theorem to unchecked conditions.

Central Flows v2 was checked for Section 3, Appendix A.1.5, Appendix A.2, and Section 8. The flow's formal projection properties remain conditional on regularity. Its relationship to local time averages is heuristic. Displacement covariance is not gradient-noise covariance. Matrix covariance support, its magnitude, and uniqueness are separate questions.

## Render and browser inspection

A full external Quarto render builds forty-five pages with valid headings, links, fragments, and assets. The final focused page refresh also passes the checker over all forty-five pages. All thirty chapter neighbor links and hub entries agree with the catalog. Exactly Parts 28 through 30 display review notices, and the ninth hub group appears locally. Internal example records and check scripts are excluded from reader resources.

Desktop inspection at 1280 by 712 shows 56, 73, and 64 mathematical containers in Parts 28, 29, and 30, with zero math errors. All three figures load with descriptive alternative text. Their labels, limits, comparisons, and annotations were visually inspected. Part 29's onset panel ends at update 160, while its other panels show the full 400-update horizon. Orange italic emphasis and skull ornaments remain visible.

A missing TeX escape in Part 29's initial-coordinate label was caught visually, recorded as PUB-006, corrected, and rechecked in the rendered page. The mathematical examples were unaffected.

At 390 by 844, all three articles have zero math errors, loaded images, working answer disclosures, and no page-wide horizontal overflow. P: and N: chapter text and assistive labels are correct. The previous link from Part 30 reaches Part 29. The temporary phone viewport was reset and its tab closed.

## Publication boundary

GitHub Pages reports the approved f6387f5 release built. Live Parts 25 through 27 match approved docs HTML byte for byte and have no draft notices. The public hub includes Part 27 and excludes Part 28. Local main and origin/main match that release.

Published docs have no diff after this batch. Removed personal references and the unwanted homepage and hub completion wording remain absent. The three drafts, figures, example record, catalog edits, and editorial updates remain uncommitted and unpushed on codex/stability-central-flow-drafts pending review.


## Publication approval

Angelo approved the actual Parts 28 through 30 on November 5, 2026. Remove review notices, rerun mathematical and catalog checks, render separately, and verify the live release after publication.
