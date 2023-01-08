#!/bin/bash --login

RUN_PATH=$1
DATA_PATH=$2
EXE=$3
BACKEND=$4
REPS=$5

module load gcc/10.2.0

if [ "serial" == "$BACKEND" ]; then
  export OMP_NUM_THREADS=36 
  ncpus="--tasks-per-node=1 --cpus-per-task=1"
  NTHREADS=1
  NGPUS=0
elif [ "openmp" == "$BACKEND" ]; then
  export OMP_NUM_THREADS=36 
  export OMP_PROC_BIND=close
  export OMP_PLACES=cores
  ncpus="--tasks-per-node=1 --cpus-per-task=36"
  ngpus=""
  NTHREADS=36
  NGPUS=0
elif [ "cuda" == "$BACKEND" ]; then
  module unload gcc
  module load nvidia/nvhpc-nompi/22.2

  export OMP_NUM_THREADS=1 
  ncpus=""
  ngpus="--gres=gpu:1"
  NTHREADS=1
  NGPUS=1
fi

FMT_ID=0

echo -e "Generating features for $BACKEND backend:"
for FILE in $DATA_PATH/*; do 
  MATRIX=$(basename $FILE)
  MATRIX_FILE="$FILE/$MATRIX.mtx"
  OUTDIR="$RUN_PATH/$MATRIX"

  rm -rf $OUTDIR && mkdir -p $OUTDIR
  
  echo -e "\t$MATRIX"
  srun --hint=nomultithread --exclusive \
     --nodes=1 --ntasks=1 $ncpus $ngpus \
     $EXE $MATRIX_FILE $OUTDIR $REPS \
     --kokkos-threads=$NTHREADS --kokkos-num-devices=$NGPUS
done

