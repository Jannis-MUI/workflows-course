mkdir -p bio-prac/{data/{raw,meta},results,analysis}
cd bio-prac

cat > data/raw/tiny.fastq << 'EOF'
@read1
ACGTAGATCGGAAGAGCAGT
+
IIIIIIIIIIIIIIIIIIIII
@read2
NNNNACGTACGTACGTACGT
+
####IIIIIIIIIIIIIIIII
@read3
ACGTACGTACGT
+
IIIIIIIIIIII
@read4
TTTTAGATCGGAAGAGTTTT
+
IIIIIIIIIIIIIIIIIIII
@read5
ACGTACGTNACGT
+
IIIIIIII#IIIII
@read6
GATCGTCGGTCTCGTAG
+
IIIIIIIIIIIIIIIII
EOF

cat > data/meta/samples.tsv << 'EOF'
sample_id	condition	replicate	fastq
S1	A	1	raw/run1_S1.fastq
S2	A	2	raw/run1_S2.fastq
S3	B	1	raw/run1_S3.fastq
S4	B	2	raw/run1_S4.fastq
S5	B	3	raw/run1_S3.fastq
S6	A	3	raw/run1_S2.fastq
EOF

cat > data/raw/tiny.vcf << 'EOF'
##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	100	.	A	G	.	.	.
chr1	250	.	T	C	.	.	.
chr2	300	.	G	GA	.	.	.
chrM	400	.	C	T	.	.	.
EOF

tar -czf bio-prac.tar.gz bio-prac
