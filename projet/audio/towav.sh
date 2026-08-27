#!/bin/bash

rm -rf wav
mkdir wav

for f in *.flac; do
    echo -e "\e[1m$f\e[0m"

    # remove everything before the first "-" and the "-" itself

    filename=$(basename "$f" .flac)

    # get the number at the beginning of the filename
    number=$(echo "$filename" | grep -o '^[0-9]\+')

    filename="${filename#*-}"

    # trim leading and trailing whitespace
    filename=$(echo "$filename" | sed 's/^[ \t]*//;s/[ \t]*$//')

    # replace spaces with underscores
    filename=$(echo "$filename" | tr ' ' '_')

    ffmpeg -hide_banner -loglevel error -y -i "$f" \
        -ar 44100 -ac 2 -sample_fmt s16 "wav/${number}_${filename}.wav"

done
