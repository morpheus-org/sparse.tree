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
    balanced_accuracy_score,
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
base_accuracy = clf_base.score(test_data, test_labels)
base_bal_acc = balanced_accuracy_score(clf_base.predict(test_data), test_labels)
print(base_accuracy, base_bal_acc)
print(clf_base.feature_importances_)
