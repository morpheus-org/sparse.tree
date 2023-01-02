include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add_executable(SparseTree_SpMV spmv.cpp)

if(SparseTree_ENABLE_GENERIC)
  message(STATUS "SparseTree: Profiling Runs are enabled with Generic Backend")
  target_compile_definitions(SparseTree_SpMV PRIVATE SparseTree_ENABLE_GENERIC)
endif()

if(SparseTree_ENABLE_OPENMP)
  message(
    STATUS "SparseTree: Profiling Runs are enabled with OpenMP Execution Space")
  target_compile_definitions(SparseTree_SpMV PRIVATE SparseTree_ENABLE_OPENMP)
elseif(SparseTree_ENABLE_CUDA)
  message(
    STATUS "SparseTree: Profiling Runs are enabled with Cuda Execution Space")
  target_compile_definitions(SparseTree_SpMV PRIVATE SparseTree_ENABLE_CUDA)
elseif(SparseTree_ENABLE_HIP)
  message(
    STATUS "SparseTree: Profiling Runs are enabled with HIP Execution Space")
  target_compile_definitions(SparseTree_SpMV PRIVATE SparseTree_ENABLE_HIP)
else()
  message(
    STATUS "SparseTree: Profiling Runs are enabled with Serial Execution Space")
  target_compile_definitions(SparseTree_SpMV PRIVATE SparseTree_ENABLE_SERIAL)
endif()

target_link_libraries(SparseTree_SpMV Morpheus::morpheus)
