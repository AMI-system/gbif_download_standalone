#!/usr/bin/env python
# coding: utf-8

"""
Author	      : Levan Bokeria
Last modified : Oct 11th, 2023
About	      : Extract and shorten multimedia and occurrence data.
"""

import argparse
import os

from dwca.read import DwCAReader


def extract_and_shorten(args):

    multimedia_fields_to_keep = [
        "coreid",
        "identifier",
    ]

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

    # Read the dwca files
    with DwCAReader(path=args.dwca_file,
                    tmp_dir=args.temp_directory) as dwca:

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

    # Save both
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
        "--temp_directory",
        help="path of the temporary folder where dwca zip file is extracted",
        required=True
    )
    parser.add_argument(
        "--dwca_file",
        help="path of the dwca file to extract",
        required=True
    )
    parser.add_argument(
        "--dwca_file_name",
        help="the name under which to save preprocessed dataframes",
        required=True
    )

    args = parser.parse_args()

    extract_and_shorten(args)
