# 03. Download Images

## General description:

Once you have prepared the species checklist (`01_prepare_checklist`) and preprocessed the appropriate dwca file (`02_preprocess_dwca`), you can download GBIF images using code in this folder.

`fetch_images_whole_dwca.py` can use the dwca file directory where raw multimedia.txt and occurrence.txt files reside. These files are typically very large (especially for all of Lepidoptera) and might make it hard to dynamically use this code (e.g. when downloading and redownloading or debugging)

`fetch_images_split_dwca.py` can use the adapted multimedia.csv file, and split occurrence CSV files for each species. This avoids having to load a huge occurrence.txt file in memory, as each smaller occurrence.csv files for each species gets loaded into memory by subprocesses.

There are also bash files available to run these using slurm:
- fetch_images_split_dwca.sh
- fetch_images_whole_dwca.sh

Finally, once images are downloaded, use `calculate_data_stats.py` to create a csv file documenting how many images we have for each species in a checklist.

## 1. Fetching the Images

As mentioned, there are two options for this. The following

### A. fetch_images_whole_dwca.py

```bash
python fetch_images_whole_dwca.py \
    --write_directory "../../../data/gbif_download_standalone/gbif_images/" \
    --dwca_dir "../../../data/gbif_download_standalone/dwca_files/lepidoptera_20231018" \
    --species_checklist "../species_checklists/uksi-moths-keys-nodup.csv" \
    --use_parallel True \
    --use_multiproc False \
    --max_data_sp 1000 \
    --skip_non_adults True
```

Description of the arguments to the script:

* `--write_directory`: Where to write GBIF images **Required**
* `--dwca_dir`: Path to the dwca folder where extracted dwca files are. **Required**
* `--species_checklist`: Path to the species checklist. **Required**
* `--use_parallel`: Whether or not to paralellise over threads and processors. If False, will use a for loop to download for each species **Required**
* `--use_multiproc`: If `--use-parallel` is True, use either multithreading or multiprocessing. Multiprocessing does not currently work, although the code is set up to be adapted for it. **Required**
* `--max_data_sp`: Maximum number of images to download per species. **Required**
* `--skip_non_adults`: If True, download only images where the `lifeStage` field is either `adult` or empty, i.e. skip all non-adult life stages. **Required**

### B. fetch_images_split_dwca.py (recommended)

```bash
python fetch_images_split_dwca.py \
    --write_directory "../../../data/gbif_download_standalone/gbif_images/" \
    --occ_files "../../../data/gbif_download_standalone/dwca_preprocessed/occurrence_dataframes_20231018/" \
    --media_file "../../../data/gbif_download_standalone/dwca_preprocessed/multimedia_lepidoptera_20231018.csv" \
    --species_checklist "../species_checklists/uksi-moths-keys-nodup.csv" \
    --use_parallel True \
    --use_multiproc False \
    --max_data_sp 1000 \
    --skip_non_adults True
```

Description of the arguments to the script:

* `--write_directory`: Where to write GBIF images **Required**
* `--occ_files`: Path to the folder where separate occurrence.csv files are for each species. **Required**
* `--media_file`: Path to the folder where the adapted multimedia.csv file is. **Required**
* `--species_checklist`: Path to the species checklist. **Required**
* `--use_parallel`: Whether or not to paralellise over threads and processors. If False, will use a for loop to download for each species **Required**
* `--use_multiproc`: If `--use-parallel` is True, use either multithreading or multiprocessing. Multiprocessing does not currently work, although the code is set up to be adapted for it. **Required**
* `--max_data_sp`: Maximum number of images to download per species. **Required**
* `--skip_non_adults`: If True, download only images where the `lifeStage` field is either `adult` or empty, i.e. skip all non-adult life stages. **Required**

### 2. calculate_data_statistics.py

```bash
python calculate_data_statistics.py \
    --write_directory "../data_stats_files/" \
    --species_checklist "../species_checklists/uksi-moths-keys-nodup.csv" \
    --gbif_img_dir "../../../data/gbif_download_standalone/gbif_images/"
```

Description of the arguments to the script:
* `--write_directory`: Where to write the data statistics file for a given checklist. **Required**
* `--species_checklist`: Path to the species checklist. **Required**
* `--gbif_img_dir`: Path to the folder with GBIF images. **Required**
