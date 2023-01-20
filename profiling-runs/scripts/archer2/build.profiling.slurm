#!/bin/bash --login

ARCHER2_SCRIPT_PATH=$1
PROFILING_ROOT_PATH=$2
BUILD_PATH=$3
BACKEND=$4
MORPHEUS_PATH=$5
KOKKOS_PATH=$6

PROFILING_INSTALL_DIR=$ARCHER2_SCRIPT_PATH/installs/$BACKEND

# Load CMake and GCC
module load cmake gcc/10.2.0

BACKEND_SERIAL="ON"
BACKEND_OPENMP="OFF"

CXX_COMPILER=$(which g++)
if [ "openmp" == "$BACKEND" ]; then
  BACKEND_OPENMP="ON"
  WITH_CUDA=""
fi

mkdir -p $BUILD_PATH && cd $BUILD_PATH
cmake $PROFILING_ROOT_PATH -DCMAKE_CXX_COMPILER=${CXX_COMPILER} \
                           -DCMAKE_BUILD_TYPE=Release \
                           -DCMAKE_INSTALL_PREFIX=${PROFILING_INSTALL_DIR} \
                           -DCMAKE_CXX_EXTENSIONS=Off \
                           -DMorpheus_ROOT=${MORPHEUS_PATH} \
                           -DSparseTree_ENABLE_SERIAL=${BACKEND_SERIAL} \
                           -DSparseTree_ENABLE_OPENMP=${BACKEND_OPENMP} && make -j