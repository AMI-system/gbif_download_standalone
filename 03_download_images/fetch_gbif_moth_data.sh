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
--write_directory "/Users/lbokeria/Documents/projects/gbif-species-trainer-data/gbif_images/sandbox" \
--occ_files "/Users/lbokeria/Documents/projects/gbif-species-trainer-data/occurrence_dataframes/" \
--media_file "/Users/lbokeria/Documents/projects/gbif-species-trainer-data/dwca_files/multimedia_lepidoptera.csv" \
--species_checklist "/Users/lbokeria/Documents/projects/gbif_download_standalone/species_checklists/uksi-moths-keys-nodup.csv" \
--use_parallel False \
--use_multiproc False \
--max_data_sp 2 \
--skip_non_adults True
