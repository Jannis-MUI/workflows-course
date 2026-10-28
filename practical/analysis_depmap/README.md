# Gene dependency and hotspot mutations in lung adenocarcinoma

Question: do LUAD models carrying a DepMap-annotated hotspot mutation in KRAS
have more negative KRAS knockout scores than models with no KRAS hotspot detected?

The reference solutions use ordinary indexing, loops, dictionaries, sets, and
base R joins. R needs no additional packages. Python data processing uses only
its standard library; plotting uses Matplotlib to write a PDF. Neither version
uses a tidy analysis library. Data processing and plotting are separate scripts
in each language.

## Run

Enter this directory first. From the repository root:

```bash
cd practical/analysis_depmap
```

Run the scripts from `analysis_depmap/`, with the downloaded data in the sibling
`data_depmap/` directory. Download and verify the four DepMap 24Q4 files first:

```bash
make -C ../data_depmap check

Rscript compare_dependency.r
Rscript plot_dependency.r

python3 compare_dependency.py
python3 plot_dependency.py
```

The gene (`KRAS`), disease (`LUAD`), and input/output paths are hardcoded near the
start of the processing scripts. Plotting paths are hardcoded near the start of
the plotting scripts. Edit these values to try a different gene or disease.
There is no command-line argument parser: adding one is part of the exercise.
The scripts assume the supplied DepMap files and their known column names.

Both implementations write the same two files directly in this directory:

| File | Contents |
| --- | --- |
| `compare_dependency.tsv` | Two rows: model counts, mean/median gene effect, quartiles, IQR, and available expression summaries per mutation group |
| `plot_dependency.pdf` | Group median gene effects and interquartile ranges, with model counts |

Processing writes only the table. Plotting reads that table and writes only the
PDF, without accessing raw data. Run either language; running the other version
replaces the same outputs. The table formats are interchangeable between the
plotting scripts. The median difference and inclusion counts are printed in the
terminal rather than saved in additional files.

The scripts are deliberately not executable. Invoke them with `Rscript` or
`python3` as shown above; adding execute permissions and running scripts directly
is part of the course.

## Processing steps and biological definitions

1. Read `Model.csv` and select the exact `OncotreeCode` `LUAD`. This excludes
   broader NSCLC classifications and any separately coded subtypes.
2. Read `OmicsSomaticMutations.csv` and select the chosen gene using `HugoSymbol`.
   Use DepMap's boolean `Hotspot` annotation to summarize variant rows into one
   mutation status per model. The classification uses the annotation, not a
   hand-maintained list of protein changes.
3. Classify a model as `hotspot` if any selected-gene variant has `Hotspot=True`.
   The supplied mutation table contains `True`/`False` flags. Collecting distinct
   model IDs ensures duplicate variant records do not add models.
4. A model with somatic records but no selected-gene hotspot is
   `no_hotspot_detected`. This includes models with annotated non-hotspot
   variants and models with no selected-gene variant record. Models absent
   from the whole mutation table are `no_mutation_data` and excluded.
5. Extract the chosen gene from both the gene-effect and expression matrices.
   Handle the unnamed first identifier column and preserve labels such as
   `KRAS (3845)`. Changing the gene constant changes mutation grouping,
   knockout measurements, expression, and output labels together.
6. Left-join by `ModelID`, never by row position. Include the `hotspot` and
   `no_hotspot_detected` groups when they have a measured gene effect. Missing
   expression does not exclude a model from the dependency comparison.
7. Summarize the two groups. Quartiles use R's type 7 / Python's inclusive
   interpolation. Expression is already `log2(TPM + 1)` and is not transformed
   again.

The `Hotspot` flag is supplied by DepMap, rather than by a gene-specific variant
list maintained in this repository. Its release-specific definition is described
in the [24Q4 mutation pipeline documentation](https://storage.googleapis.com/shared-portal-files/Tools/24Q4_Mutation_Pipeline_Documentation.pdf).
This gives the scripts a common classification rule across genes. The biological
interpretation still depends on the chosen gene: hotspot status is not a
universal gain-of-function classification. For a loss-of-function hypothesis,
DepMap's damaging annotations may be more appropriate.

The comparison group is **not confirmed wild type**. Having somatic variant
records establishes that some mutation data exist, but does not establish
sufficient coverage at the selected gene. The group may also contain non-hotspot
mutations. A stronger wild-type comparison requires independent genotype or
callability evidence. The analysis is descriptive and does not establish
causality, statistical significance, or sensitivity to a particular drug.

## Script exercises

1. **Permissions and shebangs.** Inspect the scripts' permissions, make the two
   scripts in your chosen language executable, and run them directly with
   `./compare_dependency.r` and `./plot_dependency.r` (or their Python versions).
   Explain how the shebang chooses the interpreter.
2. **Command-line arguments.** Replace the hardcoded gene, disease, data
   directory, and output table path with arguments. Give the plotting script
   arguments for its input table and output PDF. Preserve the current values as
   defaults. Keep both results for an analysis together, with the filenames
   `compare_dependency.tsv` and `plot_dependency.pdf`, creating output
   directories as needed.
3. **A second oncogene: PIK3CA.** Repeat the LUAD analysis for **PIK3CA**, changing
   the mutation grouping, gene-effect measurements, and expression together.
   PIK3CA has recurrent activating hotspot mutations and provides another
   oncogene-dependency question; its role in breast cancer is described in
   [Vasan et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7173400/).
   Compare the hotspot and reference group sizes and median differences with
   KRAS. Save the PIK3CA results separately so the KRAS results remain available.
4. **BRCA versus LUAD.** Run PIK3CA for both `BRCA` and `LUAD`, then compare the
   group counts, median gene effects, and within-disease median differences.
   Does the smaller hotspot group support the same strength of interpretation?
   Use the exact `OncotreeCode` values in `Model.csv`: `BRCA` selects that coded
   subset, while other breast models have separate codes such as `IDC` and
   `ILC`. Save each gene/disease combination in its own directory, for example
   `results/PIK3CA/BRCA/compare_dependency.tsv` and
   `results/PIK3CA/BRCA/plot_dependency.pdf`.

## Slurm exercises

Complete the argument and output-path exercises above before submitting several
analyses. Keep `analysis_depmap/` as the job working directory so the relative
input paths resolve as they did interactively.

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

## Workflow exercises

1. **Connect the scripts.** Create a `Snakefile` in `analysis_depmap/` for the
   KRAS/LUAD analysis. Define one rule that reads the four DepMap files and
   produces `compare_dependency.tsv`, and another that reads that table and
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
4. **Generalize with wildcards.** Add gene and disease wildcards and use the
   scripts' command-line arguments to run KRAS/LUAD, PIK3CA/LUAD, and PIK3CA/BRCA.
   Put the outputs in separate gene/disease directories, retaining the filenames
   `compare_dependency.tsv` and `plot_dependency.pdf`. Add all three PDFs as
   targets and allow independent calculations to run in parallel.
5. **Execute through Slurm.** With the Snakemake Slurm executor plugin installed,
   configure the course partition/account and each rule's CPU, memory, and
   runtime requirements. Run with `snakemake --executor slurm --jobs 3` and
   inspect the submitted jobs and logs. Let Snakemake submit the calculation and
   plotting commands directly instead of submitting the earlier batch wrappers
   from inside workflow jobs.

Cluster configuration is described in the
[Snakemake Slurm executor documentation](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html).
