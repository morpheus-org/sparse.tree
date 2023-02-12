# Building Feature Extraction Routine

```sh
$ BACKEND=[serial | openmp]
$ MORPHEUS_INSTALL_DIR=/path/to/morpheus/installation
$ KOKKOS_INSTALL_DIR=/path/to/kokkos/installation
$ ./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR
```

### Example: Instinct Serial
```sh
WORK_DIR=/lustre/home/ri-cstylianou
BACKEND=serial
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/milan-gnu-10.3-on-off
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/milan-gnu-10.3-on-off
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR
```

### Example: Instinct OpenMP
```sh
WORK_DIR=/lustre/home/ri-cstylianou
BACKEND=openmp
KOKKOS_INSTALL_DIR=$WORK_DIR/kokkos/installs/milan-gnu-10.2-on-on
MORPHEUS_INSTALL_DIR=$WORK_DIR/morpheus/installs/milan-gnu-10.2-on-on
./build.sh $BACKEND $MORPHEUS_INSTALL_DIR $KOKKOS_INSTALL_DIR
```

# Run Feature Extraction Routine

```sh
$ BACKEND=[serial | openmp | cuda]
$ DATASET=[small_set | square_set]
$ ./run.sh $BACKEND $DATASET $BUDGET
```

### Example: Instinct Serial
```sh
WORK_DIR=/lustre/home/ri-cstylianou
BACKEND=serial
DATASET=square_set
./run.sh $BACKEND $DATASET
```

### Example: Instinct OpenMP
```sh
WORK_DIR=/lustre/home/ri-cstylianou
BACKEND=openmp
DATASET=square_set
./run.sh $BACKEND $DATASET
```