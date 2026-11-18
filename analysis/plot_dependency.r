#!/usr/bin/env Rscript
rows <- read.delim("compare_dependency.tsv")
y <- rev(seq_len(nrow(rows)))

pdf("plot_dependency.pdf", height = 4)
par(mar = c(5, 6, 3, 1))
plot(rows$median, y, type = "n", yaxt = "n", ylab = "",
     xlim = range(0, rows$lower, rows$upper), ylim = c(0.5, max(y) + 0.5),
     xlab = "LUAD minus reference gene effect (95% credible interval)",
     main = paste("LUAD vs", rows$reference[1L]))
axis(2, at = y, labels = rows$gene, las = 1)
abline(v = 0, lty = 2, col = "grey65")
segments(rows$lower, y, rows$upper, y, col = "#2b6481", lwd = 2)
points(rows$median, y, pch = 19, col = "#2b6481")
invisible(dev.off())
