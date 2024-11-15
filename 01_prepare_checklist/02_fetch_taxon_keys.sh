#!/bin/bash
#SBATCH --account vjgo8416-amber
#SBATCH --qos turing
#SBATCH --time 10:00:00
#SBATCH --nodes 1
#SBATCH --cpus-per-task 36
#SBATCH --mem=5G
#SBATCH --output=all.out

# Module loading
module purge # unloads and loaded modules and resets the environment
module load baskerville # loads the default Baskerville environment
module load bask-apps/live # load the stable, default application stack

# module load Miniconda3/4.10.3 # load the Conda package manager
module load Miniforge3/24.1.2-0

eval "$(${EBROOTMINIFORGE3}/bin/conda shell.bash hook)"
source "${EBROOTMINIFORGE3}/etc/profile.d/mamba.sh"

set -e # exit immediately if there is an error
# eval "$(${EBROOTMINICONDA3}/bin/conda shell.bash hook)" # initialise Conda


export CONDA_ENV_PATH="/bask/projects/v/vjgo8416-amber/conda_envs/gbif_download_standalone"

# Activate the environment
conda activate "${CONDA_ENV_PATH}"

# Execute your python programme
regions=("kenya-uganda" "nigeria" "costarica", "uksi", "singapore", "thailand") #"madagascar" "japan"

for region in "${regions[@]}"; do
    echo "\033[1m ${region} \033[0m"
    echo "- using ./species_checklists/${region}-moths-preprocessed.csv"

    python fetch_taxon_keys.py \
    --species_filepath ../species_checklists/${region}-moths-preprocessed.csv \
    --column_name_species species_name_provided \
    --column_name_authority authority_name_provided \
    --output_filepath ../species_checklists/${region}-moths-keys.csv \
    --place Leeds13Nov2024 \
    --use_multithreading True

    echo "Finished for ${region}"
done
