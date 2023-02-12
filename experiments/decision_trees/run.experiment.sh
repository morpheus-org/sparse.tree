#!/bin/bash

SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"
FEATURES_PATH=$SCRIPT_PATH/../features
PROFILINGS_PATH=$SCRIPT_PATH/../profiling_runs
ffeatures=$FEATURES_PATH/square_set-features-14.csv

if [ "$#" -lt "2" ]; then
  echo -e "Script requires 1 runtime argument to run."
  echo -e "\t\$1 : System [cirrus | p3]"
  echo -e "\t\$2 : Experiment Name [baseline | tune]"
  exit 0
fi

system=$1
name=$2

# for frun in $PROFILINGS_PATH/*; do
frun=/lustre/home/ri-cstylianou/sparse.tree/experiments/profiling_runs/archer2-square_set-openmp-1000.csv
    experiment=$(basename $frun)
    if [ "cirrus" == "$system" ]; then
      sbatch --exclusive --nodes=1 --time=24:00:00 --partition=gpu \
      --qos=gpu --gres=gpu:1 --account=d403-cs --job-name=tuning_dt \
      --output=$SCRIPT_PATH/tuner_$experiment.out --error=$SCRIPT_PATH/tuner_$experiment.err \
      $SCRIPT_PATH/run.tuning.slurm $SCRIPT_PATH $name $ffeatures $frun
    elif [ "p3" == "$system" ]; then
      qsub -q milanq -l select=1:mem=128gb:ncpus=128 -l place=excl -l walltime=24:00:00 \
           -o $SCRIPT_PATH/tuner_$experiment.out -e $SCRIPT_PATH/tuner_$experiment.err \
           -N "tuning_dt" \
           -v SCRIPT_PATH=$SCRIPT_PATH,NAME=$name,FEATURES=$ffeatures,RUNS=$frun \
           $SCRIPT_PATH/run.$name.pbs
    fi 
# done