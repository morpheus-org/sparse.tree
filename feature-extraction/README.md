<!--
 Copyright 2023 cstyl
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

# CIRRUS
## Build Profiling Runs

<!-- ENV -->
```sh
CXX_COMPILER=/usr/bin/g++
KOKKOS_BUILD_DIR=/home/cstyl/work/code/kokkos/builds/gnu-9-on-off
KOKKOS_INSTALL_DIR=/home/cstyl/work/code/kokkos/installs/gnu-9-on-off
MORPHEUS_BUILD_DIR=/home/cstyl/work/code/morpheus/builds/gnu-9-on-off
MORPHEUS_INSTALL_DIR=/home/cstyl/work/code/morpheus/installs/gnu-9-on-off
SPARSETREE_BUILD_DIR=/home/cstyl/work/code/sparse.tree/builds/features/gnu-9-on-off
SPARSETREE_INSTALL_DIR=/home/cstyl/work/code/sparse.tree/installs/features/gnu-9-on-off
```

<!-- Kokkos -->
```sh
mkdir -p $KOKKOS_BUILD_DIR
cd $KOKKOS_BUILD_DIR
cmake ../.. -DCMAKE_CXX_COMPILER=${CXX_COMPILER} -DCMAKE_INSTALL_PREFIX=${KOKKOS_INSTALL_DIR} \
            -DCMAKE_BUILD_TYPE=Release -DKokkos_ENABLE_OPENMP=OFF  -DKokkos_ENABLE_SERIAL=ON \
            -DKokkos_CXX_STANDARD=17 -DKokkos_ENABLE_COMPILER_WARNINGS=On \
            -DKokkos_ENABLE_AGGRESSIVE_VECTORIZATION=On
make
make install
```

<!-- Morpheus -->
```sh
mkdir -p $MORPHEUS_BUILD_DIR
cd $MORPHEUS_BUILD_DIR
cmake ../.. -DCMAKE_CXX_COMPILER=${CXX_COMPILER} -DCMAKE_INSTALL_PREFIX=${MORPHEUS_INSTALL_DIR} \
            -DKokkos_ROOT=${KOKKOS_INSTALL_DIR} -DCMAKE_BUILD_TYPE=Release \
            -DMorpheus_ENABLE_EXAMPLES=OFF -DMorpheus_ENABLE_TESTS=OFF
make -j
make install
```

<!-- Sparse.Tree - Features -->
```sh
mkdir -p $SPARSETREE_BUILD_DIR && cd $SPARSETREE_BUILD_DIR
cmake ../../../feature-extraction -DCMAKE_CXX_COMPILER=${CXX_COMPILER} -DCMAKE_INSTALL_PREFIX=${SPARSETREE_INSTALL_DIR} \
            -DMorpheus_ROOT=${MORPHEUS_INSTALL_DIR} -DCMAKE_BUILD_TYPE=Release
make -j
make install
```


# P3
## Build Profiling Runs

<!-- ENV -->
```sh
module use -a /lustre/projects/bristol/modules/modulefiles
module load cmake
module load gcc/10.3.0
WORK_DIR=/lustre/home/ri-cstylianou
CXX_COMPILER=$(which g++)
KOKKOS_ROOT_DIR=$WORK_DIR/kokkos
KOKKOS_BUILD_DIR=$WORK_DIR/kokkos/builds/milan-gnu-10.3-on-off
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/milan-gnu-10.3-on-off
MORPHEUS_ROOT_DIR=$WORK_DIR/morpheus
MORPHEUS_BUILD_DIR=$WORK_DIR/morpheus/builds/milan-gnu-10.3-on-off
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/milan-gnu-10.3-on-off
SPARSETREE_BUILD_DIR=$WORK_DIR/sparse.tree/builds/features/gnu-9-on-off
SPARSETREE_INSTALL_DIR=$WORK_DIR/code/sparse.tree/installs/features/gnu-9-on-off

export CRAYPE_LINK_TYPE=dynamic
```

<!-- Kokkos -->
```sh
mkdir -p $KOKKOS_BUILD_DIR
cd $KOKKOS_BUILD_DIR
cmake ../.. -DCMAKE_CXX_COMPILER=${CXX_COMPILER} -DCMAKE_INSTALL_PREFIX=${KOKKOS_INSTALL_DIR} \
            -DCMAKE_BUILD_TYPE=Release -DKokkos_ENABLE_OPENMP=OFF  -DKokkos_ENABLE_SERIAL=ON \
            -DKokkos_CXX_STANDARD=17 -DKokkos_ENABLE_COMPILER_WARNINGS=On \
            -DKokkos_ENABLE_AGGRESSIVE_VECTORIZATION=On
make
make install
```

<!-- Morpheus -->
```sh
mkdir -p $MORPHEUS_BUILD_DIR
cd $MORPHEUS_BUILD_DIR
cmake ../.. -DCMAKE_CXX_COMPILER=${CXX_COMPILER} -DCMAKE_INSTALL_PREFIX=${MORPHEUS_INSTALL_DIR} \
            -DKokkos_ROOT=${KOKKOS_INSTALL_DIR} -DCMAKE_BUILD_TYPE=Release \
            -DMorpheus_ENABLE_EXAMPLES=OFF -DMorpheus_ENABLE_TESTS=OFF
make -j
make install
```

<!-- Sparse.Tree - Features -->
```sh
mkdir -p $SPARSETREE_BUILD_DIR && cd $SPARSETREE_BUILD_DIR
cmake ../../../feature-extraction -DCMAKE_CXX_COMPILER=${CXX_COMPILER} -DCMAKE_INSTALL_PREFIX=${SPARSETREE_INSTALL_DIR} \
            -DMorpheus_ROOT=${MORPHEUS_INSTALL_DIR} -DCMAKE_BUILD_TYPE=Release
make -j
make install
```