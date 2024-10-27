#!/bin/bash

dataset="$1"
force_refresh="$2"
dir_name="data"

if [ ! -d "$dir_name" ]; then
    echo "Error: Directory '$dir_name' does not exist."
    exit 1
fi

for file in "$dir_name"/*; do
    if [ -f "$file" ]; then
        echo "$(basename "$file")"
    else
        echo "refreshing data"
    fi
done