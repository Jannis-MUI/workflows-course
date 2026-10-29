# Large-Scale Data Analysis and Workflows

Two practical sessions: a refresher on Linux, Git, Slurm, and tmux, followed by
R/Python scripting and reproducible workflows with Snakemake.

## Get started

Clone the repository on the course server and inspect its contents:

```bash
git clone https://github.com/mschubert/workflows-course.git
cd workflows-course
tree .
```

Start with the [warmup exercises](warmup/README.md), then continue with the
DepMap analysis and exercises below.

## DepMap analysis

[DepMap](https://depmap.org/portal/) (Cancer Dependency Map) is a public resource
that identifies genes cancer cells depend on for growth and survival.
It studies cancer cell lines: cells derived from tumors and grown in the
laboratory as models of different cancers.
CRISPR knockout screens disable individual genes and measure the effect on
cell growth.
A gene is a dependency when its loss reduces growth or survival, with
[more negative gene-effect scores](https://forum.depmap.org/t/dependent-cell-line-list/366)
indicating stronger dependency.

Compare KRAS knockout scores in lung adenocarcinoma (LUAD) models grouped by
DepMap's hotspot mutation annotation. The analysis joins model metadata,
somatic mutations, gene effects, and expression data, then summarizes and plots
the groups.

There are separate processing and plotting scripts for R and Python. R uses
base R; Python processing uses its standard library and plotting uses Matplotlib.

### Run

From the repository root, initialize the data, then enter `analysis/`:

```bash
make -C data check
cd analysis
```

This downloads the four DepMap files into `data/` and verifies their checksums.
Run the scripts from `analysis/`, choosing either R:

```bash
Rscript compare_dependency.r
Rscript plot_dependency.r
```

or Python:

```bash
python3 compare_dependency.py
python3 plot_dependency.py
```

Processing writes `compare_dependency.tsv`, containing group counts and summary
statistics. Plotting reads that table and writes `plot_dependency.pdf`. Both
files are saved in `analysis/`.

### Exercises

1. [Scripts](analysis/EXERCISE_1-Scripts.md)
2. [Slurm](analysis/EXERCISE_2-Slurm.md)
3. [Workflows](analysis/EXERCISE_3-Workflows.md)
