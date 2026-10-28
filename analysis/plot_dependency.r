#!/usr/bin/env Rscript
# Plot group medians and IQRs with R's built-in PDF graphics device.
# Edit these paths for now. Adding command-line arguments is an exercise.
# Run this script from analysis/.
input_path <- "compare_dependency.tsv"
output_path <- "plot_dependency.pdf"

summary <- read.delim(input_path, check.names = FALSE, stringsAsFactors = FALSE)
statuses <- c("hotspot", "no_hotspot_detected")
summary <- summary[match(statuses, summary$mutation_status), , drop = FALSE]
gene <- summary$gene[1]
disease <- summary$disease[1]

pdf(output_path, width = 9, height = 6)
par(mar = c(5, 5, 3, 1))
limits <- range(c(summary$q1_effect, summary$q3_effect, -1, 0))
plot(NA, xlim = c(0.5, 2.5), ylim = limits + c(-0.15, 0.15), xaxt = "n", xlab = "",
     ylab = "Chronos gene effect (lower = stronger growth defect)",
     main = paste(gene, "gene effect in", disease))
abline(h = c(-1, 0), col = "grey80", lty = 2)
colors <- c("#bd4d38", "#38769c")
arrows(1:2, summary$q1_effect, 1:2, summary$q3_effect,
       angle = 90, code = 3, length = 0.08, lwd = 3, col = colors)
points(1:2, summary$median_effect, pch = 15, cex = 1.3, col = colors)
axis(1, at = 1:2, labels = paste0(c(paste(gene, "hotspot"), paste("No", gene, "hotspot detected")),
                                  "\n(n = ", summary$n_models, ")"))
mtext("Squares: medians; bars: interquartile ranges", side = 1, line = 3.5, cex = 0.8)
invisible(dev.off())
cat("Wrote", output_path, "\n")
