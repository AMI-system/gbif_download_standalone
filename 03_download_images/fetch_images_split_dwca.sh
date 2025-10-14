#!/bin/bash
#SBATCH --account ceh_generic
#SBATCH --qos high
#SBATCH --time 48:00:00
#SBATCH --nodes 1
#SBATCH --mem=100G
#SBATCH --partition=standard
#SBATCH --cpus-per-task=96

# Module loading
source ~/miniforge3/bin/activate
conda activate "~/conda_envs/flatbug/"

# Get region argument
region="$1"
if [ -z "$region" ]; then
    echo "Usage: $0 <region>"
    exit 1
fi

# Number of worker threads (defaults to SLURM cpus-per-task)
N_WORKERS=${SLURM_CPUS_PER_TASK:-8}

# Execute your python programme
python fetch_images_split_dwca.py \
    --write_directory "/gws/ssde/j25b/ceh_generic/kgoldmann/gbif_images" \
    --occ_files "/gws/ssde/j25b/ceh_generic/kgoldmann/dwca_preprocessed/occurrence_dataframes_20250815/" \
    --media_file "/gws/ssde/j25b/ceh_generic/kgoldmann/dwca_preprocessed/multimedia_lepidoptera_20250815.csv" \
    --species_checklist "/home/users/katriona/gbif_download_standalone/species_checklists/final_subset/${region}-moths-keys-nodup-1.csv" \
    --max_data_sp 1000 \
    --skip_non_adults \
    --use_parallel \
    --n_workers $N_WORKERS
