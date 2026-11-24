#!/usr/bin/env python3
import csv

import numpy as np
import pymc as pm
import pandas as pd
import argparse
import dask

# Use this fit unchanged throughout the exercise.
def fit(gene, is_cohort, score, cohort):
    is_cohort, score = np.asarray(is_cohort, dtype=float), np.asarray(score, dtype=float)
    n_cohort = int(is_cohort.sum())

    with pm.Model():
        baseline = pm.Normal("baseline")
        difference = pm.Normal("difference")
        pm.Normal("score", baseline + difference * is_cohort, pm.HalfNormal("sigma"), observed=score)
        draws = pm.sample(500, tune=500, chains=4, cores=1, random_seed=42, progressbar=False, quiet=True)

    lower, median, upper = np.quantile(draws.posterior["difference"].values, [0.025, 0.5, 0.975])
    return dict(gene=gene, cohort=cohort, n_luad=len(score) - n_cohort, n_cohort=n_cohort,
                lower=lower, median=median, upper=upper)

if __name__ == "__main__":
    # 2.3 ------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("cohort")
    parser.add_argument("genes", nargs=2)
    args = parser.parse_args()

    # 2.1 ------------------------------
    #COMPARISON_COHORT = "BRCA"
    COMPARISON_COHORT = args.cohort
    LUAD = "LUAD"

    metadata = pd.read_csv("../data/Model.csv")
    metadata = metadata[["ModelID", "OncotreeCode"]]
    print("metadata:\n", metadata[:5])
    genes = pd.read_csv("../data/CRISPRGeneEffect.csv", index_col=0)
    genes.index.name = "ModelID"
    # remove the id after gene name
    genes.columns = genes.columns.str.split(" ").str[0]
    #genes = genes[["KRAS (3845)", "PIK3CA (5290)"]]
    genes = genes[args.genes]
    print("genes:\n", genes[:5])

    df = pd.merge(metadata, genes, on='ModelID')    # inner join is default
    df = df[df["OncotreeCode"].isin([LUAD, COMPARISON_COHORT])]
    print("merged:\n", df[:5])
    print(df.shape)

    del metadata
    del genes

    # 2.2 ------------------------------
    # check
    assert (len(set(df["ModelID"])) == df.shape[0])

    # like concat but the other way around
    df = df.melt(id_vars=["ModelID", "OncotreeCode"], var_name="Gene")
    print("df: \n", df[:5])
    print(df.shape)
    df = df.dropna()
    print("shape after dropna: ", df.shape)

    # 2.3 ------------------------------
    df["is_cohort"] = (df["OncotreeCode"] != LUAD).astype(int)
    print(df[:5])

    # fit:
    results = []
    for gene, data in df.groupby("Gene"):
        #print(gene, data)
        results.append(fit(gene, data["is_cohort"], data["value"], COMPARISON_COHORT))

    with open(f"compare_dependency-{COMPARISON_COHORT}.tsv", "w", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=list(results[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(results)

    # 3 ------------------------------
    # hab das command line argument weggelassen und dafür etwas ausführlicher gebenchmarked, hoffe das ist ok

    # single dask run to compare tsv results:
    tasks = []
    for gene, data in df.groupby("Gene"):
        tasks.append(dask.delayed(fit)(gene, data["is_cohort"], data["value"], COMPARISON_COHORT))
    total = dask.delayed(list)(tasks)
    results = total.compute(scheduler="processes", num_workers = 2)
    with open(f"compare_dependency-dask-{COMPARISON_COHORT}.tsv", "w", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=list(results[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(results)
    with (open(f"compare_dependency-{COMPARISON_COHORT}.tsv") as f1,
        open(f"compare_dependency-dask-{COMPARISON_COHORT}.tsv") as f2):
        identical = f1.read() == f2.read()
    print("TSV contents identical: ", identical)

    # benchmark
    import time
    # Warum up runs are important here, without them the serial time is way higher
    N_WARMUP_RUNS = 3
    N_RUNS = 10

    # serial (copy paste from 2.3):
    for _ in range(N_WARMUP_RUNS):
        for gene, data in df.groupby("Gene"):
            fit(gene, data["is_cohort"], data["value"], COMPARISON_COHORT)
    start = time.perf_counter()
    for _ in range(N_RUNS):
        for gene, data in df.groupby("Gene"):
            fit(gene, data["is_cohort"], data["value"], COMPARISON_COHORT)
    mm = time.perf_counter()-start
    print("avg serial time: ", mm/N_RUNS)

    # Dask
    N_WORKERS = [1, 2, 3, 4, 5]

    # as function so the execution time of this is part of the measurement
    def setup_tasks():
        tasks = []
        for gene, data in df.groupby("Gene"):
            tasks.append(dask.delayed(fit)(gene, data["is_cohort"], data["value"], COMPARISON_COHORT))
        return tasks

    def run_dask(n_workers):
        tasks = setup_tasks()
        total = dask.delayed(list)(tasks)
        total.compute(scheduler="processes", num_workers = n_workers)

    dask_mms = []
    for n_workers in N_WORKERS:
        for _ in range(N_WARMUP_RUNS):
            run_dask(n_workers)
        start = time.perf_counter()
        for _ in range(N_RUNS):
            run_dask(n_workers)
        mm = time.perf_counter() - start
        dask_mms.append(mm / N_RUNS)

    for nw, t in zip(N_WORKERS, dask_mms):
        print(f"n_workers: {nw}, time: {t}")
