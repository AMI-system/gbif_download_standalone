#!/usr/bin/env python
# coding: utf-8

"""
Author	      : Levan Bokeria
Last modified : 30 Oct, 2023
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

    """This is the main function that will load the occurrence file, transform the
    acceptedTaxonKey column to be only integers, group it by acceptedTaxonKey and
    save each group as a separate CSV file
    """

    # If save_dir doesn't exist, create it
    if not os.path.exists(args.write_directory):
        os.makedirs(args.write_directory)

    # Load the occurrence CSV file
    print("Loading the occurrence file...")
    occ_df = pd.read_csv(args.occ_file,
                         parse_dates=True,
                         on_bad_lines="skip")
    print("Finished loading the occurrence file")

    # Select only the rows with numeric acceptedTaxonKeys
    print("Selecting only numerical acceptedTaxonKey rows...")
    mask   = occ_df["acceptedTaxonKey"].apply(is_number)
    occ_df = occ_df[mask].copy()
    print("Finished")

    print("Converting all strings to floats")
    occ_df["acceptedTaxonKey"] = occ_df["acceptedTaxonKey"].apply(convert_str_to_float)
    print("Finished...")

    print("Printing the data types in the acceptedTaxonKey column...")
    # Pring type counts
    counts1 = occ_df["acceptedTaxonKey"].apply(custom_type).value_counts()
    print(counts1)

    # Remove the rows with non-0 fraction
    # Some taxonomic keys have errors and are recorded with non-0 fractions. Remove them
    mask = ~occ_df["acceptedTaxonKey"].apply(
        lambda x: isinstance(x, float) and x != int(x)
        )
    print("Number of rows with non-0 fraction in the acceptedTaxonKey:",
          len(occ_df) - len(mask),
          "These will be removed.")
    if not len(mask) == len(occ_df):
        print("Removing these...")
        occ_df = occ_df[mask]
        print("Finished")

    # Convert everything to integer from float
    print("Converting all taxon keys to integer")
    occ_df["acceptedTaxonKey"] = occ_df["acceptedTaxonKey"].astype(int)
    print("Finished")

    # Last check of types
    print("Printing the final data types in the acceptedUseageKey column:")
    counts2 = occ_df["acceptedTaxonKey"].apply(custom_type).value_counts()
    print(counts2)

    # Create groups
    print("Creating a list of groups...")
    groups = list(occ_df.groupby("acceptedTaxonKey"))
    print("Finished")

    # Use multi-threading
    print("Starting to save groups...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(save_group, groups)
    print("Finished saving all the groups!")


def save_group(group):
    global args

    group_name, group_df = group
    filename = f"{group_name}.csv"

    try:
        group_df.to_csv(os.path.join(args.write_directory, filename), index=False)
        logging.info(f"Successfully saved {filename} with {len(group_df)} rows")
    except Exception as e:
        logging.error(f"Couldn't save {filename}: {str(e)}")


# Custom function to convert strings to floats when possible
def convert_str_to_float(x):
    if isinstance(x, str):  # Check if x is a string
        try:
            return float(x)  # Try to convert x to a float
        except ValueError:  # Handle exception if conversion is not possible
            return x  # Return the original string if conversion fails
    else:
        return x  # Return x unchanged if it's not a string


def custom_type(x):
    if pd.isna(x):
        return 'missing'
    elif isinstance(x, bool):
        return 'bool'
    else:
        return type(x).__name__


# Select only numeric acceptedTaxonKey rows
def is_number(x):
    """Returns False if the argument is not a number, a number string, or is NA """

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

    args = parser.parse_args()

    split_occurrence(args)
