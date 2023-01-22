#!/bin/sh
# run.sh
#
# EPCC, The University of Edinburgh
#
# (c) 2021 - 2023 The University of Edinburgh
#
# Contributing Authors:
# Christodoulos Stylianou (c.stylianou@ed.ac.uk)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

XCI_SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"

if [ "$#" -lt "3" ]; then
  echo -e "Script requires 3 runtime arguments to run."
  echo -e "\t\$1 : Backend [serial | openmp ]"
  echo -e "\t\$2 : Dataset [small_set | square_set]"
  echo -e "\t\$3 : Number of iterations to run SpMV."
  exit 0
fi

backend=$1
DATA_SET=$2
reps=$3
queue="arm"

if [ "serial" != "$backend" ] && [ "openmp" != "$backend" ]; then
  echo "Invalid backend ($backend)!"
  echo -e "\tAvailable backends: [serial | openmp ]"
  exit 1
fi

if [ "small_set" != "$DATA_SET" ] && [ "square_set" != "$DATA_SET" ]; then
  echo "Invalid dataset ($DATA_SET)!"
  echo -e "\tAvailable datasets: [small_set | square_set]"
  exit 1
elif [ "small_set" == "$DATA_SET" ]; then
  MAX_BOUND=100
elif [ "square_set" == "$DATA_SET" ]; then
  MAX_BOUND=2200
fi

DATA_PATH=$XCI_SCRIPT_PATH/../../../data/$DATA_SET/matrices
RUN_PATH=$XCI_SCRIPT_PATH/run/$DATA_SET/$backend
EXE=$XCI_SCRIPT_PATH/build/$backend/src/SparseTree_SpMV

echo -e "Building Feature Extraction routine:"
echo -e "\tScript Path : $XCI_SCRIPT_PATH"
echo -e "\tRun Path    : $RUN_PATH"
echo -e "\tData Path   : $DATA_PATH"
echo -e "\tExecutable  : $EXE"
echo -e "\tBackend : $backend"
echo -e "\tQueue   : $queue"

mkdir -p $RUN_PATH

INCREMENT=50
LOW_BOUND=2000
UPPER_BOUND=$(( $LOW_BOUND + $INCREMENT ))
# MAX_BOUND=2000
while [ $LOW_BOUND -lt $MAX_BOUND ]; do
  DATADIR=$DATA_PATH/$LOW_BOUND\_$UPPER_BOUND

  qsub -q $queue -l select=1:ncpus=32 -l place=excl -l walltime=24:00:00 \
     -o $RUN_PATH/$queue-report-$LOW_BOUND\_$UPPER_BOUND.out \
     -e $RUN_PATH/$queue-report-$LOW_BOUND\_$UPPER_BOUND.err \
     -N "profiling-$queue-run" \
     -v RUNPATH=$RUN_PATH,DATADIR=$DATADIR,EXE=$EXE,BACKEND=$backend,REPS=$reps \
     $XCI_SCRIPT_PATH/run.profiling.pbs

  LOW_BOUND=$(( $LOW_BOUND + $INCREMENT ))
  UPPER_BOUND=$(( $UPPER_BOUND + $INCREMENT ))
done