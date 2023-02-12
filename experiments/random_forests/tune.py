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
from sparse_tree.classifier import RandomForestClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn import ensemble
import argparse
import os
import matplotlib.pyplot as plt

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

clf = RandomForestClassifier(random_state=10)
clf_base = clf.fit(train_data, train_labels)

BASELINE_MAX_DEPTH = 0
for estimator in clf_base.estimators_:
    max_depth = estimator.tree_.max_depth
    if max_depth > BASELINE_MAX_DEPTH:
        BASELINE_MAX_DEPTH = max_depth

NFEATURES = clf_base.n_features_in_
experiment_path = os.path.join(experiment_path, str(NFEATURES))
os.makedirs(experiment_path, exist_ok=True)

depth_step = 1
max_depths = [BASELINE_MAX_DEPTH]
ctr = 0
depth = BASELINE_MAX_DEPTH - depth_step
while depth > 1:
    max_depths.append(depth)
    ctr += 1
    depth = BASELINE_MAX_DEPTH - depth_step * (ctr * 2)

class_weights = [None, "balanced", "balanced_subsample"]
criteria = ["gini", "entropy", "log_loss"]
max_features = [*[i for i in range(1, NFEATURES + 1)], "sqrt", "log2"]
min_samples_leaf = [i for i in range(1, NFEATURES + 1)]
min_samples_split = [2, 5, 10]
estimators = [i for i in range(10, 110, 10)]
bootstrap = [False, True]

random_grid = {
    "max_depth": max_depths,
    "min_samples_leaf": min_samples_leaf,
    "max_features": max_features,
    "criterion": criteria,
    "class_weight": class_weights,
    "min_samples_split": min_samples_split,
    "bootstrap": bootstrap,
    "n_estimators": estimators,
}

dt = ensemble.RandomForestClassifier(random_state=10)
dt_random = GridSearchCV(
    estimator=dt,
    param_grid=random_grid,
    cv=5,
    verbose=2,
    n_jobs=-1,
)
dt_random.fit(train_data, train_labels)
tune_parameters = dt_random.best_params_
clf = RandomForestClassifier(
    random_state=10,
    n_estimators=tune_parameters["n_estimators"],
    bootstrap=tune_parameters["bootstrap"],
    max_depth=tune_parameters["max_depth"],
    min_samples_leaf=tune_parameters["min_samples_leaf"],
    min_samples_split=tune_parameters["min_samples_split"],
    max_features=tune_parameters["max_features"],
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
    header = "experiment,system,backend,dataset,model,n_estimators,bootstrap,max_depth,min_samples_leaf,min_samples_split,max_features,criterion,class_weight,accuracy,precision,recall,fscore,balanced_accuracy\n"
    f.write(header)
    n_estimators = tune_parameters["n_estimators"]
    bootstrap = tune_parameters["bootstrap"]
    max_depth = tune_parameters["max_depth"]
    min_samples_leaf = tune_parameters["min_samples_leaf"]
    min_samples_split = tune_parameters["min_samples_split"]
    max_features = tune_parameters["max_features"]
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

    base_bal_acc = balanced_accuracy_score(clf_base.predict(test_data), test_labels)
    tuned_bal_acc = balanced_accuracy_score(clf.predict(test_data), test_labels)

    system_metrics = f"{experiment},{system},{backend},{dataset},"
    params = f"{n_estimators},{bootstrap},{max_depth},{min_samples_leaf},{min_samples_split},{max_features},{criterion},{class_weight},"

    base_metrics = f"{base_accuracy:.6f},{base_wprecision:.6f},{base_wrecall:.6f},{base_wf1:.6f},{base_bal_acc:.6f}"
    tuned_metrics = f"{tuned_accuracy:.6f},{tuned_wprecision:.6f},{tuned_wrecall:.6f},{tuned_wf1:.6f},{tuned_bal_acc:.6f}"

    base_entry = (
        system_metrics
        + "baseline,100,True,None,1,2,None,gini,None,"
        + base_metrics
        + "\n"
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
