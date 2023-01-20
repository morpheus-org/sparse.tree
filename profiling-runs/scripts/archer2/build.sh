#!/bin/sh
# build.sh
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

# Builds Morpheus Benchmark on the available systems and queues.
ARCHER2_SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"

if [ "$#" -lt "4" ]; then
  echo -e "Script requires 4 runtime arguments to run."
  echo -e "\t\$1 : Backend [Serial | OpenMP ]"
  echo -e "\t\$2 : A valid path to Morpheus Installation"
  echo -e "\t\$3 : A valid path to Kokkos Installation"
  echo -e "\t\$4 : Budget  - Account budget to be charged for the run."
  exit 0
fi

backend=$1
morpheus_dir=$2
kokkos_dir=$3
budget=$4
queue="standard"
qos="standard"

if [ "serial" == "$backend" ] || [ "openmp" == "$backend" ]; then
  queue="standard"
  qos="standard"
  ngpus=""
else
 echo "Invalid backend ($backend)!"
 echo -e "\tAvailable backends: [serial | openmp ]"
 exit 1
fi

if [ ! -d "$morpheus_dir" ];then
  echo "Path to Morpheus Installation ($morpheus_dir) does not exist!"
  exit 1
fi

if [ ! -d "$kokkos_dir" ];then
  echo "Path to Kokkos Installation ($kokkos_dir) does not exist!"
  exit 1
fi

if [ -z "$4" ]; then
  ACCOUNT=e609
else
  ACCOUNT=$budget
fi

PROFILING_ROOT_DIR=$ARCHER2_SCRIPT_PATH/../..
BUILD_PATH=$ARCHER2_SCRIPT_PATH/build/$backend

echo -e "Building Feature Extraction routine:"
echo -e "\tScript Path              : $ARCHER2_SCRIPT_PATH"
echo -e "\tProfiling Run Root Path  : $PROFILING_ROOT_DIR"
echo -e "\tBuild Path               : $BUILD_PATH"
echo -e "\tBackend : $backend"
echo -e "\tBudget  : $budget"
echo -e "\tQueue   : $queue"
echo -e "\tMorpheus Installation : $morpheus_dir"
echo -e "\tKokkos Installation   : $kokkos_dir"

rm -rf $BUILD_PATH && mkdir -p $BUILD_PATH

sbatch --exclusive --nodes=1 --time=24:00:00 --partition=$queue \
  --qos=$qos $ngpus --account=$ACCOUNT --job-name=profiling-$queue-build \
  --output=$BUILD_PATH/$queue-report.out \
  --error=$BUILD_PATH/$queue-report.err \
  $ARCHER2_SCRIPT_PATH/build.profiling.slurm $ARCHER2_SCRIPT_PATH $PROFILING_ROOT_DIR $BUILD_PATH $backend $morpheus_dir $kokkos_dir