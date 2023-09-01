import taxon_keys
import pandas as pd
import fetch_gbif

non_moth_species_path = '/bask/homes/f/fspo1218/amber/projects/on_device_classifier/01_data_download/species_lists/moth_trap_non-moths_21-08-2023.csv'
moth_species_path = '/bask/homes/f/fspo1218/amber/projects/on_device_classifier/01_data_download/species_lists/uksi-macro-moths.csv'

non_moth_output_path = '/bask/homes/f/fspo1218/amber/projects/gbif_download_standalone/output_data/keys/non-moth_data.csv'
moth_output_path = '/bask/homes/f/fspo1218/amber/projects/gbif_download_standalone/output_data/keys/moth_data.csv'

column_name = 'taxon'

def process_species_list(data, column_name, output_path):
    # fetch species names from the list
    #data = pd.read_csv(file_path, index_col=False)
    species_list = []
    for indx in data.index:
        species_list.append(data[column_name][indx])

    data_final = pd.DataFrame(
        columns=[
            "taxon_key_gbif_id",
            "order_name",
            "family_name",
            "genus_name",
            "search_species_name",
            "gbif_species_name",
            "confidence",
            "status",
            "match_type",
        ],
        dtype=object,
    )

    # fetch taxonomy data from GBIF
    for name in species_list:
        data = taxon_keys.get_gbif_key_backbone(name)
        data_final = pd.concat([data_final, data], ignore_index=True)

    # save the file
    data_final.to_csv(output_path, index=False)

    
write_directory = '/bask/homes/f/fspo1218/amber/data/binary_moth_training/nonmoth/'
species_key_filepath = non_moth_output_path
max_images_per_species = 500
resume_session= True

LIMIT_DOWN = 300  # GBIF API parameter for max results per page
MAX_SEARCHES = 11000  # maximum no. of points to iterate
moth_data = pd.read_csv(species_key_filepath)

limit_down=300
max_searches = 11000



MAX_DATA_SP = 500

fetch_gbif.get_gbif_images(moth_data, True, '/bask/homes/f/fspo1218/amber/data/binary_moth_training/nonmoth/', max_images_per_species, limit_down, max_searches)