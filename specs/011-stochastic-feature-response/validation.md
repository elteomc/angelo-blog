# Local review validation

Checked November 5, 2026. Parts 22 through 24 are published at ad91609. Parts 25 through 27 remain uncommitted local review drafts.

## Mathematical and archived checks

All twenty-five checks in tools/check_stochastic_feature_response.py pass, together with the two existing catalog checks. The calculations use low-dimensional quadrature, algebra, and selected archived results. No long trajectories or network continuations were rerun.

Eight Gaussian-response checks cover the scalar sign mean and score derivative, residual orthogonality and variance, a multivariate cubic identity, a non-Gaussian regression counterexample, normalization's changed Jacobian, polar column variance and response ordering, and the frozen scalar surrogate's variance ratio. Split quadrature independently checks the discontinuous sign map without differentiating it pointwise.

Nine feature checks cover energy derivatives, the full noisy scalar gradient, the clean Hessian trace and changing spectrum, finite-rate autoregressive variance, the raw-gradient drift sign, archived response coefficients and initial drift, the output graft's scope, off-design identifiability, and the slow horizon and trajectory-copy counts. The Gaussian score identity and frozen recursion are exact under their assumptions. The substitution into the evolving feature equation remains a leading averaging calculation, without a uniform theorem for this model.

Eight network checks cover prescribed spherical radius and angle, finite-batch mean-response matching and its change under normalization, covariance rank with twelve outcomes, entropy effective rank, within-seed paired uncertainty, article table means, mixed signs in rank and strict affine comparisons, and calibration protocols. The selected record contains twenty archived network runs and six constructed-feature measurements. Its twenty-three provenance hashes match the original files.

For the refreshed noisy-label comparison, the paired polar-minus-angular loss gap is 0.0121634766 with standard error 0.0037846709. The paired polar-minus-affine gap is -0.0000098364 with standard error 0.0004527554. For the deterministic-label every-step control, the corresponding gaps are 0.0063287137 with standard error 0.0025926473, and 0.0002468853 with standard error 0.0004070868. Each uncertainty uses four independent seeds, with step sizes averaged within seed where applicable.

## Sources and claim limits

Muon Under Gradient Noise and the Limits of Orthogonalization Near Optima v1 was checked for Proposition 3.1, Theorem 4.1, temporal effects, and the frozen-residual surrogate. The articles distinguish residual orthogonality from independence, Gaussian regression from a common-shift derivative, and a covariance ordering from a full feedback-dependent loss comparison.

What Happens after SGD Reaches Zero Loss? A Mathematical Framework v4 was checked for the minimizer-manifold, smoothness, transverse Hessian, neighborhood, and slow-time requirements of Section 4 and Theorem 4.6. It is contextual rather than a proof for our constructed recursion. Label Noise SGD Provably Prefers Flat Global Minimizers v1, Section 2.2, was checked for its finite-step spectral regularizer. Constant trace does not eliminate every sharpness mechanism.

The local stochastic_bias derivation, prediction, and controls were checked against the model and displayed coefficients. The local network_minibatch implementation, protocol, results, summary, and selected raw records were checked for independently learned parameters, fixed noisy labels, twelve finite batch outcomes, calibration, and metrics. The ordinary-network result demotes a robust extra-collapse prediction. It does not erase the constructed example or establish an optimizer ranking.

## Render and browser inspection

A full external Quarto render builds forty-two pages with valid headings, local links, fragments, and assets. All twenty-seven chapter neighbor links and hub entries agree with the ordered catalog. Exactly Parts 25 through 27 carry review notices. The eighth hub group is present locally. Internal experiment records and check tools are not bundled as reader resources.

Desktop inspection at 1280 by 712 shows 55, 86, and 23 mathematical containers in Parts 25, 26, and 27, with zero math errors. Each original SVG loads with descriptive alternative text. The three figures were visually inspected for readable labels, unclipped points, and coherent comparisons. Orange italic emphasis and skull ornaments remain visible.

Phone inspection at 390 by 844 shows zero math errors, loaded figures, working answer disclosures, and no page-wide horizontal overflow in all three articles. P: and N: text and assistive labels are correct. Following Part 27's previous link reaches Part 26. The temporary viewport was reset and its test tab closed.

## Publication boundary

Live Parts 22 through 24 match the approved docs HTML byte for byte and have no draft notices. The public hub includes Part 24 and excludes Part 25. Local main and origin/main point to ad91609. Published docs have no diff after this review batch. Removed personal references and the unwanted hub and homepage completion wording remain absent.

The local review branch is codex/stochastic-feature-response-drafts. The three new articles, figures, source record, catalog edits, and editorial updates remain uncommitted and unpushed pending review.


## Publication approval

Angelo approved the actual Parts 25 through 27 on November 5, 2026. Remove review notices, rerun the mathematical and catalog checks, and render the approved sources into a separate release directory before replacing docs. Verify the live release after publication.
