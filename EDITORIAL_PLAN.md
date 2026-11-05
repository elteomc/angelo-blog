# Editorial plan

Updated 2026-11-05.

## Published foundation and current drafts

Scale and geometry completes the agreed twelve-part sequence on normalization, weight decay, layer geometry, and modular optimization. The first fifteen posts and the hub are published, including the practical polar, stochastic averaging, and norm-budget articles approved on November 5, 2026. The opening posts establish exact scale dynamics, the middle posts build layer and modular geometry, and the closing posts develop the shared-gain question under explicit assumptions.

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
| 13 | What a finite polar iteration actually does | Follow finite singular-mode computation and distinguish approximation from training quality | Published |
| 14 | Why average before choosing an update? | Derive stochastic normalization bias, variance, tracking lag, and support-error bounds | Published |
| 15 | Weight decay as a norm budget | Derive the invariant ball and initialization envelope under bounded proposals | Published |

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


## Dossier coverage and the next writing arc

Reviewed November 4, 2026. The twelve published chapters cover scale dynamics, basic layer duality, modular budget allocation, and shared-gain compatibility. They leave substantial computational, stochastic, scaling, and empirical material in the dossiers.

This coverage review compared all twelve article outlines with the Modula reading ledger, the eight direct dossier executive maps, the spectral-condition map, selected Tensor Programs maps, selected Scion and Polar Express derivations, and the recent local research assessments. It is a targeted comparison of existing material. It does not claim a fresh full reading of every archived paper or a new reproduction of the experiments.

### Proposed follow-up order

| Order | Reader question | What the published posts already do | Substantive extension and source anchor |
| --- | --- | --- | --- |
| 1 | What does a finite polar iteration actually do? | Part 6 derives the exact SVD support direction | Newton-Schulz as a singular-value filter, rank conventions, finite precision, rectangular cost, and why approximation accuracy need not improve training. [Polar Express map](/home/acru/angelo/proj/tense/.paper-mastery/polar-express/01-executive-map.md) and [derivation D14](/home/acru/angelo/proj/tense/.paper-mastery/polar-express/06-derivations.md#d14-why-a-better-approximation-need-not-train-better). |
| 2 | Why average before choosing a norm-oracle update? | Part 4 analyzes momentum and Part 6 solves a deterministic support problem | Show a stochastic example where averaging normalized updates differs from normalizing an average. Derive the tracking error and explain the roles of gradient averaging and parameter motion. [Scion D11](/home/acru/angelo/proj/tense/.paper-mastery/norm-constrained-lmos-scion/06-derivations.md#d11-why-momentum-before-and-after-the-oracle-differ). |
| 3 | When does weight decay create a hard norm budget? | Part 3 follows radius and effective time under exact scale invariance | Derive the SCG/uSCG distinction and the bounded-direction decay recurrence, including initialization and step restrictions. Add decay's memory time scale. [Scion D4](/home/acru/angelo/proj/tense/.paper-mastery/norm-constrained-lmos-scion/06-derivations.md#d4-scg-uscg-steps-and-weight-decay) and the [normalization reading guide](/home/acru/angelo/proj/tense/output/latex/modula_normalization_reading_and_research.md). |
| 4 | How do local budgets control a whole residual block? | Part 7 gives the product-ball calculation for a stated first-order bound | Work through a complete module tree, then second derivatives, remainder control, residual depth scaling, and the regions where normalization sensitivity is bounded. Extend the dense/lookup examples to attention and convolution. [Modular norm derivations](/home/acru/angelo/proj/tense/.paper-mastery/scalable-optimization-modular-norm/06-derivations.md). |
| 5 | Why can a learning rate transfer across model widths? | Part 5 derives an RMS aspect-ratio factor for one matrix | Explain aligned matrix action, necessary lower bounds, master versus raw rates, optimizer history and damping, and measured transfer regret. Treat width and depth as separate questions. [Spectral condition](/home/acru/angelo/proj/tense/.paper-mastery/spectral-condition-feature-learning/01-executive-map.md), [Extending muP](/home/acru/angelo/proj/tense/.paper-mastery/extending-mup/01-executive-map.md), and [Tensor Programs V](/home/acru/angelo/proj/tense/.paper-mastery/tensor-programs-v/01-executive-map.md). |
| 6 | How can a small matrix step rotate a normalized head a lot? | Parts 2 and 5 discuss normalization and linear activation changes | Derive the projection-margin sensitivity, the packed-head construction, and the moving-input bound. Separate an attainable worst case from a prediction about ordinary optimizer directions. [Current reaudit](/home/acru/angelo/proj/tense/research/modula/2026-11-04_reaudit/ASSESSMENT.md) and [derivations](/home/acru/angelo/proj/tense/research/modula/2026-11-04_reaudit/DERIVATION.md). |
| 7 | How is the tangent spectral problem actually solved? | Part 8 shows why an ambient polar factor followed by projection can waste budget | Derive skew lifting, the exact oracle, zero-rank choices, QR compression, and the separate retraction step. [Exact Stiefel Muon](/home/acru/angelo/proj/tense/.paper-mastery/exact-stiefel-muon/01-executive-map.md). |
| 8 | Should attention and MLP matrices use the same constraints? | Part 8 distinguishes manifold definitions | Explain the permitted spectra and the proposed logit mechanism, then specify the missing mediation measurements and implementation controls. [Module-wise manifolds](/home/acru/angelo/proj/tense/.paper-mastery/module-wise-manifold/01-executive-map.md). |
| 9 | What did our matched-step experiments actually test? | Part 12 evaluates a finite frozen-teacher design and proposes a research protocol | Build a case study from the archived training comparisons, function-class controls, failed local forecasts, and calibration limits. Preserve the distinction between custom angular Adam and Modula. Use the later scale audit to qualify conclusions from the small masked-byte benchmark. [Functional-step assessment](/home/acru/angelo/proj/tense/research/modula/2026-11-04_functional_steps/ASSESSMENT.md), [reaudit](/home/acru/angelo/proj/tense/research/modula/2026-11-04_reaudit/ASSESSMENT.md), and [scale audit](/home/acru/angelo/proj/tense/research/modula/2026-11-04_scale_audit/ASSESSMENT.md). |
| 10 | Can redundant scales still change which solution training selects? | Parts 3 and 9 analyze clocks and schedules | Develop intrinsic-learning-rate noise models and normalization's sharpness bias under their actual assumptions. Connect to symmetry-aware optimizer state as a separate design question. This needs another focused primary-source pass before drafting. [Reading guide, Sections 3, 9, 14 and 15](/home/acru/angelo/proj/tense/output/latex/modula_normalization_reading_and_research.md). |

Start with finite polar computation, averaging before the oracle, and decay as a norm budget. These directly extend the existing support-direction discussion and have worked derivations ready in the dossiers. Keep the research case study after the distinction between pointwise bounds, finite evaluation, and training evidence has been developed.

The experimental material can support several case studies. The [stochastic feature-selection calculation](/home/acru/angelo/proj/tense/research/modula/stochastic_bias/ASSESSMENT.md) and [ordinary-network response controls](/home/acru/angelo/proj/tense/research/modula/network_minibatch/RESULTS.md) add a different line of evidence from the attention experiments. Keep the constructed-model averaging assumptions, finite evaluations, and limits of network validation explicit.

### Adjacent sequences

Tensor Programs, kernel versus feature-learning regimes, and the full muP/depth story support a separate sequence with its own prerequisites. The [Tensor Programs IV](/home/acru/angelo/proj/tense/.paper-mastery/tensor-programs-iv/01-executive-map.md), [IVb](/home/acru/angelo/proj/tense/.paper-mastery/tensor-programs-ivb/01-executive-map.md), and [VI](/home/acru/angelo/proj/tense/.paper-mastery/tensor-programs-vi/01-executive-map.md) maps give the entry points.

Progressive sharpening, edge of stability, self-stabilization, and central flows form another coherent dynamics sequence. Their finite-step, averaged-flow, and empirical claims need separate treatment. The [research index](/home/acru/angelo/proj/tense/.paper-mastery/RESEARCH_INDEX.md) and [central-flows map](/home/acru/angelo/proj/tense/.paper-mastery/central-flows/01-executive-map.md) locate that material.

These are editorial candidates. The public hub keeps its existing chapter list, and no additional article or experiment is created by this review.


## Practical follow-up release

Prepared November 4 and approved for publication November 5, 2026.

| Part | Title | Review state |
| --- | --- | --- |
| 13 | What a finite polar iteration actually does | Published November 5 after review |
| 14 | Why average before choosing an update? | Published November 5 after review |
| 15 | Weight decay as a norm budget | Published November 5 after review |

All three were reviewed and approved for publication. Their sources, figures, hub entries, and title-based chapter links are included in the release. The series uses open-ended part labels.
