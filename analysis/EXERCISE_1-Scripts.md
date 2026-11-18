# Exercise 1 — Tidy data and parallel MCMC

Follow the [main README](../README.md) to prepare the two input files. Work
from `analysis/` and choose either R or Python.

How does dependency on KRAS and PIK3CA differ between lung adenocarcinoma
(LUAD) and breast invasive carcinoma (BRCA) models? DepMap measures cell
growth after knocking out each gene. More negative gene-effect scores
indicate a larger growth defect and stronger dependency on that gene.

## 1. Establish a baseline

The starter comparison scripts are [compare_dependency.py](compare_dependency.py)
for Python and [compare_dependency.r](compare_dependency.r) for R.

Inspect the starter, make it executable, and run it directly. Explain how its
shebang selects the interpreter. Save the TSV and render it with the plotting
script. The starter fits `score ~ is_cohort` for KRAS and PIK3CA with LUAD as the
baseline. Each fit estimates the BRCA minus LUAD difference in mean gene
effect. The TSV has one row per gene with measured model counts and a
posterior median and 95% credible interval for the difference.

## 2. Rewrite the comparison with pandas or dplyr

Keep the supplied `fit()` function at the top of the script unchanged. Prepare
measured scores and their `is_cohort` indicators for each gene before calling it.

1. Select `ModelID` and `OncotreeCode` from the metadata and just the requested
   gene columns from the wide matrix. Match by `ModelID` and filter to LUAD and
   the requested comparison cohort.
2. Reshape to one row per model and gene, omit missing scores, and group by gene
   for the fits. Check that the join preserves one row per model before reshaping.
3. Accept the comparison cohort's `OncotreeCode` followed by the gene symbols.
   Use `argparse` in Python or `docopt` in R. Code LUAD as `is_cohort = 0` and
   the comparison cohort as `is_cohort = 1`. Use `BRCA` to check your results
   against the starter, then use `LUSC` to compare lung squamous cell
   carcinoma against LUAD. Put the comparison cohort code before the extension,
   as in `compare_dependency-BRCA.tsv`.

## 3. Run one MCMC fit per worker

Use a serial loop first. Then dispatch the same function once per gene with
Dask processes or `clustermq::Q()`. Add a `--workers` argument and run with one
and two workers. Compare the elapsed time and the TSV contents. Each fit uses
one CPU. On Slurm, request at least as many CPUs as workers. Use at most five
workers for this exercise.

Run your revised comparison script and pass the same cohort code to the
plot script.

```bash
python3 compare_dependency.py --workers=2 BRCA KRAS PIK3CA
python3 plot_dependency.py BRCA

Rscript compare_dependency.r --workers=2 BRCA KRAS PIK3CA
Rscript plot_dependency.r BRCA
```

## 4. Submit the comparison and its plot

Write a Bash launcher that submits the starter with one CPU, captures its
job ID with `sbatch --parsable`, and immediately submits plotting with
`--dependency=afterok:<job-id>`. Run both jobs from `analysis/` and use
separate log names with `%j`. Verify the outcomes with `sacct`.
[Slurm sbatch reference](https://slurm.schedmd.com/sbatch.html)
