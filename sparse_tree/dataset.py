"""
 setup.py
 
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

import pandas
from sklearn.model_selection import train_test_split


class MatrixDataset:
    """
    Class that loads the dataset to be used for training/testing and provides routines
    on loading the dataset from files and spliting it into train/validation/test sets.
    """

    def __init__(self, features_filename, targets_filename):
        self.data = None
        self.target = None
        self.matrices = None
        self.feature_names = None
        self.load_dataset(features_filename, targets_filename)

    def load_dataset(self, features_filename, targets_filename):
        """
        Loads the dataset from a file that contains the features and from another
        file that contains the targets.

        Parameters
        ----------
        features_filename : str
            The name of the file that contains the features.
        targets_filename : str
            The name of the file that contains the targets.
        """
        df = pandas.read_csv(features_filename)
        self.feature_names = [
            feature for feature in df.columns if feature.lower() != "matrix"
        ]
        df = df.merge(pandas.read_csv(targets_filename))
        df = df[df["Format"] == df["OptimumFormat"]]

        self.data = df[self.feature_names].to_numpy()
        self.target = df["OptimumFormat"].to_numpy()
        self.matrices = df["matrix"].to_numpy()

    def split(
        self,
        data,
        targets,
        matrices,
        test_size=None,
        val_size=None,
        train_size=None,
        **kwargs,
    ):
        """
        Splits the data and targets into train, validation and test sets.

        Parameters
        ----------
        data : numpy nd-array
            Two-dimensional array containing the features.
        targets : numpy nd-array
            One-dimensional array containing the classification targets.
        matrices : numpy nd-array
            One-dimensional array containing the names of the matrices.
        test_size : float or int, default = None
            If float, should be between 0.0 and 1.0 and represent the proportion
            of the dataset to include in the test split. If int, represents the
            absolute number of test samples.
        val_size : float or int, default = None
            If float, should be between 0.0 and 1.0 and represent the proportion
            of the dataset to include in the validation split. If int, represents
            the absolute number of validation samples.
        train_size : float or int, default = None
            If float, should be between 0.0 and 1.0 and represent the proportion
            of the dataset to include in the train split. If int, represents the
            absolute number of train samples.

        Returns:
        --------
        splitting : dict
            Dictionary containing train-validation-test split of inputs.
        """
        if data.shape[0] != targets.shape[0]:
            raise ValueError(
                f"Major dimension of data and targets parameters must match: {data.shape[0]} != {targets.shape[0]}"
            )

        if data.shape[0] != matrices.shape[0]:
            raise ValueError(
                f"Major dimension of data and matrices parameters must match: {data.shape[0]} != {matrices.shape[0]}"
            )

        major_size = data.shape[0]

        test_size = self._validate_size(test_size, major_size, "test_size")
        val_size = self._validate_size(val_size, major_size, "val_size")
        train_size = self._validate_size(train_size, major_size, "train_size")

        total_size = test_size + val_size + train_size
        if total_size not in [1.0, major_size]:
            raise ValueError(
                f"Total size ({total_size}) of each split must add up to the total size of dataset entries ({major_size[0]}) or 1.0"
            )

        X, Xt, Y, Yt, Z, Zt = train_test_split(
            data,
            targets,
            matrices,
            test_size=test_size,
            train_size=val_size + train_size,
            **kwargs,
        )

        split = {
            "train": {"data": X, "target": Y, "matrices": Z},
            "val": None,
            "test": {"data": Xt, "target": Yt, "matrices": Zt},
        }

        if val_size != 0.0:
            train_val_size = val_size + train_size
            Xtr, Xv, Ytr, Yv, Ztr, Zv = train_test_split(
                X,
                Y,
                Z,
                test_size=val_size / train_val_size if val_size != 0.0 else None,
                train_size=train_size / train_val_size,
                **kwargs,
            )

            split["train"] = {"data": Xtr, "target": Ytr, "matrices": Ztr}
            split["val"] = {"data": Xv, "target": Yv, "matrices": Zv}

        return split

    def _validate_size(self, size, max_size, set_name="train_size"):
        if size:
            if isinstance(size, float):
                if size < 0.0 or size > 1.0:
                    raise ValueError(
                        f"{set_name} ({size}) must be in the range of [0.0, 1.0]"
                    )
                elif isinstance(size, int):
                    if size < 0 or size > max_size:
                        raise ValueError(
                            f"{set_name} ({size}) must be in the range of [0, {max_size}]"
                        )
        else:
            size = 0.0
        return size
