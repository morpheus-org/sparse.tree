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
import matplotlib.pylab as plt

script_path = os.path.realpath(os.path.dirname(__file__))
outdir = os.path.join(script_path, "profiling-runs")
os.makedirs(outdir, exist_ok=True)

colors = {
    0: "blue",
    1: "green",
    2: "orange",
    3: "maroon",
    4: "purple",
    5: "dodgerblue",
    6: "olive",
    7: "lightseagreen",
    8: "saddlebrown",
    9: "darkgray",
}

markers = {
    0: "x",
    1: "d",
    2: "s",
    3: "o",
    4: "*",
    5: ">",
}

def map_backend(backend):
    if backend.lower() == "serial":
        backend_id = 0
    elif backend.lower() == "openmp":
        backend_id = 1
    elif backend.lower() == "cuda":
        backend_id = 2
    elif backend.lower() == "hip":
        backend_id = 3
    return backend_id


def map_system(system):
    if system.lower() == "cirrus":
        system_id = 0
    elif system.lower() == "archer2":
        system_id = 1
    elif system.lower() == "xci":
        system_id = 2
    elif system.lower() == "a64fx":
        system_id = 3
    elif system.lower() == "ampere":
        system_id = 4
    elif system.lower() == "instinct":
        system_id = 5
    return system_id


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

dfs = []
for experiment in experiments:
    fmat = script_path + "/../profiling_runs/" + experiment + ".csv"
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
    sorted_df = merged_df.sort_values(by=["speedup"], ascending=False)

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

    sorted_df["experiment"] = experiment
    dfs.append(sorted_df)

total_df = pd.concat(dfs).reset_index().drop("index", axis=1).astype({'OptimumFormat': 'int32'})
total_df = total_df[total_df.OptimumFormat != 1].reset_index().drop("index", axis=1)

matrices = total_df.matrix.unique()

for i, matrix in enumerate(matrices):
    total_df.loc[total_df["matrix"] == matrix, "matrix_id"] = i
total_df = total_df.astype({"matrix_id": "int32"})

total_df.sort_values(by=["speedup"], ascending=False).to_csv(
    os.path.join(outdir, "experiment.csv"), index=True
)

speedup_df = total_df[["experiment", "matrix_id", "speedup"]]

splits = (
    speedup_df["experiment"]
    .str.split(pat="-", expand=True)
    .rename(columns={0: "system", 1: "dataset", 2: "backend", 3: "reps"})
)

df = pd.concat([speedup_df, splits], axis=1).drop(
    ["experiment", "dataset", "reps"], axis=1
)
df['backend_label'] = df['backend']
df.loc[df["backend"] == 'cuda', "backend_label"] = 'gpu'
df.loc[df["backend"] == 'hip', "backend_label"] = 'gpu'

styles = {0: "solid", 1: "dotted", 2: "dashed", 3: "dashdot", 4: (5, (10, 3)), 5: (0, (5, 10))}

for backend_label in df.backend_label.unique():
    backend_label_df = df.loc[(df["backend_label"] == backend_label)]
    fig, ax = plt.subplots(tight_layout=True)
    for backend in backend_label_df.backend.unique():
        backend_df = backend_label_df.loc[(backend_label_df["backend"] == backend)]
        for system in backend_df.system.unique():
            experiment_df = backend_df.loc[(backend_df["system"] == system) & (backend_df['backend']==backend)]
            plot_df = (
                experiment_df[["matrix_id", "speedup",'backend','backend_label']]
                .sort_values(by=["matrix_id"])
                .set_index("matrix_id")
            )
            print(plot_df.mean())
            markerline, stemlines, baseline = plt.stem(plot_df.reset_index().matrix_id, 
                                                    plot_df.reset_index().speedup,
                                                    markerfmt=".",
                                                    linefmt=colors[map_system(system) % len(colors)], 
                                                    label=system.upper(), bottom=0, basefmt=" ")
            plt.setp(stemlines, linewidth=0.3)
            plt.setp(markerline, markersize=5)

            plt.axhline(y = plot_df.mean().to_numpy()[0], color = colors[map_system(system) % len(colors)], linestyle = styles[map_system(system) % len(styles)], label=r'$\mu_{'+system.upper()+'}$')
    plt.yscale("log")
    plt.xscale("log")
    plt.grid()
    ax.legend()
    ax.set_xlabel("Matrix ID")
    ax.set_ylabel("Speedup ("+ r'$\frac{T_{CSR}}{T_{OPTIMAL}}$'+")")
    fig.savefig(
        os.path.join(outdir, f"{backend_label}_stemplot.jpg"),
        format="jpg",
    )
    plt.close("all")
