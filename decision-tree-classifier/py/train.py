from sklearn.datasets import load_iris
from sklearn import tree
from matplotlib import pyplot as plt

iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

feature_names = iris.feature_names

left = clf.tree_.children_left
right = clf.tree_.children_right
threshold = clf.tree_.threshold
features = [feature_names[i] for i in clf.tree_.feature]
value = clf.tree_.value

print(clf.tree_.node_count)
print(clf.tree_.max_depth)
print(left)
print(right)
print(threshold)
# print(value)
# print(clf.tree_.feature)
# print(features)

# tree.plot_tree(clf)

# def recurse_tree(left, right, threshold, features, nodeid):


# def recurse_tree(left, right, threshold, features, node, tabs):
#         code = ""
#         if threshold[node] != -2:
#             code += "%sif (feature_vector.at(%s) <= %s) {\n" % (
#                 tabs * "\t",
#                 feature_names.index(features[node]),
#                 round(threshold[node], 2),
#             )
#             tabs += 1

#             if left[node] != -1:
#                 code += recurse_tree(left, right, threshold, features, left[node], tabs)
#             tabs -= 1
#             code += "%s}\n%selse {\n" % (tabs * "\t", tabs * "\t")

#             tabs += 1
#             if right[node] != -1:
#                 code += recurse_tree(left, right, threshold, features, right[node], tabs)
#             tabs -= 1
#             code += "%s}\n" % (tabs * "\t")

#         else:
#             code += "%sreturn %s;\n" % (tabs * "\t", value[node].argmax())

#         return code

# def save(tree, feature_names, class_names):
#     left = tree.tree_.children_left
#     right = tree.tree_.children_right
#     threshold = tree.tree_.threshold
#     features = [feature_names[i] for i in tree.tree_.feature]
#     value = tree.tree_.value

#     return recurse_tree(left, right, threshold, features, 0, 1)

# tree_stream = recurse_tree(left, right, threshold, features, 0, 1)
# print(tree_stream)
