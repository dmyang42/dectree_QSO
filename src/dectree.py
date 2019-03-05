from sklearn.decomposition import PCA 
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
from sklearn import tree
from sklearn.externals import joblib
from data_util import merge_data
import subprocess

# 前20个数据块合并
index_list = range(1,6)
data, label = merge_data(index_list)

# PCA预处理 - 数据降维
# PCA模型需要保存, 在测试集和实际使用时都要使用
pca = PCA(n_components='mle', svd_solver='full')
# pca = PCA()
new_data = pca.fit_transform(data)
print("PCA training finished! - with " + str(pca.n_components_) + " features")

# 标准化数据格式, data_list为存放字典的列表
# 每一个字典表示一个数据, 或者说一个源
# 此处feature为之前各个feature的线性组合
data_list = []
feature = list(map(str, range(pca.n_components_)))
for i in range(len(new_data)):
    unit_dict = {}
    for j in range(pca.n_components_):
        unit_dict[feature[j]] = new_data[i][j]
    data_list.append(unit_dict)
vec = DictVectorizer()

# 决策树训练, 也要保存下来测试使用
X = vec.fit_transform(data_list).toarray()
lb = preprocessing.LabelBinarizer()
Y = lb.fit_transform(label)
clf = tree.DecisionTreeClassifier(criterion="entropy")
clf = clf.fit(X, Y)
print("Decision Tree training finished!")

# 模型可视化输出
dt_file = "./model/tree.dot"
with open(dt_file,"w") as f:
    tree.export_graphviz(clf, feature_names=vec.get_feature_names(), out_file = f)
    # dt_png = "./model/tree.png"
    # command = ["dot", "-Tpng", dt_file, "-o", dt_png]
    # command = " ".join(command)
    # try:
    #     subprocess.check_call(command, shell=True)
    # except Exception as e:
    #     print(e)
    #     exit("Could not run dot, ie graphviz, to "
    #          "produce visualization")
print("Dot file generated!")

# 模型保存
joblib.dump(pca, "./model/test_pca.m")
joblib.dump(clf, "./model/test_dt.m")
print("All model saved!")