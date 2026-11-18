#!/usr/bin/env python3
import csv

import numpy as np
import pymc as pm


# Use this fit unchanged throughout the exercise.
def fit(gene, is_luad, score, reference):
    is_luad, score = np.asarray(is_luad, dtype=float), np.asarray(score, dtype=float)
    n_luad = int(is_luad.sum())

    with pm.Model():
        baseline = pm.Normal("baseline")
        difference = pm.Normal("difference")
        pm.Normal("score", baseline + difference * is_luad, pm.HalfNormal("sigma"), observed=score)
        draws = pm.sample(500, tune=500, chains=4, cores=1, random_seed=42, progressbar=False)

    lower, median, upper = np.quantile(draws.posterior["difference"].values, [0.025, 0.5, 0.975])
    return dict(gene=gene, reference=reference, n_luad=n_luad, n_reference=len(score) - n_luad,
                lower=lower, median=median, upper=upper)


GENES = ("KRAS", "PIK3CA")
REFERENCE = "BRCA"

with open("../data/Model.csv", newline="") as source:
    models = {row["ModelID"]: int(row["OncotreeCode"] == "LUAD")
              for row in csv.DictReader(source) if row["OncotreeCode"] in ("LUAD", REFERENCE)}

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
    is_luad, score = zip(*rows)
    results.append(fit(gene, is_luad, score, REFERENCE))

with open("compare_dependency.tsv", "w", newline="") as target:
    writer = csv.DictWriter(target, fieldnames=list(results[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(results)
