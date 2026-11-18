#!/usr/bin/env Rscript
# Use this fit unchanged throughout the exercise.
fit <- function(gene, rows, reference) {
    model <- rstanarm::stan_glm(score ~ is_luad, data = rows, chains = 2, cores = 1,
                               iter = 1000, seed = 42, refresh = 0)

    interval <- quantile(as.matrix(model)[, "is_luad"], c(.025, .5, .975))
    data.frame(gene, reference, n_luad = sum(rows$is_luad), n_reference = sum(rows$is_luad == 0L),
               lower = interval[1L], median = interval[2L], upper = interval[3L])
}

genes <- c("KRAS", "PIK3CA")
reference <- "BRCA"

models <- read.csv("../data/Model.csv")
models <- models[models$OncotreeCode %in% c("LUAD", reference), c("ModelID", "OncotreeCode")]

effects_path <- "../data/CRISPRGeneEffect.csv"
header <- strsplit(readLines(effects_path, n = 1), ",")[[1]]
symbols <- sub(" \\(.*$", "", gsub('"', "", header))
# In colClasses, "NULL" skips a column.
types <- rep("NULL", length(header))
types[1] <- "character"
types[symbols %in% genes] <- "numeric"
effects <- read.csv(effects_path, colClasses = types, check.names = FALSE)
names(effects) <- c("ModelID", sub(" \\(.*$", "", names(effects)[-1]))

rows <- merge(effects, models, by = "ModelID", sort = FALSE)
rows$is_luad <- as.integer(rows$OncotreeCode == "LUAD")

results <- data.frame()
for (gene in genes) {
    data <- na.omit(data.frame(is_luad = rows$is_luad, score = rows[[gene]]))
    results <- rbind(results, fit(gene, data, reference))
}

write.table(results, "compare_dependency.tsv", sep = "\t", row.names = FALSE)
