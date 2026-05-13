#!/bin/bash
# Generates manifest.json from presentations/ folder
# Run after adding a new presentation: bash build-manifest.sh
cd "$(dirname "$0")"
ls presentations/*.html 2>/dev/null | sed 's|presentations/||' | \
  jq -R -s 'split("\n") | map(select(. != ""))' > manifest.json
echo "Manifest updated: $(cat manifest.json | jq length) presentation(s) found"
