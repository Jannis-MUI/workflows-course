# Exercise 3: Workflows

Start by completing the supplied [Snakefile](Snakefile), which is a commented
template with no rules defined yet. Use only the single KRAS/LUAD case and
the two outputs `compare_dependency.tsv` and `plot_dependency.pdf`.
Use the command-line arguments added in the Scripts exercise, keeping KRAS
and LUAD as the script defaults.

Run Snakemake from `analysis/`. For the initial exercises, download and verify
the inputs with `make -C ../data check`. Exercise 5 will bring downloading into
the workflow itself.

1. **Connect the scripts.** Complete the supplied `Snakefile` in
   `analysis/`, choosing either the R or Python scripts. Define one rule
   that reads the four DepMap files and produces `compare_dependency.tsv`,
   and another that reads that table and
   produces `plot_dependency.pdf`. Include the corresponding script as an
   input to each rule so script changes trigger the appropriate work. Make the
   PDF the final target. Use named inputs to distinguish raw data from the
   script itself. Pass the declared input/output paths (or their data
   directory) through the scripts' command-line arguments, using Snakemake's
   `input` and `output` placeholders where appropriate. Keep KRAS/LUAD as the defaults.
   Check that the paths in the rule declarations match the files actually
   read and written by the scripts.
2. **Preview and run locally.** Move the manually generated table and PDF aside
   so the workflow can create them. Inspect a dry run with
   `snakemake --dry-run --cores 1`, then execute with `snakemake --cores 1`.
   Run it again and explain why no steps need to execute.
3. **Explore dependencies.** Delete the PDF and rerun: only plotting should run.
   Change the plotting script: only plotting should run. Change the calculation
   script: calculation and plotting should run. Explain the input/output
   dependencies behind each outcome.

   **Failure and recovery.** Move the table and PDF aside, then temporarily
   make the calculation rule's shell command exit with a nonzero status.
   Run the workflow and inspect the error. Confirm that plotting does not
   start. Restore the command, rerun, and check that both outputs are produced.
   Explain how this differs from a command that succeeds but writes incorrect
   results.
4. **Use blocking sbatch inside the rules.** Change each rule's shell command
   to submit its R or Python script with `sbatch --wait`, using the `#SBATCH`
   directives you added in the Slurm exercise. Keep Snakemake running locally
   and force both steps to rerun with `snakemake --cores 2 --forceall`. Monitor
   the jobs and their logs. Confirm that plotting starts only after calculation
   finishes successfully. Explain why plain `sbatch` would return too early,
   and how `--wait` passes a failed job's exit status back to Snakemake. Compare
   this with manually checking completion and submitting the next script.
   Repeat with `--cores 4`. Does this change which jobs can run at the same
   time, or how many CPUs each Slurm job receives? Discuss the dependency
   between calculation and plotting, Snakemake's local execution slots, and
   the resource requests in the scripts' `#SBATCH` directives.
5. **Add downloading as a module.** Create `data/Snakefile` with rules to
   download the four DepMap CSV files. Use the URLs in `data/Makefile` and
   verify each download against the existing `data/md5sums.txt` as part of
   producing the file. Include the checksum file as an input and make a
   checksum mismatch fail the rule.

   Use unprefixed filenames in the module, such as `Model.csv` and
   `md5sums.txt`, so it can run on its own from `data/`. Import its rules into
   `analysis/Snakefile` using `module` and `use rule`, with
   `prefix: "../data"`. Distinguish the path locating the module's Snakefile
   from its input/output paths, which resolve against the working directory.
   Check that the imported outputs match the `../data/` analysis inputs. Keep
   the PDF as the final target, connecting downloading, verification,
   calculation, and plotting in one workflow. Inspect a forced dry run to see
   the complete chain, then run it, reusing existing data where possible.

   **When are checksums checked?** Verification inside a download rule runs
   when that rule executes; it does not automatically recheck an existing,
   up-to-date CSV. Explain this distinction. Temporarily use an incorrect
   expected hash for only `Model.csv` and force only that download rule to
   rerun. Confirm that verification fails, then restore the correct expectation
   and retry. Keep the reference `md5sums.txt` unchanged and avoid redownloading
   the large matrices for this experiment. Optionally, investigate Snakemake's
   `ensure(..., md5=...)` as an alternative to a checksum shell command.

   **Should downloading be a Slurm job?** Discuss network access on compute
   nodes, queueing overhead, resource needs, and the course cluster's policy
   for downloads on the submission host. For this exercise, mark the download
   rules, including verification, as local with `localrules`, using the imported
   rule names. They should run on the host running Snakemake, including when the
   analysis rules use a cluster executor.

   **Optional: independent work.** When downloads are needed, compare
   `--cores 2` with `--cores 4`. Which download rules can run concurrently,
   unlike calculation and plotting? Use dry runs to plan this comparison and
   avoid repeatedly downloading the large files just to change concurrency.
6. **Use the Slurm executor.** Install the Snakemake Slurm executor plugin and
   restore the calculation and plotting rules' shell commands to run their
   scripts with `Rscript` or `python3`, passing their input/output arguments.
   Set CPU, memory, and runtime requests in those rules using `threads`,
   `mem_mb`, and `runtime` (minutes). The supplied scripts use one CPU; asking
   for more does not make them parallel. Supply the course account and
   partition with `--default-resources slurm_account=<account>
   slurm_partition=<partition>` when running
   `snakemake --executor slurm --jobs 1`. The executor submits the rule
   commands; the R/Python scripts' `#SBATCH` comments no longer request
   resources. Move only the table and PDF aside to rerun these steps. Inspect
   jobs and logs, and use `sacct` to compare the allocations with the rule
   settings. Calculation and plotting should be Slurm jobs, while needed
   downloads and verification stay local. Keep downloaded data in place.

   Discuss the advantages over embedding `sbatch --wait` in the rules: resource
   requests are managed by Snakemake and the executor tracks remote jobs
   directly. The same rule commands can also run locally by changing the
   execution settings. Both
   approaches already enforce the calculation-to-plotting order; what does the
   executor add? Why would increasing `--jobs` alone not make this two-step
   chain run in parallel?
7. **Create and use a profile.** Create `analysis/profiles/slurm/config.yaml`.
   Reproduce the previous run's settings through this profile: executor,
   maximum concurrent jobs, account, partition, CPU, memory, and runtime.
   Investigate `default-resources`, `set-resources`, and `set-threads` to keep
   appropriate differences between calculation and plotting. Remove the
   corresponding resource settings from the rules for this experiment.
   From `analysis/`, run `snakemake --profile profiles/slurm --dry-run`, then
   move only the table and PDF aside and run
   `snakemake --profile profiles/slurm`. Confirm with `sacct` that the profile
   produces the intended allocations and that downloads remain local.

   **What belongs in the profile, and what belongs in a rule?** Discuss site
   settings such as account and partition, execution settings such as the
   executor and job limit, and requirements intrinsic to a particular step.
   Should calculation and plotting have the same memory and runtime? Where
   should a tool's thread count or memory requirements that scale with input
   size be recorded? A profile can hold site defaults and deployment-specific
   overrides; rules can express the workflow's own resource requirements.
   Decide which settings you would keep in each place after this experiment,
   and explain how the choice helps someone run the workflow on another
   cluster or locally.

Blocking submission is described in the
[Slurm sbatch reference](https://slurm.schedmd.com/sbatch.html#OPT_wait).
See the Snakemake documentation on
[modules](https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html#modules)
and [local rules](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#local-rules)
for the download exercise.
Output checks are described under
[ensuring output properties](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#ensuring-output-file-properties-like-non-emptyness-or-checksum-compliance).
Executor configuration is described in the
[Snakemake Slurm executor documentation](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html).
See also the documentation on
[profiles](https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles).
