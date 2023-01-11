"""
 classifier.py
 
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

from sklearn import tree, ensemble
from collections import Counter
import numpy as np
import os

from .utils import extract_array


class DecisionTreeClassifier(tree.DecisionTreeClassifier):
    """
    Extends the DecisionTreeClassifier from sklearn by providing routines
    to extract the resulting tree in a file
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def extract(self, filename, feature_names):
        """
        Extracts the tree in a file.

        Parameters
        ----------
        filename : str
            A path to the filename to extract the tree in.
        feature_names : list
            A list containing the name of each feature.
        """
        tree = self.tree_

        if isinstance(feature_names, list):
            features_size = len(feature_names)
        elif isinstance(feature_names, np.ndarray):
            features_size = feature_names.shape[0]
        else:
            raise TypeError(
                f"Type of feature_names ({type(feature_names)}) must be either list or numpy.ndarray"
            )

        with open(filename, "w") as f:
            # Write sizes
            f.write("# Sizes (NFeatures, Nclasses, NodeCount, MaxDepth)\n")
            f.write(str(features_size) + "\t")
            f.write(str(self.n_classes_) + "\t")
            f.write(str(tree.node_count) + "\t")
            f.write(str(tree.max_depth) + "\n")

            # Write Classes
            extract_array(f, self.classes_, self.n_classes_, comment="Classes")
            # Write Feature Names
            extract_array(f, feature_names, features_size, comment="Feature Names")

            # Write tree data
            extract_array(f, tree.children_left, tree.node_count, comment="Left")
            extract_array(f, tree.children_right, tree.node_count, comment="Right")
            extract_array(f, tree.threshold, tree.node_count, comment="Threshold")
            extract_array(f, tree.feature, tree.node_count, comment="Feature")

            f.write("# Values\n")
            for i in range(tree.node_count):
                extract_array(f, tree.value[i, 0], self.n_classes_)

    def evaluate(self, sample):
        """
        Evaluates the class of the provided sample.

        Parameters
        ----------
        sample : numpy nd-array
            One-dimensional array containing the sample with the features.

        Returns:
        --------
        class_label : int
            The class label in which the sample belongs to.
        """
        if len(sample.shape) != 1:
            raise ValueError(
                f"The input sample must be a one dimensional array but instead has {len(sample.shape)} dimensions"
            )
        return self.__recurse(sample)

    def __recurse(self, sample, node=0):
        tree = self.tree_
        if tree.threshold[node] != -2:
            if sample[tree.feature[node]] <= tree.threshold[node]:
                return self.__recurse(sample, node=tree.children_left[node])
            else:
                return self.__recurse(sample, node=tree.children_right[node])
        else:
            idx = tree.value[node].argmax()
            return self.classes_[idx]


def convert_decision_tree(classifier):
    if not isinstance(classifier, tree.DecisionTreeClassifier):
        raise TypeError(
            f"Type of the classifier ({type(classifier)} must be {type(tree.DecisionTreeClassifier)}!"
        )

    classifier.__class__ = DecisionTreeClassifier
    return classifier


class RandomForestClassifier(ensemble.RandomForestClassifier):
    """
    Extends the RandomForestClassifier from sklearn by providing routines
    to extract the resulting trees in various files
    """

    def __init__(self, **kwargs):
        super(RandomForestClassifier, self).__init__(**kwargs)
        self.estimators = []

    def fit(self, X, y, sample_weight=None):
        self = super().fit(X, y, sample_weight=sample_weight)

        for i in range(len(self.estimators_)):
            self.estimators.append(convert_decision_tree(self.estimators_[i]))

        return self

    def extract(self, dirname, feature_names):
        """
        Extracts the forest in multiple files. One file contains
        the metadata of the forest and then for each tree a new
        file is created.

        Parameters
        ----------
        dirname : str
            A path to the directory to extract the random forest.
        feature_names : list
            A list containing the name of each feature.
        """

        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)

        # Write metadata
        metafile = "/".join([dirname, f"metadata.txt"])
        with open(metafile, "w") as f:
            # Write sizes
            f.write("# Sizes (NFeatures, Nclasses, NOutputs)\n")
            f.write(str(self.n_features_in_) + "\t")
            f.write(str(self.n_classes_) + "\t")
            f.write(str(self.n_outputs_) + "\n")

            # Write Classes
            extract_array(f, self.classes_, self.n_classes_, comment="Classes")
            # Write Feature Names
            extract_array(
                f, feature_names, self.n_features_in_, comment="Feature Names"
            )

        # Write each tree in a file
        for i in range(len(self.estimators)):
            filename = "/".join([dirname, f"tree_{i}.txt"])
            self.estimators[i].extract(filename, feature_names)

    def evaluate(self, sample):
        """
        Evaluates the class of the provided sample by recursing each tree in the forest.

        Parameters
        ----------
        sample : numpy nd-array
            One-dimensional array containing the sample with the features.

        Returns:
        --------
        class_label : int
            The class label in which the sample belongs to.
        """
        if len(sample.shape) != 1:
            raise ValueError(
                f"The input sample must be a one dimensional array but instead has {len(sample.shape)} dimensions"
            )

        outputs = []
        for estimator in self.estimators_:
            outputs.append(estimator.evaluate(sample))

        return Counter(outputs).most_common(1)[0][0]
