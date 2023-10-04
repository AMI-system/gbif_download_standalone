#!/usr/bin/env python
# coding: utf-8

"""
Author        : Aditya Jain
Edited by     : Levan Bokeria
Last modified : Sept 27, 2023
About         : This script fetches unique taxon keys for species list from GBIF
"""

import argparse
import concurrent.futures

import pandas as pd
from pygbif import species as species_api


def get_gbif_key_backbone(name_species, name_authority, place):
    """given a species name, this function returns the unique gbif key and other
    attributes using backbone API
    """

    print("Fetching for", name_species)

    # default values
    acc_taxon_key  = [-1]
    order          = ["NotAvail"]
    family         = ["NotAvail"]
    genus          = ["NotAvail"]
    search_species = [name_species]
    gbif_species   = [
        "NotAvail"
    ]  # the name returned on search, can be different from the search
    status         = ["NotAvail"]
    rank           = ["NotAvail"]
    place          = [place]

    data = species_api.name_backbone(name=name_species, strict=True, rank="species")

    if data["matchType"] == "NONE" or data["matchType"] == "HIGHERRANK":

        # Try searching with authority as well
        search_name = name_species + " " + name_authority

        # Change the default value
        search_species = [search_name]

        print("Could not find data for ", name_species, " Retrying for ", search_name)

        data = species_api.name_backbone(name=search_name, strict=True, rank="species")

    # add entries to the fields
    confidence = [data["confidence"]]
    match_type = [data["matchType"]]
    if "order" in data.keys():
        order = [data["order"]]
    if "family" in data.keys():
        family = [data["family"]]
    if "genus" in data.keys():
        genus = [data["genus"]]
    if "status" in data.keys():
        status = [data["status"]]
    if "rank" in data.keys():
        rank = [data["rank"]]

    if data["matchType"] != "NONE" and data["matchType"] != "HIGHERRANK":
        gbif_species = [data["species"]]
        if "acceptedUsageKey" in data.keys():
            acc_taxon_key = [data["acceptedUsageKey"]]
        else:
            acc_taxon_key = [data["usageKey"]]

    df = pd.DataFrame(
        list(
            zip(
                acc_taxon_key,
                order,
                family,
                genus,
                search_species,
                gbif_species,
                confidence,
                status,
                match_type,
                rank,
                place,
            )
        ),
        columns=[
            "accepted_taxon_key",
            "order_name",
            "family_name",
            "genus_name",
            "search_species_name",
            "gbif_species_name",
            "confidence",
            "status",
            "match_type",
            "rank",
            "source",
        ],
    )
    return df


def save_taxon_keys(args):
    """main function for saving the taxon keys and related data for each species"""

    # fetch species names from the list
    data = pd.read_csv(args.species_filepath, index_col=False)
    species_list   = []
    authority_list = []

    for indx in data.index:
        species_list.append(data[args.column_name_species][indx])
        authority_list.append(data[args.column_name_authority][indx])

    # define all columns
    data_final = pd.DataFrame(
        columns=[
            "accepted_taxon_key",
            "order_name",
            "family_name",
            "genus_name",
            "search_species_name",
            "gbif_species_name",
            "confidence",
            "status",
            "match_type",
            "rank",
            "source",
        ],
        dtype=object,
    )

    # fetch taxonomy data from GBIF
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(
            executor.map(
                get_gbif_key_backbone,
                species_list,
                authority_list,
                [args.place] * len(species_list)
                )
            )

    data_final = pd.concat([data_final] + results, ignore_index=True)

    # save the file
    data_final.to_csv(args.output_filepath, index=False)

    # fetch taxonomy data from GBIF
    # for count, name in enumerate(species_list):

    #     print("Fetching for", name, count, "of", len(species_list))
    #     data = get_gbif_key_backbone(name, authority_list[count], args.place)
    #     data_final = pd.concat([data_final, data], ignore_index=True)

    # # save the file
    # data_final.to_csv(args.output_filepath, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--species_filepath", help="path of the species list", required=True
    )
    parser.add_argument(
        "--column_name_species",
        help="column name of the species entries", required=True
    )
    parser.add_argument(
        "--column_name_authority",
        help="column name of the preferred authority entries", required=True
    )
    parser.add_argument(
        "--output_filepath",
        help="path to the output file with csv extension",
        required=True,
    )
    parser.add_argument(
        "--place", help="source name from which the list is obtained", required=True
    )
    args = parser.parse_args()

    save_taxon_keys(args)
