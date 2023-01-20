# Building Profiling Runs Routine

```sh
$ BACKEND=[serial | openmp ]
$ MORPHEUS_INSTALL_DIR=/path/to/morpheus/installation
$ KOKKOS_INSTALL_DIR=/path/to/kokkos/installation
$ BUDGET=[budget code]
$ ./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR $BUDGET
```

### Example: Archer2 Serial
```sh
WORK_DIR=/work/e609/e609/cstyl
BACKEND=serial
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/gnu-10.2-off-on
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/gnu-10.2-off-on
BUDGET=e609
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR $BUDGET
```

### Example: Archer2 OpenMP
```sh
WORK_DIR=/work/e609/e609/cstyl
BACKEND=openmp
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/gnu-10.2-on-on
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/gnu-10.2-on-on
BUDGET=e609
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR $BUDGET
```

# Run Profiling Runs Routine

```sh
$ BACKEND=[serial | openmp ]
$ DATASET=/path/to/dataset
$ REPETITIONS=1000
$ BUDGET=[budget code]
$ ./run.sh $BACKEND $DATASET $REPETITIONS $BUDGET
```

### Example: Archer2 Serial
```sh
WORK_DIR=/work/e609/e609/cstyl
BACKEND=serial
DATASET=square_set
REPETITIONS=1000
BUDGET=e609
./run.sh $BACKEND $DATASET $REPETITIONS $BUDGET
```

### Example: Archer2 OpenMP
```sh
WORK_DIR=/work/e609/e609/cstyl
BACKEND=openmp
DATASET=square_set
REPETITIONS=1000
BUDGET=e609
./run.sh $BACKEND $DATASET $REPETITIONS $BUDGET
```