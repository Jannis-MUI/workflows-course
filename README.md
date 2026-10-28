# Large-Scale Data Analysis and Workflows

Two hands-on sessions on working at the Linux command line, using shared compute resources, and turning analyses into reproducible workflows. Participants should have some prior command-line and programming experience; the first session refreshes and consolidates those skills.

The sessions do not need to be equally long. Session 1 covers a broader set of tools, while session 2 focuses on developing one analysis from a script into a workflow. Time spent on each topic can be adjusted to participants' experience and progress through the exercises.

## Session 1: Linux command line, Git, Slurm, and tmux

Presentation: [1_bash-git-slurm.pptx](1_bash-git-slurm.pptx)

By the end of this session, participants should be able to work on a remote Linux server, track their scripts with Git, and run and monitor jobs through Slurm while using tmux to manage terminal sessions.

### Linux and Bash refresher

- Connect to a remote server with SSH and transfer files with `scp` or `rsync`.
- Navigate the filesystem, use relative and absolute paths, and find command help.
- Inspect, create, copy, move, and remove files; extract archives and compress or decompress data.
- Edit files with `nano` or Vim.
- Inspect and transform text with commands such as `head`, `tail`, `wc`, `grep`, `sed`, `sort`, and `column`.
- Combine commands using pipes, wildcards, and input/output redirection.
- Use variables, command substitution, shell arithmetic, aliases, tab completion, and command history.
- Understand file permissions, executable scripts, `$PATH`, and shell configuration in `~/.bashrc`.
- Write small Bash scripts with arguments, conditionals, and loops.

**Practice (exercises 1–2):** Transfer and extract the practice archive, explore its directories, compress and inspect a VCF file, display a sample sheet as a table, and extract and sort FASTQ read names. Convert a TSV file to CSV, create an executable script that accepts an argument, and configure useful aliases.

### Processes and persistent terminals with tmux

- Understand standard input, standard output, and standard error.
- Interrupt, suspend, resume, and background commands; inspect and terminate processes.
- Recognize the roles of `nohup` and `disown` when disconnecting from a server.
- Create tmux sessions, split windows into panes, and detach and reattach to keep terminal work available across SSH connections.

**Practice:** Start a tmux session, arrange multiple panes, disconnect, and reconnect to the session.

### Version control with Git

- Initialize a repository and inspect the working tree with `git status`.
- Stage selected changes, review staged differences, and create commits.
- Use `.gitignore` to keep raw data and generated files out of version control.
- Inspect commit history and check author information.
- Create branches, make changes, and merge them back into the main development branch.

**Practice (exercise 3):** Put the practice project's scripts under version control, exclude raw data, review and commit changes, and try a branch-and-merge cycle.

### Cluster computing with Slurm

- Understand how a scheduler allocates resources on shared compute nodes.
- Inspect partitions and jobs with `sinfo` and `squeue`.
- Request interactive resources with `salloc`, launch commands with `srun`, and submit batch scripts with `sbatch`.
- Specify tasks, CPUs per task, memory, runtime, and partition using command-line options or `#SBATCH` directives.
- Monitor processes and CPU use, and relate requested resources to the commands actually running.

**Practice (exercise 4):** Use tmux panes to allocate resources, inspect the queue, and monitor a compute node. Run and stop a simulated CPU-intensive command, explore resource limits and multiple processes, and submit a small script with `srun` and `sbatch`.

The session also introduces convenient Bash, tmux, and SSH configuration.

## Session 2: Scripts and workflows

Presentation: [2_scripts_workflows.pptx](2_scripts_workflows.pptx)

By the end of this session, participants should be able to write an analysis script with configurable inputs and outputs, organize its files, and connect analysis and plotting steps in a reproducible Snakemake workflow.

### From interactive analysis to scripts

- Run Bash, R, and Python scripts using an appropriate shebang and executable permissions.
- Submit scripts through Slurm, specify resources, and capture output in log files.
- Perform an analysis in either R or Python, save a results table, and produce a plot.
- Introduce tidy data operations in R: selecting, filtering, transforming, grouping, summarizing, sorting, and joining tables.
- Replace hardcoded paths and parameters with command-line arguments, using tools such as `docopt` or Python's `argparse`.
- Separate input data, analysis code, and generated results; split calculation and plotting into reusable scripts.

**Practice (exercises 5–6):** Use the `nycflights13` data to identify the ten destination airports with the highest average arrival delay among flights lasting 4–12 hours. Report each airport's full name, coordinates, average delay, and the number of flights contributing to that average. Save the results and a simple plot, then adapt the scripts to accept input and output paths as arguments.

### Reproducible workflows with Snakemake

- Describe analysis steps as rules with explicit inputs, outputs, and commands in a `Snakefile`.
- Connect calculation and plotting through file dependencies.
- Preview execution with a dry run and execute the workflow locally.
- Understand how dependencies determine which steps need to run again when data or scripts change.
- Introduce parallel execution and running workflow steps through Slurm.

**Practice (exercise 7):** Create a workflow that runs the calculation script and passes its output to the plotting script. Check a dry run, execute the workflow, and verify that changing the plotting script reruns plotting, while changing the calculation script reruns both steps. Explore execution on the course cluster.

Nextflow is mentioned as a workflow manager to be covered in a later session.

## Practice materials

The practical files are organized as follows:

```text
practical/
├── analysis_warmup/         # Scripts for the command-line exercises
├── analysis_depmap/         # Scripts for the cancer dependency analysis
├── data_warmup/
│   ├── samples.tsv
│   ├── tiny.fastq
│   └── tiny.vcf
└── data_depmap/
    ├── Makefile
    └── md5sums.txt
```

The warmup data files are stored directly in `practical/data_warmup/`. For the
DepMap analysis, download the cell-model metadata, CRISPR gene effects, and
gene-expression matrix from [DepMap Public 24Q4, version 1](https://doi.org/10.25452/figshare.plus.27993248.v1):

```bash
make -C practical/data_depmap
make -C practical/data_depmap check
```

The `check` target downloads missing files and verifies all three against the
manually recorded reference hashes in `md5sums.txt`. A mismatch causes it to
fail. Existing files are reused; remove a failed file before downloading it
again. Downloaded CSV files are ignored by Git. The downloads total about
936 MB and require `curl`, GNU Make, and `md5sum`.

The original slide exercises use the following legacy project layout.
[bio-prac.tar.gz](bio-prac.tar.gz) contains a minimal starter project. Extract it with:

```bash
tar -xzf bio-prac.tar.gz
```

The archive provides `data/meta/samples.tsv`, `data/raw/tiny.fastq`, and `data/raw/tiny.vcf`, plus empty `analysis/` and `results/` directories. These small example files support the command-line exercises. The flight and airport data needed for session 2 are added during that session.

The project develops towards this structure (using either R or Python scripts):

```text
bio-prac/
├── analysis/
│   ├── calculate.r / calculate.py
│   └── plot.r / plot.py
├── data/
│   ├── meta/                # Sample sheet and airport metadata
│   └── raw/                 # FASTQ, VCF, and flight data
├── results/
│   ├── airport_delay.tsv
│   └── airport_delay.pdf
└── Snakefile
```

Participants need a terminal with SSH access, a text editor, Git, tmux, and access to the course Slurm environment. Session 2 additionally uses R or Python with the chosen analysis packages, and Snakemake.
