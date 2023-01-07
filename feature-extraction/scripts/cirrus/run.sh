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

CIRRUS_SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"

if [ "$#" -lt "3" ]; then
  echo -e "Script requires 3 runtime arguments to run."
  echo -e "\t\$1 : Backend [serial | openmp | cuda]"
  echo -e "\t\$2 : Dataset [small_set | square_set]"
  echo -e "\t\$3 : Budget  - Account budget to be charged for the run."
  exit 0
fi

backend=$1
DATA_SET=$2
budget=$3
queue="standard"
qos="standard"

if [ "serial" == "$backend" ]; then
  queue="standard"
  qos="standard"
  ncpus="--tasks-per-node=1 --cpus-per-task=1"
  ngpus=""
elif [ "openmp" == "$backend" ]; then
  queue="standard"
  qos="standard"
  ncpus="--tasks-per-node=1 --cpus-per-task=36"
  ngpus=""
elif [ "cuda" == "$backend" ]; then
  queue="gpu"
  qos="gpu"
  ngpus="--gres=gpu:1"
else
 echo "Invalid backend ($backend)!"
 echo -e "\tAvailable backends: [serial | openmp | cuda]"
 exit 1
fi

if [ -z "$3" ]; then
  ACCOUNT=e609
else
  ACCOUNT=$budget
fi

DATA_SET=small_set
DATA_PATH=$CIRRUS_SCRIPT_PATH/../../../data/$DATA_SET/matrices
RUN_PATH=$CIRRUS_SCRIPT_PATH/run/$DATA_SET/$backend
EXE=$CIRRUS_SCRIPT_PATH/build/$backend/src/SparseTree_Features

echo -e "Building Feature Extraction routine:"
echo -e "\tScript Path : $CIRRUS_SCRIPT_PATH"
echo -e "\tRun Path    : $RUN_PATH"
echo -e "\tData Path   : $DATA_PATH"
echo -e "\tExecutable  : $EXE"
echo -e "\tBackend : $backend"
echo -e "\tBudget  : $budget"
echo -e "\tQueue   : $queue"

mkdir -p $RUN_PATH

sbatch --exclusive --nodes=1 --time=24:00:00 --partition=$queue \
  --qos=$qos $ncpus $ngpus --account=$ACCOUNT --job-name=fe-$backend-run \
  --output=$RUN_PATH/$queue-report.out \
  --error=$RUN_PATH/$queue-report.err \
  $CIRRUS_SCRIPT_PATH/run.fe.slurm $RUN_PATH $DATA_PATH $EXE $backend