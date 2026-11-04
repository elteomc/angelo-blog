# Editorial plan

Updated 2026-11-04.

## Completed main series

Scale and geometry completes the agreed twelve-part sequence on normalization, weight decay, layer geometry, and modular optimization. All twelve posts and the hub are published. The opening posts establish exact scale dynamics, the middle posts build layer and modular geometry, and the closing posts develop the shared-gain question under explicit assumptions.

Angelo reviewed Parts 1 through 6 in pairs, approved their publication, and authorized completion and publication of Parts 7 through 12 without another review gate. Mathematical checks and rendered presentation checks remain part of publication. No future release dates or automatic publications have been set.

The six free-probability posts remain available with the bold In process of rewriting... notice. Their revision queue follows this completed explanatory series. Preserve their sources and URLs.

## Scale and geometry reading order

| Part | Title | Reader outcome | State |
| --- | --- | --- | --- |
| 1 | The same network, a different step | Derive gradient scaling and compute an exact two-dimensional SGD step | Published |
| 2 | What normalization makes invariant | Distinguish input normalization, block invariance, and joint gain compensation | Published |
| 3 | Weight decay changes the clock | Separate a direct penalty from radius dynamics and the resulting effective step | Published |
| 4 | Momentum, rotation, and normalized updates | Derive radial and tangent motion with explicit optimizer conventions | Published |
| 5 | What counts as a small layer change? | Relate activation perturbations to a choice of matrix norm | Published |
| 6 | Choosing an update with a dual norm | Solve a matrix support problem and derive its maximizing direction | Published |
| 7 | How Modula combines layer budgets | Derive the product-ball interpretation of the weighted maximum and its alternatives | Published |
| 8 | Constraining weights, constraining motion | Separate a weight manifold, tangent directions, update budgets, and retractions | Published |
| 9 | Fixed norms and the schedule question | Derive the actual rotation and specify angular-schedule controls | Published |
| 10 | Which scales should stay learnable? | Trace gains, branch multipliers, and effective-map differentials | Published |
| 11 | One gain, several constraints | Derive positive shared-gain feasibility and a scalar fitting floor | Published |
| 12 | From a counterexample to a research claim | Evaluate synthetic controls and test the explanation against attention symmetries | Published |

## Research follow-ups

Completion of the writing does not establish an optimizer improvement on a trainable Transformer. The research direction remains open. Possible follow-ups should be selected from the mechanisms and controls in Parts 11 and 12.

- Extend frozen branch teachers to channelwise gain bounds and measure compatibility and conditioning.
- Test frozen attention teachers while allowing their actual function-preserving transformations. Include positional operators and the output projection in the specification.
- Let upstream features adapt and determine whether they remove the local restriction.
- Only after the mechanism survives those controls, compare tuned decay, fixed norms, grouped constraints, and established multipliers at completed training budgets.

The present numerical record contains direct finite-design loss evaluations and algebra checks. It contains no training sweep or new benchmark result.

## Evidence and attribution

- Cite primary sources beside their claims and check the referenced sections.
- Derive exact identities under stated assumptions and identify approximations when they enter.
- Keep published findings, worked examples, measured synthetic controls, and proposed experiments distinct.
- The shared-gain criterion concerns fixed features and prescribed branch maps. Final attention behavior can admit other representatives, as Part 12 demonstrates.
- Account for gain and bias placement, epsilon, optimizer state, and attention reparameterizations whenever they affect a claim.
- Use results from completed budgets and separately tuned baselines when evaluating practical optimizer benefits.

## Continuing editorial practice

The standing aim for future writing is at least two posts per week when a new active sequence begins. Maintain one main sequence, with smaller standalone notes when a longer article needs more work. The cadence does not override mathematical or editorial checks.

Reconstruct central arguments, check numerical examples, rebuild relevant figures, and inspect narrow-screen presentation before a release. Revisit published derivations during ordinary maintenance and record corrections when evidence requires them. This plan creates no automatic reminders or releases.

The earlier free-probability dates were proposals and are superseded. The learning-theory sequence beginning with small neuron updates and substantial output learning remains a later candidate.

## Voice and presentation

Keep occasional italic emphasis in the established orange accent. Use it for a phrase carrying a distinction. Preserve skull link ornaments and the Yo twin, go read... source headings.

Bottom chapter navigation displays P: and N: followed by the respective post title, with descriptive assistive labels. New scale and geometry chapters carry no review-draft notices. The free-probability rewriting notices remain visible.
