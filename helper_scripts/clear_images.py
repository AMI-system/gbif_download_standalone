import os
import shutil

import pandas as pd

home_dir = "/bask/projects/v/vjgo8416-amber/projects/gbif_download_standalone/"
data_dir = "/bask/projects/v/vjgo8416-amber/data/gbif_download_standalone/"


checklist = pd.read_csv(
    os.path.join(home_dir, "species_checklists", "costarica-moths-keys-nodup.csv")
    )

for idx, iRow in checklist.iterrows():

    if iRow["gbif_species_name"] != "NotAvail":

        # Get the folder name
        dirname = os.path.join(
            data_dir, "gbif_images", iRow["family_name"],
            iRow["genus_name"], iRow["gbif_species_name"])

        if os.path.isdir(dirname):
            print('Deleting...')
            shutil.rmtree(dirname)
            print('Deleted!')
        else:
            print('Not a dir')
