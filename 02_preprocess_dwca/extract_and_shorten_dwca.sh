#!/bin/bash
#SBATCH --account vjgo8416-amber
#SBATCH --qos turing
#SBATCH --time 01:15:00
#SBATCH --nodes 1
#SBATCH --cpus-per-task 36
#SBATCH --mem=400G

# Module loading
module purge # unloads and loaded modules and resets the environment
module load baskerville # loads the default Baskerville environment
module load bask-apps/live # load the stable, default application stack
module load Miniconda3/4.10.3 # load the Conda package manager

set -e # exit immediately if there is an error
eval "$(${EBROOTMINICONDA3}/bin/conda shell.bash hook)" # initialise Conda

export CONDA_ENV_PATH="/bask/projects/v/vjgo8416-amber/conda_envs/gbif_download_standalone"

# Activate the environment
conda activate "${CONDA_ENV_PATH}"

# Execute your python programme

python extract_and_shorten_dwca.py \
--write_directory /bask/homes/r/rybf4168/vjgo8416-amber/data/gbif-species-trainer-AMI-fork/ \
--temp_directory /bask/homes/r/rybf4168/vjgo8416-amber/data/gbif-species-trainer-AMI-fork/temp/ \
--dwca_file_name lepidoptera \
--dwca_file /bask/homes/r/rybf4168/vjgo8416-amber/data/gbif-species-trainer-AMI-fork/dwca_files/lepidoptera.zip
