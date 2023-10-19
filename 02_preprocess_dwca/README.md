## Sequence to run

The scripts in this folder load the multimedia and occurrence dataframes from a given dwca file directory, save them in an adapted CSV format, and split the occurrence dataframe into smaller dataframes for each species.

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

### 3. Split up occurrence dataframe

```bash
python split_up_occurrence_df.py \
--write_directory "/bask/homes/r/rybf4168/vjgo8416-amber/data/gbif_download_standalone/dwca_preprocessed/occurrence_dataframes_20231018/" \
--occ_file "/bask/homes/r/rybf4168/vjgo8416-amber/data/gbif_download_standalone/dwca_preprocessed/occurrence_lepidoptera_20231018.csv"

```

Description of the arguments to the script:
* `--write_directory`: where to write the occurrence CSV files. **Required**.
* `--occ_file`: location of the large occurrence CSV file. **Required**.
