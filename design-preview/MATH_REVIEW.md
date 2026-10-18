# Free probability mathematical review

Reviewed all six article sources and their current preview snapshots.

## Analytic checks

- The two 2 by 2 diagonal examples have sum eigenvalues (-2, 2) and (0, 0).
- Centered alternating freeness gives the fourth sum moment with coefficient four, compared with six under classical independence.
- The moment-cumulant relations through order four and all exercise answers are consistent.
- The symmetric sign R-transform gives the arcsine law with second and fourth moments 2 and 6. The Cauchy-transform branch and sign conventions are consistent.
- Positive product moments, projection examples and S-transform scaling agree with direct expansion.
- The mean-one covariance convention gives variance gamma, zero mass max(1-1/gamma, 0), and S(w)=1/(1+gamma*w).
- The square covariance product equation w=t*(1+w)^3 gives moments 1, 3, 12, 55 and right endpoint 27/4.

Cross-checked the sign-sum example with https://arxiv.org/html/1908.08125v2 and the covariance-product equation and support with https://arxiv.org/html/1407.1282, Section IV.2.1.

## Numerical reproduction

Ran tools/free_probability_figures.py in an isolated temporary output directory using the existing project environment. All assertions passed and the output JSON matched the saved checks.json exactly. Product empirical means were 1.0002094856, 3.0014662662, 12.0032888320 and 54.9645143785.

This checks the implemented examples, not a proof of the cited limit theorems.

## Display checks

All six browser pages rendered mathematical content with zero reported MathJax errors and no page-wide horizontal overflow. Article subtitles remain in the source but are hidden. The boxed plus symbol is additive free convolution, not a rendering artifact. The opening 2 by 2 matrices also render correctly.

Light, Dark and System preferences, navigation persistence and the hidden series sidebar were checked in the preceding presentation batch. No public deployment was performed.
