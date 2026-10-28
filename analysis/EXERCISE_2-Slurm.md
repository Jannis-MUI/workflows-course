# Exercise 2: Slurm

Complete the argument and output-path tasks in
[Exercise 1: Scripts](EXERCISE_1-Scripts.md) before submitting several analyses.
Keep `analysis/` as the job working directory so the relative input paths
resolve as they did interactively.

1. **Submit calculation.** Write a Bash batch script that runs the calculation
   script in your chosen language. Request one CPU, memory, and a time limit
   with `#SBATCH` directives. Set the working directory explicitly, use the
   course software environment, and save a log whose filename includes the job
   ID (`%j`). Submit it with `sbatch`, record the job ID, and inspect it with
   `squeue`. Find the table and the log after it finishes.
2. **Inspect the job.** Use `sacct` to inspect its state, exit code, runtime, and
   peak memory use. Compare the observed use with the requested resources.
   Distinguish a successfully submitted job from a successfully completed job.
3. **Submit plotting separately.** Write a second batch script for plotting.
   Submit it with `--dependency=afterok:<calculation_job_id>` so it starts after
   successful calculation. Check that it reads `compare_dependency.tsv` and
   produces `plot_dependency.pdf`. Inspect the logs, and explain what happens
   to the plotting job if calculation fails.
4. **Run independent analyses.** Submit calculation and dependent plotting jobs
   for KRAS and PIK3CA in LUAD, plus PIK3CA in BRCA. Pass the gene, disease, and
   distinct output paths as arguments. Monitor the jobs together and check that
   their tables, plots, and logs do not overwrite one another.

The relevant submission options are documented in the
[Slurm sbatch reference](https://slurm.schedmd.com/sbatch.html).
