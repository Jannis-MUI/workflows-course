#!/usr/bin/env python3
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("compare_dependency.tsv", newline="") as source:
    rows = list(csv.DictReader(source, delimiter="\t"))

figure, axis = plt.subplots(figsize=(7, 4))
for i, row in enumerate(rows):
    lower, median, upper = (float(row[key]) for key in ("lower", "median", "upper"))
    axis.hlines(i, lower, upper, color="#2b6481")
    axis.plot(median, i, "o", color="#2b6481")
axis.axvline(color="0.65", linestyle="--")
axis.set_yticks(range(len(rows)), [row["gene"] for row in rows])
axis.invert_yaxis()
axis.set_xlabel("LUAD minus reference gene effect (95% credible interval)")
axis.set_title(f"LUAD vs {rows[0]['reference']}")
figure.tight_layout()
figure.savefig("plot_dependency.pdf")
