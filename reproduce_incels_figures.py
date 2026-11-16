#!/usr/bin/env python3
"""Reconstruct summary statistics and the five explanatory figures.

Input: rounded published statistics; NO participant-level data.
Figures are analytically equivalent recreations, not exact pixel copies of
those embedded in the companion Substack article. Default output: reproduced_figures/.

Run: python reproduce_incels_figures.py
     python reproduce_incels_figures.py --out /some/other/folder
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy.stats import chi2_contingency, f as f_distribution

ROOT = Path(__file__).resolve().parent
INK = "#142d40"
TEAL = "#548c8d"
SLATE = "#788b9b"
ORANGE = "#bc7655"
LIGHT = "#ecf0f1"
GRID = "#dfe6e9"


def load(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, records: list[dict], columns: list[str]):
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns)
        w.writeheader()
        w.writerows(records)


def reported_percent_counts(total: int, pct: float, decimals: int = 0) -> list[int]:
    """Whole-number counts whose percentage rounds to the displayed percentage.

    Tie convention is immaterial for the present inputs (none lie on exact ties).
    """
    half_unit = 0.5 * 10 ** (-decimals)
    return [k for k in range(total + 1)
            if pct - half_unit - 1e-10 <= 100*k/total < pct + half_unit - 1e-10]


def regression_reconstructions(rows: list[dict[str, str]]) -> list[dict]:
    out = []
    for r in rows:
        F = float(r["F"])
        df1, df2 = int(r["df1"]), int(r["df2"])
        n = df1 + df2 + 1
        r2 = F*df1/(F*df1 + df2)
        adj_r2 = 1 - (1-r2)*(n-1)/(n-df1-1)
        p_calc = f_distribution.sf(F, df1, df2)
        out.append({"model":r["model"],"F":F,"df1":df1,"df2":df2,"implied_n":n,
                    "reported_r2":r["reported_r2"],"calculated_r2":round(r2,7),
                    "calculated_adjusted_r2":round(adj_r2,7),"published_p":r["reported_p"],
                    "calculated_p_from_F":round(p_calc,8)})
    return out


def orientation_compatibility(total: int, pct_rows: list[dict[str, str]]) -> list[dict]:
    return [{"assumed_total":total,"category":r["group"],"printed_percent":r["reported_percent"],
             "compatible_counts": ";".join(map(str, reported_percent_counts(total,float(r["reported_percent"]),decimals=1))) or "none"}
            for r in pct_rows]


def chisquare_sensitivity(male_counts=(225,255)) -> list[dict]:
    # The article states 68% of 108 women and 60% of the men had sex in three years.
    out=[]
    for n_men in male_counts:
        for yes_w in reported_percent_counts(108, 68, decimals=0):
            for yes_m in reported_percent_counts(n_men, 60, decimals=0):
                table = [[yes_w,108-yes_w],[yes_m,n_men-yes_m]]
                chi2,p,_,_=chi2_contingency(table,correction=False)
                out.append({"women_n":108,"men_n":n_men,"women_yes":yes_w,"men_yes":yes_m,
                            "pearson_chi2_no_yates":round(chi2,8),"p_no_yates":round(p,8)})
    return out


def denominator_candidates(max_n=100) -> list[dict]:
    # The same published 36% appears for both sex-activity windows, but counts
    # need not be the same individuals. We do not infer subgroup n from this.
    out=[]
    for n in range(1,max_n+1):
        in_relationship=reported_percent_counts(n,7,0)
        sexually_active=reported_percent_counts(n,36,0)
        for a in in_relationship:
            for b in sexually_active:
                out.append({"candidate_incel_subgroup_n":n,"count_7_percent":a,
                            "count_36_percent":b,"status":"rounding-compatible; not verified"})
    return out


def comparison_sensitivity(group_rows: list[dict[str,str]]) -> list[dict]:
    cutoff=0.05/12
    out=[]
    for row in group_rows:
        if row["table_p"]=="ns" and not row["prose_p"]:
            status="not reported; not reconstructed"
            p=""
        elif row["table_p"]=="ns":
            status="non-significant in table; prose p available"
            p=row["prose_p"]
        else:
            p=row["prose_p"] or row["table_p"]
            x=float(p)
            # Published p values are rounded to 3 decimals when prose prints 0.0xx.
            uncertainty=0.0005 if len(p.split(".")[-1])==3 else 0.005
            if x-uncertainty<cutoff<x+uncertainty:
                status="borderline: rounded p spans threshold"
            else:
                status="below cutoff" if x<cutoff else "above cutoff"
        out.append({"group":row["group"],"outcome":row["outcome"],
                    "published_p_used":p,"bonferroni_family_n":12,
                    "cutoff":round(cutoff,8),"interpretation":status})
    return out


def style_axes(ax):
    ax.set_facecolor("white")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ("top","right","left"): ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="both", length=0, colors=INK, labelsize=10)


def save(fig, out, name):
    fig.savefig(out/name, dpi=180, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def effect_size_chart(out, rows):
    keep=[("Incel subculture","RMET","Incel identification: lower RMET",INK),
          ("Involuntarily celibate","Hostile attribution","Involuntarily celibate: higher hostility",TEAL),
          ("Involuntarily single","Hostile attribution","Involuntarily single: higher hostility",TEAL),
          ("MRA","RMET","MRA identification: lower RMET",SLATE)]
    data={(r["group"],r["outcome"]):r for r in rows}
    fig,ax=plt.subplots(figsize=(10.1,5.0))
    vals=[]
    for group,outcome,label,color in keep:
        r=data[group,outcome]
        v=float(r["cohens_d_table"])
        vals.append(v)
    y=list(range(len(keep)))
    ax.barh(y, vals, height=.56, color=[x[3] for x in keep])
    ax.set_yticks(y, [x[2] for x in keep]); ax.invert_yaxis()
    ax.set_xlim(0,1.1)
    ax.set_xlabel("Published standardized mean difference (Cohen's d)",labelpad=10,color=INK)
    ax.set_title("Four selected group differences in the survey",fontsize=17,weight="bold",color=INK,pad=18)
    for i,v in enumerate(vals):ax.text(v+.025,i,f"d = {v:.2f}",va="center",fontsize=10,color=INK,weight="bold")
    style_axes(ax)
    fig.text(.15,.02,"MRA uses the Table 1 effect (0.69); prose reports 0.80. Confidence intervals unavailable.",color=SLATE,fontsize=9)
    fig.subplots_adjust(left=.37,bottom=.20,right=.95,top=.82)
    save(fig,out,"figure_01_effect_sizes.png")


def multiplicity_chart(out, rows):
    focus=[("Involuntarily single","Hostile attribution","Involuntarily single / hostile attribution"),
           ("Involuntarily celibate","Hostile attribution","Involuntarily celibate / hostile attribution"),
           ("Incel subculture","RMET","Incel identification / RMET"),
           ("MRA","RMET","MRA identification / RMET")]
    look={(r["group"],r["outcome"]):r for r in rows}
    fig,ax=plt.subplots(figsize=(10.6,5.4))
    fig.patch.set_facecolor("white");ax.set_axis_off()
    ax.set_xlim(0,10);ax.set_ylim(0,5)
    ax.text(0,4.76,"Which results remain below a stricter threshold?",fontsize=18,color=INK,weight="bold")
    ax.text(0,4.34,"Illustration: 12 Table 1 comparisons → Bonferroni cutoff p < .00417",fontsize=12,color=INK)
    for i,(g,o,label) in enumerate(focus):
        y=3.55-i*.95
        p=float(look[g,o]["prose_p"] or look[g,o]["table_p"])
        state=("Below threshold",TEAL) if p==.003 else (("Borderline*",ORANGE) if p==.004 else ("Above threshold",SLATE))
        ax.add_patch(FancyBboxPatch((.02,y-.26),9.7,.72,boxstyle="round,pad=0.02,rounding_size=.17",
                                    ec=GRID,facecolor="#f7f8f8",linewidth=1))
        ax.plot([.45,.45],[y-.08,y+.32],lw=7,color=state[1],solid_capstyle="round")
        ax.text(.73,y+.16,label,fontsize=11.5,color=INK,va="center")
        ax.text(.73,y-.13,state[0],fontsize=10.5,color=state[1],va="center",weight="bold")
        ax.text(9.38,y+.05,f"p = {p:.3f}",fontsize=11.5,color=INK,weight="bold",ha="right",va="center")
    ax.text(.02,.12,"*Printed p = .004 is rounded: exact value could lie on either side of .00417.",fontsize=9.5,color=SLATE)
    ax.text(.02,-.14,"Sensitivity example, not a prespecified family of hypotheses.",fontsize=9.5,color=SLATE)
    save(fig,out,"figure_02_multiplicity.png")


def rmet_chart(out,rows):
    constructs=[r["construct"] for r in rows]
    values=[float(r["correlation"]) for r in rows]
    fig,ax=plt.subplots(figsize=(9.5,5.8))
    y=range(len(rows)); ax.barh(y,values,height=.55,color=[TEAL,INK,SLATE,"#a7b5bc","#c3cdd0"])
    ax.set_yticks(list(y),constructs);ax.invert_yaxis();ax.set_xlim(0,.46)
    ax.set_xlabel("Average published meta-analytic correlation (r)",labelpad=9,color=INK)
    ax.set_title("What does the Eyes Test correlate with?",fontsize=17,weight="bold",color=INK,pad=16)
    for i,x in enumerate(values):ax.text(x+.01,i,f"r = {x:.2f}",fontsize=10,color=INK,va="center",weight="bold")
    style_axes(ax)
    fig.text(.18,.03,"Kittel et al. (2022): estimates drawn from different groups of studies; not paired comparisons.",fontsize=9,color=SLATE)
    fig.subplots_adjust(left=.27,right=.94,bottom=.18,top=.85)
    save(fig,out,"figure_03_rmet_correlations.png")


def r2_chart(out, regressions):
    select=[("Hostile attribution and no sex in 3 years","No sex in 3 years",SLATE),
            ("Hostile attribution and no sex in 12 months","No sex in 12 months",TEAL),
            ("Hostile attribution and relationship success full sample","Self-rated relationship success",INK)]
    x={r["model"]:float(r["reported_r2"])*100 for r in regressions}
    fig,ax=plt.subplots(figsize=(10.2,4.7))
    for i,(k,label,c) in enumerate(select):
        ax.barh(i,100,color=LIGHT,height=.6)
        ax.barh(i,x[k],color=c,height=.6)
        ax.text(6,i,f"{x[k]:.1f}%",color=INK,weight="bold",va="center",fontsize=11)
    ax.set_yticks(range(3),[r[1] for r in select]);ax.invert_yaxis()
    ax.set_xlim(0,100)
    ax.set_xlabel("Share of variation in outcome (0 to 100%)",labelpad=10,color=INK)
    ax.set_title("Little of the outcome variation is explained",fontsize=17,weight="bold",color=INK,pad=18)
    style_axes(ax)
    fig.text(.11,.02,"Reported R² values; first two appear unadjusted although the article labels all R² as adjusted.",fontsize=9,color=SLATE)
    fig.subplots_adjust(left=.30,bottom=.23,right=.97,top=.80)
    save(fig,out,"figure_04_explained_variance.png")


def sample_chart(out, demographics):
    data={r["group"]:int(r["reported_count"]) for r in demographics if r["reported_count"] and r["category"]=="sex"}
    total = data["Women"]+data["Men"]+data["Other"]
    implied=366+2
    fig,ax=plt.subplots(figsize=(9.6,3.7))
    ax.set_xlim(0,10);ax.set_ylim(0,3);ax.set_axis_off()
    for x,heading,num,foot in [(0,"Published demographic total",total,"108 women + 225 men + 5 other"),
                               (5.1,"Implied by regressions",implied,"Residual df = 366, simple OLS")]:
        ax.add_patch(FancyBboxPatch((x+.12,.66),4.65,1.85,boxstyle="round,pad=.1,rounding_size=.15",
                                    edgecolor=GRID,facecolor="#f7f8f8",lw=1.2))
        ax.text(x+.40,2.17,heading,fontsize=11,color=INK)
        ax.text(x+.40,1.4,str(num),fontsize=33,color=SLATE if x==0 else INK,weight="bold")
        ax.text(x+.40,1.02,foot,fontsize=9,color=SLATE)
    ax.text(.18,.2,"Sexual-orientation percentages are also compatible with n = 368; microdata unavailable.",fontsize=10,color=SLATE)
    save(fig,out,"figure_05_sample_discrepancy.png")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",default="reproduced_figures",help="Output folder (relative to repository root by default)")
    args=parser.parse_args()
    out=Path(args.out)
    if not out.is_absolute():out=ROOT/out
    out.mkdir(parents=True,exist_ok=True)
    groups=load("published_group_comparisons.csv")
    regress=load("published_regressions.csv")
    demographics=load("published_demographics.csv")
    meta=load("rmet_meta_correlations.csv")
    assert len(groups)==12
    reg_results=regression_reconstructions(regress)
    compare_results=comparison_sensitivity(groups)
    pct_rows=[r for r in demographics if r["category"]=="sexual_orientation"]
    orientation=[*orientation_compatibility(338,pct_rows),*orientation_compatibility(368,pct_rows)]
    chi=chisquare_sensitivity()
    denoms=denominator_candidates(100)
    write_csv(out/"regression_recalculations.csv",reg_results,list(reg_results[0]))
    write_csv(out/"multiplicity_sensitivity.csv",compare_results,list(compare_results[0]))
    write_csv(out/"orientation_compatibility.csv",orientation,list(orientation[0]))
    write_csv(out/"chi_square_enumeration.csv",chi,list(chi[0]))
    write_csv(out/"possible_incel_denominators.csv",denoms,list(denoms[0]))
    effect_size_chart(out,groups)
    multiplicity_chart(out,groups)
    rmet_chart(out,meta)
    r2_chart(out,regress)
    sample_chart(out,demographics)
    lines=["Date Psychology incel/ToM article — published-summary reconstruction",
           "Not a participant-level replication. All values below are derived from rounded published summaries.",
           "", "REPORTED GROUP COMPARISONS / BONFERRONI SENSITIVITY (family size 12, cutoff .004167)"]
    for q in compare_results:
        if q["published_p_used"]:
            lines.append(f"{q['group']} | {q['outcome']}: p={q['published_p_used']}; {q['interpretation']}")
    lines += ["", "REGRESSIONS: ordinary R² vs adjusted R² reconstructed from printed F and df"]
    for x in reg_results:
        lines.append(f"{x['model']}: n implied={x['implied_n']}, reported R²={x['reported_r2']}, "
                     f"ordinary R²={x['calculated_r2']:.5f}, adjusted R²={x['calculated_adjusted_r2']:.5f}, "
                     f"F-derived p={x['calculated_p_from_F']:.6f}")
    lines += ["", "DEMOGRAPHICS / ORIENTATION PERCENTAGES"]
    lines.append("Published sex counts sum to 338 (108+225+5). F(1,366) implies 368 for one-predictor OLS.")
    for n in (338,368):
        sub=[o for o in orientation if o["assumed_total"]==n]
        lines.append(f"n={n} compatible orientation counts: "+", ".join(f"{r['category']}={r['compatible_counts']}" for r in sub))
    lines += ["", "CHI-SQUARE CHECK: 68% of 108 women vs 60% of n men, Pearson without Yates"]
    for n in (225,255):
        sub=[r for r in chi if r["men_n"]==n]
        lines.append(f"men n={n}: χ² range {min(x['pearson_chi2_no_yates'] for x in sub):.4f}–"
                     f"{max(x['pearson_chi2_no_yates'] for x in sub):.4f}; "
                     f"source printed χ²=3.2466")
    lines += ["", "SMALL INCEL DENOMINATOR EXAMPLE"]
    lines.append("n=14 allows 1/14≈7%, 5/14≈36%. Other n also fit; this is NOT a verified subgroup count.")
    lines.append("",)
    lines.append("No original raw data, exact full p-value list, survey questionnaire, or code was supplied.")
    report="\n".join(lines)+"\n"
    (out/"reconstruction_results.txt").write_text(report,encoding="utf-8")
    print(report)
    print(f"Wrote 5 chart PNGs + 5 audit CSV files + report to {out}")

if __name__=="__main__":main()
