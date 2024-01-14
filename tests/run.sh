#!/bin/bash

pushd /core

for folder in /core/*; do
    echo $folder
    folder=${folder%/}  # Remove trailing slash
    if [ -d "$folder" ] && [ "$(basename "$folder")" != "__pycache__" ]; then
        echo "Processing folder: $folder"
        $folder/cli.py protoc
    fi
done

popd
