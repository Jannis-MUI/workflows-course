# DepMap 24Q4 Public, version 1:
# https://doi.org/10.25452/figshare.plus.27993248.v1
# Keep the reference checksums in md5sums.txt independent of the downloads.

FILES := Model.csv CRISPRGeneEffect.csv OmicsExpressionProteinCodingGenesTPMLogp1.csv

.PHONY: all check
.DELETE_ON_ERROR:

all: $(FILES)

Model.csv:
	curl --fail --location --retry 3 --output $@ https://ndownloader.figshare.com/files/51065297

CRISPRGeneEffect.csv:
	curl --fail --location --retry 3 --output $@ https://ndownloader.figshare.com/files/51064667

OmicsExpressionProteinCodingGenesTPMLogp1.csv:
	curl --fail --location --retry 3 --output $@ https://ndownloader.figshare.com/files/51065489

check: $(FILES) md5sums.txt
	md5sum --check md5sums.txt
