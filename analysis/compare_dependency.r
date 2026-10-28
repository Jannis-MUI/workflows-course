#!/usr/bin/env Rscript
# Gene hotspot / dependency exercise, using only packages shipped with R.

# Edit these values for now. Adding command-line arguments is an exercise.
# Run this script from analysis/.
gene <- "KRAS"
disease <- "LUAD"
data_dir <- "../data"
output_path <- "compare_dependency.tsv"

read_gene <- function(path, gene, value_name) {
    # Read the header without changing gene labels such as 'KRAS (3845)'.
    header <- names(read.csv(path, nrows = 0, check.names = FALSE))
    symbols <- sub(" \\([^()]+\\)$", "", header)
    column <- which(symbols == gene)
    classes <- rep("NULL", length(header))
    classes[1] <- "character"
    classes[column] <- "numeric"
    result <- read.csv(path, colClasses = classes, check.names = FALSE)
    names(result) <- c("ModelID", value_name)
    result
}

# 1. Filter metadata to a single disease.
models <- read.csv(file.path(data_dir, "Model.csv"), check.names = FALSE,
                   colClasses = "character", na.strings = c("", "NA"))
models <- models[, c("ModelID", "CellLineName", "OncotreeCode")]
cohort <- models[!is.na(models$OncotreeCode) & models$OncotreeCode == disease, , drop = FALSE]

# 2. Summarize many variant rows into one genotype record per model.
mutation_path <- file.path(data_dir, "OmicsSomaticMutations.csv")
header <- names(read.csv(mutation_path, nrows = 0, check.names = FALSE))
columns <- c("ModelID", "HugoSymbol", "Hotspot")
classes <- rep("NULL", length(header))
classes[header %in% columns] <- "character"
mutations <- read.csv(mutation_path, colClasses = classes, check.names = FALSE,
                      na.strings = c("", "NA"))
mutations <- mutations[mutations$ModelID %in% cohort$ModelID, columns, drop = FALSE]
profiled <- unique(mutations$ModelID) # Evidence of some somatic data, not gene-level callability.
gene_calls <- mutations[!is.na(mutations$HugoSymbol) & mutations$HugoSymbol == gene, , drop = FALSE]
hotspot_models <- unique(gene_calls$ModelID[gene_calls$Hotspot == "True"])
rm(mutations)

genotypes <- data.frame(ModelID = cohort$ModelID, mutation_status = "no_mutation_data")
for (i in seq_len(nrow(genotypes))) {
    model <- genotypes$ModelID[i]
    if (model %in% hotspot_models) {
        genotypes$mutation_status[i] <- "hotspot"
    } else if (model %in% profiled) {
        genotypes$mutation_status[i] <- "no_hotspot_detected"
    }
}

# 3. Extract measurements, then left-join by ID rather than row position.
effects <- read_gene(file.path(data_dir, "CRISPRGeneEffect.csv"), gene, "gene_effect")
expression <- read_gene(file.path(data_dir, "OmicsExpressionProteinCodingGenesTPMLogp1.csv"),
                        gene, "log2_tpm_plus_1")
joined <- merge(cohort, genotypes, by = "ModelID", all.x = TRUE)
joined <- merge(joined, effects, by = "ModelID", all.x = TRUE)
joined <- merge(joined, expression, by = "ModelID", all.x = TRUE)

# 4. Filter and summarize; expression missingness does not exclude a model.
statuses <- c("hotspot", "no_hotspot_detected")
included <- joined[joined$mutation_status %in% statuses & !is.na(joined$gene_effect), , drop = FALSE]
groups <- list()
summaries <- list()
for (status in statuses) {
    selected <- included[included$mutation_status == status, , drop = FALSE]
    values <- selected$gene_effect
    expressed <- selected$log2_tpm_plus_1[!is.na(selected$log2_tpm_plus_1)]
    groups[[status]] <- values
    quartiles <- quantile(values, c(0.25, 0.75), type = 7, names = FALSE)
    summaries[[status]] <- data.frame(gene = gene, disease = disease,
        mutation_status = status, n_models = length(values), mean_effect = mean(values),
        median_effect = median(values), q1_effect = quartiles[1], q3_effect = quartiles[2],
        iqr_effect = diff(quartiles), n_expression = length(expressed),
        median_log2_tpm_plus_1 = median(expressed))
}
summary <- do.call(rbind, summaries)
difference <- median(groups$hotspot) - median(groups$no_hotspot_detected)

# 5. Save just the group summary; report the contrast in the terminal.
write.table(summary, output_path, sep = "\t", quote = TRUE,
            row.names = FALSE, na = "NA")
cat(sprintf("%d/%d models included; median difference = %.4f\n",
            nrow(included), nrow(joined), difference))
cat("Wrote", output_path, "\n")
cat("Reference: no", gene, "hotspot detected in a profiled model; not confirmed wild type.\n")
