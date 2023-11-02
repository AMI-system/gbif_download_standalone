#!/bin/bash
#SBATCH --account vjgo8416-amber
#SBATCH --qos turing
#SBATCH --time 04:00:00
#SBATCH --nodes 1
#SBATCH --cpus-per-task 36
#SBATCH --mem=100G
#SBATCH --output=download.out

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
python fetch_images_split_dwca.py \
--write_directory "../../../data/gbif_download_standalone/gbif_images/" \
--occ_files "../../../data/gbif_download_standalone/dwca_preprocessed/occurrence_dataframes_20231018/" \
--media_file "../../../data/gbif_download_standalone/dwca_preprocessed/multimedia_lepidoptera_20231018.csv" \
--species_checklist "../species_checklists/uksi-moths-keys-nodup.csv" \
--use_parallel True \
--use_multiproc False \
--max_data_sp 1000 \
--skip_non_adults True
