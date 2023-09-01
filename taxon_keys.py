#!/usr/bin/env python
# coding: utf-8

"""
Author       : Aditya Jain
Date Started : May 9, 2022

Edited by    : Katriona Goldmann, Levan Bokeria
About        : This script fetches unique taxon keys for species list
                from GBIF database
"""

from pygbif import species as species_api
import pandas as pd
import argparse
import warnings

def get_gbif_key_backbone(name):
    """given a species name, this function returns the unique gbif key and
    other attributes using backbone API
    """

    # default values
    taxon_key = [-1]
    order = ["NA"]
    family = ["NA"]
    genus = ["NA"]
    search_species = [name]
    # the name returned on search, can be different from the search
    gbif_species = ["NA"]
    confidence = [""]
    status = ["NA"]
    match_type = ["NONE"]

    data = species_api.name_backbone(name=name, strict=True)

    # if rank not a key in data
    if "rank" not in data:
        print(name + " returns no rank")

    elif data["rank"] != "SPECIES":
        print(name + " returns rank=" + data["rank"] + " instead of SPECIES")

    else:
        if data["matchType"] == "NONE":
            confidence = [data["confidence"]]

        else:

            taxon_key = [data["usageKey"]]
            order = [data["order"]]
            family = [data["family"]]
            genus = [data["genus"]]
            confidence = [data["confidence"]]
            gbif_species = [data["species"]]
            status = [data["status"]]
            match_type = [data["matchType"]]

        df = pd.DataFrame(
            list(
                zip(
                    taxon_key,
                    order,
                    family,
                    genus,
                    search_species,
                    gbif_species,
                    confidence,
                    status,
                    match_type,
                )
            ),
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
        )
        return df



