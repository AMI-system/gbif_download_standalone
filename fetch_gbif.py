#!/usr/bin/env python
# coding: utf-8

"""
Author       : Aditya Jain
Date Started : May 10, 2022

Edited by    : Katriona Goldmann, Levan Bokeria
About        : This script scraps data from GBIF for a list of moth species
"""


import pandas as pd
from pygbif import occurrences as occ
import pandas as pd
import os
import urllib
import json
import time
import math
import argparse
from urllib.parse import quote  

# Downloading gbif data
def inat_metadata_gbif(data):
    """returns the relevant gbif metadata for a GBIF observation"""

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
        "datasetName",
    ]

    meta_data = {}

    for field in fields:
        if field in data.keys():
            meta_data[field] = data[field]
        else:
            meta_data[field] = ""

    return meta_data

def get_gbif_images(moth_data, resume_session, write_dir, MAX_DATA_SP, LIMIT_DOWN, MAX_SEARCHES ):
    
    import pandas as pd
    from pygbif import occurrences as occ
    import pandas as pd
    import os
    import urllib
    import json
    import time
    import math
    import argparse
    from urllib.parse import quote  

    
    dataset_list = []
    taxon_key = list(moth_data["taxon_key_gbif_id"])  # list of taxon keys
    species_name = list(
        moth_data["search_species_name"]
    )  # list of species name that is searched
    gbif_species_name = list(
        moth_data["gbif_species_name"]
    )  # list of species name returned by gbif [can be different from above or NA]
    genus_name = list(moth_data["genus_name"])  
    family_name = list(moth_data["family_name"]) 
    columns = ["taxon_key_gbif_id", "search_species_name", "gbif_species_name", "count"]
    count_list = pd.DataFrame(columns=columns, dtype=object)

    # if resuming the download session
    if resume_session is True:
        count_list = pd.read_csv(write_dir + "datacount.csv")

    for i in range(len(taxon_key)):
        if int(taxon_key[i]) in count_list["taxon_key_gbif_id"].tolist():
            print(f"Already downloaded for {species_name[i]}")
            continue
        print(
            "Downloading for: ",
            species_name[i],
            "(" + str(i) + "/" + str(len(taxon_key)) + ")",
        )
        begin = time.time()
        if taxon_key[i] == -1:  # taxa not there on GBIF
            count_list = pd.append([count_list,
                pd.DataFrame([[-1, species_name[i], "NA", "NA"]], columns=columns)],
                ignore_index=True,
            )
        else:
            data = occ.search(taxonKey=int(taxon_key[i]), mediatype="StillImage", limit=1)
            total_count = data["count"]

            if total_count == 0:  # no image data found for the species
                count_list = pd.concat([count_list,
                    pd.DataFrame(
                        [[int(taxon_key[i]), species_name[i], gbif_species_name[i], 0]],
                        columns=columns,
                    )],
                    ignore_index=True,
                )
            else:
                image_count = 0  # images downloaded for every species
                max_count = min(total_count, MAX_DATA_SP)
                total_pag = math.ceil(
                    MAX_SEARCHES / LIMIT_DOWN
                )  # total pages to be fetched with max 300 entries each
                offset = 0

                family = family_name[i]
                genus = genus_name[i]
                species = gbif_species_name[i]

                m_data = {}  # dictionary variable to store metadata
                write_loc = write_dir + family + "/" + genus + "/" + species

                try:
                    os.makedirs(write_loc)
                    # creating hierarchical structure for image storage
                except OSError:
                    pass

                for j in range(total_pag):
                    try:
                        data = occ.search(
                            taxonKey=int(taxon_key[i]),
                            mediatype="StillImage",
                            limit=LIMIT_DOWN,
                            offset=offset,
                        )
                    # add exception for occ.search error
                    except Exception as e:
                        print("Error occured: ", e)
                        tot_points = 0
                    else:
                        tot_points = len(data["results"])

                    for k in range(tot_points):
                        if (
                            data["results"][k]["media"]
                            and "lifeStage" in data["results"][k].keys()
                        ):
                            if (
                                data["results"][k]["lifeStage"] == "Adult"
                                or data["results"][k]["lifeStage"] == "Imago"
                            ):
                                gbifid = data["results"][k]["gbifID"]
                                first_media = data["results"][k]["media"][0]

                                if "identifier" in first_media.keys():
                                    image_url = first_media["identifier"]                             


                                    try:                                    
                                        # catch non-ascii characters in url
                                        if not all(ord(c) < 128 for c in image_url):
                                            image_url = quote(image_url, safe='/:?=&')


                                        urllib.request.urlretrieve(
                                            image_url, write_loc + "/" + gbifid + ".jpg"
                                        )
                                        image_count += 1
                                        meta_data = inat_metadata_gbif(
                                            data["results"][k]
                                        )  # fetching metadata
                                        m_data[gbifid] = meta_data
                                        if meta_data["datasetName"] not in dataset_list:
                                            pd.concat([dataset_list, meta_data["datasetName"]])

                                    # if image_url is not valid
                                    except urllib.error.HTTPError:
                                        continue
                                    except: # catch all other exceptions
                                        print("Unknown error occured for URL " + image_url)
                                        continue
                        if image_count >= MAX_DATA_SP:
                            break

                    offset += LIMIT_DOWN
                    if image_count >= MAX_DATA_SP:
                        break

                with open(write_loc + "/" + "metadata.txt", "w") as outfile:
                    json.dump(m_data, outfile)

                count_list = pd.concat([count_list,
                    pd.DataFrame(
                        [
                            [
                                int(taxon_key[i]),
                                species_name[i],
                                gbif_species_name[i],
                                int(image_count),
                            ]
                        ],
                        columns=columns,
                    )],
                    ignore_index=True,
                )

                end = time.time()
                print(
                    "Time taken to download data for ",
                    gbif_species_name[i],
                    " is - ",
                    round(end - begin),
                    "sec for ",
                    image_count,
                    " images",
                )

        count_list.to_csv(write_dir + "datacount.csv", index=False)


    print("I'm finished downloading all the data! :)")