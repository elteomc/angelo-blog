# Local review validation

Checked November 5, 2026. Parts 16 through 18 are published at efeddf5. Parts 19 through 21 remain uncommitted local review drafts.

## Numerical and archived-record checks

All twenty-five checks in tools/check_geometry_evidence.py pass. The tangent checks verify tangency, spectral feasibility, and the nuclear support certificate on several rectangular shapes, compare compressed and dense actions, exercise rank-deficient and normal costs, recover the single-column solution, compare explicit skew completions, distinguish kernel-optimal selections, and check full-polar skewing and the finite polar retraction.

The attention checks verify Gram spectra, packed contractions, the DGram zero-step counterexample, the exact finite-horizon norm envelope, reciprocal query-key scaling, the winner-gap and common-offset controls, finite-difference softmax and GELU derivatives, the softmax null direction, and the bounded-logit lower bound.

The evidence checks verify the exact cross-entropy identity, the predictive-Fisher quadratic limit, positive global scaling cancellation, and the distinction between an ideal nested-subspace oracle and a particular optimizer. Archived paired test losses are differenced and averaged again, including both CPU and fixed-step endpoints. Initialization means are reconstructed from the saved old losses. Forecast counts, checkpoint signs, and routing means are independently aggregated from the selected record. Both original JSON source hashes match the stored provenance.

The four-head matched fixed-step mean is 0.04062435366124095 and rounds to the article's 0.040624. A mistyped full-precision test expectation was corrected and recorded in ISSUE_REGISTRY.md. The actual article value and source record were already correct.

The two existing catalog checks pass. Three SVG figures reproduce from tools/geometry_evidence_figures.py. The tangent example's normalized zero-block lift has norm approximately 1.144122806 while its prescribed action and completed lift have norm one. The attention figure evaluates four-token softmax directly. The paired-seed plot reads archived aggregates. These checks do not rerun training or reproduce external runtime benchmarks.

## Primary source inspection

Exact Stiefel Muon v1 was checked for Proposition 3, Theorem 2, Remark 4, the QR algorithm, and rank-deficient polar evaluation. The article explicitly imports the block-completion theorem and separates exact support, numerical rank choices, and finite retraction.

Module-wise manifolds v1 was checked for Table 1, the attention-group spectral figure, the stated rate and step budget, packing, and the Appendix A restoration formula. Its archived figure was visually inspected. The pinned implementation confirms the stated sorted-singular-value restoration, while no run-to-revision link is asserted. The zero-step counterexample and conditional growth-budget discrepancy are stated without attributing the observed failures to either one.

The functional-step protocols, derivations, assessment, primary numeric summary, and later scale audit were checked. The article keeps custom angular Adam-based proposals distinct from Modula and the tangent spectral oracle. It distinguishes initialization replays, prescribed KL clocks, conservative probes, and diagnostic follow-ups. It reports three trained checkpoints per probe setting rather than treating 24 updates as independent networks.

## Build and browser inspection

A full external Quarto build renders thirty-six pages without warnings. A subsequent article refresh also validates all thirty-six. The post-render checker finds no missing assets, broken local links or fragments, duplicate IDs, or heading-count errors. A separate audit verifies all twenty-one chapter neighbors and hub links, exactly three draft notices, and the sixth hub group. Removed personal references, count panels, and completion text remain absent. Internal tools, specs, and the numeric record stay outside rendered reader resources.

Desktop browser inspection at the default 1280 by 712 viewport gives 88, 65, and 27 mathematical containers in Parts 19, 20, and 21, with zero math errors. Each figure loads with alternative text. All three figures and the article openings were visually inspected. A clipped attention-figure footnote was shortened and rechecked. Orange italic emphasis remains visible, including the final Part 21 polish.

At a 390 by 844 viewport, every draft has zero math errors, loaded images, an opening answer disclosure, and no page-wide horizontal overflow. P: and N: titles and descriptive assistive labels are correct. The previous link from Part 21 reaches Part 20. The temporary viewport is reset and its test tab closed.

The live Parts 16 through 18 match their approved docs HTML byte for byte, have no review notices, and appear on the public hub. Part 19 is absent from that hub. Local main and origin/main match. Published docs have no diff after preparing this batch. All three new articles remain uncommitted and unpushed for review.


## Publication approval

Angelo approved the actual Parts 19 through 21 on November 5, 2026. Remove their review notices, rerun the numerical and catalog checks, and render the approved sources into a separate release directory before updating docs. Verify the live deployment afterward.
