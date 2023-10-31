#!/usr/bin/env python
# coding: utf-8

"""
Author        : Aditya Jain
Edited by     : Levan Bokeria
Last modified : 30 Oct, 2023
About	      : Calculate the image count for a given species list
"""


import argparse
import datetime
import logging
import os

import pandas as pd
from pygbif import species as species_api


def setup_logger(logger_name, log_suffix):
    """Set up loggers to record any errors and exceptions"""

    # Specify the directory where you want to save the log files
    log_dir = "data_stats_log_files"

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


def check_stats(args):
    """Main script that loads a species checklist and counts the number of images
    for each species, using the meta_data.json file in their correponding folder.

    It also checks that the number of images on disk matches entries in the meta data.
    """

    # Setup loggers

    # Log when the number of images on disk do not match entries in meta data
    setup_logger('mismatch_logger', 'mismatch_log')
    # Log if meta data file is not found
    setup_logger('metadata_logger', 'metadata_log')

    mismatch_logger = logging.getLogger('mismatch_logger')
    metadata_logger = logging.getLogger('metadata_logger')

    # Read the checklist for which we're counting files
    df = pd.read_csv(args.species_checklist)

    # Create an empty dataframe to record species for which image count on disk does not
    # match meta data entries.
    df_mismatch = []

    # Define a column for n images
    df["n_imgs"] = ""

    # Iterate through each species and check the count of images
    for idx, row in df.iterrows():

        family  = row["family_name"]
        genus   = row["genus_name"]
        species = row["gbif_species_name"]

        # Check if directory exists
        species_dir = (
            os.path.join(args.gbif_img_dir, family, genus, species)
            )

        if os.path.isdir(species_dir):
            n_images_on_disk = len(
                [f for f in os.listdir(species_dir) if f.lower().endswith('.jpg')]
                )
            # print(f"{species} Count files method has", n_images_on_disk, "images")

            # Load metadata
            try:

                # Count the number of images for this species
                md2_n_imgs_downloaded = 0

                try:
                    # Count images in meta data
                    md2 = pd.read_json(
                        os.path.join(species_dir, "meta_data.json"), orient='index'
                        )

                    if md2.empty:
                        md2_n_imgs_downloaded = 0
                    else:
                        md2_n_imgs_downloaded = md2["image_is_downloaded"].sum()

                    # print(
                        # f"{species} Count dataframe metadata has",
                        # md2_n_imgs_downloaded, "images"
                        # )

                except Exception as e:
                    # print(f"{species} error counting dataframe way: {e}")
                    metadata_logger.warning(f"Error {e} for {species_dir}")

                # Do n images match?
                if n_images_on_disk != md2_n_imgs_downloaded:

                    # print(
                    #     f"Mismatch! File count {n_images_on_disk}, "
                    #     f"metadata has {md2_n_imgs_downloaded}, {species_dir}"
                    # )

                    mismatch_logger.warning(
                        f"Mismatch! File count {n_images_on_disk}, "
                        f"metadata has {md2_n_imgs_downloaded}, {species_dir}"
                    )

                    # Get the GBIF scientificName for this species, to help resolve
                    # why image counts don't add up
                    gbif_data = species_api.name_backbone(
                        name=row["search_species_name"],
                        strict=True,
                        rank="species"
                    )

                    row["scientificName"] = gbif_data["scientificName"]

                    # Save this row in a separate CSV file
                    df_mismatch.append(row)

            except Exception as e:
                pass
                # print(f"No metadata for {species_dir}. Error {e}")

                metadata_logger.warning(f"No metadata for {species_dir}. Error {e}")
        else:

            # If directory for this species doesn't exist, then the species didn't exist
            # on GBIF so has no images.
            n_images_on_disk = 0

        # print(f"{species} has {n_images_on_disk} images")

        # Record this
        df.loc[idx, "n_imgs"] = n_images_on_disk

    # Save the dataframe
    save_name = os.path.basename(args.species_checklist)
    df.to_csv(os.path.join(args.write_directory, "data_stats_"+save_name), index=False)

    # Save the mismatch dataframe
    df_mismatch = pd.DataFrame(df_mismatch)
    df_mismatch.to_csv(
        os.path.join("data_stats_log_files", "mismatch_list_"+save_name),
        index=False
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write_directory", help="path of the folder to save the stats data",
        required=True
    )
    parser.add_argument(
        "--species_checklist", help="path of the species checlist file", required=True
    )
    parser.add_argument(
        "--gbif_img_dir", help="path of the folder with gbif images", required=True
    )

    args = parser.parse_args()

    check_stats(args)
