# Complete the free probability series
status: complete, 2026-10-17

## Problem
The existing introduction asks how to add large random matrices but stops before its calculations, limiting law, and experiment. The site needs a finite, coherent series that the author can study, explain, and publish.

## Goal
Finish a six-post introduction to additive free probability, with a complete mathematical argument at each stage and reproducible numerical illustrations.

## Proposed scope
1. Spectra and freeness: preserve the opening question, define the tracial setting, compute mixed second and fourth moments, and explain the random-orientation model.
2. Noncrossing partitions and free cumulants: work through orders two through four, derive cumulant additivity from the mixed-cumulant criterion, and explain the semicircular limit.
3. The R-transform: connect cumulants to the Cauchy transform, specify inverse branches, and calculate the sum of two symmetric two-point laws.
4. Random-matrix experiments: compare aligned, randomly permuted, and Haar-rotated eigenbases, validate the predicted arcsine law and mixed moments, and explain what these experiments and the limiting theory establish.

5. Products and the S-transform: define positive multiplicative convolution, derive the transform convention, and work out projection and covariance examples.
6. Covariance matrices and products: derive the Marchenko-Pastur law in the mean-one convention, check its zero atom, and compute moments of a product of two square covariance matrices.

## Requirements
- Preserve the current site design and existing unrelated edits.
- Each article has a clear question, prerequisite links, worked mathematics, a figure or concrete calculation, exercises with answer sketches, and primary references.
- Use consistent trace, Cauchy-transform, variance, and scaling conventions.
- State sufficient hypotheses for asymptotic freeness and distinguish finite matrices from their limiting joint distribution.
- Include a series landing page and previous/next navigation.
- Supply reproducible figure code, fixed random seeds, recorded numerical checks, and dependency instructions.
- Remove empty sections and repair malformed mathematics in the existing introduction.
- Update FUNCTIONALITIES.md and record identified issues and their resolution in ISSUE_REGISTRY.md.
- Record the author's publication cadence as at least two posts per week in an editorial plan. Proposed release dates remain proposals until chosen.

## Non-goals
- A general operator-algebra course or proofs of the Haar asymptotic-freeness theorem.
- Deployment, automatic publication, or committing unrelated local changes.

## Acceptance
- All six posts render successfully with Quarto and contain no unfinished sections.
- Numerical illustrations agree with the exact moments and limiting distribution within documented finite-size accuracy.
- Internal links, figure paths, mathematical markup, and desktop/mobile presentation are checked.
- Source files, figures, rendered pages, and editorial plan are available for review.

## Open question
None. The user selected six posts including multiplication.
