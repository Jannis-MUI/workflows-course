# Large-Scale Data Analysis and Workflows

Two practical sessions cover Linux, Git, Slurm, and tmux, followed by tidy data
preparation, parallel MCMC in R or Python, and workflows with Snakemake.

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

Compare gene dependency between lung adenocarcinoma (LUAD) and breast invasive
carcinoma (BRCA) models. Join model metadata to gene-effect scores and fit a
Bayesian linear regression by MCMC for each gene. The plot shows the estimated
LUAD minus BRCA difference and its 95% credible interval.

The R starter uses base R to read selected columns and prepare the data.
It uses rstanarm to fit the model.
The Python starter uses the standard-library CSV reader, NumPy, and PyMC.
Python plotting uses Matplotlib.

### Run

From the repository root, initialize the data, then enter `analysis/`:

```bash
make -C data check
cd analysis
```

This downloads the two required DepMap files into `data/` and verifies their checksums.
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

Processing writes `compare_dependency.tsv` with group counts and posterior
summaries for KRAS and PIK3CA. Plotting reads that table and writes
`plot_dependency.pdf`. Both scripts use these fixed names in the working directory.

### Exercises

1. [Scripts, tidy data, and parallel MCMC](analysis/EXERCISE_1-Scripts.md)
2. [Workflows](analysis/EXERCISE_2-Workflows.md)
