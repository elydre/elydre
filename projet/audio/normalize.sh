#!/bin/bash

TARGET=-12

rm -rf normalized
mkdir normalized

for f in *.flac; do
  echo -e "\e[1m$f\e[0m"

  # Analyse en JSON
  analysis=$(ffmpeg -hide_banner -i "$f" -af loudnorm=I=$TARGET:TP=-1.5:LRA=11:print_format=json -f null - 2>&1  | grep -A 12 "{")
  
  # Extraction avec jq
  I=$(echo "$analysis" | jq -r '.input_i')
  TP=$(echo "$analysis" | jq -r '.input_tp')
  LRA=$(echo "$analysis" | jq -r '.input_lra')
  THRESH=$(echo "$analysis" | jq -r '.input_thresh')
  OFFSET=$(echo "$analysis" | jq -r '.target_offset')

  # Calcul du gain appliqué
  gain=$(awk -v t=$TARGET -v i=$I 'BEGIN {printf "%.2f", t - i}')

  echo "    Gain: $gain dB"

  # Application (pass 2)
  ffmpeg -hide_banner -loglevel error -y -i "$f" \
    -af loudnorm=I=$TARGET:TP=-1.5:LRA=11:measured_I=$I:measured_TP=$TP:measured_LRA=$LRA:measured_thresh=$THRESH:offset=$OFFSET:linear=true \
    -c:a flac "normalized/$f"
done

echo "✅ Fichiers normalisés disponibles dans ./normalized/"
