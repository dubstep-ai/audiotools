#!/bin/bash
# Trim the beginning and the end of the audio file for silences
FILES='*'
for f in $(find ~/data/LatinAmericanTTS -name "22050_*.wav")
do
  dirname=$(dirname "$f")
  filename=$(basename "$f")
  # take action on each file. $f store current file name
  sox $dirname/$filename temp.wav silence 1 0.07 1% reverse
  sox temp.wav $dirname/trimmed_$filename silence 1 0.09 1% reverse 
  #rm $dirname/trimmed_$filename
done

