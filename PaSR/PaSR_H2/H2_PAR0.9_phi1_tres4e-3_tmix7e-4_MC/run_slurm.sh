#!/bin/bash -l
#SBATCH --ntasks-per-node=1
#SBATCH -N 1
#SBATCH -t 1-00:00:00
#SBATCH -J PaSR_E_phi
#SBATCH -e job%J.err
#SBATCH -o job%J.out
#SBATCH --constraint=intel

cp /home/luz0a/ISAT-CK7/ISAT/bin/PaSR_MixingModels .

srun ./PaSR_MixingModels

cp /home/luz0a/ISAT-CK7/ISAT/bin/PaSR_particles_post .

srun ./PaSR_particle_post
