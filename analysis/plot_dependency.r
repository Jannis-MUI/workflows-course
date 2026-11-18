#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly = TRUE)
suffix <- if (length(args) > 0) paste0("-", args[1]) else ""

rows <- read.delim(paste0("compare_dependency", suffix, ".tsv"))
cohort <- rows$cohort[1L]
y <- rev(seq_len(nrow(rows)))

pdf(paste0("plot_dependency", suffix, ".pdf"), height = 4)
par(mar = c(5, 6, 3, 1))
plot(rows$median, y, type = "n", yaxt = "n", ylab = "",
     xlim = range(0, rows$lower, rows$upper), ylim = c(0.5, max(y) + 0.5),
     xlab = paste(cohort, "minus LUAD gene effect (95% credible interval)"),
     main = paste(cohort, "vs LUAD"))
axis(2, at = y, labels = rows$gene, las = 1)
abline(v = 0, lty = 2, col = "grey65")
segments(rows$lower, y, rows$upper, y, col = "#2b6481", lwd = 2)
points(rows$median, y, pch = 19, col = "#2b6481")
invisible(dev.off())
