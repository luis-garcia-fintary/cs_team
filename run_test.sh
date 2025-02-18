#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_file_path> <input_string> <output_file_path>"
    exit 1
fi

INPUT_FILE=$1
INPUT_STRING=$2
OUTPUT_FILE=$3

# Navigate to the repository (assumed to be cloned in the home directory)
REPO_DIR=~/cs_team  # Change this path if cloned elsewhere

if [ ! -d "$REPO_DIR" ]; then
    echo "Repository directory not found. Cloning..."
    git clone https://<your_token>@github.com/luis-garcia-fintary/cs_team.git "$REPO_DIR"
fi

# Navigate to repo and pull latest changes
cd "$REPO_DIR" || exit
git pull origin main

# Run the Python script with the provided arguments
python3 test.py "$INPUT_FILE" "$INPUT_STRING" "$OUTPUT_FILE"
