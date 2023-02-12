#!/bin/sh

# On Isambard
python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/a64fx-square_set-openmp-1000/10/test_targets.csv \
                      --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-a64fx-square_set-openmp-1000.txt

python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/a64fx-square_set-serial-1000/10/test_targets.csv \
                      --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-a64fx-square_set-serial-1000.txt

python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/ampere-square_set-cuda-1000/10/test_targets.csv \
                      --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-ampere-square_set-cuda-1000.txt

python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/instinct-square_set-hip-1000/10/test_targets.csv \
                      --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-instinct-square_set-hip-1000.txt
                      
python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/xci-square_set-openmp-1000/10/test_targets.csv \
                      --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-xci-square_set-openmp-1000.txt

python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/xci-square_set-serial-1000/10/test_targets.csv \
                      --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-xci-square_set-serial-1000.txt

# # On Archer2
# python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/archer2-square_set-openmp-1000/10/test_targets.csv \
#                       --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-archer2-square_set-openmp-1000.txt

# python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/archer2-square_set-serial-1000/10/test_targets.csv \
#                       --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-archer2-square_set-serial-1000.txt

# # On Cirrus
# python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/cirrus-square_set-cuda-1000/10/test_targets.csv \
#                       --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-cirrus-square_set-cuda-1000.txt
                      
# python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/cirrus-square_set-openmp-1000/10/test_targets.csv \
#                       --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-cirrus-square_set-openmp-1000.txt

# python matrix_list.py --fset=/lustre/home/ri-cstylianou/sparse.tree/experiments/decision_trees/baseline/cirrus-square_set-serial-1000/10/test_targets.csv \
#                       --fout=/lustre/home/ri-cstylianou/sparse.tree/experiments/utils/test_lists/matrices-cirrus-square_set-serial-1000.txt