#!/bin/bash
#SBATCH -A k1242
#SBATCH -J MIX-MC_tres-0.004_tmix-0.5_eqv-0.8_Zfvar-0.1
#SBATCH -n 1
#SBATCH -t 1-00:00:00
#SBATCH -e job%J.err
#SBATCH -o job%J.out
#SBATCH -p workq

OMP_NUM_THREADS=1

srun --hint=nomultithread PaSR_particles_init
srun --hint=nomultithread PaSR_PPF_MIX