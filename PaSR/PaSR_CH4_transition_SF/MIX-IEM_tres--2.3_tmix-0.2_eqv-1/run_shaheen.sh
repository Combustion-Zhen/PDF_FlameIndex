#!/bin/bash
#SBATCH -A k1242
#SBATCH -J MIX-IEM_tres--2.3_tmix-0.2_eqv-1
#SBATCH -n 1
#SBATCH -t 3-00:00:00
#SBATCH -e job%J.err
#SBATCH -o job%J.out
#SBATCH -p workq

OMP_NUM_THREADS=1

srun --hint=nomultithread PaSR_PPF_MIX
