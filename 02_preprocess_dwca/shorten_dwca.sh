#!/bin/bash
#SBATCH --account orchid
#SBATCH --qos orchid
#SBATCH --time 02:15:00
#SBATCH --nodes 1
#SBATCH --cpus-per-task 36
#SBATCH --mem=200G

# Module loading
source ~/miniforge3/bin/activate
conda activate "~/conda_envs/flatbug/"

# Execute your python programme

python shorten_dwca.py \
--write_directory /gws/nopw/j04/ceh_generic/kgoldmann/dwca_preprocessed/ \
--dwca_file_name lepidoptera_20250815 \
--dwca_file_dir /gws/nopw/j04/ceh_generic/kgoldmann/dwca_files/lepidoptera_20250815/
