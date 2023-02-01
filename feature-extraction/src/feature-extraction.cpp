/**
 * feature-extraction.cpp
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
#include <sys/stat.h>

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

using Matrix      = Morpheus::DynamicMatrix<scalar_t, local_int_t, backend_t>;
using size_type   = typename Matrix::size_type;
using index_type  = typename Matrix::index_type;
using value_type  = typename Matrix::value_type;
using IndexVector = Morpheus::DenseVector<index_type, local_int_t, backend_t>;

template <typename T>
void generate_line(std::stringstream& ss, T& container, size_t len) {
  for (size_t i = 0; i < len; i++) {
    ss << container[i] << (i == len - 1 ? "\n" : ",");
  }
}

int main(int argc, char* argv[]) {
  Morpheus::initialize(argc, argv, false);
  MORPHEUS_START_SCOPE();

  const int rt_args = 4;

  if (argc != rt_args) {
    std::stringstream rt_error_msg;
    rt_error_msg << "Routine requires " << rt_args - 1
                 << " runtime input arguments:\n";
    rt_error_msg << "\tfilename : Matrix Market file to be used.\n";
    rt_error_msg << "\toutdir   : Output Directory to write the features in.\n";
    rt_error_msg << "\tfmt_id   : The format ID to switch to.\n";
    rt_error_msg << "Received " << argc - 1 << " arguments !\n ";

    std::cout << rt_error_msg.str() << std::endl;
    exit(-1);
  }

  std::string filename = argv[1], outdir = argv[2];
  int fmt_id = atoi(argv[3]);

  std::cout << "\nRunning SparseTree Feature Extraction routine with:\n";
  std::cout << "\tFilename    : " << filename << "\n";
  std::cout << "\tOutDir      : " << outdir << "\n";
  std::cout << "\tFormat ID   : " << fmt_id << "\n";

  Matrix A;
  typename Matrix::HostMirror Ah;
  try {
    // Read matrix from a file using matrix market file-format
    Morpheus::IO::read_matrix_market_file(Ah, filename);
  } catch (Morpheus::NotImplementedException& e) {
    std::cerr << "Exception Raised:: " << e.what() << std::endl;
    exit(0);
  }

  if (Ah.active_index() != fmt_id) {
    Morpheus::convert<Morpheus::Serial>(Ah, fmt_id);
  }

  // Setup local matrix on Device
  A.activate(Ah.active_index());
  A.resize(Ah);
  Morpheus::copy(Ah, A);

  // Start feature extraction
  IndexVector nnz_per_row(A.nrows(), 0),
      nnz_per_diag(A.nrows() + A.ncols() - 1, 0);
  Morpheus::count_nnz_per_row<backend_t>(A, nnz_per_row, false);
  Morpheus::count_nnz_per_diagonal<backend_t>(A, nnz_per_diag, false);

  const size_t features_size               = 10;
  scalar_t features[features_size]         = {0};
  std::string feature_names[features_size] = {
      "Nrows",      "Ncols",      "Nnnz",       "AvgNnnz", "Density",
      "MaxRowNnnz", "MinRowNnnz", "StdRowNnnz", "NDiags",  "NTrueDiags"};

  features[0] = Morpheus::number_of_rows(A);
  features[1] = Morpheus::number_of_columns(A);
  features[2] = Morpheus::number_of_nnz(A);
  features[3] = Morpheus::average_nnnz(A);
  features[4] = Morpheus::density(A);
  features[5] = Morpheus::max<backend_t>(nnz_per_row, nnz_per_row.size());
  features[6] = Morpheus::min<backend_t>(nnz_per_row, nnz_per_row.size());
  features[7] = Morpheus::std<backend_t>(nnz_per_row, nnz_per_row.size(),
                                         Morpheus::average_nnnz(A));
  features[8] = Morpheus::count_nnz<backend_t>(nnz_per_diag);
  features[9] = Morpheus::count_nnz<backend_t>(nnz_per_diag, A.nrows() / 5);

  std::stringstream ss;
  generate_line(ss, feature_names, features_size);
  generate_line(ss, features, features_size);

  struct stat buffer;
  if (stat(outdir.c_str(), &buffer) != 0) {
    if (mkdir(outdir.c_str(), 0777) != 0) {
      std::cout << "Output Directory (" << outdir << ") was NOT created!"
                << std::endl;
      exit(1);
    }
  }

  std::ofstream outFile;
  outFile.open(outdir + "/features.csv");
  outFile << ss.str();
  outFile.close();

  MORPHEUS_END_SCOPE();
  Morpheus::finalize();

  return 0;
}