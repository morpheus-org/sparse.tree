"""
 filter_best.py
 
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
import os
import pandas as pd

script_path = os.path.realpath(os.path.dirname(__file__))

outdir = os.path.join(script_path, "filtered")
os.makedirs(outdir, exist_ok=True)

experiments = [
    "baseline",
    "max_depth_tuning",
    "min_samples_tuning",
    "balanced_data_tuning",
    "max_features_tuning",
    "splitter_tuning",
    "criterion_tuning",
]

dfs = []
for experiment in experiments:
    path = os.path.join(script_path, experiment)
    dfs.append(pd.read_csv(os.path.join(path, f"{experiment}-accuracy.csv")))

df = pd.concat(dfs).drop(["dataset", "set", "total_set_matrices", "misses"], axis=1)
max_df = (
    df.groupby(["system", "backend", "experiment"])["accuracy"]
    .max()
    .reset_index()
    .set_index(["system", "backend", "experiment", "accuracy"])
)

filtered_df = (
    df.reset_index()
    .set_index(["system", "backend", "experiment", "accuracy"])
    .drop("index", axis=1)
)

filtered_df = (
    filtered_df.loc[max_df.index]
    .reset_index()
    .set_index(["system", "backend", "experiment"])
)

filtered_df.to_csv(os.path.join(outdir, "result.csv"))
