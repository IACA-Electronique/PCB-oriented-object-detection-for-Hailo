#!/bin/bash

# 1. Download dataset based
# 2. Download background
# 3. Download distraction

# All are place in ./data (ignored by gitignore)
# If already exist, prevent user if he want override (test only ./data presence)

################################################################################################################ PARAMETERS

DATA_DIR=.data

################################################################################################################ FUNCTIONS

function download() {
    local name="$1"
    local url="$2"

    local output
    output="$(mktemp).zip"

    if ! wget -q "${url}" -O "${output}" > /dev/null; then
        return 1
    fi

    if ! unzip -o "${output}" -d "${DATA_DIR}/${name}" > /dev/null; then
        rm "$output"
        return 2
    fi

    rm "$output"
}

################################################################################################################ MAIN

if [ -d "${DATA_DIR}" ]; then
    read -r -p "Data folder already exists ('${DATA_DIR}'). Override it? [y/N] " answer
    case "$answer" in
        [Yy]* ) ;;
        * ) echo "Aborted." && exit 1 ;;
    esac
else
    mkdir "${DATA_DIR}"
fi

echo "Downloading data.."
download distraction https://repo.os.iaca-electronique.com/ai/hailo/models/training/pcb-1/distraction.zip || { echo "ERROR: Unable to download distraction." && exit 1; }
download base https://repo.os.iaca-electronique.com/ai/hailo/models/training/pcb-1/dataset_base.yolov11.zip || { echo "ERROR: Unable to download base." && exit 1; }
download background https://repo.os.iaca-electronique.com/ai/hailo/models/training/pcb-1/background.zip || { echo "ERROR: Unable to download background." && exit 1; }

echo -e "\e[1;32mRepository ready, good luck !\e[0m"
