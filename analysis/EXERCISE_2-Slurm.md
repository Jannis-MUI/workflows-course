# Exercise 2: Slurm

Complete the argument and output-path tasks in
[Exercise 1: Scripts](EXERCISE_1-Scripts.md) before submitting several analyses.
Keep `analysis/` as the job working directory so the relative input paths
resolve as they did interactively. Activate the course software environment
before submission so the interpreter and packages are available to the jobs.

1. **Submit calculation.** Add `#SBATCH` directives directly to
   `compare_dependency.r` or `compare_dependency.py`. Keep the shebang on the
   first line and place the directives immediately below it, before any R or
   Python code (including the Python docstring). Request one CPU, memory, and a
   time limit. Set the working directory to the absolute path of `analysis/`
   and save a log whose filename includes the job ID (`%j`). Submit the script
   itself with `sbatch compare_dependency.r` or `sbatch compare_dependency.py`,
   record the job ID, and inspect it with `squeue`. Find the table and the log
   after it finishes.
2. **Inspect the job.** Use `sacct` to inspect its state, exit code, runtime, and
   peak memory use. Compare the observed use with the requested resources.
   Distinguish a successfully submitted job from a successfully completed job.
3. **Check calculation, then submit plotting.** Add `#SBATCH` directives below
   the shebang in `plot_dependency.r` or `plot_dependency.py` as well. Before
   submitting it, manually confirm that calculation finished successfully:
   inspect `sacct` for state `COMPLETED` and exit code `0:0`, read the log, and
   check that this run produced the expected `compare_dependency.tsv`. A job
   disappearing from `squeue` alone does not establish success. If calculation
   failed, fix it and rerun it first. Once the table is ready, submit the plotting
   script directly with `sbatch plot_dependency.r` or `sbatch plot_dependency.py`.
   Check its completion, log, and `plot_dependency.pdf`. The next exercise will
   use a workflow to automate the ordering of these steps.
4. **Run independent analyses.** Submit the calculation scripts directly for
   KRAS and PIK3CA in LUAD, plus PIK3CA in BRCA. Pass the gene, disease, and
   distinct output paths as arguments after the script filename. Monitor the
   jobs together; for each analysis, manually check successful calculation
   before submitting its plotting script. Check that tables, plots, and logs
   do not overwrite one another.

The relevant submission options are documented in the
[Slurm sbatch reference](https://slurm.schedmd.com/sbatch.html).
