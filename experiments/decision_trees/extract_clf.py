"""
 extract_clf.py
 
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
import matplotlib.pyplot as plt

from sklearn.metrics import (
    balanced_accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

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

parser.add_argument(
    "--parameters",
    type=str,
    required=True,
    dest="parameters",
    help="Absolute path to the parameters file.",
)
args = parser.parse_args()

script_path = os.path.realpath(os.path.dirname(__file__))
experiment = "extract_clf"
tune_path = os.path.join(script_path, experiment)
rt_base = os.path.basename(args.runtimes)

system = rt_base.split("-")[0]
dataset = rt_base.split("-")[1]
backend = rt_base.split("-")[2]
repetitions = rt_base.split("-")[3].replace(".csv", "")
exp_lbl = "-".join([system, dataset, backend, repetitions])
experiment_path = os.path.join(tune_path, exp_lbl)
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

train_data = split["train"]["data"]
train_labels = split["train"]["target"]

keys = [
    "max_depth",
    "min_samples_leaf",
    "min_samples_split",
    "max_features",
    "splitter",
    "criterion",
    "class_weight",
    "accuracy",
]

df = pd.read_csv(args.parameters)
base_df = df[df.model == "baseline"][keys].reset_index().drop("index", axis=1)
tuned_df = df[df.model == "tuned"][keys].reset_index().drop("index", axis=1)

base_max_features = base_df.max_features[0]
if base_max_features == "None":
    base_max_features = None
elif base_max_features not in ["sqrt", "log2"]:
    base_max_features = int(base_max_features)

clf_base = DecisionTreeClassifier(
    random_state=10,
    max_depth=int(base_df.max_depth[0]) if base_df.max_depth[0] != "None" else None,
    min_samples_leaf=base_df.min_samples_leaf[0],
    min_samples_split=base_df.min_samples_split[0],
    max_features=base_max_features,
    splitter=base_df.splitter[0],
    criterion=base_df.criterion[0],
    class_weight=base_df.class_weight[0] if base_df.class_weight[0] != "None" else None,
)
clf_base = clf_base.fit(train_data, train_labels)
# clf_base.extract(
#     os.path.join(experiment_path, "baseline_tree.txt"),
#     matrices.feature_names,
# )
print(clf_base.score(split["test"]["data"], split["test"]["target"]))
print(
    balanced_accuracy_score(
        clf_base.predict(split["test"]["data"]), split["test"]["target"]
    )
)
print(clf_base.feature_importances_)

tuned_max_features = tuned_df.max_features[0]
if tuned_max_features == "None":
    tuned_max_features = None
elif tuned_max_features not in ["sqrt", "log2"]:
    tuned_max_features = int(tuned_max_features)

clf_tuned = DecisionTreeClassifier(
    random_state=10,
    max_depth=int(tuned_df.max_depth[0]) if tuned_df.max_depth[0] != "None" else None,
    min_samples_leaf=tuned_df.min_samples_leaf[0],
    min_samples_split=tuned_df.min_samples_split[0],
    max_features=tuned_max_features,
    splitter=tuned_df.splitter[0],
    criterion=tuned_df.criterion[0],
    class_weight=tuned_df.class_weight[0]
    if tuned_df.class_weight[0] != "None"
    else None,
)
clf_tuned = clf_tuned.fit(train_data, train_labels)
# clf_tuned.extract(
#     os.path.join(experiment_path, "tuned_tree.txt"),
#     matrices.feature_names,
# )
print(clf_tuned.score(split["test"]["data"], split["test"]["target"]))
print(
    balanced_accuracy_score(
        clf_tuned.predict(split["test"]["data"]), split["test"]["target"]
    )
)
print(clf_tuned.feature_importances_)

# tuned confusion
fcm_tuned = "tuned_cm.jpg"
cm_tuned = confusion_matrix(
    split["test"]["target"],
    clf_tuned.predict(split["test"]["data"]),
    labels=clf_tuned.classes_,
)
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm_tuned, display_labels=clf_tuned.classes_
)
disp.plot()
plt.savefig(fcm_tuned)