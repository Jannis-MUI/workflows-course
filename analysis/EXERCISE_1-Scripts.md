# Exercise 1 — Tidy data and parallel MCMC

Follow the [main README](../README.md) to prepare the two input files. Work
from `analysis/` and choose either R or Python.

## 1. Establish a baseline

Inspect the starter, make it executable, and run it directly. Explain how its
shebang selects the interpreter. Save the TSV and render it with the plotting
script. The starter fits `score ~ is_luad` for KRAS and PIK3CA in LUAD and BRCA.
Each fit estimates the LUAD minus BRCA difference in mean gene effect. The TSV
has one row per gene with measured model counts and a posterior median and 95%
credible interval for the difference.

## 2. Rewrite the comparison with pandas or dplyr

Keep the supplied `fit()` function at the top of the script unchanged. Prepare
measured scores and their `is_luad` indicators for each gene before calling it.

1. Select `ModelID` and `OncotreeCode` from the metadata and just the requested
   gene columns from the wide matrix. Match by `ModelID` and filter to LUAD and
   the requested reference.
2. Reshape to one row per model and gene, omit missing scores, and group by gene
   for the fits. Check that the join preserves one row per model before reshaping.
3. Accept the reference and gene symbols on the command line.
   Compare the LUAD–BRCA result against the starter in your chosen language.
   Save a copy of the BRCA table before running LUAD–LUSC. Each run writes
   `compare_dependency.tsv` in the working directory.

## 3. Run one MCMC fit per worker

Use a serial loop first. Then dispatch the same function once per gene with
Dask processes or `clustermq::Q()`. For R, set
`options(clustermq.scheduler = "MULTIPROCESS")` in the R startup profile
to run local processes. Each fit uses one CPU. Run with one and two workers
and compare the elapsed time and the TSV contents. On Slurm, run the driver
and its local workers inside a CPU allocation with at least as many CPUs
as workers.

The solutions use `argparse`, pandas, Dask, and PyMC in
[Python](compare_dependency-solution.py), and `docopt`, dplyr, readr, tidyr,
clustermq, and rstanarm in [R](compare_dependency-solution.r). Both accept
`--workers` and an optional `--data-dir`. Use at most five workers for this
exercise.

```bash
python3 compare_dependency-solution.py --workers=2 BRCA KRAS PIK3CA
Rscript compare_dependency-solution.r --workers=2 BRCA KRAS PIK3CA
```

## 4. Submit the comparison and its plot

Write a Bash launcher that submits the starter with one CPU, captures its
job ID with `sbatch --parsable`, and immediately submits plotting with
`--dependency=afterok:<job-id>`. Run both jobs from `analysis/` and use
separate log names with `%j`. Verify the outcomes with `sacct`. The supplied
Python example runs with `bash submit_dependency_solution.sh` from
`analysis/`.
[Submission script](submit_dependency_solution.sh) ·
[Slurm sbatch reference](https://slurm.schedmd.com/sbatch.html)
