from sparse_tree.dataset import MatrixDataset
from sparse_tree.classifier import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt

f1 = "/work/d403/d403/cstyl16/sparse.tree/feature-extraction/scripts/cirrus/processed/small_set/features-serial.csv"
f2 = "/work/d403/d403/cstyl16/sparse.tree/profiling-runs/scripts/cirrus/processed/small_set/runtimes-openmp.csv"

matrices = MatrixDataset(f1, f2)
split = matrices.split(
    matrices.data,
    matrices.target,
    matrices.matrices,
    train_size=0.6,
    test_size=0.1,
    val_size=0.3,
    random_state=100,
)
feature_names = matrices.feature_names
clf = DecisionTreeClassifier(random_state=10)
clf = clf.fit(split["train"]["data"], split["train"]["target"])

clf.extract("tree.txt", feature_names)

for i in range(split["val"]["data"].shape[0]):
    print(
        split["val"]["target"][i],
        clf.evaluate(split["val"]["data"][i]),
        clf.predict([split["val"]["data"][i]]),
    )

plt.figure()
tree.plot_tree(clf, filled=True)
plt.savefig("tree.pdf", format="pdf", bbox_inches="tight")
