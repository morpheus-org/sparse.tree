#!/bin/bash

SCRIPT_PATH="$(
  cd -- "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"

if [ "$#" -lt "2" ]; then
  echo -e "Script requires 2 runtime argument to run."
  echo -e "\t\$1 : Absolute path to the file with the list of matrices"
  echo -e "\t\$2 : Directory with the matrices" 
  exit 0
fi

fmat=$1
dmat=$2

outfile=$(basename $fmat)
outfile=${outfile%.*}
outfile="$(dirname $fmat)/list-$outfile.txt"

touch $outfile


for mat_path in $dmat/*/*; do
  mat=$(basename $mat_path)
  while IFS= read -r line
  do
    if [ "$mat" == "$line" ]; then
      echo "$mat"
      echo "$mat_path" >> $outfile
      continue
    fi
  done < "$fmat"
done

# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-a64fx-square_set-openmp-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices
# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-a64fx-square_set-serial-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices
# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-ampere-square_set-cuda-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices
# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-archer2-square_set-openmp-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices
# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-archer2-square_set-serial-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices
# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-cirrus-square_set-cuda-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices
# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-cirrus-square_set-openmp-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices
# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-cirrus-square_set-serial-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices
# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-instinct-square_set-hip-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices
# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-xci-square_set-openmp-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices
# ./generate_paths.sh /lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-xci-square_set-serial-1000.txt /lustre/home/ri-cstylianou/sparse.tree/data/square_set/matrices