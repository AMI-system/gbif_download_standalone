## Sequence to run

The scripts in this folder load the multimedia and occurrence dataframes from a given dwca file, save them in an adapted CSV format, and split the occurrence dataframe into smaller dataframes for each species.

### 1. Extract and shorten the multimedia and occurrence files
Run `extract_and_shorten.py` to load the multimedia and occurrence files from the dwca zip file, loading only specific columns and saving them as CSV files. This significantly reduces the size of these dataframes.

```bash

python extract_and_shorten_dwca.py \
--write_directory "/bask/homes/r/rybf4168/vjgo8416-amber/data/gbif-species-trainer-AMI-fork/" \
--temp_directory "/bask/homes/r/rybf4168/vjgo8416-amber/data/gbif-species-trainer-AMI-fork/temp/" \
--dwca_file_name "lepidoptera" \
--dwca_file "/bask/homes/r/rybf4168/vjgo8416-amber/data/gbif-species-trainer-AMI-fork/dwca_files/lepidoptera.zip"

```

Description of the arguments to the script:
* `--write_directory`: Path to the folder where adapted multimedia and occurrence CSV files will be saved. **Required**.
* `--temp_directory`: For lepidoptera dwca file, the extracted dataframes are too large (115GB+) for the default temporary directory. Indicate a custom temporary directory somewhere on the baskerville project space which has enough space. **Required**.
* `--dwca_file_name`: Name which will be appended to the saved dataframes. Eg: "lepidoptera" **Required**.
* `--dwca_file`: Path to the dwca zip file. **Required**.

### 2. Split up occurrence dataframe

```bash
python fetch_taxon_keys.py \

--species_filepath "../species_checklists/singapore-moths-preprocessed.csv" \
--column_name_species "species_name_provided" \
--column_name_authority "Authority" \
--output_filepath "../species_checklists/singapore-moths-keys.csv" \
--place "London06October2023" \
--use_multithreading True

```

Description of the arguments to the script:
* `--species_filepath`: Path to the csv file containing list of species names. Example species lists are provided in the `example_species_lists` folder. **Required**.
* `--column_name_species`: Column name in the above csv file containing species' names. **Required**.
* `--column_name_authority`: Column name in the above csv file containing authority names. **Required**.
* `--output_filepath`: Output file path with csv as extension. **Required**.
* `--place`: A placeholder name which identifies the source of the species list - important when combining multiple lists. **Required**.
* `--use_multithreading`: Whether or not to use multithreading when checking the names. Number of workers are set to max=2, due to API call limitations. **Required**.
