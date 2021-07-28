#!/bin/bash
# ffmpeg convert all files to wav format
INPUT_DIR='/Users/arvindsuresh/projects/ai/datasets/podcasts/btcsessions/*.m4a'
OUTPUT_DIR='/Users/arvindsuresh/projects/ai/datasets/podcasts/btcsessions/'
i = 0
for f in $INPUT_DIR
do
  ((i = i + 1))
  ffmpeg -i $f -ar 22050 -ac 1 -af afftdn $OUTPUT_DIR$i.wav
done
