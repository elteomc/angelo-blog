# Editorial plan

Updated 2026-11-04.

## Current priority

Scale and geometry is the active main series. Its thread is normalization, weight decay, layer geometry, and modular optimization. Each post answers one question with a worked argument, example, or experiment. Organize the writing around the questions rather than one summary per paper.

The existing website and six free-probability posts were pushed on November 4 with a bold In process of rewriting... notice. They remain available as unfinished writing. Preserve their sources and URLs while moving their revision queue behind the new series.

Angelo authorized publication of the series hub and first two posts on November 4 after reviewing the local preview, with homepage and source-section presentation refinements. Angelo also approved publication of Parts 3 and 4 after reviewing their local drafts. The remaining eight chapters are planned. No future release dates or automatic publication have been set.

## Standing commitment

Aim for at least two posts per week as the series develops. Maintain one main sequence, with smaller standalone notes available when a longer article needs more work. Do not turn the cadence into a reason to publish an unsupported claim or an unrehearsed derivation.

## Scale and geometry queue

| Part | Working title | Reader outcome | Current state |
| --- | --- | --- | --- |
| 1 | The same network, a different step | Derive gradient scaling and compute an exact two-dimensional SGD step | Approved for publication |
| 2 | What normalization makes invariant | Distinguish input normalization, block invariance, and joint gain compensation | Approved for publication |
| 3 | Weight decay changes the clock | Separate a direct penalty from radius dynamics and the resulting effective step | Approved for publication |
| 4 | Momentum, rotation, and normalized updates | Derive the radial and tangent update decomposition and keep optimizer conventions explicit | Approved for publication |
| 5 | What counts as a small layer change? | Relate activation perturbations to a choice of matrix norm | Planned |
| 6 | Choosing an update with a dual norm | Solve a concrete linear support problem and connect it to matrix update directions | Planned |
| 7 | How Modula combines layer budgets | Derive the product-ball interpretation of the weighted maximum and its alternatives | Planned |
| 8 | Constraining weights, constraining motion | Distinguish a weight manifold, tangent directions, update budgets, and retractions | Planned |
| 9 | Fixed norms and the schedule question | Compare fixed weight and update norms with fair angular-schedule controls | Planned |
| 10 | Which scales should stay learnable? | Trace gains, branch multipliers, and effective maps through a module | Planned |
| 11 | One gain, several constraints | Derive shared-gain feasibility and a scalar fitting floor under explicit frozen-feature assumptions | Planned research note |
| 12 | From a counterexample to a research claim | Design tests that account for attention symmetries, feature adaptation, and tuned baselines | Planned research note |

Parts 1 through 4 establish scale dynamics. Parts 5 through 8 build the language of layer and modular geometry. Parts 9 through 12 connect those tools to open research questions. The boundaries may change during editorial review.

The first four posts were approved in pairs. Later posts need their own complete drafts and checks. A planned chapter appears on the hub without a link until its source exists.

## Evidence and attribution

- Cite primary sources beside the claims they support. Verify section references rather than relying on a reading list.
- Derive exact identities under their stated assumptions. Label an approximation or modeling assumption when it first enters.
- Keep published results, worked examples, and proposed experiments distinct.
- The shared-gain calculations concern frozen features and specified branch outputs. Do not present them as a full Transformer capacity theorem or a publication-priority result.
- Include gain and bias placement, epsilon, optimizer state, and attention reparameterizations whenever they affect a claim.

## Weekly practice

- Reconstruct the central argument before consulting the sources, then resolve gaps.
- Check every equation and numerical example. Rebuild figures from their source when relevant.
- Review prose in the author's own voice and inspect the rendered article on a narrow screen.
- One week after a release, repeat the derivation or solve a changed example and record any correction needed.

## Deferred queues

The previous October and November free-probability release dates were proposals, not a completed publication schedule. They are superseded. Keep all six posts available with rewriting notices and return to their revision after the new series has a stable cadence.

The learning-theory sequence beginning with small neuron updates and substantial output learning remains a later series. It does not compete with the current sequence for the first release slots.


## Voice and presentation

Keep occasional italic emphasis in the established orange accent. Use it for a phrase that carries a distinction, without coloring entire paragraphs. Preserve the skull link ornaments and the Yo twin, go read... source headings.
