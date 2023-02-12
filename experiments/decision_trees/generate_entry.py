# Copyright 2023 cstyl16
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pandas as pd
import os

script_path = os.path.realpath(os.path.dirname(__file__))
NFEATURES=10
# NFEATURES=14
experiments=["archer2-square_set-serial-1000","archer2-square_set-openmp-1000","cirrus-square_set-serial-1000","cirrus-square_set-openmp-1000","cirrus-square_set-cuda-1000","a64fx-square_set-serial-1000","a64fx-square_set-openmp-1000","ampere-square_set-cuda-1000","instinct-square_set-hip-1000","xci-square_set-serial-1000","xci-square_set-openmp-1000"]
keys = [
    "max_depth",
    "min_samples_leaf",
    "min_samples_split",
    "max_features",
    "splitter",
    "criterion",
    "class_weight",
    "accuracy",
    "balanced_accuracy",
]
for experiment in experiments:
    file = os.path.join(script_path, "tune", experiment, str(NFEATURES), "results.csv")

    df = pd.read_csv(file)
    base_df = df[df.model == "baseline"][keys]
    tuned_df = df[df.model == "tuned"][keys]

    entry = ""
    for i, key in enumerate(keys):
        base_entry = base_df[key].to_numpy()[0]
        tuned_entry = tuned_df[key].to_numpy()[0]
        delimiter = " & " if i != len(keys) - 1 else " \\\\"
        if key == "accuracy" or key== "balanced_accuracy":
            entry += f"{(base_entry*100):.2f} & {(tuned_entry*100):.2f} {delimiter}"
        else:
            entry += f"{base_entry} & {tuned_entry} {delimiter}"
            

    print(entry)
