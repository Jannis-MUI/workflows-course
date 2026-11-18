#!/usr/bin/env Rscript
# Use this fit unchanged throughout the exercise.
fit <- function(gene, rows, cohort) {
    model <- rstanarm::stan_glm(score ~ is_cohort, data = rows, chains = 2, cores = 1,
                               iter = 1000, seed = 42, refresh = 0)

    interval <- quantile(as.matrix(model)[, "is_cohort"], c(.025, .5, .975))
    data.frame(gene, cohort, n_luad = sum(rows$is_cohort == 0L), n_cohort = sum(rows$is_cohort),
               lower = interval[1L], median = interval[2L], upper = interval[3L])
}

genes <- c("KRAS", "PIK3CA")
cohort <- "BRCA"

models <- read.csv("../data/Model.csv")
models <- models[models$OncotreeCode %in% c("LUAD", cohort), c("ModelID", "OncotreeCode")]

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
rows$is_cohort <- as.integer(rows$OncotreeCode == cohort)

results <- data.frame()
for (gene in genes) {
    data <- na.omit(data.frame(is_cohort = rows$is_cohort, score = rows[[gene]]))
    results <- rbind(results, fit(gene, data, cohort))
}

write.table(results, "compare_dependency-BRCA.tsv", sep = "\t", row.names = FALSE)
