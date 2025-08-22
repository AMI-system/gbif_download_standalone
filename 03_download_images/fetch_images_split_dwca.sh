#!/bin/bash
#SBATCH --account ceh_generic
#SBATCH --qos standard
#SBATCH --time 24:00:00
#SBATCH --nodes 1
#SBATCH --mem=100G
#SBATCH --output=download_thailand.out
#SBATCH --partition=standard
#SBATCH --job-name=download_thailand

# Module loading
source ~/miniforge3/bin/activate
conda activate "~/conda_envs/flatbug/"

# Execute your python programme
python fetch_images_split_dwca.py \
    --write_directory "/gws/nopw/j04/ceh_generic/kgoldmann/gbif_images" \
    --occ_files "/gws/nopw/j04/ceh_generic/kgoldmann/dwca_preprocessed/occurrence_dataframes_20250815/" \
    --media_file "/gws/nopw/j04/ceh_generic/kgoldmann/dwca_preprocessed/multimedia_lepidoptera_20250815.csv" \
    --species_checklist "/home/users/katriona/gbif_download_standalone/species_checklists/thailand-moths-keys-nodup.csv" \
    --max_data_sp 1000 \
    --skip_non_adults

