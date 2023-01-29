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

from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
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

clf = RandomForestClassifier(random_state=10)
clf_base = clf.fit(train_data, train_labels)

BASELINE_MAX_DEPTH = 0
for estimator in clf_base.estimators_:
    max_depth = estimator.tree_.max_depth
    if max_depth > BASELINE_MAX_DEPTH:
        BASELINE_MAX_DEPTH = max_depth
print(BASELINE_MAX_DEPTH)
