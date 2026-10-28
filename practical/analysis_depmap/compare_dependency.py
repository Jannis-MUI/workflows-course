#!/usr/bin/env python3
"""Gene hotspot / dependency exercise using only the Python standard library."""

import csv
from pathlib import Path
import statistics

# Edit these values for now. Adding command-line arguments is an exercise.
# Run this script from the repository root.
GENE = "KRAS"
DISEASE = "LUAD"
DATA_DIR = Path("practical/data_depmap")
OUTPUT_PATH = Path("practical/analysis_depmap/dependency.tsv")


def read_gene(path, gene):
    """Extract a wide matrix column, preserving the actual model identifiers."""
    result = {}
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        column = next(i for i, label in enumerate(header)
                      if label.split(" (")[0] == gene)
        # Empty measurements remain missing; absent model IDs are handled by get().
        return {row[0]: float(row[column]) if row[column] else None for row in reader}


def main():
    # 1. Filter metadata to a single disease.
    with (DATA_DIR / "Model.csv").open(newline="") as handle:
        cohort = {row["ModelID"]: row for row in csv.DictReader(handle)
                  if row["OncotreeCode"] == DISEASE}

    # 2. Summarize many variant rows into one genotype record per model.
    profiled = set()
    hotspot_models = set()
    with (DATA_DIR / "OmicsSomaticMutations.csv").open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            model = row["ModelID"]
            if model not in cohort:
                continue
            profiled.add(model)  # Some somatic data exist; not proof of gene-level callability.
            if row["HugoSymbol"] == GENE and row["Hotspot"] == "True":
                hotspot_models.add(model)

    # 3. Extract measurements, then left-join by ID rather than row position.
    effects = read_gene(DATA_DIR / "CRISPRGeneEffect.csv", GENE)
    expression = read_gene(DATA_DIR / "OmicsExpressionProteinCodingGenesTPMLogp1.csv", GENE)
    rows = []
    for model, metadata in sorted(cohort.items()):
        if model in hotspot_models:
            status = "hotspot"
        elif model in profiled:
            status = "no_hotspot_detected"
        else:
            status = "no_mutation_data"
        effect = effects.get(model)
        rows.append({"ModelID": model, "CellLineName": metadata["CellLineName"],
                     "mutation_status": status, "gene_effect": effect,
                     "log2_tpm_plus_1": expression.get(model)})

    # 4. Filter and summarize; expression missingness does not exclude a model.
    included = [row for row in rows
                if row["mutation_status"] in ("hotspot", "no_hotspot_detected")
                and row["gene_effect"] is not None]
    groups = {}
    summaries = []
    for status in ("hotspot", "no_hotspot_detected"):
        selected = [row for row in included if row["mutation_status"] == status]
        values = [row["gene_effect"] for row in selected]
        expressed = [row["log2_tpm_plus_1"] for row in selected
                     if row["log2_tpm_plus_1"] is not None]
        groups[status] = values
        q1, _, q3 = statistics.quantiles(values, n=4, method="inclusive")
        summaries.append({"gene": GENE, "disease": DISEASE,
                          "mutation_status": status, "n_models": len(values),
                          "mean_effect": statistics.mean(values), "median_effect": statistics.median(values),
                          "q1_effect": q1, "q3_effect": q3, "iqr_effect": q3 - q1,
                          "n_expression": len(expressed),
                          "median_log2_tpm_plus_1": statistics.median(expressed)})
    difference = statistics.median(groups["hotspot"]) - statistics.median(groups["no_hotspot_detected"])

    # 5. Save just the group summary; report the contrast in the terminal.
    with OUTPUT_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summaries[0], delimiter="\t")
        writer.writeheader()
        writer.writerows(summaries)
    print(f"{len(included)}/{len(rows)} models included; median difference = {difference:.4f}")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Reference: no {GENE} hotspot detected in a profiled model; not confirmed wild type.")


if __name__ == "__main__":
    main()
