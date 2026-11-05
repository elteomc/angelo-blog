# Local review validation

Checked November 5, 2026. Parts 28 through 30 are published at 309a3fa. Parts 31 through 33 remain uncommitted local review drafts.

## Mathematical checks

All twenty-five checks in tools/check_width_feature_operators.py pass, together with the two existing catalog checks. The calculations use explicit finite models, finite differences, exact recurrences, and one-step scale evaluations. They run no benchmark training or external paper experiments.

Eight fixed-kernel checks cover equality of parameter and output recurrences, the kernel spectrum and fitting floor, positivity and nullspace preservation, pseudoinverse test predictions, the two-layer tangent kernel against an independently evaluated finite derivative, RMS normalization and growing-horizon distinctions, a deterministic kernel with random initial outputs, and the loss-normalized stability boundary.

Eight width checks cover individual neuron gradients before symmetry reduction, exponent constraints, the exact centered-neuron formula against a full parameter update, width-independent feature-learning changes, the tangent limit, the vanishing unadjusted mean-output limit, coupled raw and effective coordinates over five finite updates, and initial variance scaling. The three-example kernel has eigenvalues zero, one, and three. Its limiting residual is (-1/3,-1/3,1/3), with mean half-squared loss 1/18.

The centered tanh example uses independent trainable neuron coordinates with identical deterministic initialization, a fixed initial-function subtraction, input one, target one, and rate constant 0.2. The feature-learning mean scaling gives activation change 0.0330816916 and output change 0.1541257879 at every tested width. It is an exact controlled example, not a Gaussian initialization theorem or a predictive-performance comparison. The figure evaluates powers of two from 16 through 16384.

Nine nonlinear-operator checks cover identity processing, failure of homogeneity, the state-dependent PSD Jacobian, the finite potential gradient, the finite loss-change identity and large-rate failure, normalized tangent coordinates, scaled versus fixed epsilon, actual moment histories that meet and separate, and the changed temporal correlation caused by resampling a tangent coordinate. The explicit uncorrected moment rule reaches output zero from both initial signs after one update, then gives opposite outputs of magnitude 0.9022584728. Its damping is inside the square root, as stated in the article.

The internal example record retains selected values and six source-dossier hashes, all checked against their original files.

## Focused source pass

Feature Learning in Infinite-Width Neural Networks v3 was checked for the shallow tangent and mean-field examples in Section 3.1, the parameterization-dependent classification in Section 3.2, the maximal-update convention in Section 5, and the fixed-feature argument located by the Appendix H dossier. The articles preserve fixed input dimension, depth, and finite training horizon, activation and moment hypotheses, random initialization versus deterministic kernels, and the distinction between exact finite coordinate equivalence and a width-limit theorem.

Tensor Programs IVb v2 was checked for the operator and memory formulations in Section 2.4, their update-function assumptions, the forward/backward coordinate-pair construction, and its damping convention. The finite model illustrates the contraction without endorsing every advertised architecture extension. The potential is derived directly for a memoryless finite map, rather than claimed as an unconditional Adam theorem. The same tangent coordinate persists through its temporal history.

Maximal width order, useful feature learning, a stable finite step, and optimal hyperparameter transfer remain separate claims. No deep-network classification proof or growing-horizon guarantee is inferred from the shallow power count.

## Render and browser inspection

A full external Quarto build renders forty-eight pages with valid headings, links, fragments, and assets. All thirty-three chapter neighbor links and hub entries agree with the catalog. Exactly Parts 31 through 33 display review notices. The tenth hub group appears locally, and internal example records and check scripts are excluded from reader resources.

Desktop inspection at 1280 by 712 shows 41, 58, and 59 mathematical containers in Parts 31, 32, and 33, with zero math errors. All three figures load with descriptive alternative text. Their scales, legends, annotations, and surrounding equations were inspected visually. Orange italic emphasis and skull ornaments remain visible.

An interrupted browser connection was restored before completing the inspection. At 390 by 844, all three drafts have zero math errors, loaded images, working answer disclosures, and no page-wide horizontal overflow. Chapter text and assistive labels use P: and N: correctly. Following Part 33's previous link reaches Part 32. The temporary phone viewport was reset and its tab closed.

## Publication boundary

GitHub Pages reports the approved 309a3fa release built. Live Parts 28 through 30 match the approved docs HTML byte for byte and have no draft notices. The public hub includes Part 30 and excludes Part 31. Local main and origin/main match that release.

Published docs have no diff after the new batch. Removed personal references and the unwanted homepage and hub completion wording remain absent. The drafts, figures, example record, catalog edits, and editorial updates remain uncommitted and unpushed on codex/width-feature-operator-drafts pending review.


## Publication approval

Angelo approved the actual Parts 31 through 33 on November 5, 2026. Remove review notices and rerun the mathematical and catalog checks. Copy the verified forty-eight-page review build into a separate release directory, refresh the three approved article pages, and validate all pages before installing docs. Verify the live release after pushing. No new draft batch is included in this publication.
