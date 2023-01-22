# Building Profiling Runs Routine

```sh
$ BACKEND=[serial | openmp ]
$ MORPHEUS_INSTALL_DIR=/path/to/morpheus/installation
$ KOKKOS_INSTALL_DIR=/path/to/kokkos/installation
$ ./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR
```

### Example: XCI Serial
```sh
WORK_DIR=/home/ri-cstylianou
BACKEND=serial
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/xci-gnu-10.3-on-off
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/xci-gnu-10.3-on-off
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR
```

### Example: XCI OpenMP
```sh
WORK_DIR=/home/ri-cstylianou
BACKEND=openmp
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/xci-gnu-10.3-on-on
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/xci-gnu-10.3-on-on
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR
```

# Run Profiling Runs Routine

```sh
$ BACKEND=[serial | openmp ]
$ DATASET=/path/to/dataset
$ REPETITIONS=1000
$ ./run.sh $BACKEND $DATASET $REPETITIONS
```

### Example: XCI Serial
```sh
WORK_DIR=/home/ri-cstylianou
BACKEND=serial
DATASET=square_set
REPETITIONS=1000
./run.sh $BACKEND $DATASET $REPETITIONS
```

### Example: XCI OpenMP
```sh
WORK_DIR=/home/ri-cstylianou
BACKEND=openmp
DATASET=square_set
REPETITIONS=1000
./run.sh $BACKEND $DATASET $REPETITIONS
```
