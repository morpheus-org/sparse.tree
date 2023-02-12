"""
 plot_matrices.py
 
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
import numpy as np
import matplotlib.pyplot as plt


def customize_legend(handles, labels, case="color"):

    Handles = []
    Labels = []

    for h, l in zip(handles, labels):
        co = h.patches[0].get_facecolor()
        ha = h.patches[0].get_hatch()

        LABS = l.split("-")
        backend = LABS[0]
        format = LABS[1]

        if case in "color":
            # Color
            COLOR = plt.bar((0, 1), (0, 0), color=co)
            if format.upper() not in Labels:
                Handles.append(COLOR)
                Labels.append(format.upper())
        elif case in "hatch":
            # HATCH
            STYLE = plt.bar((0, 1), (0, 0), color="k", fill=False, hatch=ha)
            if backend.upper() not in Labels:
                Handles.append(STYLE)
                Labels.append(backend.upper())

    return Handles, Labels


script_path = os.path.realpath(os.path.dirname(__file__))
experiments_path = os.path.join(script_path, "baseline")
outdir = os.path.join(script_path, "plots")
os.makedirs(outdir, exist_ok=True)

dataset = "square_set"
repetitions = "1000"
nfeatures = 10

systems = {
    "a64fx": ["serial", "openmp"],
    "ampere": ["cuda"],
    "archer2": ["serial", "openmp"],
    "cirrus": ["serial", "openmp", "cuda"],
    "instinct": ["hip"],
    "xci": ["serial", "openmp"],
}

dfs = []
for system, backends in systems.items():
    for backend in backends:
        path = os.path.join(
            experiments_path,
            f"{system}-{dataset}-{backend}-{repetitions}",
            str(nfeatures),
        )
        dfs.append(pd.read_csv(os.path.join(path, "matrix_stats.csv")))

df = pd.concat(dfs).drop(
    [
        "dataset",
        "set",
        "total_set_matrices",
        "class_matrices",
        "set_percentage",
        "total_dataset_matrices",
    ],
    axis=1,
)

for lbl in ["ampere", "instinct"]:
    df.loc[df["system"] == lbl, "system"] = "p3"

sum_df = df.groupby(["system", "backend", "class_id"]).sum().reset_index()


nsys = sum_df.system.unique().shape[0]
nbackends = sum_df.backend.unique().shape[0]
nclasses = sum_df.class_id.unique().shape[0]

data = np.zeros((nclasses, nbackends, nsys))
acc = np.zeros_like(data)

for i, cid in enumerate(sum_df.class_id.unique()):
    for j, backend in enumerate(sum_df.backend.unique()):
        for k, system in enumerate(sum_df.system.unique()):
            tmp = sum_df.loc[
                (sum_df.system == system)
                & (sum_df.backend == backend)
                & (sum_df.class_id == cid),
                "dataset_percentage",
            ].to_numpy()
            if tmp.shape[0] == 1:
                data[i, j, k] = tmp[0]

formats = ["COO", "CSR", "DIA", "ELL", "HYB", "HDC"]
backends = sum_df.backend.unique()
colors = ["tab:blue", "tab:orange", "tab:green", "tab:purple", "tab:olive", "tab:red"]
hatches = ["//", "++", "\\\\", ".."]
X = np.arange(sum_df.system.unique().shape[0])

fig = plt.figure()
ax = plt.subplot(111)
ax.bar(
    X - 0.30,
    data[0, 0],
    color=colors[0],
    fill=True,
    label=backends[0] + "-" + formats[0],
    hatch=hatches[0],
    width=0.20,
)
ax.bar(
    X - 0.10,
    data[0, 1],
    color=colors[0],
    fill=True,
    label=backends[1] + "-" + formats[0],
    hatch=hatches[1],
    width=0.20,
)
ax.bar(
    X + 0.10,
    data[0, 2],
    color=colors[0],
    fill=True,
    label=backends[2] + "-" + formats[0],
    hatch=hatches[2],
    width=0.20,
)
ax.bar(
    X + 0.30,
    data[0, 3],
    color=colors[0],
    fill=True,
    label=backends[3] + "-" + formats[0],
    hatch=hatches[3],
    width=0.20,
)

acc[0, 0] = data[0, 0]
acc[0, 1] = data[0, 1]
acc[0, 2] = data[0, 2]
acc[0, 3] = data[0, 3]
for i in range(1, data.shape[0]):
    ax.bar(
        X - 0.30,
        data[i, 0],
        color=colors[i],
        bottom=acc[0, 0],
        fill=True,
        label=backends[0] + "-" + formats[i],
        hatch=hatches[0],
        width=0.20,
    )
    ax.bar(
        X - 0.10,
        data[i, 1],
        color=colors[i],
        bottom=acc[0, 1],
        fill=True,
        label=backends[1] + "-" + formats[i],
        hatch=hatches[1],
        width=0.20,
    )
    ax.bar(
        X + 0.10,
        data[i, 2],
        color=colors[i],
        bottom=acc[0, 2],
        fill=True,
        label=backends[2] + "-" + formats[i],
        hatch=hatches[2],
        width=0.20,
    )
    ax.bar(
        X + 0.30,
        data[i, 3],
        color=colors[i],
        bottom=acc[0, 3],
        fill=True,
        label=backends[3] + "-" + formats[i],
        hatch=hatches[3],
        width=0.20,
    )
    acc[0, 0] += data[i, 0]
    acc[0, 1] += data[i, 1]
    acc[0, 2] += data[i, 2]
    acc[0, 3] += data[i, 3]

ax.set_xlabel("System")
ax.set_ylabel("Format Distribution (%)")
ax.set_xticks(X, (x.upper() for x in sum_df.system.unique()))

handles, labels = plt.gca().get_legend_handles_labels()
l_handles, l_labels = customize_legend(handles, labels, "color")
l1 = plt.legend(
    l_handles,
    l_labels,
    bbox_to_anchor=(1.04, 1),
    title="Format:",
    loc="upper left",
    borderaxespad=0,
)
l1._legend_box.align = "center"
ax.add_artist(l1)

s_handles, s_labels = customize_legend(handles, labels, "hatch")
l2 = plt.legend(
    s_handles,
    s_labels,
    bbox_to_anchor=(1.04, 0.4),
    title="Backend:",
    loc="center left",
    borderaxespad=0,
)
l2._legend_box.align = "center"
ax.add_artist(l2)
plt.tight_layout(rect=[0, 0, 0.8, 1])
fig.savefig(os.path.join(outdir, f"matrix_distribution.pdf"))
