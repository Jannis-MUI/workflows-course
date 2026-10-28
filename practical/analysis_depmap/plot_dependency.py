#!/usr/bin/env python3
"""Plot group medians and IQRs from the processed table as a PDF."""

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Edit these paths for now. Adding command-line arguments is an exercise.
# Run this script from practical/analysis_depmap/.
INPUT_PATH = Path("compare_dependency.tsv")
OUTPUT_PATH = Path("plot_dependency.pdf")


def main():
    with INPUT_PATH.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    statuses = ("hotspot", "no_hotspot_detected")
    gene, disease = rows[0]["gene"], rows[0]["disease"]
    summary = {row["mutation_status"]: row for row in rows}

    figure, axis = plt.subplots(figsize=(9, 6))
    for x, status, color in zip((0, 1), statuses, ("#bd4d38", "#38769c")):
        row = summary[status]
        median = float(row["median_effect"])
        lower = median - float(row["q1_effect"])
        upper = float(row["q3_effect"]) - median
        axis.errorbar(x, median, yerr=[[lower], [upper]],
                      fmt="s", color=color, capsize=6, markersize=7, linewidth=2)
    for reference in (-1, 0):
        axis.axhline(reference, color="0.8", linestyle="--", zorder=0)
    labels = [f"{gene} hotspot", f"No {gene} hotspot detected"]
    axis.set_xticks([0, 1], [f"{label}\n(n = {summary[status]['n_models']})"
                            for label, status in zip(labels, statuses)])
    axis.set_xlim(-0.5, 1.5)
    axis.set_ylabel("Chronos gene effect (lower = stronger growth defect)")
    axis.set_xlabel("Squares: medians; bars: interquartile ranges")
    axis.set_title(f"{gene} gene effect in {disease}")
    figure.tight_layout()
    figure.savefig(OUTPUT_PATH)
    plt.close(figure)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
