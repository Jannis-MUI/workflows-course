#!/bin/bash
set -euo pipefail

starter_id=$(sbatch --parsable compare_dependency.sh)
echo "Submitted starter: $starter_id"

plot_id=$(sbatch --parsable --dependency=afterok:"$starter_id" plot_dependency.sh)
echo "Submitted plotting: $plot_id"

echo "sacct -j $starter_id,$plot_id --format=JobID,JobName,State,ExitCode,Elapsed"