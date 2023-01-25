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
import numpy as np
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
        df = df.merge(pandas.read_csv(targets_filename)).dropna()
        df = df[df["Format"] == df["OptimumFormat"]]

        self.data = df[self.feature_names].to_numpy()
        self.target = df["OptimumFormat"].to_numpy(dtype=int)
        self.matrices = df["matrix"].to_numpy()

    def split(
        self,
        data,
        targets,
        matrices,
        per_class=False,
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

        if per_class:
            X, Xt, Y, Yt, Z, Zt = [], [], [], [], [], []
            for class_id in np.unique(targets):
                sidx = targets == class_id

                _size = test_size
                if isinstance(test_size, int):
                    _size = test_size / total_size

                if targets[sidx].shape[0] * _size <= 1:
                    sX = data[sidx]
                    sY = targets[sidx]
                    sZ = matrices[sidx]
                    for i in range(data[sidx].shape[0]):
                        X.append(sX[i].tolist())
                        Y.append(sY[i])
                        Z.append(sZ[i])
                    continue

                sX, sXt, sY, sYt, sZ, sZt = train_test_split(
                    data[sidx],
                    targets[sidx],
                    matrices[sidx],
                    test_size=test_size,
                    train_size=val_size + train_size,
                    **kwargs,
                )
                for i in range(sX.shape[0]):
                    X.append(sX[i].tolist())
                    Y.append(sY[i])
                    Z.append(sZ[i])
                for i in range(sXt.shape[0]):
                    Xt.append(sXt[i].tolist())
                    Yt.append(sYt[i])
                    Zt.append(sZt[i])
            X = np.array(X)
            Y = np.array(Y)
            Z = np.array(Z)
            Xt = np.array(Xt)
            Yt = np.array(Yt)
            Zt = np.array(Zt)
        else:
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
            if per_class:
                Xtr, Xv, Ytr, Yv, Ztr, Zv = [], [], [], [], [], []
                for class_id in np.unique(Y):
                    sidx = Y == class_id

                    _size = val_size
                    if isinstance(val_size, int):
                        _size = val_size / total_size

                    if Y[sidx].shape[0] * _size <= 1:
                        sX = X[sidx]
                        sY = Y[sidx]
                        sZ = Z[sidx]
                        for i in range(X[sidx].shape[0]):
                            Xtr.append(sX[i].tolist())
                            Ytr.append(sY[i])
                            Ztr.append(sZ[i])
                        continue

                    sXtr, sXv, sYtr, sYv, sZtr, sZv = train_test_split(
                        X[sidx],
                        Y[sidx],
                        Z[sidx],
                        train_size=train_size / train_val_size,
                        **kwargs,
                    )
                    for i in range(sXtr.shape[0]):
                        Xtr.append(sXtr[i].tolist())
                        Ytr.append(sYtr[i])
                        Ztr.append(sZtr[i])
                    for i in range(sXv.shape[0]):
                        Xv.append(sXv[i].tolist())
                        Yv.append(sYv[i])
                        Zv.append(sZv[i])
                Xtr = np.array(Xtr)
                Ytr = np.array(Ytr)
                Ztr = np.array(Ztr)
                Xv = np.array(Xv)
                Yv = np.array(Yv)
                Zv = np.array(Zv)
            else:
                Xtr, Xv, Ytr, Yv, Ztr, Zv = train_test_split(
                    X,
                    Y,
                    Z,
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
