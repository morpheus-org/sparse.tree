#!/bin/sh
# merge_runs.sh
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

if [ "$#" -lt "1" ]; then
  echo -e "Script requires 1 runtime arguments to run."
  echo -e "\t\$1 : Backend [cuda]"
  echo -e "\t\$2 : Dataset [small_set | square_set]"
  echo -e "\t\$3 : Results Path"
  exit 0
fi

backend=$1
DATA_SET=$2
RUN_PATH=$3

if [ "cuda" != "$backend" ]; then
  echo "Invalid backend ($backend)!"
  echo -e "\tAvailable backends: [hip]"
  exit 1
fi

if [ ! -d $RUN_PATH ]; then
  echo "Results path ($RUN_PATH) does not exist!"
  exit 1
fi

PROCESSED_PATH=$CIRRUS_SCRIPT_PATH/processed/$DATA_SET
OUTFILE="$PROCESSED_PATH/runtimes-$backend.csv"
mkdir -p $PROCESSED_PATH


header=""
for MATRIX_DIR in $RUN_PATH/*; do 
  if [ ! -d $MATRIX_DIR ]; then
    continue
  fi

  MATRIX=$(basename $MATRIX_DIR)
  FILE="$MATRIX_DIR/runtime.csv"
  if [ -z "$header" ]; then
    header="matrix,$(head -n 1 $FILE)"
    echo "$header" > $OUTFILE
  fi

  # count lines in a file
  nlines=$(wc -l < $FILE)
  
  for i in $(seq 2 ${nlines}); do
    entry="$MATRIX,$(sed -n "$i p" $FILE)"
    echo "$entry" >> $OUTFILE
  done
done

