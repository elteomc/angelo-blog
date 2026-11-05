# Residual budgets, width transfer, and normalized heads

Status: actual drafts reviewed and publication approved November 5, 2026.

## Agreed scope

Continue the next three topics from the existing editorial plan after publishing the approved Parts 13 through 15. Prepare the actual articles for review before any commit or push of this batch.

- Part 16 follows first and second derivatives through an averaged residual stack, states uniform pathwise bounds, derives a finite Taylor remainder and a conditional loss bound, and explains module-specific estimates.
- Part 17 derives shape factors from proposal norms, demonstrates the role of alignment and cancellation, checks exact square and rectangular examples, and distinguishes one-step diagnostics from measured hyperparameter transfer.
- Part 18 derives exact local normalization sensitivity, constructs a large head rotation while a packed matrix remains orthogonal, and includes finite incoming-feature motion and stabilization.
- Preserve the accepted layout, orange italic emphasis, informal source headings, skull ornaments, and title-based P: and N: navigation. Add one figure and answer sketches per article.
- Build and inspect desktop and phone presentation outside docs. Keep the public release unchanged and the new drafts uncommitted until review.

## Evidence base

Use the modular norm and spectral-condition derivation dossiers, Extending muP and Tensor Programs V maps, and the November 4 normalized-module reaudit. Verify pinned primary sources for paper-specific statements. All new numerical figures are explicit finite algebraic examples. No training benchmark is introduced.

## Source anchors checked

- Scalable Optimization in the Modular Norm v1, Section 3.4, Proposition 4, Proposition 5, Appendices A.3, B, C, and E. Residual blocks have independent parameters and branch coefficient 1/L. Uniform derivatives must hold throughout the path.
- A Spectral Condition for Feature Learning v2, Section 3.1 and Section 4. Single-example outer products align with their generating feature. General network lower bounds need overlap and non-cancellation.
- Extending muP v1, Section 4.1. The proposal spectral scale determines a conditional raw learning-rate quotient. The article does not endorse every optimizer-specific extension.
- Tensor Programs V v2, Sections 4 and 6, Appendix B.3. Master and layerwise quantities differ. Non-negligible optimizer epsilon can require scaling. The stabilized-sign toy is not a full Adam model.
- Normalized-module reaudit derivations, Sections 1 through 3. Projection margins are data dependent, the orthogonal witness is attainable, and no frequency or final-loss conclusion follows from it.
