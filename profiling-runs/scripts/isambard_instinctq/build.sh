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
INSTINCTQ_SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"

if [ "$#" -lt "3" ]; then
  echo -e "Script requires 3 runtime arguments to run."
  echo -e "\t\$1 : Backend [hip]"
  echo -e "\t\$2 : A valid path to Morpheus Installation"
  echo -e "\t\$3 : A valid path to Kokkos Installation"
  exit 0
fi

backend=$1
morpheus_dir=$2
kokkos_dir=$3
queue="instinctq"

if [ ! -d "$morpheus_dir" ];then
  echo "Path to Morpheus Installation ($morpheus_dir) does not exist!"
  exit 1
fi

if [ ! -d "$kokkos_dir" ];then
  echo "Path to Kokkos Installation ($kokkos_dir) does not exist!"
  exit 1
fi

PROFILING_ROOT_DIR=$INSTINCTQ_SCRIPT_PATH/../..
BUILD_PATH=$INSTINCTQ_SCRIPT_PATH/build/$backend

echo -e "Building Feature Extraction routine:"
echo -e "\tScript Path              : $INSTINCTQ_SCRIPT_PATH"
echo -e "\tProfiling Run Root Path  : $PROFILING_ROOT_DIR"
echo -e "\tBuild Path               : $BUILD_PATH"
echo -e "\tBackend : $backend"
echo -e "\tQueue   : $queue"
echo -e "\tMorpheus Installation : $morpheus_dir"
echo -e "\tKokkos Installation   : $kokkos_dir"

rm -rf $BUILD_PATH && mkdir -p $BUILD_PATH

PROFILING_INSTALL_DIR=$INSTINCTQ_SCRIPT_PATH/installs/$backend

module use -a /lustre/projects/bristol/modules/modulefiles
module load cmake

BACKEND_SERIAL="ON"
BACKEND_HIP="ON"
CXX_COMPILER=$(which hipcc)

mkdir -p $BUILD_PATH && cd $BUILD_PATH
cmake $PROFILING_ROOT_DIR -DCMAKE_CXX_COMPILER=${CXX_COMPILER} \
                           -DCMAKE_BUILD_TYPE=Release \
                           -DCMAKE_INSTALL_PREFIX=${PROFILING_INSTALL_DIR} \
                           -DCMAKE_CXX_EXTENSIONS=Off \
                           -DMorpheus_ROOT=${morpheus_dir} \
                           -DSparseTree_ENABLE_SERIAL=${BACKEND_SERIAL} \
                           -DSparseTree_ENABLE_HIP=${BACKEND_HIP} && make -j