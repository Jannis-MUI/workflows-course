# Exercise 3: Workflows

Start by completing the supplied [Snakefile](Snakefile), which is a commented
template with no rules defined yet. Use only the single KRAS/LUAD case and
the two outputs `compare_dependency.tsv` and `plot_dependency.pdf`.
Keep KRAS and LUAD as the script defaults if you have added command-line
arguments in the earlier exercises.

Run Snakemake from `analysis_depmap/`. Download and verify the inputs first
with `make -C ../data_depmap check`.

1. **Connect the scripts.** Complete the supplied `Snakefile` in
   `analysis_depmap/`, choosing either the R or Python scripts. Define one rule
   that reads the four DepMap files and produces `compare_dependency.tsv`,
   and another that reads that table and
   produces `plot_dependency.pdf`. Include the corresponding script as an
   input to each rule so script changes trigger the appropriate work. Make the
   PDF the final target.
2. **Preview and run locally.** Move the manually generated table and PDF aside
   so the workflow can create them. Inspect a dry run with
   `snakemake --dry-run --cores 1`, then execute with `snakemake --cores 1`.
   Run it again and explain why no steps need to execute.
3. **Explore dependencies.** Delete the PDF and rerun: only plotting should run.
   Change the plotting script: only plotting should run. Change the calculation
   script: calculation and plotting should run. Explain the input/output
   dependencies behind each outcome.
4. **Execute through Slurm.** With the Snakemake Slurm executor plugin installed,
   configure the course partition/account and each rule's CPU, memory, and
   runtime requirements. Run with `snakemake --executor slurm --jobs 1` and
   inspect the submitted jobs and logs. Let Snakemake submit the calculation and
   plotting commands directly instead of submitting the earlier batch wrappers
   from inside workflow jobs.

Cluster configuration is described in the
[Snakemake Slurm executor documentation](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html).
