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

        self.feature_names = None
        self.nfeatures = None

    def extract(self, file, feature_names=None, format="bin"):
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

        with_feature_names = False
        if feature_names is not None:
            if isinstance(feature_names, list):
                nfeatures = len(feature_names)
            elif isinstance(feature_names, np.ndarray):
                nfeatures = feature_names.shape[0]
            else:
                raise TypeError(
                    f"Type of feature_names ({type(feature_names)}) must be either list or numpy.ndarray"
                )

            if nfeatures != self.n_features_in_:
                raise ValueError(
                    f"Number of Features provided differs from the one used during fitting. ({nfeatures} != {self.n_features_in_})"
                )

            self.feature_names = feature_names
            with_feature_names = True
        self.nfeatures = self.n_features_in_

        if isinstance(file, str):
            if format == "bin":
                with open(file, "wb") as f:
                    self._extract_buffer(f, extract_fnames=with_feature_names)
            elif format == "txt":
                with open(file, "w") as f:
                    self._extract_text(f, extract_fnames=with_feature_names)
        elif isinstance(file, io.BufferedWriter):
            self._extract_buffer(file, extract_fnames=with_feature_names)
        elif isinstance(file, io.TextIOWrapper):
            self._extract_text(file, extract_fnames=with_feature_names)
        else:
            raise TypeError(
                f"file {type(file)} must be either a filename (str) or a binary buffer (io.BufferedWriter)!"
            )

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

    def tree_size(self, with_feature_names=True):
        """
        Computes the size of the tree written to the file including metadata, but excluding comments.

        Returns:
        --------
        size : int
            The size of the tree in bytes.
        """
        int_size = 4
        char_size = 1
        float_size = 8

        metadata_size = (4 + self.n_classes_) * int_size

        if with_feature_names:
            if self.feature_names == None:
                raise ValueError("feature_names has not been initialized!")

            metadata_size += (
                self.nfeatures * int_size
                + sum(build_str_sizelist(self.feature_names)) * char_size
            )

        tree_data_size = (
            3 * self.tree_.node_count * int_size
            + (self.tree_.node_count + self.tree_.node_count * self.n_classes_)
            * float_size
        )

        return metadata_size + tree_data_size

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

    def _extract_buffer(self, file, extract_fnames=True):
        if not isinstance(file, io.BufferedWriter):
            raise TypeError("file handler must be of type io.BufferedWriter!")

        tree = self.tree_

        write_to_bytes(file, self.nfeatures)
        write_to_bytes(file, self.n_classes_)
        write_to_bytes(file, tree.node_count)
        write_to_bytes(file, tree.max_depth)
        write_array_to_bytes(file, self.classes_)
        if extract_fnames:
            if self.feature_names == None:
                raise ValueError("feature_names has not been initialized!")
            write_array_to_bytes(file, build_str_sizelist(self.feature_names))
            write_array_to_bytes(file, self.feature_names)
        write_array_to_bytes(file, tree.children_left)
        write_array_to_bytes(file, tree.children_right)
        write_array_to_bytes(file, tree.threshold, dtype=np.float64)
        write_array_to_bytes(file, tree.feature)
        write_array_to_bytes(file, tree.value, dtype=np.float64)

    def _extract_text(self, file, extract_fnames=True):
        tree = self.tree_

        # Write sizes
        file.write("# Sizes (NFeatures, Nclasses, NodeCount, MaxDepth)\n")
        file.write(str(self.nfeatures) + "\t")
        file.write(str(self.n_classes_) + "\t")
        file.write(str(tree.node_count) + "\t")
        file.write(str(tree.max_depth) + "\n")

        # Write Classes
        extract_array(file, self.classes_, self.n_classes_, comment="Classes")
        if extract_fnames:
            if self.feature_names == None:
                raise ValueError("feature_names has not been initialized!")
            # Write Feature Names Sizes
            extract_array(
                file,
                build_str_sizelist(self.feature_names),
                self.nfeatures,
                comment="Feature Names Sizes",
            )
            # Write Feature Names
            extract_array(
                file, self.feature_names, self.nfeatures, comment="Feature Names"
            )

        # Write tree data
        extract_array(file, tree.children_left, tree.node_count, comment="Left")
        extract_array(file, tree.children_right, tree.node_count, comment="Right")
        extract_array(file, tree.threshold, tree.node_count, comment="Threshold")
        extract_array(file, tree.feature, tree.node_count, comment="Feature")

        file.write("# Values\n")
        for i in range(tree.node_count):
            extract_array(file, tree.value[i, 0], self.n_classes_)


def convert_decision_tree(classifier):
    if not isinstance(classifier, tree.DecisionTreeClassifier):
        raise TypeError(
            f"Type of the classifier ({type(classifier)} must be {type(tree.DecisionTreeClassifier)}!"
        )

    if classifier.__class__ != DecisionTreeClassifier:
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
        self.feature_names = None
        self.nfeatures = None

    def fit(self, X, y, sample_weight=None):
        self = super().fit(X, y, sample_weight=sample_weight)

        for i in range(len(self.estimators_)):
            self.estimators.append(convert_decision_tree(self.estimators_[i]))

        return self

    def extract(self, file, feature_names=None, format="bin"):
        """
        Extracts the forest in a binary or text file/buffer.

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
        with_feature_names = False
        if feature_names is not None:
            if isinstance(feature_names, list):
                nfeatures = len(feature_names)
            elif isinstance(feature_names, np.ndarray):
                nfeatures = feature_names.shape[0]
            else:
                raise TypeError(
                    f"Type of feature_names ({type(feature_names)}) must be either list or numpy.ndarray"
                )

            if nfeatures != self.n_features_in_:
                raise ValueError(
                    f"Number of Features provided differs from the one used during fitting. ({nfeatures} != {self.n_features_in_})"
                )

            self.feature_names = feature_names
            self.nfeatures = nfeatures
            with_feature_names = True

        if isinstance(file, str):
            if format == "bin":
                with open(file, "wb") as f:
                    self._extract_buffer(f, extract_fnames=with_feature_names)
            elif format == "txt":
                with open(file, "w") as f:
                    self._extract_text(f, extract_fnames=with_feature_names)
        elif isinstance(file, io.BufferedWriter):
            self._extract_buffer(file, extract_fnames=with_feature_names)
        elif isinstance(file, io.TextIOWrapper):
            self._extract_text(file, extract_fnames=with_feature_names)
        else:
            raise TypeError(
                f"file {type(file)} must be either a filename (str) or a binary buffer (io.BufferedWriter)!"
            )

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

    def _extract_buffer(self, file, extract_fnames=True):
        if not isinstance(file, io.BufferedWriter):
            raise TypeError("file handler must be of type io.BufferedWriter!")

        write_to_bytes(file, self.n_features_in_)
        write_to_bytes(file, self.n_classes_)
        write_to_bytes(file, self.n_outputs_)
        write_to_bytes(file, len(self.estimators_))
        # Estimator Sizes
        estimator_sizes = [
            convert_decision_tree(self.estimators[i]).tree_size(
                with_feature_names=False
            )
            for i in range(len(self.estimators))
        ]
        print(estimator_sizes)
        print(type(estimator_sizes))
        write_array_to_bytes(file, estimator_sizes)
        write_array_to_bytes(file, self.classes_)
        if extract_fnames:
            if self.feature_names == None:
                raise ValueError("feature_names has not been initialized!")
        write_array_to_bytes(file, build_str_sizelist(self.feature_names))
        write_array_to_bytes(file, self.feature_names)

        for i in range(len(self.estimators)):
            convert_decision_tree(self.estimators[i]).extract(file, format="bin")

    def _extract_text(self, file, extract_fnames=True):
        # Write sizes
        file.write("# Sizes (NFeatures, Nclasses, NOutputs, NEstimators)\n")
        file.write(str(self.n_features_in_) + "\t")
        file.write(str(self.n_classes_) + "\t")
        file.write(str(self.n_outputs_) + "\t")
        file.write(str(len(self.estimators_)) + "\n")

        # Write Estimator Sizes
        estimator_sizes = [
            convert_decision_tree(self.estimators[i]).tree_size(
                with_feature_names=False
            )
            for i in range(len(self.estimators))
        ]
        extract_array(
            file, estimator_sizes, len(self.estimators_), comment="Estimator Sizes"
        )
        # Write Classes
        extract_array(file, self.classes_, self.n_classes_, comment="Classes")
        if extract_fnames:
            if self.feature_names == None:
                raise ValueError("feature_names has not been initialized!")
            # Write Feature Names Sizes
            extract_array(
                file,
                build_str_sizelist(self.feature_names),
                self.nfeatures,
                comment="Feature Names Sizes",
            )
            # Write Feature Names
            extract_array(
                file, self.feature_names, self.nfeatures, comment="Feature Names"
            )

        # Write each tree in a file
        for i in range(len(self.estimators)):
            file.write("# " + f"tree_{i}" + "\n")
            convert_decision_tree(self.estimators[i]).extract(file, format="txt")
