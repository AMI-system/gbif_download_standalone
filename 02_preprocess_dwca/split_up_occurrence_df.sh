#!/bin/bash
#SBATCH --account orchid
#SBATCH --qos orchid
#SBATCH --time 03:00:00
#SBATCH --nodes 1
#SBATCH --cpus-per-task 36
#SBATCH --mem=200G

# set up for JASMIN
source ~/miniforge3/bin/activate
conda activate "~/conda_envs/flatbug/"

# Execute your python programme

python split_up_occurrence_df.py \
--write_directory "/gws/nopw/j04/ceh_generic/kgoldmann/dwca_preprocessed/occurrence_dataframes_20250815/" \
--occ_file "/gws/nopw/j04/ceh_generic/kgoldmann/dwca_preprocessed/occurrence_lepidoptera_20250815.csv"
