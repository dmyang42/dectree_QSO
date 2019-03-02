import sys
from load_data import load_data
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
from sklearn import tree

filename = "data/" + sys.argv[1]
feature, data = load_data(filename, [0,4,5,6,16])

data_list = []
label_list = []
for i in range(len(data)):
    unit_dict = {}
    for j in range(1, len(feature)-1):
        unit_dict[feature[j]] = data[i][j]
    data_list.append(unit_dict)
    label_list.append(data[i][len(feature)-1])
vec = DictVectorizer()
X = vec.fit_transform(data_list).toarray()
lb = preprocessing.LabelBinarizer()
Y = lb.fit_transform(label_list)

clf = tree.DecisionTreeClassifier(criterion="entropy")
clf = clf.fit(X, Y)
with open("tree.dot","w") as f:
    f = tree.export_graphviz(clf, feature_names=vec.get_feature_names(), out_file = f)