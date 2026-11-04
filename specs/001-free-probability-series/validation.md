# Validation

Checked 2026-10-17.

## Mathematical review

- Checked centered second and fourth mixed moments by direct word expansion.
- Checked moment-cumulant coefficients through order four and the Catalan pairing recurrence.
- Derived the R-transform equation from the block containing position one.
- Checked the semicircle and arcsine inverse branches, moments, and absence of endpoint atoms in the arcsine law.
- Derived the second product moment by centering and checked the first-order S-transform expansion.
- Checked the covariance convention n/m, mean one, Marchenko-Pastur quadratic, and zero atom.
- Derived the square-covariance product equation, Lagrange coefficient formula, and critical point 27/4.
- Distinguished imported asymptotic-freeness and random-matrix theorems from derivations supplied in the articles.

Primary references are linked next to the relevant statements and in further-reading sections. The exposition does not claim to prove the imported Haar or Wishart limit theorems.

## Numerical execution

Ran tools/free_probability_figures.py with seed 1729, NumPy 2.5.2, and Matplotlib 3.11.1. The check report is assets/free-probability/checks.json.

- Maximum unitarity error: 1.34e-15 or less.
- At n=256, mean sum moments: 2.00121 and 6.01167, against exact limits 2 and 6.
- At n=256, RMS alternating fourth moment: 0.00522.
- Covariance zero fractions agree with the exact rank counts at all three tested aspect ratios.
- Product moment means across eight n=384 matrices: 1.00021, 3.00147, 12.00329, 54.96451.
- Recursive series expansion agrees with the closed Fuss-Catalan formula through order eight.

## Rendering and navigation

- Full Quarto 1.10.18 render succeeded for all 13 site pages.
- Static link checking covered the homepage, listing, series page, and six articles, with no missing local files or anchors.
- Desktop browser checks found no missing images or MathJax errors in any article. Typeset formula counts were 69, 58, 82, 36, 71, and 79.
- Mobile checks at 390 pixels exposed and resolved equation overflow and a wide result table. Articles and series landing page fit within the viewport, with local scrolling for wide content.
- Visually inspected the series landing page, article typography, and the generated spectral figures.
- New article prose and editorial records contain no forbidden dash characters or semicolons.

The cache environment used for the restricted build was set to temporary writable directories. This is an execution-environment detail, not a site dependency.
