#!/bin/bash
#SBATCH -A k1164
#SBATCH -J MIX-EMST_tres-0.01_tmix-0.05_eqv-1.2_Zfvar-0.02_dtmix-0.01_phif-4.76
#SBATCH -n 1
#SBATCH -t 1-00:00:00
#SBATCH -e job%J.err
#SBATCH -o job%J.out
#SBATCH -p workq

OMP_NUM_THREADS=1

srun --hint=nomultithread PaSR_PPF_MIX
