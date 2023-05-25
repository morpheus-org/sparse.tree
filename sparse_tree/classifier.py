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
import io

from .utils import (
    extract_array,
    write_array_to_bytes,
    write_to_bytes,
    build_str_sizelist,
)


class DecisionTreeClassifier(tree.DecisionTreeClassifier):
    """
    Extends the DecisionTreeClassifier from sklearn by providing routines
    to extract the resulting tree in a file
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def extract(self, file, feature_names, format="bin"):
        """
        Extracts the tree in a binary or text file/buffer.

        Parameters
        ----------
        filename : str
            A path to the filename to extract the tree in.
        feature_names : list
            A list containing the name of each feature.
        format : str
            The file format to be used when storing the tree.
            Options are [bin | txt] for binary and text formats.
        """

        if isinstance(feature_names, list):
            nfeatures = len(feature_names)
        elif isinstance(feature_names, np.ndarray):
            nfeatures = feature_names.shape[0]
        else:
            raise TypeError(
                f"Type of feature_names ({type(feature_names)}) must be either list or numpy.ndarray"
            )

        if isinstance(file, str):
            if format == "bin":
                with open(file, "wb") as f:
                    self._extract_buffer(f, nfeatures, feature_names)
            elif format == "txt":
                with open(file, "w") as f:
                    self._extract_text(f, nfeatures, feature_names)
        elif isinstance(file, io.BufferedWriter):
            self._extract_buffer(file, nfeatures, feature_names)
        elif isinstance(file, io.TextIOWrapper):
            self._extract_text(file, nfeatures, feature_names)
        else:
            raise TypeError(
                f"file {type(file)} must be either a filename (str) or a binary buffer (io.BufferedWriter)!"
            )

    def _extract_buffer(self, file, nfeatures, feature_names):
        if not isinstance(file, io.BufferedWriter):
            raise TypeError("file handler must be of type io.BufferedWriter!")

        tree = self.tree_

        write_to_bytes(file, nfeatures)
        write_to_bytes(file, self.n_classes_)
        write_to_bytes(file, tree.node_count)
        write_to_bytes(file, tree.max_depth)
        write_array_to_bytes(file, self.classes_)
        write_array_to_bytes(file, build_str_sizelist(feature_names))
        write_array_to_bytes(file, feature_names)
        write_array_to_bytes(file, tree.children_left)
        write_array_to_bytes(file, tree.children_right)
        write_array_to_bytes(file, tree.threshold, dtype=np.float64)
        write_array_to_bytes(file, tree.feature)
        write_array_to_bytes(file, tree.value, dtype=np.float64)

    def _extract_text(self, file, nfeatures, feature_names):
        tree = self.tree_

        # Write sizes
        file.write("# Sizes (NFeatures, Nclasses, NodeCount, MaxDepth)\n")
        file.write(str(nfeatures) + "\t")
        file.write(str(self.n_classes_) + "\t")
        file.write(str(tree.node_count) + "\t")
        file.write(str(tree.max_depth) + "\n")

        # Write Classes
        extract_array(file, self.classes_, self.n_classes_, comment="Classes")
        # Write Feature Names Sizes
        extract_array(
            file,
            build_str_sizelist(feature_names),
            nfeatures,
            comment="Feature Names Sizes",
        )
        # Write Feature Names
        extract_array(file, feature_names, nfeatures, comment="Feature Names")

        # Write tree data
        extract_array(file, tree.children_left, tree.node_count, comment="Left")
        extract_array(file, tree.children_right, tree.node_count, comment="Right")
        extract_array(file, tree.threshold, tree.node_count, comment="Threshold")
        extract_array(file, tree.feature, tree.node_count, comment="Feature")

        file.write("# Values\n")
        for i in range(tree.node_count):
            extract_array(file, tree.value[i, 0], self.n_classes_)

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
