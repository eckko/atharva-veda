#!/bin/sh
# Fetch source S1 (DharmicData AtharvaVeda JSON, 20 files) into DIR.
# Usage: sh fetch_s1.sh DIR
set -e
dir="${1:?usage: fetch_s1.sh DIR}"
mkdir -p "$dir"
for k in $(seq 1 20); do
  curl -sSf -L -o "$dir/atharvaveda_kaanda_$k.json" \
    "https://raw.githubusercontent.com/bhavykhatri/DharmicData/main/AtharvaVeda/atharvaveda_kaanda_$k.json"
done
( cd "$dir" && sha256sum atharvaveda_kaanda_*.json )
