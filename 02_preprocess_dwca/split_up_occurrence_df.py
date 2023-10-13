#!/usr/bin/env python
# coding: utf-8

"""
Author	      : Levan Bokeria
Last modified : Oct 11th, 2023
About	      : Split the Occurrence CSV file by species
"""

import argparse
import concurrent.futures
import logging
import os

import pandas as pd

# Configure logging
logging.basicConfig(filename='split_log.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] - %(message)s')


def split_occurrence(args):

    # If save_dir doesn't exist, create it
    if not os.path.exists(args.write_directory):
        os.makedirs(args.write_directory)

    # Load the occurrence CSV file
    occ_df = pd.read_csv(args.occ_file, parse_dates=True, on_bad_lines="skip")

    # Select only the rows with numeric acceptedTaxonKeys
    mask   = occ_df["acceptedTaxonKey"].apply(is_number)
    occ_df = occ_df[mask].copy()

    # Create groups
    groups = list(occ_df.groupby("acceptedTaxonKey"))

    # Use multi-threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(save_group, groups)


def save_group(group):
    global args

    group_name, group_df = group
    filename = f"{group_name}.csv"

    try:
        group_df.to_csv(os.path.join(args.write_directory, filename), index=False)
        logging.info(f"Successfully saved {filename} with {len(group_df)} rows")
    except Exception as e:
        logging.error(f"Couldn't save {filename}: {str(e)}")


# Select only numeric acceptedTaxonKey rows
def is_number(x):
    try:
        # Check for NaN
        if pd.isna(x):
            return False
        # Try converting the element to a float.
        float(x)
        return True  # If conversion is successful, it's a number or a number string.
    except ValueError:  # If conversion fails, it's not a number string.
        return False
    except TypeError:
        # If type conversion is not possible (e.g., for NaNs), also not considered as a
        # number.
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write_directory", help="path of the folder to save the data", required=True
    )
    parser.add_argument(
        "--occ_file", help="path of the occurrence CSV file", required=True
    )
    # parser.add_argument(
    #     "--use_multithreading",
    #     help="False/True; to use multithreading",
    #     required=True,
    # )

    args = parser.parse_args()

    split_occurrence(args)
