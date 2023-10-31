#!/usr/bin/env python
# coding: utf-8

"""
Author        : Aditya Jain
Edited by     : Levan Bokeria
Last modified : 30 Oct, 2023
About	      : Extract and shorten multimedia and occurrence data.
"""

import argparse
import os

from dwca.read import DwCAReader


def extract_and_shorten(args):
    """
    This function will use the dwca reader module to read only the relevant columns of
    the occurrence.txt and multimedia.txt files and save them as CSV files
    """

    # Which columns of the media file to load:
    multimedia_fields_to_keep = [
        "coreid",
        "identifier",
    ]

    # Which columns of the occurrence file to load:
    occurrence_fields_to_keep = [
        "id",
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

    # Read the files
    with DwCAReader(path=args.dwca_file_dir) as dwca:

        print('Starting reading the multimedia file...')

        media_df = dwca.pd_read(
            "multimedia.txt",
            parse_dates=True,
            on_bad_lines="skip",
            usecols=multimedia_fields_to_keep)

        print('Finished reading the multimedia...')

        print('Starting reading the occurrence file...')

        occ_df = dwca.pd_read(
            "occurrence.txt",
            parse_dates=True,
            on_bad_lines="skip",
            usecols=occurrence_fields_to_keep)

        print('Finished reading the occurrence...')

    # Save both as csv
    print("Starting to save multimedia...")
    media_df.to_csv(
        os.path.join(args.write_directory, "multimedia_"+args.dwca_file_name+".csv"),
        index=False
    )
    print("Finished saving multimedia...")
    print("Starting to save occurrence...")
    occ_df.to_csv(
        os.path.join(args.write_directory, "occurrence_"+args.dwca_file_name+".csv"),
        index=False
    )
    print("Finished saving occurrence...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--write_directory",
        help="path of the folder to save the preprocessed csv files",
        required=True
    )
    parser.add_argument(
        "--dwca_file_dir",
        help="path of the extracted dwca files",
        required=True
    )
    parser.add_argument(
        "--dwca_file_name",
        help="the name under which to save preprocessed dataframes",
        required=True
    )

    args = parser.parse_args()

    extract_and_shorten(args)
