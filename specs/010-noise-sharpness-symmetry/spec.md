# Noise, sharpness, and symmetry

Status: actual drafts reviewed and publication approved November 5, 2026.

## Scope and editorial decision

Publish the reviewed Parts 19 through 21, then prepare the next three articles for review. The remaining tenth follow-up in the editorial plan bundles intrinsic-rate noise, normalization sharpness bias, and symmetry-aware optimizer state. Split those into Parts 22 through 24. Do not commit or push the new batch before review.

- Part 22 derives the iteration-time Itô model under sampled-loss scale invariance. Track the fourth-power radius, solve its constant-trace balance, and distinguish the effective directional rate from its reciprocal. State the discrete fourth-moment correction and separate radius relaxation from mixing.
- Part 23 compares radius-dependent raw Hessians with spherical curvature. Derive an exact local longitude update for a smooth polynomial loss on the sphere, with a finite 3000-update decay and no-decay comparison. State the published local theorem's smoothness, manifold, top-eigenvalue, step-regime, and perturbed-initialization assumptions.
- Part 24 derives the linear covector, vector, and mobility transformation laws. Check raw-rate, buffer, and damping conventions under scale transformations, then compare diagonal and full-matrix moment behavior under rotations. An explicit translation example separates equivariance from horizontality. State the architecture's actual group action before using it.
- Include a figure, exercises, answer sketches, checked source links, and the established orange italic emphasis in each article. Preserve skull ornaments and P: and N: navigation.
- Build outside docs, inspect desktop and phone presentation, and leave the published twenty-one-post release intact.

## Primary source pass

- Intrinsic Learning Rate v1, Sections 3 and 5, Theorem 5.1, Equations 9 through 12, and Conjecture 5.3. Derive the effective coefficient as the reciprocal square root of the fourth-power radius variable. A nearby v1 prose expression reverses that relationship, so rely on the displayed ODE and independently checked algebra.
- Normalization Sharpness Reduction v3, Section 4.2, Assumptions 4.5 and 4.6, Equation 3, and Theorem 4.7. The theorem is local and uses a specified perturbed initialization. The explicit valley figure is an independent finite demonstration rather than a theorem reproduction or a neural-network benchmark.
- Exponential Learning Rate v3, Sections 2 and 4, with the existing derivation dossier. Gradient-flow time change, finite scale transformations, and optimizer-state conventions must stay distinct.
- Dead-Direction Conditioners v1, Sections 3.1 and 3.2, especially scalar and matrix rotation moments. Use the narrow orthogonal-conjugation calculation rather than endorsing broad statements about every coordinate action. In particular, translation equivariance can hold even when a coordinatewise update is not horizontal.

## Verification boundaries

All new calculations use explicit ODEs, a smooth three-dimensional loss, or low-dimensional optimizer states. They are not neural-network training experiments. Equal covariance trace does not determine directional noise. A lower sharpness value does not establish generalization. A symmetry-respecting update does not establish an optimizer advantage. Check the forward symmetry, the complete state, and the actual finite update separately.
