#!/bin/bash
cd /c/Users/kanet/20260522/instagram-automation
GEN=/c/Users/kanet/20260522/safe1/gen_v12.mjs
LOG=/c/Users/kanet/20260522/safe1/gen_v12_all.log
echo "=== run_all_v12 START ===" > "$LOG"
for c in 1 2 3 4 5 6; do
  for k in illust photo; do
    echo "--- case $c $k ---" >> "$LOG"
    node "$GEN" --case=$c --kind=$k --n=5 >> "$LOG" 2>&1
    echo "done case $c $k" >> "$LOG"
  done
done
echo "=== run_all_v12 DONE ===" >> "$LOG"
