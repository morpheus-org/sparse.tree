#!/bin/bash --login

SCRIPT_PATH=$1
NAME=$2
FFEATURES=$3
FRUN=$4

eval "$(/work/d403/d403/cstyl16/miniconda3/bin/conda shell.bash hook)"
conda activate test_env

experiment=$(basename $FRUN)
LOG_FILE=$SCRIPT_PATH/$experiment.log
MPLCONFIGDIR=$SCRIPT_PATH python $SCRIPT_PATH/$NAME.py --features=$FFEATURES --runtimes=$FRUN 2>&1 | tee -a $LOG_FILE