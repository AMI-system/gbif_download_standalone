# GBIF Download Standalone

## Setting up the environment

The repository uses conda to manage the environment and packages which are specified in the `environment.yml` file.

For first time use, run `conda env create -f environment.yml`. This will create a conda environment called "gbif_download_standalone".

Then, run `conda activate gbif_download_standalone`

## Pre-commits

Pre-commits are specified in the `.pre-commit-config.yaml` file.

For first time use, run `pre-commit install --install-hooks`.

## Sequence of steps to take:

1. Prepare the species checklist file.
This will be used to download GBIF images. See `01_prepare_checklist` for further instructions.

2. Preprocess the Darwin Core Archive file
The Darwin Core Archive (dwca) file for the checklist needs to be extracted and preprocessed. See `02_preprocess_dwca` for further instructions.

3. Download GBIF images
Using the dwca files and the checklist, get images from GBIF. Then, calculate a summary file documenting how many images we have for the checklist. See `03_download_images` for further instructions.

## License and authorship

The code in this repository is adapted and modified from [RolnickLab Species Trainer repository](https://github.com/RolnickLab/gbif-species-trainer).

See the `LICENSE` file.
