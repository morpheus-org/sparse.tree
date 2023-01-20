#!/bin/bash --login

RUN_PATH=$1
DATA_PATH=$2
EXE=$3
BACKEND=$4
REPS=$5

module load gcc/10.2.0

if [ "serial" == "$BACKEND" ]; then
  export OMP_NUM_THREADS=18 
  ncpus="--hint=nomultithread --exclusive --nodes=1 --ntasks=1 --tasks-per-node=1 --cpus-per-task=16"
  NTHREADS=1
  NGPUS=0
elif [ "openmp" == "$BACKEND" ]; then
  export OMP_NUM_THREADS=18 
  export OMP_PROC_BIND=close
  export OMP_PLACES=cores
  ncpus="--hint=nomultithread --exclusive --nodes=1 --ntasks=1 --tasks-per-node=1 --cpus-per-task=16"
  ngpus=""
  NTHREADS=18
  NGPUS=0
fi

SET=$(basename $DATA_PATH)
LOG_FILE="$RUN_PATH/$SET.log"
echo -e "Generating profiling runs for $BACKEND backend:"
for FILE in $DATA_PATH/*; do 
  MATRIX=$(basename $FILE)
  MATRIX_FILE="$FILE/$MATRIX.mtx"
  OUTDIR="$RUN_PATH/matrices/$MATRIX"

  mkdir -p $OUTDIR
  
  echo -e "\t$MATRIX"
  srun $ncpus $ngpus \
     $EXE $MATRIX_FILE $OUTDIR $REPS \
     --kokkos-threads=$NTHREADS --kokkos-num-devices=$NGPUS 2>&1 | tee -a $LOG_FILE
done

