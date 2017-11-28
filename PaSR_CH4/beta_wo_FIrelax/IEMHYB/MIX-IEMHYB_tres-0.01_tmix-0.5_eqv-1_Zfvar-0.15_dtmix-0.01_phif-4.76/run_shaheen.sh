#!/bin/bash
#SBATCH -A k1164
#SBATCH -J MIX-IEMHYB_tres-0.01_tmix-0.5_eqv-1_Zfvar-0.15_dtmix-0.01_phif-4.76
#SBATCH -n 1
#SBATCH -t 1-00:00:00
#SBATCH -e job%J.err
#SBATCH -o job%J.out
#SBATCH -p workq

OMP_NUM_THREADS=1

srun --hint=nomultithread PaSR_PPF_MIX
