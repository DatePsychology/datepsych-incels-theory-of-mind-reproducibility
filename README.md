# Incels, Theory of Mind and Hostile Attribution — Reproducibility Materials

Code, transcribed published statistics, five figure reconstructions, and numerical audit results accompanying the methodological review **“Do Incels Have a Theory-of-Mind Deficit? A Closer Look at Date Psychology’s Survey.”**

**Scope:** This is an **independent reconstruction from published summary statistics**, **not** a reanalysis of participant-level data and **not** an independent replication of Alexander's survey. The original microdata, questionnaire, and analysis code were not available. The estimates, testing assumptions and numerical discrepancies are interpreted accordingly. No new evidence about individual incels is generated here.

The format is deliberately similar to the [Status Signals reproducibility repository](https://github.com/DatePsychology/datepsych-status-signals-reproducibility): a compact README, a standalone Python script, documented CSV inputs, a checked output report, and figures.

## Contents

| File | Purpose |
|---|---|
| `reproduce_incels_figures.py` | Recomputes ordinary/adjusted R², F-test p-values, Bonferroni sensitivity, orientation-count compatibility, subgroup-denominator examples, and chi-square enumerations; regenerates five plots. |
| `published_group_comparisons.csv` | All 12 group-by-measure Table 1 cells, with nonsignificant cells left **unquantified** rather than invented, and both reported MRA effect sizes. |
| `published_regressions.csv` | Transcription of printed F statistics, degrees of freedom, p-values and claimed R² for five regressions. |
| `published_demographics.csv` | Printed sex counts, sexual-orientation percentages, recent sexual activity percentages and incel Table 2 proportions. |
| `rmet_meta_correlations.csv` | Five meta-analytic RMET associations reported by Kittel et al. (2022). |
| `SOURCE_AUDIT.md` | Exact provenance, formulas, assumptions, caveats, and source links for every chart and calculation. |
| `reconstruction_results.txt` | Checked reference output of the numeric reconstruction (same content as `reproduced_figures/reconstruction_results.txt`). |
| `article_figures/figure_01_...png` through `figure_05_...png` | **Exact copies** of the five existing Substack article figures, unchanged. |
| `reproduced_figures/figure_01_...png` through `figure_05_...png` | Script-generated figures using the same data and interpretations. Visually similar but **not pixel-for-pixel identical** to the Substack illustrations. |
| `reproduced_figures/*.csv` | Auditable machine-readable outputs for regressions, testing thresholds, orientation counts, chi-square possibilities and subgroup-denominator examples. |
| `tests/test_reconstruction.py` | Automated checks for the statistical reconstruction. |
| `requirements.txt` | Dependencies for the code. |
| `.gitignore` | Basic Python exclusions. |

## Reproduce the calculations and figures

Requires **Python 3.10+**. From the repository folder:

```bash
python -m pip install -r requirements.txt
python reproduce_incels_figures.py
python -m unittest discover -s tests -v
```

The script prints the numerical audit, writes five new `.png` figures, five derived `.csv` files, and `reconstruction_results.txt` in **`reproduced_figures/`**. By default it does **not** overwrite the five `article_figures/` originals. Choose a different output directory with `python reproduce_incels_figures.py --out another_folder`.

The checked reference output is also supplied as [`reconstruction_results.txt`](reconstruction_results.txt). Minor differences in plot font/layout across platforms do not alter the statistics.

## What the numbers show—and do not show

1. **Small groups:** Table 2's 7% and 36% entries are consistent with n = 14 (1/14 and 5/14), **but other denominators fit**. Group n = 14 is an illustrative reconstruction, not an established sample size.
2. **Multiple tests:** The four highlighted results can be compared to an **illustrative** 12-test Bonferroni threshold of .00417; this was not a prespecified family. Bonferroni is valid even for dependent tests but may be conservative; rounded p = .004 cannot be confidently classified relative to .00417.
3. **Sample reporting:** Printed demographics give 338 (108+225+5), whereas a standard F(1,366) regression implies 368 observations; the orientation percentages are compatible with n = 368 under normal rounding. This is strong evidence of a reporting discrepancy, **not** proof of which source value is wrong.
4. **R² reporting:** F = 7.092 and 6.359 imply ordinary R² ≈ .0190 and .0171 but adjusted R² ≈ .0163 and .0144. The article labels all values adjusted; others, like .037 for the pooled success model, are consistent with adjustment.
5. **Chi-square reporting:** From 68% of 108 women and 60% of 225 or 255 men, all compatible whole-person count tables yield a Pearson χ² below 2.1, not printed χ² = 3.2466. Missing denominators or undocumented procedures cannot be ruled out.
6. **Conceptual limits:** RMET performance is not synonymous with general theory of mind. Neither observational association establishes causation, a specific incel-wide trait, or the accuracy of real interactions with potential partners.

See [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md) for methods, mathematical assumptions, and the source-by-source audit.

## Source and companion article

- **Primary:** [Alexander (2023), “Theory of mind, hostile attribution bias, and incels.”](https://datepsychology.com/theory-of-mind-hostile-attribution-bias-and-incels/)
- **RMET associations:** [Kittel, Olderbak & Wilhelm (2022)](https://doi.org/10.1177/1073191121996469)
- **Hostile attribution questionnaire:** [Coccaro, Noblett & McCloskey (2009)](https://doi.org/10.1016/j.jpsychires.2009.01.012)
- **RMET measurement debate:** [Murphy & Hall (2024)](https://doi.org/10.1016/j.cpr.2024.102506); [Higgins et al. (2025)](https://doi.org/10.1016/j.cpr.2024.102530)
- **Additional related evidence:** [Koo et al. (2022)](https://doi.org/10.3389/fpsyg.2022.863763); [Costello et al. (2023)](https://doi.org/10.1080/00224499.2023.2248096)

The [companion article)](https://datepsych.substack.com/p/do-incels-have-a-theory-of-mind-deficit) contains the full methodological interpretation and bibliography. This repository does **not** redistribute third-party PDFs, source webpages, or original participant records.


