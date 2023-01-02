/**
 * spmv.cpp
 *
 * EPCC, The University of Edinburgh
 *
 * (c) 2023 The University of Edinburgh
 *
 * Contributing Authors:
 * Christodoulos Stylianou (c.stylianou@ed.ac.uk)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * 	http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "Morpheus_Core.hpp"

#include <vector>
#include <chrono>
#include <limits>

#define MORPHEUS_START_SCOPE() {  // Open Morpheus Scope
#define MORPHEUS_END_SCOPE() }    // Close Morpheus Scope

using local_int_t = int;
using scalar_t    = double;

#if defined(SparseTree_ENABLE_GENERIC)
namespace morpheus_space_t = Morpheus::Generic;
#else
namespace morpheus_space_t = Morpheus::Custom;
#endif

// Define Morpheus Execution, Memory Spaces and Backend
#if defined(SparseTree_ENABLE_OPENMP)
using exec_space_t = typename morpheus_space_t::OpenMP::execution_space;
using mem_space_t  = typename morpheus_space_t::OpenMP::memory_space;
using backend_t    = typename morpheus_space_t::OpenMP::backend;
#elif defined(SparseTree_ENABLE_CUDA)
using exec_space_t         = typename morpheus_space_t::Cuda::execution_space;
using mem_space_t          = typename morpheus_space_t::Cuda::memory_space;
using backend_t            = typename morpheus_space_t::Cuda::backend;
#elif defined(SparseTree_ENABLE_HIP)
using exec_space_t = typename morpheus_space_t::HIP::execution_space;
using mem_space_t  = typename morpheus_space_t::HIP::memory_space;
using backend_t    = typename morpheus_space_t::HIP::backend;
#else
using exec_space_t = typename morpheus_space_t::Serial::execution_space;
using mem_space_t  = typename morpheus_space_t::Serial::memory_space;
using backend_t    = typename morpheus_space_t::Serial::backend;
#endif

using Matrix    = Morpheus::DynamicMatrix<scalar_t, local_int_t, backend_t>;
using Vector    = Morpheus::DenseVector<scalar_t, local_int_t, backend_t>;
using Timings_t = Morpheus::DenseMatrix<double, size_t, Morpheus::HostSpace>;
using ns        = std::chrono::nanoseconds;

template <typename ExecSpace, typename Matrix>
void tune_spmv(Matrix& A, int reps, Timings_t& timings) {
  auto Ah = Morpheus::create_mirror_container(A);
  Morpheus::copy(A, Ah);

  Vector x(A.ncols(), scalar_t(2)), y(A.nrows(), scalar_t(0));

  for (auto fmt_idx = 0; fmt_idx < Morpheus::NFORMATS; fmt_idx++) {
    Morpheus::conversion_error_e status =
        Morpheus::convert<Morpheus::Serial>(Ah, fmt_idx);

    if (status == Morpheus::CONV_SUCCESS) {
      A.activate(Ah.active_index());
      A.resize(Ah);
      Morpheus::copy(Ah, A);

      for (int rep = 0; rep < reps; rep++) {
        auto start = std::chrono::steady_clock::now();
        Morpheus::multiply<ExecSpace>(A, x, y, true);
        auto end = std::chrono::steady_clock::now();

        timings(fmt_idx, rep) =
            std::chrono::duration_cast<ns>(end - start).count() * 1e-9;
      }
    }
  }
}

int main(int argc, char* argv[]) {
  Morpheus::initialize(argc, argv, false);
  MORPHEUS_START_SCOPE();

  const int rt_args = 3;

  if (argc != rt_args) {
    std::stringstream rt_error_msg;
    rt_error_msg << "Benchmark requires " << rt_args - 1
                 << " runtime input arguments:\n";
    rt_error_msg << "\tfilename   : Matrix Market file to be used.\n";
    rt_error_msg << "\treps : How many repetitions for each format.\n";
    rt_error_msg << "Received " << argc - 1 << " arguments !\n ";

    std::cout << rt_error_msg.str() << std::endl;
    exit(-1);
  }

  std::string filename = argv[1];
  size_t reps          = atoi(argv[2]);

  std::cout << "\nRunning SparseTree SpMV Benchmark with:\n";
  std::cout << "\tFilename    : " << filename << "\n";
  std::cout << "\tRepetitions : " << reps << "\n\n";

  Matrix A;
  typename Matrix::HostMirror Ah;
  try {
    // Read matrix from a file using matrix market file-format
    Morpheus::IO::read_matrix_market_file(Ah, filename);
  } catch (Morpheus::NotImplementedException& e) {
    std::cerr << "Exception Raised:: " << e.what() << std::endl;
    exit(0);
  }

  // Setup local matrix on Device
  A.activate(Ah.active_index());
  A.resize(Ah);
  Morpheus::copy(Ah, A);

  // Tune Matrices
  Timings_t timings(Morpheus::NFORMATS, reps,
                    std::numeric_limits<double>::max());
  tune_spmv<backend_t>(A, reps, timings);

  // Process Timings
  std::vector<double> avg_timings(Morpheus::NFORMATS, 0);
  for (size_t i = 0; i < Morpheus::NFORMATS; i++) {
    double sumt = 0.0;
    for (size_t j = 0; j < reps; j++) {
      sumt += timings(i, j);
    }
    avg_timings[i] = sumt / reps;
  }

  double mint   = avg_timings[0];
  int format_id = 0;
  for (int i = 0; i < Morpheus::NFORMATS; i++) {
    if (avg_timings[i] < mint) {
      mint      = avg_timings[i];
      format_id = i;
    }
  }
  for (size_t i = 0; i < avg_timings.size(); i++) {
    std::cout << "(" << i << ") | " << avg_timings[i] << std::endl;
  }
  std::cout << "Optimum Format = " << format_id << std::endl;

  MORPHEUS_END_SCOPE();
  Morpheus::finalize();

  return 0;
}