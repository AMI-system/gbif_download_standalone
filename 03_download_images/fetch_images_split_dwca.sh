#!/bin/bash
#SBATCH --account vjgo8416-amber
#SBATCH --qos turing
#SBATCH --time 24:00:00
#SBATCH --nodes 1
#SBATCH --cpus-per-task 36
#SBATCH --mem=100G
#SBATCH --output=download_thailand.out

# Module loading
module purge
module load baskerville
module load bask-apps/live
module load Miniforge3/24.1.2-0
eval "$(${EBROOTMINIFORGE3}/bin/conda shell.bash hook)"
source "${EBROOTMINIFORGE3}/etc/profile.d/mamba.sh"

# Define the path to your existing Conda environment (modify as appropriate)
CONDA_ENV_PATH="/bask/projects/v/vjgo8416-amber/conda_envs/gbif_download_standalone"

mamba activate "${CONDA_ENV_PATH}"

# Execute your python programme
python fetch_images_split_dwca.py \
    --write_directory "/bask/projects/v/vjgo8416-amber/data/gbif_download_standalone/gbif_images/" \
    --occ_files "/bask/projects/v/vjgo8416-amber/data/gbif_download_standalone/dwca_preprocessed/occurrence_dataframes_20231018/" \
    --media_file "/bask/projects/v/vjgo8416-amber/data/gbif_download_standalone/dwca_preprocessed/multimedia_lepidoptera_20231018.csv" \
    --species_checklist "/bask/homes/f/fspo1218/amber/projects/gbif_download_standalone/species_checklists/kenya-uganda-moths-keys-nodup.csv" \
    --max_data_sp 1000 \
    --skip_non_adults


# --rerun_nonzero
