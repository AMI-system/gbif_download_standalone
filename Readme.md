# GBIF Download Standalone

This repo is purely for the purposes of downloading images from GBIF using species lists.

- moth_nonmoth_dataset.ipynb: downloads images of moths and non-moths in the uk
- moth_nonmoth_dataset.py: does the same but can be executed in background (`nohup moth_nonmoth_dataset.py`)

# Setting up the environment

The repository uses conda to manage the environment and packages which are specified in the `environment.yml` file.

For first time use, run `conda env create -f environment.yml`. This will create a conda environment called "gbif_download_standalone. Then run `conda activate gbif_download_standalont`

# Pre-commits

Pre-commits are specified in the `.pre-commit-config.yaml` file.
For first time use, run `pre-commit install --install-hooks`.
