#!/bin/bash -l
#SBATCH --ntasks-per-node=1
#SBATCH -N 1
#SBATCH -t 1-00:00:00
#SBATCH -J fltD_Sc
#SBATCH -e job%J.err
#SBATCH -o job%J.out
#SBATCH --constraint=intel

cp /home/luz0a/ISAT-CK7/ISAT/bin/PaSR_MixingModels .

srun ./PaSR_MixingModels
