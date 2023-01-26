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
  echo -e "\t\$1 : Experiment Name [baseline | balanced_data_tuning | max_depth_tuning] | "
  echo -e "\t                       min_samples_tuning | splitter_tuning | criterion_tuning | "
  echo -e "\t                       max_features_tuning]"
  exit 0
fi

name=$1

for frun in $PROFILINGS_PATH/*; do
    echo "python $SCRIPT_PATH/$name.py --features=$ffeatures --runtimes=$frun"
    python $SCRIPT_PATH/$name.py --features=$ffeatures --runtimes=$frun
done

# merge accuracy of each experiment in single file
fout=$SCRIPT_PATH/$name/$name-accuracy.csv
write_header=1
for experiment in $SCRIPT_PATH/$name/*/; do
    FILE=$experiment/accuracy.csv
    if [ $write_header -eq 1 ]; then
        header="$(sed -n "1 p" $FILE)"
        echo $header > $fout
        write_header=0
    fi
    # count lines in a file
    nlines=$(wc -l < $FILE)
    for i in $(seq 2 ${nlines}); do
      entry="$(sed -n "$i p" $FILE)"
      echo $entry >> $fout
    done
done
