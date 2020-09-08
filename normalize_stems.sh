#!/bin/bash
INPUT_DIRECTORY="/Users/arvindsuresh/projects/ai/datasets/stems/"
OUTPUT_DIRECTORY="/Users/arvindsuresh/projects/ai/datasets/normalized/"

for f in $INPUT_DIRECTORY/*
do
    ffmpeg -i $f/vocals.wav -ar 22050 -ac 1 -af afftdn $OUTPUT_DIRECTORY/Mono22kCleanVocals_"${f##*/}".wav  
    sox $OUTPUT_DIRECTORY/Mono22kCleanVocals_"${f##*/}".wav $OUTPUT_DIRECTORY/normalized_"${f##*/}".wav silence -l 1 0.1 0.2% -1 0.5 0.2% 
done
