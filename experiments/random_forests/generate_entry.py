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

# file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/a64fx-square_set-openmp-1000/results.csv"
# file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/a64fx-square_set-serial-1000/results.csv"
# file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/ampere-square_set-cuda-1000/results.csv"
# file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/archer2-square_set-openmp-1000/results.csv"
# file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/archer2-square_set-serial-1000/results.csv"
file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/cirrus-square_set-cuda-1000/results.csv"
# file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/cirrus-square_set-openmp-1000/results.csv"
# file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/cirrus-square_set-serial-1000/results.csv"
# file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/instinct-square_set-hip-1000/results.csv"
# file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/xci-square_set-openmp-1000/results.csv"
# file = "/work/d403/d403/cstyl16/sparse.tree/experiments/random_forests/tune/xci-square_set-serial-1000/results.csv"
keys = [
    "n_estimators",
    "bootstrap",
    "max_depth",
    "min_samples_leaf",
    "min_samples_split",
    "max_features",
    "criterion",
    "class_weight",
    "accuracy",
]

df = pd.read_csv(file)
base_df = df[df.model == "baseline"][keys]
tuned_df = df[df.model == "tuned"][keys]

entry = ""
for i, key in enumerate(keys):
    base_entry = base_df[key].to_numpy()[0]
    tuned_entry = tuned_df[key].to_numpy()[0]
    delimiter = " & " if i != len(keys) - 1 else " \\\\"
    if key != "accuracy":
        entry += f"{base_entry} & {tuned_entry} {delimiter}"
    else:
        entry += f"{(base_entry*100):.2f} & {(tuned_entry*100):.2f} {delimiter}"

print(entry)
