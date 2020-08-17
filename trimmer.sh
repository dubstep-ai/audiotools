#!/bin/bash
# Trim the beginning and the end of the audio file for silences
FILES='*'
for f in $FILES
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  sox $f temp.wav silence 1 0.1 1% reverse
  sox temp.wav ../ModiDatasetTrimmed/$f silence 1 0.1 1% reverse 
done

