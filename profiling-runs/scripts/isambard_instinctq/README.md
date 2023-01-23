# Building Profiling Runs Routine

```sh
$ BACKEND=[hip]
$ MORPHEUS_INSTALL_DIR=/path/to/morpheus/installation
$ KOKKOS_INSTALL_DIR=/path/to/kokkos/installation
$ ./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR
```

### Example: Isambard P3 Instinct GPU
```sh
BACKEND=hip
WORK_DIR=/lustre/home/ri-cstylianou
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/hip-4.5-on-on
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/hip-4.5-on-on
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR
```

# Run Profiling Runs Routine

```sh
$ BACKEND=[hip]
$ DATASET=/path/to/dataset
$ REPETITIONS=1000
$ ./run.sh $BACKEND $DATASET $REPETITIONS
```

### Example: Isambard P3 Instinct GPU
```sh
DATASET=square_set
BACKEND=hip
REPETITIONS=1000
./run.sh $BACKEND $DATASET $REPETITIONS
```

