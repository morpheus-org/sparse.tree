# Building Profiling Runs Routine

```sh
$ BACKEND=[cuda]
$ MORPHEUS_INSTALL_DIR=/path/to/morpheus/installation
$ KOKKOS_INSTALL_DIR=/path/to/kokkos/installation
$ ./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR
```

### Example: Isambard P3 Ampere GPU
```sh
BACKEND=cuda
WORK_DIR=/lustre/home/ri-cstylianou
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/cuda-11.7-on-on
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/cuda-11.7-on-on
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR
```

# Run Profiling Runs Routine

```sh
$ BACKEND=[cuda]
$ DATASET=/path/to/dataset
$ REPETITIONS=1000
$ ./run.sh $BACKEND $DATASET $REPETITIONS
```

### Example: Isambard P3 Ampere GPU
```sh
DATASET=square_set
BACKEND=cuda
REPETITIONS=1000
./run.sh $BACKEND $DATASET $REPETITIONS
```

