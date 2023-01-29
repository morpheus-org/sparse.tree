#!/bin/bash

SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"
FEATURES_PATH=$SCRIPT_PATH/../features
PROFILINGS_PATH=$SCRIPT_PATH/../profiling_runs
ffeatures=$FEATURES_PATH/square_set-features.csv

if [ "$#" -lt "1" ]; then
  echo -e "Script requires 1 runtime argument to run."
  echo -e "\t\$1 : Experiment Name [tune]"
  exit 0
fi

name=$1

for frun in $PROFILINGS_PATH/*; do
    experiment=$(basename $frun)
    sbatch --exclusive --nodes=1 --time=24:00:00 --partition=gpu \
    --qos=gpu --gres=gpu:1 --account=d403-cs --job-name=tuning_dt \
    --output=$SCRIPT_PATH/tuner_$experiment.out --error=$SCRIPT_PATH/tuner_$experiment.err \
    $SCRIPT_PATH/run.tuning.slurm $SCRIPT_PATH $name $ffeatures $frun
done
