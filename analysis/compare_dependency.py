#!/usr/bin/env python3
import csv

import numpy as np
import pymc as pm


# Use this fit unchanged throughout the exercise.
def fit(gene, is_cohort, score, cohort):
    is_cohort, score = np.asarray(is_cohort, dtype=float), np.asarray(score, dtype=float)
    n_cohort = int(is_cohort.sum())

    with pm.Model():
        baseline = pm.Normal("baseline")
        difference = pm.Normal("difference")
        pm.Normal("score", baseline + difference * is_cohort, pm.HalfNormal("sigma"), observed=score)
        draws = pm.sample(500, tune=500, chains=4, cores=1, random_seed=42, progressbar=False)

    lower, median, upper = np.quantile(draws.posterior["difference"].values, [0.025, 0.5, 0.975])
    return dict(gene=gene, cohort=cohort, n_luad=len(score) - n_cohort, n_cohort=n_cohort,
                lower=lower, median=median, upper=upper)


GENES = ("KRAS", "PIK3CA")
COHORT = "BRCA"

with open("../data/Model.csv", newline="") as source:
    models = {row["ModelID"]: int(row["OncotreeCode"] == COHORT)
              for row in csv.DictReader(source) if row["OncotreeCode"] in ("LUAD", COHORT)}

with open("../data/CRISPRGeneEffect.csv", newline="") as source:
    rows = csv.reader(source)
    columns = [label.partition(" (")[0] for label in next(rows)]
    selected = {gene: columns.index(gene) for gene in GENES}
    groups = {gene: [] for gene in GENES}

    for row in rows:
        if row[0] in models:
            for gene, column in selected.items():
                if row[column] not in ("", "NA", "NaN"):
                    groups[gene].append((models[row[0]], float(row[column])))

results = []
for gene, rows in groups.items():
    is_cohort, score = zip(*rows)
    results.append(fit(gene, is_cohort, score, COHORT))

with open("compare_dependency-BRCA.tsv", "w", newline="") as target:
    writer = csv.DictWriter(target, fieldnames=list(results[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(results)
