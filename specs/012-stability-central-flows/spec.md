# Oscillations, sharpness, and central flows

Status: actual drafts reviewed and publication approved November 5, 2026.

## Agreed workflow and selected scope

Publish the actual reviewed Parts 25 through 27, then prepare the next three articles from the editorial plan for review. Select its existing training-dynamics candidate arc. Do not commit or push Parts 28 through 30 before review.

- Part 28 develops exact quadratic stability, mixed-mode loss transients, a segment-integral descent requirement, and the sign-sensitive sharpening identity. State that neural edge-of-stability behavior is an empirical observation with exceptions.
- Part 29 derives both derivatives of a mixed cubic term, then independently solves a local polynomial's period-two orbit and return-map stability. Separate coordinate curvature from full sharpness and a finite calculation from a global theorem.
- Part 30 develops a displacement-covariance correction, boundary variance balance, critical-subspace complementarity, and conditional projected motion. Preserve a visible onset mismatch and distinguish center loss, average raw loss, and gradient-noise covariance.
- Include a reproducible figure, exercises, answer sketches, orange italic emphasis, skull ornaments, informal source headings, and title-based chapter links in each article. Inspect desktop and phone rendering.
- Keep the published twenty-seven-post docs output intact. Run no network training or paper experiment reproduction.

## Focused source pass

- Gradient Descent on Neural Networks Typically Occurs at the Edge of Stability v3, Sections 2 through 4 and Appendices A and B. Read the empirical qualifications, the fixed quadratic calculation, and the open sharpening question. Exclude exact unexcited modes from unconditional divergence wording.
- Self-Stabilization v2, Lemma 2, Section 4, Section 5.3, and Section 8.3. The cubic feedback is conditional on local geometry. Its coupling is finite-horizon, uses a constrained reference plus oscillatory displacement, and assumes sharpening alignment and derivative controls. Do not quote a general convergence claim or silently apply it to the independent polynomial.
- Understanding Optimization in Deep Learning with Central Flows v2, Section 3, Appendix A.1.5, Appendix A.2, and Section 8. Its local averaging is heuristic. The projected GD flow has formal properties under constraint regularity, while its relationship to an unspecified local average of discrete iterates lacks a general approximation theorem.
- Existing source dossiers locate derivations and known qualifications. Record their hashes internally. The new figures and polynomial calculations are independent explanatory examples, not reproductions of paper measurements.

## Verification boundaries

Use independent finite differences, scalar recurrences, numerical quadrature, return-map eigenvalues, and exact covariance checks. The two-variable loss is only a local model and is unbounded below globally. Its selected trajectory is finite and its cycle is locally attracting. The central model predicts its equilibrium while missing delayed oscillation onset. Static PSD support alone does not determine covariance magnitude or guarantee uniqueness.
