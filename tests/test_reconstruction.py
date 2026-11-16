"""Checks for deterministic published-summary reconstructions (stdlib unittest)."""
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import reproduce_incels_figures as r


class TestPublicationReconstruction(unittest.TestCase):
    def test_group_table_has_twelve_comparisons(self):
        rows=r.load("published_group_comparisons.csv")
        self.assertEqual(len(rows),12)
        by_pair={(x["group"],x["outcome"]):x for x in rows}
        self.assertEqual(by_pair[("Incel subculture","RMET")]["table_p"],"0.008")
        self.assertEqual(by_pair[("MRA","RMET")]["cohens_d_table"],"0.69")
        self.assertEqual(by_pair[("MRA","RMET")]["cohens_d_prose"],"0.80")

    def test_simple_ols_regression_recalculation(self):
        out=r.regression_reconstructions(r.load("published_regressions.csv"))
        sexual=next(x for x in out if x["model"].endswith("12 months"))
        self.assertEqual(sexual["implied_n"],368)
        self.assertAlmostEqual(sexual["calculated_r2"],.0190087,places=6)
        self.assertAlmostEqual(sexual["calculated_adjusted_r2"],.0163284,places=6)
        female=next(x for x in out if x["model"].endswith("women"))
        self.assertEqual(female["implied_n"],108)
        self.assertAlmostEqual(female["calculated_adjusted_r2"],.0375707,places=6)

    def test_orientation_compatibility(self):
        rows=[x for x in r.load("published_demographics.csv") if x["category"]=="sexual_orientation"]
        total368=r.orientation_compatibility(368,rows)
        self.assertEqual([x["compatible_counts"] for x in total368],["323","32","9","4"])
        total338=r.orientation_compatibility(338,rows)
        self.assertNotEqual([x["compatible_counts"] for x in total338],["323","32","9","4"])
        self.assertIn("none",[x["compatible_counts"] for x in total338])

    def test_chi_square_range(self):
        vals=r.chisquare_sensitivity()
        self.assertEqual(len(vals),6)
        self.assertLess(max(x["pearson_chi2_no_yates"] for x in vals),2.1)
        self.assertGreater(min(x["pearson_chi2_no_yates"] for x in vals),1.5)

    def test_denominator_examples_are_not_unique(self):
        candidates=r.denominator_candidates(100)
        d={v["candidate_incel_subgroup_n"]:v for v in candidates}
        self.assertEqual((d[14]["count_7_percent"],d[14]["count_36_percent"]),(1,5))
        self.assertEqual((d[28]["count_7_percent"],d[28]["count_36_percent"]),(2,10))

    def test_bonferroni_rounding_caveat(self):
        rows=r.comparison_sensitivity(r.load("published_group_comparisons.csv"))
        group={(x["group"],x["outcome"]):x for x in rows}
        self.assertIn("borderline",group[("Involuntarily celibate","Hostile attribution")]["interpretation"])
        self.assertEqual(group[("Incel subculture","RMET")]["interpretation"],"above cutoff")
        self.assertEqual(group[("Involuntarily single","Hostile attribution")]["interpretation"],"below cutoff")

if __name__=="__main__":unittest.main()
