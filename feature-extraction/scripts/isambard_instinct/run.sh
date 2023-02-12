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

SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"

if [ "$#" -lt "2" ]; then
  echo -e "Script requires 2 runtime arguments to run."
  echo -e "\t\$1 : Backend [serial | openmp]"
  echo -e "\t\$2 : Dataset [small_set | square_set]"
  exit 0
fi

backend=$1
DATA_SET=$2
budget=$3
queue="instinctq"

if [ "serial" == "$backend" ] || [ "openmp" == "$backend" ]; then
  queue="instinctq"
else
 echo "Invalid backend ($backend)!"
 echo -e "\tAvailable backends: [serial | openmp]"
 exit 1
fi

if [ "small_set" != "$DATA_SET" ] && [ "square_set" != "$DATA_SET" ]; then
 echo "Invalid dataset ($DATA_SET)!"
 echo -e "\tAvailable datasets: [small_set | square_set]"
 exit 1
fi

DATA_PATH=$SCRIPT_PATH/../../../data/$DATA_SET/matrices
RUN_PATH=$SCRIPT_PATH/run/$DATA_SET/$backend
EXE=$SCRIPT_PATH/build/$backend/src/SparseTree_Features

echo -e "Building Feature Extraction routine:"
echo -e "\tScript Path : $SCRIPT_PATH"
echo -e "\tRun Path    : $RUN_PATH"
echo -e "\tData Path   : $DATA_PATH"
echo -e "\tExecutable  : $EXE"
echo -e "\tBackend : $backend"
echo -e "\tQueue   : $queue"

mkdir -p $RUN_PATH

INCREMENT=50
LOW_BOUND=0
UPPER_BOUND=$(( $LOW_BOUND + $INCREMENT ))

while [ $LOW_BOUND -lt 2200 ]; do
  DATADIR=$DATA_PATH/$LOW_BOUND\_$UPPER_BOUND

  # sbatch --exclusive --nodes=1 --time=24:00:00 --partition=$queue \
  #   --qos=$qos $ncpus $ngpus --account=$ACCOUNT --job-name=fe-$backend-run \
  #   --output=$RUN_PATH/$queue-report-$LOW_BOUND\_$UPPER_BOUND.out \
  #   --error=$RUN_PATH/$queue-report-$LOW_BOUND\_$UPPER_BOUND.err \
  #   $SCRIPT_PATH/run.fe.slurm $RUN_PATH $DATADIR $EXE $backend
  
  qsub -q $queue -l select=1:mem=128gb:ncpus=32 -l place=excl -l walltime=24:00:00 \
           -o $RUN_PATH/$queue-report-$LOW_BOUND\_$UPPER_BOUND.out \
           -e $RUN_PATH/$queue-report-$LOW_BOUND\_$UPPER_BOUND.err \
           -N fe-$backend-run \
           -v RUN_PATH=$RUN_PATH,DATADIR=$DATADIR,EXE=$EXE,BACKEND=$backend \
           $SCRIPT_PATH/run.fe.pbs

  LOW_BOUND=$(( $LOW_BOUND + $INCREMENT ))
  UPPER_BOUND=$(( $UPPER_BOUND + $INCREMENT ))
done