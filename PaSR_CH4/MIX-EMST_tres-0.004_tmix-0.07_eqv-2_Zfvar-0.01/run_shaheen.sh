#!/bin/bash
#SBATCH -A k1242
#SBATCH -J MIX-EMST_tres-0.004_tmix-0.07_eqv-2_Zfvar-0.01
#SBATCH -n 1
#SBATCH -t 1-00:00:00
#SBATCH -e job%J.err
#SBATCH -o job%J.out
#SBATCH -p workq

OMP_NUM_THREADS=1

srun --hint=nomultithread PaSR_particles_init
srun --hint=nomultithread PaSR_PPF_MIX