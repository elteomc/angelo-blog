# Width, features, and tangent operators

Status: actual drafts reviewed and publication approved November 5, 2026.

## Workflow and selected scope

Publish the actual reviewed Parts 28 through 30, then prepare the next three posts from the editorial plan for review. Select its existing Tensor Programs and kernel-versus-feature-learning arc. Do not commit or push Parts 31 through 33 before review.

- Part 31 derives the finite tangent model, kernel spectrum, nullspace residual, and pseudoinverse prediction. Explain how a wide two-layer SGD model can change its output while its typical features move vanishingly. A frozen nonlinear-network approximation requires a theorem beyond the exact linear algebra.
- Part 32 derives shallow width exponents and the distinction between centered random initialization and coherent learned updates. Check an exact deterministic centered tanh step and the finite raw-coordinate equivalence of mean-field and shallow maximal-update conventions. The power count is not the general deep-network classification or proof of predictive superiority.
- Part 33 derives an exact nonlinear frozen-feature response, its Jacobian and convex potential, and the finite loss-change identity. Specify epsilon and coordinate scaling, then preserve actual moment history. A nonlinear tangent operator is distinct from a changing feature law.
- Include a reproducible figure, exercises, answer sketches, orange emphasis, skull ornaments, informal source headings, and title-based links per article. Inspect desktop and phone presentation.
- Preserve the published thirty-post docs release. Run no benchmark training or external research-code experiments.

## Source pass

- Feature Learning in Infinite-Width Neural Networks v3, Section 3.1, Section 3.2, Theorems 3.6 and 3.8, Section 5, and the fixed-feature derivation in Appendix H. Check the shallow mean-field coordinate equivalence, activation and stability assumptions, fixed depth and input dimension, and width-independent training horizon. Do not quote a literal zero-function conclusion after nonzero updates or treat a random initial output as deterministic merely because its kernel is deterministic.
- Tensor Programs IVb v2, Section 2.4, Definitions 2.4.4 and 2.4.8, Theorems 2.4.7 and 2.4.9, and its epsilon conventions. Preserve the forward/backward pair in matrix tangent variables and reuse the same coordinate over time. The finite model avoids relying on broad general-architecture extensions whose formulas or proofs need qualifications in the dossier.
- The two source dossiers locate the relevant derivations and known limitations. Record their hashes internally. The figures are independent worked examples, not copied paper assets or benchmark reproductions.

## Verification boundaries

Use finite differences, spectral identities, full-versus-reduced parameter updates, exact coupled-coordinate trajectories, and explicit moment histories. The centered tanh example initializes every neuron identically with independently trainable coordinates, unlike a Gaussian width-limit theorem. Keep that distinction visible. Nonvanishing feature motion, width-stable output updates, useful representation learning, and transfer of optimal hyperparameters are separate claims.
