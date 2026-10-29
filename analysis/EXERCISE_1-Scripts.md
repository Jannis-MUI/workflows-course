# Exercise 1: Scripts

Start with the setup and analysis description in the [main README](../README.md).
Run the scripts from `analysis/` and choose either R or Python.

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
5. **Rewrite with dplyr or pandas.** Rewrite `compare_dependency.r` using
   **dplyr**, or `compare_dependency.py` using **pandas**. Express the filtering,
   joins, grouping, and summaries with your chosen library. Keep the same
   command-line arguments, mutation definitions, missing-data handling, and
   output columns so the plotting script can still read the table. Save the
   original KRAS/LUAD summary before rewriting, rerun the calculation, and
   compare group counts and summary values, allowing for numeric rounding.
   Which parts become easier to read, and which still need care?
6. **Share your solution in a pull request.** Fork the original course
   repository if needed and create a branch for your rewrite. Replace the
   processing script at its existing path (`analysis/compare_dependency.r` or
   `analysis/compare_dependency.py`), commit it, and push the branch to your
   fork. Open a pull request against the original course repository, focused
   on that file. Describe the library you used, the main changes, and how you
   confirmed that the results agree. We will review the code in the different
   pull requests together and compare the approaches.
