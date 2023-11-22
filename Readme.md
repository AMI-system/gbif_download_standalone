# GBIF Download Standalone

## Description of folders:

- 01_prepare_checklist: code to preprocess species checklists and fetch GBIF taxonomic data
- 02_preprocess_dwca: code to preprocess the Darwin Core Archive files, to be used by subsequent download code.
- 03_download_images: code to download GBIF images.
- species_checklists: original checklists provided by CEH, as well as their preprocessed versions.
- data_stats_files: csv files containing an "n_imgs" column specifying how many images we have downloaded for a given species checklist.
- helper_files: miscellaneous helper files.
- helper_scripts: miscellaneous helper scripts for code development, debugging, testing, etc.


## Setting up the environment

The repository uses conda to manage the environment and packages which are specified in the `environment.yml` file.

For first time use, create a new conda environment using `conda create --name gbif_download_standalone`. On Baskerville, the `--name` argument should be the full path to the location of the environment, e.g. `/bask/projects/v/vjgo8416-amber/conda_envs/gbif_download_standalone`

Run `conda activate gbif_download_standalone`.

Update the environment with packages specified in `environment.yml`: `conda env update --file environment.yml --prune`

**On basekerville you can skip straight to:**

`conda activate /bask/projects/v/vjgo8416-amber/conda_envs/gbif_download_standalone`

## Pre-commits

Pre-commits are specified in the `.pre-commit-config.yaml` file.

For first time use, run `pre-commit install --install-hooks`.

Note various exceptions for flake8 specified in file `.flake8`

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
