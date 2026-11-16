# Source audit and calculations

This document maps the numbers in the five graphics and numerical checks to **published summary statistics**. Nothing in this repository purports to recover participant records or to replicate Alexander's original R analysis.

## 1. The Date Psychology source and its disclosures

Original article: [Alexander (2023), “Theory of mind, hostile attribution bias, and incels”](https://datepsychology.com/theory-of-mind-hostile-attribution-bias-and-incels/), accessed for this reconstruction from an HTML copy of the article.

- **Table 1:** six group categories (“involuntarily celibate,” “involuntarily single,” “incels,” “Red Pill,” “Black Pill,” “Men’s Rights Activists”) crossed with two outcomes (hostile attribution and RMET). It gives four significant cells, but not exact p-values or effect sizes for the other eight cells. The surrounding prose gives p = .159 for incel identity vs hostile attribution.
- **Main Analysis / Manosphere Subanalysis:** incel/RMET p = .008, d = .88; involuntary celibacy/hostility p = .004, d = .41; involuntary single/hostility p = .003, d = .38; MRA/RMET p = .042, d = .80 in prose, versus approximately .04 and d = .69 in Table 1. Figure 1 uses the table's d = .69 for MRA and notes the discrepancy.
- **Results / Statistics:** states 108 women, 225 men, five other participants, total 338; the reported regression F(1,366) statistics imply 368 observations in an ordinary one-predictor least-squares regression. A women-only regression uses F(1,106), consistent with 108. The source claims all reported R² values are adjusted.
- **Descriptive statistics:** prints heterosexual 87.8%, bisexual 8.7%, gay/lesbian 2.4%, other 1.1%. At ordinary one-decimal rounding these are compatible with exactly 323, 32, 9 and 4 among 368, whereas 338 cannot yield all four displayed percentages. This strengthens, but does **not establish**, an N = 368 correction: there could be mixing of dataset versions or other reporting errors.
- **Gender Subanalysis:** 68% of women and 60% of men reported sex within the previous three years; a Pearson chi-square is given as 3.2466. Our enumeration checks compatible integer counts under **either** 225 or 255 men and finds substantially lower uncorrected Pearson chi-squares. This is conditional on the stated sex counts, ordinary rounding and the conventional Pearson formulation; missing data or another undocumented denominator could change the reconciliation.
- **Table 2:** 7% of the incel-identity subgroup is reported as in a relationship and 36% as sexually active in each displayed window. One in 14 is ~7%, five in 14 is ~36%, but other counts (e.g., 2 and 10 in 28) fit. **Do not cite 14 as an observed sample size.**

## 2. Five graphics

| Figure | Input | Computation | Caveats |
|---|---|---|---|
| 01 — Four effect sizes | `published_group_comparisons.csv` | Plot printed Cohen's d values .88, .41, .38, .69 | Different psychological outcomes; no subgroup counts, standard errors or original confidence intervals; Wilcoxon p-values need not target the Cohen's d estimand |
| 02 — Multiple testing | `published_group_comparisons.csv` | Threshold .05 / 12 = .0041667, compare with four prose p-values | Only an **illustrative** family of 12 tests; dependence does not invalidate Bonferroni but can make it conservative; p = .004 is rounded and could fall either side |
| 03 — RMET correlations | `rmet_meta_correlations.csv` | Plot five separate meta-analytic estimates from Kittel et al. (2022) | The studies behind the five estimates are not identical; not a paired contrast or original meta-analysis |
| 04 — Explained variance | `published_regressions.csv` | Plot printed .017, .019, .037 as percentages of **100%** of variation | At least two printed R² values appear **unadjusted**, despite the article's adjusted-R² statement; explained variance is not causal importance |
| 05 — Sample-size discrepancy | `published_demographics.csv`, `published_regressions.csv` | Compare arithmetic total 108+225+5 = 338 with n = 366+2 = 368 | Assumes ordinary one-predictor OLS with intercept; not an independently recovered participant count |

## 3. Recalculating simple-regression statistics

For an ordinary least-squares model with an intercept and **one** predictor, with numerator df = 1 and residual degrees of freedom `df2`, the implied number of complete observations is `n = df2 + 2`.

The ordinary coefficient of determination follows from its F statistic:

```
R2 = F / (F + df2)
adjusted_R2 = 1 - (1 - R2) * (n - 1)/(n - 2)
```

The source's F(1,366) = 7.092 implies ordinary R² = 0.019009, adjusted R² = 0.016328. F(1,366) = 6.359 gives ordinary R² = 0.017078 and adjusted R² = 0.014392. These reproduce the *printed* values to rounding as ordinary R², not as adjusted R². For the relationship-success model F(1,366) = 15.02, the adjusted R² is 0.036796, consistent with printed 0.037.

The script also evaluates corresponding p-values from the F distribution using `scipy.stats.f.sf`, allowing readers to verify the F–p combinations. This does not reproduce the original regressions or detect all possible modeling choices.

## 4. Rounding and count enumeration

Published percentages are rounded. For a one-decimal percentage `p`, the code enumerates integers `k` satisfying `p - 0.05 ≤ 100*k/n < p + 0.05`. For a whole percentage, the analogous interval is ±0.5 percentage point. That explains both the orientation check and the range of chi-square reconstructions.

The chi-square values are *uncorrected Pearson* values calculated from all integer 2×2 tables consistent with the stated rounded sex-specific three-year percentages and assumed denominators (108 and 225 or 255). A Yates correction would make the values smaller; it would not explain the larger reported χ² = 3.2466 on those tables. The original cells and statistical code are not available.

## 5. What remains unverifiable

- Exact group Ns, group means, medians, variances, data exclusions and missingness.
- Reliability of Alexander's randomly selected 25 RMET items and selected hostile-attribution items in **his** sample.
- Actual Wilcoxon statistics, p-values for all nonsignificant comparisons, preregistered testing family, and full multiple-comparison correction.
- A complete confidence interval for incel/RMET d = .88. Any CI assuming n = 14 would be hypothetical, not a sourced estimate.
- Robustness to covariates, duplicate or careless responses, real-world dating behavior, or longitudinal causal explanations.
- Explanation for apparent disagreement between pooled and sex-specific regressions. Group-specific correlation cannot be recovered by simply weighting correlations by subgroup size.

## 6. Independent sources and research context

- [Kittel, Olderbak & Wilhelm (2022)](https://doi.org/10.1177/1073191121996469): meta-analytic RMET correlations in Figure 3. Its meta-analysis covered 61 studies and 8,611 participants overall; individual construct-specific correlations can involve different sets of studies.
- [Coccaro, Noblett & McCloskey (2009)](https://doi.org/10.1016/j.jpsychires.2009.01.012): development and validation of the social information-processing hostile-attribution subscale. The questionnaire is described as SIP-AEQ in the paper's main text and SIP-ABQ in its appendix; the abbreviation difference alone is **not** an error by Alexander.
- [Murphy & Hall (2024)](https://doi.org/10.1016/j.cpr.2024.102506), [Higgins et al. (2025)](https://doi.org/10.1016/j.cpr.2024.102530): contrasting interpretations of RMET measurement validity. Neither justifies interpreting a brief RMET difference as a specific general theory-of-mind deficit.
- [Koo et al. (2022)](https://doi.org/10.3389/fpsyg.2022.863763): an observational correlation between a Korean-language RMET and a different hostile-attribution questionnaire; not independent replication of Alexander's sample.
- [Costello et al. (2023)](https://doi.org/10.1080/00224499.2023.2248096): incel and non-incel single men's estimates of *stated* mate preferences; not a RMET study, and not evidence of greater general mind-reading error among incels.

These sources are linked, not redistributed. Copyrighted PDFs, third-party article text and survey microdata are intentionally excluded.
