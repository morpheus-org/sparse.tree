"""
 baseline.py
 
 EPCC, The University of Edinburgh
 
 (c) 2023 The University of Edinburgh
 
 Contributing Authors:
 Christodoulos Stylianou (c.stylianou@ed.ac.uk)
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
 	http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from sparse_tree.dataset import MatrixDataset
from sparse_tree.classifier import DecisionTreeClassifier
import argparse
import os
import numpy as np
import pandas as pd


parser = argparse.ArgumentParser()
# Basename of format <dataset>-features.csv
parser.add_argument(
    "--features",
    type=str,
    required=True,
    dest="features",
    help="Absolute path to the features file.",
)
# Basename of format <backend>-<dataset>-<backend>-<reps>.csv
parser.add_argument(
    "--runtimes",
    type=str,
    required=True,
    dest="runtimes",
    help="Absolute path to the profilings file.",
)
# Number of features
parser.add_argument(
    "--nfeatures",
    type=int,
    required=True,
    dest="nfeatures",
    help="Number of features.",
)
args = parser.parse_args()

script_path = os.path.realpath(os.path.dirname(__file__))
experiment = "baseline"
baseline_path = os.path.join(script_path, experiment)
rt_base = os.path.basename(args.runtimes)

system = rt_base.split("-")[0]
dataset = rt_base.split("-")[1]
backend = rt_base.split("-")[2]
repetitions = rt_base.split("-")[3].replace(".csv", "")
nclasses = 6
exp_lbl = "-".join([system, dataset, backend, repetitions])
experiment_path = os.path.join(baseline_path, exp_lbl, str(args.nfeatures))
os.makedirs(experiment_path, exist_ok=True)

matrices = MatrixDataset(args.features, args.runtimes)
split = matrices.split(
    matrices.data,
    matrices.target,
    matrices.matrices,
    train_size=0.8,
    test_size=0.2,
    random_state=100,
    per_class=True,
)

total_matrices = sum(split[sset]["target"].shape[0] for sset in ["train", "test"])
# Dataset split stats
fmat_stats = os.path.join(experiment_path, "matrix_stats.csv")
print(f"Writing Matrix Stats: ", fmat_stats)
with open(fmat_stats, "w") as f:
    header = "system,backend,dataset,set,class_id,class_matrices,total_set_matrices,set_percentage,total_dataset_matrices,dataset_percentage\n"
    f.write(header)
    for sset in ["train", "test"]:
        total_set_matrices = split[sset]["target"].shape[0]
        for class_id in range(nclasses):
            class_matrices = np.count_nonzero(split[sset]["target"] == class_id)
            dataset_percentage = class_matrices / total_matrices
            set_percentage = class_matrices / total_set_matrices
            entry = f"{system},{backend},{dataset},{sset},{class_id},{class_matrices},{total_set_matrices},{set_percentage*100:.2f},{total_matrices},{dataset_percentage*100:.2f}\n"
            f.write(entry)

# Save Test Set
ftest_set = os.path.join(experiment_path, "test_set.csv")
ftest_targets = os.path.join(experiment_path, "test_targets.csv")
pd.concat(
    [
        pd.DataFrame(split["test"]["matrices"], columns=["Matrix"]),
        pd.DataFrame(split["test"]["data"], columns=matrices.feature_names),
    ],
    axis=1,
).to_csv(ftest_set, index=False)
pd.concat(
    [
        pd.DataFrame(split["test"]["matrices"], columns=["Matrix"]),
        pd.DataFrame(split["test"]["target"], columns=["Class"]),
    ],
    axis=1,
).to_csv(ftest_targets, index=False)

clf = DecisionTreeClassifier(random_state=10)
clf = clf.fit(split["train"]["data"], split["train"]["target"])
clf.extract(
    os.path.join(experiment_path, "tree.txt"),
    matrices.feature_names,
)
