#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=1
#SBATCH --mem=100G
#SBATCH --time=1-0
#SBATCH --job-name=dayton_deduper
#SBATCH --output=slurm_out/slurm%j_blastp.out
#SBATCH --error=slurm_out/slurm%j_blastp.err
#SBATCH --mail-user=adayton@uoregon.edu
#SBATCH --mail-type=ALL

file=/projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam
sortfile=data/sorted_C1_SE_uniqAlign.sam

conda activate bgmp_py312

/usr/bin/time -v ./dayton_deduper.py \
-f $sortfile \
-u STL96.txt \
-o data/daytondeduperoutput_C1SEuniqAlign.sam
