# 01. Prepare the checklist for download

## Sequence to run

Once you receive a species checklist from CEH, the provided species names must be checked against the GBIF backbone.

### 1. Preprocess the checklist:
Run `01_preprocess_species_list.ipynb` to load the checklist and modify the species and authority columns in a way expected by subsequent scripts.

### 2. Fetch taxonomic keys from GBIF

For quickly calling the `fetch_taxon_keys.py`, use `02_fetch_taxon_keys_wrapper.ipynb` where you can define and modify the arguments. Otherwise you can use `02_fetch_taxon_keys.sh` for slurm calls.

```sh
python fetch_taxon_keys.py \
    --species_filepath "../species_checklists/singapore-moths-preprocessed.csv" \
    --column_name_species "species_name_provided" \
    --column_name_authority "Authority" \
    --output_filepath "../species_checklists/singapore-moths-keys.csv" \
    --place "London06October2023" \
    --use_multithreading True
```

The description of the arguments to the script:
* `--species_filepath`: Path to the csv file containing list of species names. Example species lists are provided in the `example_species_lists` folder. **Required**.
* `--column_name_species`: Column name in the above csv file containing species' names. **Required**.
* `--column_name_authority`: Column name in the above csv file containing authority names. **Required**.
* `--output_filepath`: Output file path with csv as extension. **Required**.
* `--place`: A placeholder name which identifies the source of the species list - important when combining multiple lists. **Required**.
* `--use_multithreading`: Whether or not to use multithreading when checking the names. Number of workers are set to max=2, due to API call limitations. **Required**.

Check the resulting checklist with CEH, by sharing it as a google docs file. They should confirm that any species not found on GBIF were spelled correctly, and any FUZZY matches are correct.

### 3. Remove duplicate species and species not on GBIF

Species often have synonyms, and checklist often contain accepted species names along with their synonyms. If run as is, images for both will be downloaded in a folder named according to the accepted species name, needlessly duplicating the process.

Run `03_remove_duplicate_species.ipynb` to identify duplicate rows and remove them, so images are downloaded only once per species.

The code also removes rows for species that are not available on GBIF, so that the downstream code that downloads GBIF images does not needlessly loop over them.
