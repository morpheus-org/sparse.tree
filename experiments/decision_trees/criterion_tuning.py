"""
 criterion_tuning.py
 
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
args = parser.parse_args()

script_path = os.path.realpath(os.path.dirname(__file__))
experiment = "criterion_tuning"
baseline_path = os.path.join(script_path, experiment)
rt_base = os.path.basename(args.runtimes)

system = rt_base.split("-")[0]
dataset = rt_base.split("-")[1]
backend = rt_base.split("-")[2]
repetitions = rt_base.split("-")[3].replace(".csv", "")
nclasses = 6
exp_lbl = "-".join([system, dataset, backend, repetitions])
experiment_path = os.path.join(baseline_path, exp_lbl)
os.makedirs(experiment_path, exist_ok=True)

matrices = MatrixDataset(args.features, args.runtimes)
split = matrices.split(
    matrices.data,
    matrices.target,
    matrices.matrices,
    train_size=0.7,
    test_size=0.1,
    val_size=0.2,
    random_state=100,
    per_class=True,
)

clfs = []
clf_misses = []
criteria = []
for criterion in ["gini", "entropy", "log_loss"]:
    clf = DecisionTreeClassifier(random_state=10, criterion=criterion)
    clf = clf.fit(split["train"]["data"], split["train"]["target"])

    clf.extract(
        os.path.join(experiment_path, f"tree-{criterion}.txt"),
        matrices.feature_names,
    )

    misses_str = "MissCtr,Matrix,Experimental,Actual\n"
    misses = 0
    nval_samples = split["val"]["data"].shape[0]
    for i in range(nval_samples):
        experimental = clf.evaluate(split["val"]["data"][i])
        actual = split["val"]["target"][i]
        if experimental != actual:
            matrix = split["val"]["matrices"][i]
            misses_str += f"{misses},{matrix},{experimental},{actual}\n"
            misses += 1

    fmisses = os.path.join(experiment_path, "misses.csv")
    print(f"Writing Misses (criterion={criterion}): ", fmisses)
    with open(fmisses, "w") as f:
        f.write(misses_str)

    clfs.append(clf)
    clf_misses.append(misses)
    criteria.append(criterion)

facc = os.path.join(experiment_path, "accuracy.csv")
print(f"Writing Accuracy: ", facc)
with open(facc, "w") as f:
    header = "experiment,criterion,system,backend,dataset,set,total_set_matrices,misses,accuracy\n"
    f.write(header)
    total_set_matrices = split["val"]["target"].shape[0]
    for clf, misses, criterion in zip(clfs, clf_misses, criteria):
        accuracy = (1 - misses / nval_samples) * 100
        f.write(
            f"{experiment},{criterion},{system},{backend},{dataset},val,{total_set_matrices},{misses},{accuracy:.4f}\n"
        )
