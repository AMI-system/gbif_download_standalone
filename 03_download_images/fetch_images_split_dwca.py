#!/usr/bin/env python
# coding: utf-8

"""
Author        : Aditya Jain
Edited by     : Levan Bokeria
Last modified : 30 Oct, 2023
About	      : Split the Occurrence CSV file by species
"""

import argparse
import datetime
import json
import logging
import os
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from urllib.request import urlretrieve

import pandas as pd


def fetch_meta_data(data: pd.DataFrame):
    """returns the relevant metadata for a GBIF observation"""

    fields = [
        "decimalLatitude",
        "decimalLongitude",
        "order",
        "family",
        "genus",
        "species",
        "acceptedScientificName",
        "year",
        "month",
        "day",
        "datasetName",
        "taxonID",
        "acceptedTaxonKey",
        "lifeStage",
        "basisOfRecord",
    ]

    meta_data = {}

    for field in fields:
        if pd.isna(data[field]):
            meta_data[field] = "NA"
        else:
            meta_data[field] = data[field]

    return meta_data


def setup_logger(logger_name, log_suffix):

    # Specify the directory where you want to save the log files
    log_dir = "download_log_files"

    # Ensure the directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Use the timestamp string to create a unique filename for the log file
    timestamp    = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_dir, f"{log_suffix}_{timestamp}.log")

    # Get the root logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # If logger has handlers, clear them
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    formatter    = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def fetch_image_data(i_taxon_key: int):
    global skip_non_adults, max_data_sp, moth_data, write_directory, occ_files, \
        media_df, occurrence_logger, metadata_logger, image_logger

    # get taxa information specific to the species
    taxon_data = moth_data[moth_data["accepted_taxon_key"] == i_taxon_key]

    family_name         = taxon_data["family_name"].item()
    genus_name          = taxon_data["genus_name"].item()
    species_name        = taxon_data["gbif_species_name"].item()
    write_location      = os.path.join(
        write_directory,family_name,genus_name,species_name
        )

    # print("Write location is:", write_location)

    # Count the number of images for this species
    image_count = 0

    # Does meta_data exist for this species?
    if os.path.isfile(os.path.join(write_location,"meta_data.json")):
        # Load it
        with open(os.path.join(write_location,"meta_data.json")) as file:
            species_md = json.load(file)

        # Count the number of images for this species
        count_md = 0
        for key, value in species_md.items():
            if value.get("image_is_downloaded") == True:
                count_md += 1
        image_count = count_md

        # Do we have enough images already
        if image_count >= max_data_sp:
            print(f"{species_name} has ENOUGH images, skipping", flush=True)
            return
        else:
            print(
                f"Downloading for {species_name} which already has "
                f"{image_count} images",
                flush=True
                )

    else:
        # Creat the metadata
        print(f"Downloading for {species_name}", flush=True)
        species_md = {}

    # creating hierarchical folder structure for image storage
    if not os.path.isdir(write_location):
        try:
            os.makedirs(write_location)
        except:
            print(f"Could not create the directory for {write_location}", flush=True)
            return

    # Read the occurrence dataframe
    if os.path.isfile(os.path.join(occ_files,
                                    str(i_taxon_key) + ".csv")):
        i_occ_df = pd.read_csv(os.path.join(occ_files,
                                            str(i_taxon_key) + ".csv"))
        total_occ = len(i_occ_df)
    else:
        occurrence_logger.warning(
            f"No occurrence csv file found for {species_name}, taxon key {i_taxon_key}"
            )
        # print("No occurrence file")
        return

    if total_occ != 0:
        # print(f"{species_name} has some occurrences")

        for idx, row in i_occ_df.iterrows():

            if skip_non_adults:

                if (not pd.isna(row["lifeStage"])) & (row["lifeStage"] != "Adult"):

                    # print("Life stage is", row["lifeStage"], "skipping...")

                    continue

            obs_id = row["id"]

            # Is there already an entry for this image in the metadata file?
            # Then, its either downloaded, or is corrupt or a thumbnail, or broken URL.
            # So skip
            if len(species_md) != 0:
                if str(obs_id)+".jpg" in species_md.keys():
                        continue

            # check occurrence entry in media dataframe
            try:
                media_entry = media_df.loc[media_df["coreid"] == obs_id]

                if not media_entry.empty:
                    # print(f"{species_name} has some media")

                    if len(media_entry) > 1:  # multiple images for an observation
                        media_entry = media_entry.iloc[0, :]
                        image_url = media_entry["identifier"]
                    else:
                        image_url = media_entry["identifier"].item()
                else:

                    # print(f"{species_name} has NO media")
                    continue

            except Exception as e:
                print(e, flush=True)
                continue

            # download image
            try:
                # print("Trying the image download", image_url)
                image_write_path = os.path.join(write_location,str(obs_id)+".jpg")

                urlretrieve(image_url, image_write_path)

                url_works        = True
                image_downloaded = True
                image_count += 1

            except Exception as e:

                image_logger.warning(
                    f"Error downloading URL: '{image_url}'. Error: {e}"
                    )
                # print(f"Error downloading URL: '{image_url}'. Error: {e}")

                url_works        = False
                image_downloaded = False

                # Sometimes the image still gets saved to disk but is corrupted.
                # If this happened, delete it
                if os.path.exists(image_write_path):
                    os.remove(image_write_path)

                    # Log this
                    image_logger.warning(
                        f"Image download failed but corrupted file was still created. "
                        f"Deleting {image_write_path}"
                        )
                    # print(
                    #     f"Image download failed but corrupted file still created. "
                    #     f"Deleting {image_write_path}"
                    #     )

            # Get meta data for this occurrence
            # print("Getting metadata")
            try:
                occ_meta_data                        = fetch_meta_data(row)
                occ_meta_data["image_is_downloaded"] = image_downloaded
                occ_meta_data["image_url_works"]     = url_works
                occ_meta_data["image_is_corrupted"]  = ""
                occ_meta_data["image_is_thumbnail"]  = ""

                species_md[str(obs_id) + ".jpg"]     = occ_meta_data
                # print("Got metadata")
            except Exception as e:
                # print(
                #     f"Couldn't create metadata {species_name}, taxon key {i_taxon_key}."
                #     f"Error {e}"
                #     )
                metadata_logger.warning(
                    f"Couldnt create metadata {species_name}, taxon key {i_taxon_key}."
                    f"Error {e}"
                    )

            try:
                if image_count >= max_data_sp:
                    # print("reached the max images")
                    break
            except Exception as e:
                print(f"Error checking image count: '{image_count}'. Error: {e}")

        # Dump metadata
        # print("Writing metadata")
        try:
            with open(write_location + "/" + "meta_data.json", "w") as outfile:
                json.dump(species_md, outfile)
        except Exception as e:
            # print(
            #     f"Couldn't save metadata {species_name}, taxon key {i_taxon_key}."
            #     f"Error {e}"
            # )
            metadata_logger.warning(
                f"Couldnt save metadata {species_name}, taxon key {i_taxon_key}."
                f"Error {e}"
            )
        # print("Wrote metadata")

    print(f"Downloading complete for {species_name} with {image_count} images.",
            flush=True)

    return


def prep_and_read_files(args):

    global skip_non_adults, max_data_sp, moth_data, write_directory, occ_files, \
        media_df, occurrence_logger, metadata_logger, image_logger

    max_data_sp     = int(args.max_data_sp)
    skip_non_adults = args.skip_non_adults
    write_directory = args.write_directory
    occ_files       = args.occ_files

    # Read the multimedia file
    print("Reading the multimedia file...")
    media_df = pd.read_csv(args.media_file)
    print("Done reading the multimedia file!")

    # read species list
    moth_data  = pd.read_csv(args.species_checklist)
    taxon_keys = list(moth_data["accepted_taxon_key"])
    taxon_keys = [int(taxon) for taxon in taxon_keys]

    # Setup logger
    setup_logger('occurrence_logger', 'occurrence_log')
    setup_logger('metadata_logger', 'metadata_log')
    setup_logger('image_logger', 'image_log')

    occurrence_logger = logging.getLogger('occurrence_logger')
    image_logger      = logging.getLogger('image_logger')
    metadata_logger   = logging.getLogger('metadata_logger')

    # Lastly, call the function with your taxon keys:
    begin = time.time()

    if args.use_parallel:

        if args.use_multiproc:

            try:
                with ProcessPoolExecutor() as executor:

                    # You can use the executor to parallelize your function call:
                    executor.map(fetch_image_data, taxon_keys)

            except Exception as e:
                print(f"Error: {e}")

        else:

            with ThreadPoolExecutor() as executor:

                # You can use the executor to parallelize your function call:
                results = list(executor.map(fetch_image_data, taxon_keys))

    else:

        for i_taxon_key in taxon_keys:
            # print(f"Calling for {i_taxon_key}")
            fetch_image_data(i_taxon_key)


    end = time.time()

    print("Finished downloading for the given list! Time taken:",
          round(end - begin),
          "seconds",
          flush=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write_directory", help="path of the folder to save the data", required=True
    )
    parser.add_argument(
        "--occ_files", help="path of the species occurrence CSV files", required=True
    )
    parser.add_argument(
        "--media_file", help="path of the multimedia CSV file", required=True
    )
    parser.add_argument(
        "--species_checklist", help="path of the species checlist file", required=True
    )
    parser.add_argument(
        "--use_parallel", help="use multithreading/multiprocessing or not",
        required=True
    )
    parser.add_argument(
        "--use_multiproc", help="use multiprocessing or not", required=True
    )
    parser.add_argument(
        "--max_data_sp", help="number of images per species", required=True
    )
    parser.add_argument(
        "--skip_non_adults", help="get only images labeled as adult or with no label",
        required=True
    )

    args = parser.parse_args()

    prep_and_read_files(args)
