## Two approaches to downloading GBIF images using dwca files

1. Get the dwca file for your species checklist and extract it to a folder. That folder can then be used by code in `03_download_images/fetch_images_whole_dwca.py` to download images.
2. Get the dwca file for your species checklist and extract it to a folder. Then, use code in `02_preprocess_dwca` to load the extracted occurrence.txt and multimedia.txt files, shorten them and save them as CSV files. Additionally, take the occurrence.csv file and split it into many smaller CSV files, one for each species. These adapted and split CSV files can then be used by code in `03_download_images/fetch_images_split_dwca.py` to download images.
This second approach avoids having to load a huge occurrence.txt file in memory, and makes debugging easier.

## Steps to take to preprocess dwca files:

### 1. Unzip the dwca file in a folder

From a terminal, run `unzip dwca.zip -d <destination_folder>`. This will take quite some time as the files are large. Make sure you have 200GB+ space available on the device.

### 2. Shorten the multimedia and occurrence files
Run `shorten_dwca.py` to load the multimedia and occurrence files from the extracted dwca file directory, loading only specific columns and saving them as CSV files. This significantly reduces the size of these dataframes.

```bash

python shorten_dwca.py \
--write_directory "/bask/homes/r/rybf4168/vjgo8416-amber/data/gbif_download_standalone/dwca_preprocessed/" \
--dwca_file_dir "/bask/homes/r/rybf4168/vjgo8416-amber/data/gbif_download_standalone/dwca_files/lepidoptera_20231018/"
--dwca_file_name "lepidoptera_20231018" \
```

Description of the arguments to the script:
* `--write_directory`: Path to the folder where adapted multimedia and occurrence CSV files will be saved. **Required**.
* `--dwca_file_dir`: Path to the unzipped dwca files. **Required**.
* `--dwca_file_name`: Name which will be appended to the saved dataframes. Eg: "lepidoptera_20231018" **Required**.

### 3. Split up the occurrence dataframe

Load the shortened occurrence.csv file and split it into smaller CSV files, one for each species.

```bash
python split_up_occurrence_df.py \
--write_directory "/bask/homes/r/rybf4168/vjgo8416-amber/data/gbif_download_standalone/dwca_preprocessed/occurrence_dataframes_20231018/" \
--occ_file "/bask/homes/r/rybf4168/vjgo8416-amber/data/gbif_download_standalone/dwca_preprocessed/occurrence_lepidoptera_20231018.csv"

```

Description of the arguments to the script:
* `--write_directory`: where to write the occurrence CSV files. **Required**.
* `--occ_file`: location of the large occurrence CSV file. **Required**.
