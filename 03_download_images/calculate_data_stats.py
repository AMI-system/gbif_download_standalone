import json
import os
import sys

import pandas as pd

if sys.platform.startswith("linux"):
    data_dir = "/bask/projects/v/vjgo8416-amber/data/gbif_download_standalone/"
elif sys.platform == "darwin":
    data_dir = "/Users/lbokeria/Documents/projects/gbif-species-trainer-data/"
else:
    print("Not linux or mac!")

######################################
checklist_name = "singapore-moths-keys-nodup"

gbif_img_loc = os.path.join(data_dir, "gbif_images")

df = pd.read_csv(os.path.join("../species_checklists", checklist_name+".csv"))

df["n_imgs"] = ""
for idx, row in df.iterrows():

    family  = row["family_name"]
    genus   = row["genus_name"]
    species = row["gbif_species_name"]

    # Check if directory exists
    species_dir = (
        os.path.join(gbif_img_loc, family, genus, species)
        )

    if os.path.isdir(species_dir):
        n_images_on_disk = len(
            [f for f in os.listdir(species_dir) if f.lower().endswith('.jpg')]
            )
        # print(f"{species} Count files method has", n_images_on_disk, "images")

        # Load metadata
        try:

            with open(os.path.join(species_dir, "meta_data.json")) as file:

                meta_data = json.load(file)

            # Count the number of images for this species
            md2_n_imgs_downloaded = 0

            try:
                # 2nd way of counting images
                md2 = pd.read_json(
                    os.path.join(species_dir, "meta_data.json"), orient='index'
                    )

                if md2.empty:
                    md2_n_imgs_downloaded = 0
                else:
                    md2_n_imgs_downloaded = md2["image_is_downloaded"].sum()

            except Exception as e:
                print(e)
                print(f"{species} error counting dataframe way: {e}")

            # Do n images match?
            if n_images_on_disk == md2_n_imgs_downloaded:
                # print(f"N images match for {species_dir}")
                pass
            else:
                print(
                    f"Mismatch! File count {n_images_on_disk}, "
                    f"metadata has {md2_n_imgs_downloaded}, {species_dir}"
                )
        except Exception as e:
            pass
            print(f"No metadata for {species_dir}. Error {e}")

    else:

        n_images_on_disk = 0

    # print(f"{species} has {n_images_on_disk} images")

    # Record this
    df.loc[idx, "n_imgs"] = n_images_on_disk

# Save the df
df.to_csv(os.path.join("../data_stats_files/", "data_stats_"+checklist_name+".csv"))
