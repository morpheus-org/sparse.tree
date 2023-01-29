#!/bin/bash

SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"
FEATURES_PATH=$SCRIPT_PATH/../features
PROFILINGS_PATH=$SCRIPT_PATH/../profiling_runs
ffeatures=$FEATURES_PATH/square_set-features.csv


for frun in $PROFILINGS_PATH/*; do
    echo "python $SCRIPT_PATH/tuned.py --features=$ffeatures --runtimes=$frun"
    python $SCRIPT_PATH/test.py --features=$ffeatures --runtimes=$frun
done

