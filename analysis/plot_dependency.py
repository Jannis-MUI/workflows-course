#!/usr/bin/env python3
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("cohort")
cohort = parser.parse_args().cohort

with open(f"compare_dependency-{cohort}.tsv", newline="") as source:
    rows = list(csv.DictReader(source, delimiter="\t"))
cohort = rows[0]["cohort"]

figure, axis = plt.subplots(figsize=(7, 4))
for i, row in enumerate(rows):
    lower, median, upper = (float(row[key]) for key in ("lower", "median", "upper"))
    axis.hlines(i, lower, upper, color="#2b6481")
    axis.plot(median, i, "o", color="#2b6481")
axis.axvline(color="0.65", linestyle="--")
axis.set_yticks(range(len(rows)), [row["gene"] for row in rows])
axis.invert_yaxis()
axis.set_xlabel(f"{cohort} minus LUAD gene effect (95% credible interval)")
axis.set_title(f"{cohort} vs LUAD")
figure.tight_layout()
figure.savefig(f"plot_dependency-{cohort}.pdf")
