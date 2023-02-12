#!/bin/bash

SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"

if [ "$#" -lt "2" ]; then
  echo -e "Script requires 2 runtime argument to run."
  echo -e "\t\$1 : Experiment Name [baseline | test]"
  echo -e "\t\$2 : Number of features [10 | 14]"
  exit 0
fi

name=$1
nfeatures=$2

FEATURES_PATH=$SCRIPT_PATH/../features
PROFILINGS_PATH=$SCRIPT_PATH/../profiling_runs
ffeatures=$FEATURES_PATH/square_set-features-$nfeatures.csv


for frun in $PROFILINGS_PATH/*; do
    echo "python $SCRIPT_PATH/tuned.py --features=$ffeatures --runtimes=$frun --nfeatures=$nfeatures"
    python $SCRIPT_PATH/$name.py --features=$ffeatures --runtimes=$frun --nfeatures=$nfeatures
done

