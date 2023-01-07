# Building Feature Extraction Routine

```sh
$ BACKEND=[serial | openmp | cuda]
$ MORPHEUS_INSTALL_DIR=/path/to/morpheus/installation
$ KOKKOS_INSTALL_DIR=/path/to/kokkos/installation
$ BUDGET=[budget code]
$ ./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR $BUDGET
```

### Example: Cirrus Serial
```sh
WORK_DIR=/work/d403/d403/cstyl16
BACKEND=serial
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/gnu-10.2-off-on
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/gnu-10.2-off-on
BUDGET=d403-cs
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR $BUDGET
```

### Example: Cirrus OpenMP
```sh
WORK_DIR=/work/d403/d403/cstyl16
BACKEND=openmp
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/gnu-10.2-on-on
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/gnu-10.2-on-on
BUDGET=d403-cs
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR $BUDGET
```

### Example: Cirrus GPU
```sh
WORK_DIR=/work/d403/d403/cstyl16
BACKEND=cuda
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/cuda-11.6-on-on
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/cuda-11.6-on-on
BUDGET=d403-cs
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR $BUDGET
```