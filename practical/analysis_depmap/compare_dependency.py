#!/usr/bin/env python3
"""Gene hotspot / dependency exercise using only the Python standard library."""

import csv
import math
from pathlib import Path
import statistics

# Edit these values for now. Adding command-line arguments is an exercise.
# Run this script from the repository root.
GENE = "KRAS"
DISEASE = "LUAD"
DATA_DIR = Path("practical/data_depmap")
OUTPUT_PATH = Path("practical/analysis_depmap/dependency.tsv")


def number(value):
    if value.strip() in ("", "NA", "NaN", "nan"):
        return None
    result = float(value)
    return result if math.isfinite(result) else None


def boolean(value):
    text = value.strip().lower()
    if text in ("", "na", "nan"):
        return None
    if text in ("true", "1"):
        return True
    if text in ("false", "0"):
        return False
    raise ValueError(f"Invalid Hotspot annotation: {value!r}")


def read_gene(path, gene):
    """Extract a wide matrix column, preserving the actual model identifiers."""
    result = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        matches = [i for i, label in enumerate(header[1:], 1)
                   if label.rsplit(" (", 1)[0] == gene]
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one {gene} column in {path}")
        column = matches[0]
        for row in reader:
            model = row[0].strip()  # The first column header can be empty.
            if not model or model in result:
                raise ValueError(f"Missing or duplicate ModelID in {path}: {model!r}")
            result[model] = number(row[column])
    return result


def write_table(path, columns, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "NA" if row[key] is None else row[key]
                             for key in columns})


def main():
    # 1. Filter metadata to a single disease, checking the join key first.
    with (DATA_DIR / "Model.csv").open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"ModelID", "CellLineName", "OncotreeCode"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Model.csv requires columns {sorted(required)}")
        models = {}
        for row in reader:
            model = row["ModelID"].strip()
            if not model or model in models:
                raise ValueError(f"Missing or duplicate metadata ModelID: {model!r}")
            models[model] = row
    cohort = {key: row for key, row in models.items() if row["OncotreeCode"] == DISEASE}
    if not cohort:
        raise ValueError(f"No models have OncotreeCode={DISEASE!r}")

    # 2. Summarize many variant rows into one genotype record per model.
    profiled = set()
    hotspot_flags = {model: [] for model in cohort}
    with (DATA_DIR / "OmicsSomaticMutations.csv").open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"ModelID", "HugoSymbol", "Hotspot"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Mutation file requires columns {sorted(required)}")
        for row in reader:
            model = row["ModelID"]
            if model not in cohort:
                continue
            profiled.add(model)  # Some somatic data exist; not proof of gene-level callability.
            if row["HugoSymbol"] == GENE:
                hotspot_flags[model].append(boolean(row["Hotspot"]))

    # 3. Extract measurements, then left-join by ID rather than row position.
    effects = read_gene(DATA_DIR / "CRISPRGeneEffect.csv", GENE)
    expression = read_gene(DATA_DIR / "OmicsExpressionProteinCodingGenesTPMLogp1.csv", GENE)
    rows = []
    for model, metadata in sorted(cohort.items()):
        flags = hotspot_flags[model]
        if True in flags:
            status = "hotspot"
        elif None in flags:
            status = "unknown_hotspot_status"
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
        if len(values) < 2:
            raise ValueError(f"Need at least two measured models in {status}; found {len(values)}")
        groups[status] = values
        q1, _, q3 = statistics.quantiles(values, n=4, method="inclusive")
        summaries.append({"gene": GENE, "disease": DISEASE,
                          "mutation_status": status, "n_models": len(values),
                          "mean_effect": statistics.mean(values), "median_effect": statistics.median(values),
                          "q1_effect": q1, "q3_effect": q3, "iqr_effect": q3 - q1,
                          "n_expression": len(expressed),
                          "median_log2_tpm_plus_1": statistics.median(expressed) if expressed else None})
    difference = statistics.median(groups["hotspot"]) - statistics.median(groups["no_hotspot_detected"])

    # 5. Save just the group summary; report the contrast in the terminal.
    write_table(OUTPUT_PATH, list(summaries[0]), summaries)
    print(f"{len(included)}/{len(rows)} models included; median difference = {difference:.4f}")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Reference: no {GENE} hotspot detected in a profiled model; not confirmed wild type.")


if __name__ == "__main__":
    main()
