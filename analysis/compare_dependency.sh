#!/bin/bash
#SBATCH --job-name=compare_dependency
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=5
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=compare_dependency-%j.out

python ./compare_dependency.py LUSC KRAS PIK3CA