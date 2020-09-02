#!/bin/bash
INPUT_DIRECTORY="/Users/arvindsuresh/projects/ai/datasets/splits/CenterChannel100s/"

for f in $INPUT_DIRECTORY/*.wav
do
    docker run -v $INPUT_DIRECTORY:/data -v /Users/arvindsuresh/projects/ai/datasets/stems:/out -v /Users/arvindsuresh/projects/ai/datasets/spleetermodels:/model -e MODEL_PATH=/model -m 16g researchdeezer/spleeter separate -i /data/"${f##*/}" -p spleeter:2stems -o /out/
done
