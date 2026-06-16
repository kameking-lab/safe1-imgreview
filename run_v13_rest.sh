#!/bin/bash
cd /c/Users/kanet/20260522/instagram-automation
GEN=/c/Users/kanet/20260522/safe1/gen_v13.mjs
LOG=/c/Users/kanet/20260522/safe1/gen_v13_rest.log
echo "=== v13 rest START ===" > "$LOG"
for c in 2 3 4 5 6; do
  echo "--- case $c ---" >> "$LOG"
  node "$GEN" --case=$c --n=3 >> "$LOG" 2>&1
  echo "done case $c" >> "$LOG"
done
echo "=== v13 rest DONE ===" >> "$LOG"
