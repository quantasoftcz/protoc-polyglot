#!/bin/bash

alias DOCKER_RUN="docker run --rm -v $GITHUB_WORKSPACE/output:/data/output -v $GITHUB_WORKSPACE/tests:/data/tests -v $GITHUB_WORKSPACE/samples:/data/protos protocpolyglot/protoc-polyglot"

for folder in /data/protoc_polyglot/*; do
    echo $folder
    folder=${folder%/}  # Remove trailing slash
    if [ -d "$folder" ] && [ "$(basename "$folder")" != "__pycache__" ]; then
        echo "Processing folder: $folder"
        DOCKER_RUN --languages $folder --service-yml /data/protos/services.yml
    fi
done
