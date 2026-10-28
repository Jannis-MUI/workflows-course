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

## Exercises

Work through the exercises in order, using either the R or Python scripts:

1. [Scripts](EXERCISE_1-Scripts.md): permissions, command-line arguments, PIK3CA,
   and BRCA versus LUAD.
2. [Slurm](EXERCISE_2-Slurm.md): submit calculation and plotting jobs, inspect
   resources, and run independent analyses.
3. [Workflows](EXERCISE_3-Workflows.md): complete the Snakefile for KRAS/LUAD,
   explore dependencies, and run through Slurm.
