"""
 tune.py
 
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

from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn import tree
import argparse
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pprint import pprint

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
experiment = "tune"
tune_path = os.path.join(script_path, experiment)
rt_base = os.path.basename(args.runtimes)

system = rt_base.split("-")[0]
dataset = rt_base.split("-")[1]
backend = rt_base.split("-")[2]
repetitions = rt_base.split("-")[3].replace(".csv", "")
nclasses = 6
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
test_data = split["test"]["data"]
test_labels = split["test"]["target"]

clf = DecisionTreeClassifier(random_state=10)
clf_base = clf.fit(train_data, train_labels)

NFEATURES = clf_base.n_features_in_
BASELINE_MAX_DEPTH = clf_base.tree_.max_depth
depth_step = 1
max_depths = [BASELINE_MAX_DEPTH]
ctr = 0
depth = BASELINE_MAX_DEPTH - depth_step
while depth > 1:
    max_depths.append(depth)
    ctr += 1
    depth = BASELINE_MAX_DEPTH - depth_step * (ctr * 2)

class_weights = [None, "balanced"]
criteria = ["gini", "entropy", "log_loss"]
splitters = ["best", "random"]
max_features = [*[i for i in range(1, NFEATURES + 1)], "sqrt", "log2"]
min_samples_leaf = [i for i in range(1, NFEATURES + 1)]
min_samples_split = [2, 5, 10]

random_grid = {
    "max_depth": max_depths,
    "min_samples_leaf": min_samples_leaf,
    "max_features": max_features,
    "splitter": splitters,
    "criterion": criteria,
    "class_weight": class_weights,
    "min_samples_split": min_samples_split,
}

dt = tree.DecisionTreeClassifier(random_state=10)
dt_random = GridSearchCV(
    estimator=dt,
    param_grid=random_grid,
    cv=5,
    verbose=2,
    n_jobs=-1,
)
dt_random.fit(train_data, train_labels)
tune_parameters = dt_random.best_params_
clf = DecisionTreeClassifier(
    random_state=10,
    max_depth=tune_parameters["max_depth"],
    min_samples_leaf=tune_parameters["min_samples_leaf"],
    min_samples_split=tune_parameters["min_samples_split"],
    max_features=tune_parameters["max_features"],
    splitter=tune_parameters["splitter"],
    criterion=tune_parameters["criterion"],
    class_weight=tune_parameters["class_weight"],
)
clf = clf.fit(train_data, train_labels)


base_accuracy = clf_base.score(test_data, test_labels)
tuned_accuracy = clf.score(test_data, test_labels)

base_predicted = clf_base.predict(test_data)
tuned_predicted = clf.predict(test_data)

# write in file parameters and baseline/tuned accuracy
fres = os.path.join(experiment_path, "results.csv")
print(f"Writing Results: ", fres)
with open(fres, "w") as f:
    header = "experiment,system,backend,dataset,model,max_depth,min_samples_leaf,min_samples_split,max_features,splitter,criterion,class_weight,accuracy,precision,recall,fscore\n"
    f.write(header)
    max_depth = tune_parameters["max_depth"]
    min_samples_leaf = tune_parameters["min_samples_leaf"]
    min_samples_split = tune_parameters["min_samples_split"]
    max_features = tune_parameters["max_features"]
    splitter = tune_parameters["splitter"]
    criterion = tune_parameters["criterion"]
    class_weight = tune_parameters["class_weight"]

    base_wprecision = precision_score(test_labels, base_predicted, average="weighted")
    tuned_wprecision = precision_score(test_labels, tuned_predicted, average="weighted")
    base_precision = precision_score(test_labels, base_predicted, average=None)
    tuned_precision = precision_score(test_labels, tuned_predicted, average=None)

    base_wrecall = recall_score(test_labels, base_predicted, average="weighted")
    tuned_wrecall = recall_score(test_labels, tuned_predicted, average="weighted")
    base_recall = recall_score(test_labels, base_predicted, average=None)
    tuned_recall = recall_score(test_labels, tuned_predicted, average=None)

    base_wf1 = f1_score(test_labels, base_predicted, average="weighted")
    tuned_wf1 = f1_score(test_labels, tuned_predicted, average="weighted")
    base_f1 = f1_score(test_labels, base_predicted, average=None)
    tuned_f1 = f1_score(test_labels, tuned_predicted, average=None)

    system_metrics = f"{experiment},{system},{backend},{dataset},"
    params = f"{max_depth},{min_samples_leaf},{min_samples_split},{max_features},{splitter},{criterion},{class_weight},"

    base_metrics = (
        f"{base_accuracy:.6f},{base_wprecision:.6f},{base_wrecall:.6f},{base_wf1:.6f}"
    )
    tuned_metrics = f"{tuned_accuracy:.6f},{tuned_wprecision:.6f},{tuned_wrecall:.6f},{tuned_wf1:.6f}"

    base_entry = (
        system_metrics + "baseline,None,1,2,None,best,gini,None," + base_metrics + "\n"
    )
    f.write(base_entry)
    tuned_entry = system_metrics + "tuned," + params + tuned_metrics + "\n"
    f.write(tuned_entry)

# baseline confusion
fcm_baseline = os.path.join(experiment_path, "baseline_cm.jpg")
cm_baseline = confusion_matrix(test_labels, base_predicted, labels=clf_base.classes_)
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm_baseline, display_labels=clf_base.classes_
)
disp.plot()
plt.savefig(fcm_baseline)

# tuned confusion
fcm_tuned = os.path.join(experiment_path, "tuned_cm.jpg")
cm_tuned = confusion_matrix(test_labels, tuned_predicted, labels=clf.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm_tuned, display_labels=clf.classes_)
disp.plot()
plt.savefig(fcm_tuned)
