project(SparseTreeFeatures CXX)

cmake_minimum_required(VERSION 3.16)

find_package(Morpheus REQUIRED)
message(STATUS "Found Morpheus at ${Morpheus_DIR}")

option(SparseTree_ENABLE_GENERIC "Enable Morpheus Generic backends" OFF)
option(SparseTree_ENABLE_SERIAL "Enable Serial Execution Space" OFF)
option(SparseTree_ENABLE_OPENMP "Enable OpenMP Execution Space" OFF)
option(SparseTree_ENABLE_CUDA "Enable Cuda Execution Space" OFF)
option(SparseTree_ENABLE_HIP "Enable HIP Execution Space" OFF)
add_subdirectory(src)
