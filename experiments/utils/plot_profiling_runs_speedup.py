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

experiments = [
    "cirrus-square_set-cuda-1000",
    "cirrus-square_set-openmp-1000",
    "cirrus-square_set-serial-1000",
    "archer2-square_set-openmp-1000",
    "archer2-square_set-serial-1000",
    "xci-square_set-openmp-1000",
    "xci-square_set-serial-1000",
    "a64fx-square_set-openmp-1000",
    "a64fx-square_set-serial-1000",
    "ampere-square_set-cuda-1000",
    "instinct-square_set-hip-1000",
]

for experiment in experiments:
    fmat = (
        "/work/d403/d403/cstyl16/sparse.tree/experiments/profiling_runs/"
        + experiment
        + ".csv"
    )
    df = pd.read_csv(fmat)

    csr_df = (
        df[df.Format == 1]
        .drop(["OptimumFormat", "Format"], axis=1)
        .reset_index()
        .rename(columns={"Timings": "Tcsr"})
        .drop(["index"], axis=1)
    )

    optimal_df = (
        df[df.Format == df.OptimumFormat]
        .drop(["Format"], axis=1)
        .reset_index()
        .rename(columns={"Timings": "Topt"})
        .drop(["index"], axis=1)
    )

    merged_df = pd.merge(csr_df, optimal_df, on=["matrix"], how="left")
    merged_df["speedup"] = merged_df.Tcsr / merged_df.Topt
    # merged_df.sort_values(by=["speedup"], ascending=False).to_csv(experiment + ".csv")

    print(f"{experiment}:")
    print("\tTotal Dataset Stats:")
    print("\t\tDistribution: ", end="")
    for c in range(0, 6):
        if c != 5:
            print(merged_df[merged_df.OptimumFormat == c].count()[0], ", ", end="")
        else:
            print(merged_df[merged_df.OptimumFormat == c].count()[0])

    print(
        f"\t\tmin: {merged_df.speedup.min():.4f}, max: {merged_df.speedup.max():.4f}, mean: {merged_df.speedup.mean():.4f}, median: {merged_df.speedup.median():.4f}"
    )

    filtered_df = merged_df[merged_df.speedup > 1]
    filtered_df.sort_values(by=["speedup"], ascending=False).to_csv(
        experiment + "-filtered.csv"
    )

    print("\tFiltered Dataset Stats:")
    print("\t\tDistribution: ", end="")
    for c in range(0, 6):
        if c != 5:
            print(filtered_df[filtered_df.OptimumFormat == c].count()[0], ", ", end="")
        else:
            print(filtered_df[filtered_df.OptimumFormat == c].count()[0])

    print(
        f"\t\tmin: {filtered_df.speedup.min():.4f}, max: {filtered_df.speedup.max():.4f}, mean: {filtered_df.speedup.mean():.4f}, median: {filtered_df.speedup.median():.4f}\n"
    )
