#!/bin/bash
# Wrapper script to run fetch_images_split_dwca.sh for each region

# List of region names (update as needed)
regions=(
    "anguilla"
    "costarica"
    "japan"
    "kenya-uganda"
    "madagascar"
    "namibia"
    "nigeria"
    "singapore"
    "thailand"
    "uksi"
)

# Path to the fetch_images_split_dwca.sh script
SCRIPT_DIR="$(dirname "$0")"
FETCH_SCRIPT="$SCRIPT_DIR/fetch_images_split_dwca.sh"

for region in "${regions[@]}"; do
    echo "Running fetch_images_split_dwca for region: $region"
    sbatch --output=download_$region.out --job-name=download_$region "$FETCH_SCRIPT" "$region"
    if [ $? -ne 0 ]; then
        echo "Error running fetch_images_split_dwca for $region" >&2
    fi
done
