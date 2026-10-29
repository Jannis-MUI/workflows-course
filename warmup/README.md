# Warmup: Linux, Git, Slurm, and tmux

These short exercises refresh the command-line skills used in the analysis.
Start by cloning the repository as described in the [main README](../README.md).
From the repository root, enter the warmup directory:

```bash
cd warmup
```

The example files are `samples.tsv`, `tiny.fastq`, and `tiny.vcf`. Work on copies
when modifying or compressing them.

## Linux and Bash

1. **Connect and explore.** Connect to the course server with SSH and transfer
   a file with `scp` or `rsync`. Navigate the repository using relative and
   absolute paths. Create a directory, copy and move files, and remove your
   copies. Find command help and edit a text file with `nano` or Vim.
2. **Inspect and transform data.** Use `head`, `tail`, `wc`, and `grep` to inspect
   the example files. Display the sample sheet as a table with `column`.
   Compress a copy of the VCF, inspect it while compressed, and decompress it
   again. Extract FASTQ read names and sort them. Convert the sample sheet
   from TSV to CSV. Combine commands with pipes, wildcards, and redirection.
3. **Write a small script.** Put one of these transformations into a Bash
   script that accepts a filename as an argument. Add a shebang, make the
   script executable, and run it directly. Use variables, command substitution,
   a conditional, and a loop to process several files. Inspect `$PATH` and
   define a useful alias in `~/.bashrc`; try tab completion and command history.

## Processes and tmux

1. **Control processes.** Redirect standard output and standard error to
   separate files. Start a long-running command, interrupt it, then try
   suspending and resuming it. Run it in the background, inspect the process,
   and terminate it. Explain when `nohup` or `disown` would be useful.
2. **Keep a terminal session.** Start a tmux session and split it into panes.
   Run a command, detach, disconnect from SSH, then reconnect and reattach.
   Configure a useful tmux or SSH shortcut.

## Git

1. **Inspect and commit.** From the repository root, inspect `git status` and
   the commit history. Check your author information. Stage your warmup script,
   review the staged diff, and commit it. Use `.gitignore` to exclude generated
   files and keep data out of your exercise commits.
2. **Branch and merge.** Create a branch, change your script, and commit the
   change. Switch back and merge the branch. Inspect the history and working
   tree after each step.

## Slurm

1. **Explore the cluster.** Inspect partitions and jobs with `sinfo` and
   `squeue`. Use tmux panes to watch the queue while requesting an interactive
   allocation with `salloc`. Launch a command with `srun`.
2. **Observe resources.** Run a simulated CPU-intensive command inside the
   allocation and monitor its CPU use. Stop it, then try several processes.
   Compare CPU and memory use with the requested resources and explore the
   effects of resource limits.
3. **Submit a small job.** Submit your warmup script with `sbatch`. Request
   tasks, CPUs per task, memory, runtime, and the course partition. Inspect
   the job and its output, and compare `srun` with `sbatch`.
