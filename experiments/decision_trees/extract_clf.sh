#!/bin/bash

SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"
FEATURES_PATH=$SCRIPT_PATH/../features
PROFILINGS_PATH=$SCRIPT_PATH/../profiling_runs
PARAMETERS_PATH=$SCRIPT_PATH/tune
ffeatures=$FEATURES_PATH/square_set-features.csv

for frun in $PROFILINGS_PATH/*; do
  experiment_csv=$(basename $frun)
  experiment=${experiment_csv%.*}
  fparams=$PARAMETERS_PATH/$experiment/results.csv
  echo $experiment
  python $SCRIPT_PATH/extract_clf.py --features=$ffeatures --runtimes=$frun --parameters=$fparams
done
