#!/bin/bash
#SBATCH --partition orchid
#SBATCH --account orchid
#SBATCH --qos orchid
#SBATCH --time 10:00:00
#SBATCH --output=taxon_keys.out
#SBATCH --gres gpu:1

source ~/miniforge3/bin/activate
conda activate "~/conda_envs/gbif_download_standalone/"

# Execute your python programme
# regions=("anguilla" "costarica" "japan" "madagascar" "namibia" "nigeria" "kenya-uganda" "singapore" "thailand" "uksi")
regions=("kenya-uganda")


for region in "${regions[@]}"; do
    echo "\033[1m ${region} \033[0m"
    echo "- using ./species_checklists/preprocessed/${region}-moths-preprocessed.csv"

    python fetch_taxon_keys.py \
    --species_filepath ../species_checklists/preprocessed/${region}-moths-preprocessed.csv \
    --column_name_species species_name_provided \
    --column_name_authority authority_name_provided \
    --output_filepath ../species_checklists/keys/${region}-moths-keys.csv \
    --place Leeds25Sept2025 \
    --use_multithreading True

    echo "Finished for ${region}"
done
