from sklearn.decomposition import PCA 
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.externals import joblib
from data_util import merge_data, std_data
import subprocess
import visualize as viz

# 数据块合并
index_list = range(10,670)
data, label = merge_data(index_list)

# PCA预处理 - 数据降维
# PCA模型需要保存, 在测试集和实际使用时都要使用
pca = PCA(n_components='mle', svd_solver='full')
# pca = PCA()
new_data = pca.fit_transform(data)
print("PCA training finished! - with " + str(pca.n_components_) + " features")

feature = list(map(str, range(pca.n_components_)))
X, Y, vec = std_data(new_data, label, feature)

# 决策树训练, 也要保存下来测试使用
dtc = tree.DecisionTreeClassifier(criterion="gini", max_depth=10, min_samples_split=30, \
    min_samples_leaf=20, max_leaf_nodes=25)
dtc = dtc.fit(X, Y)
print("Decision Tree training finished!")

# 随机森林训练
rfc = RandomForestClassifier(n_estimators=233, oob_score=True, criterion="gini", max_depth=50, \
    min_samples_split=10, min_samples_leaf=5, max_leaf_nodes=66, max_features="log2")
rfc.fit(X, Y)
print("Random Forest training finished!")
print("Random Forest oob_score: " + str(rfc.oob_score_))

# viz.dt_viz(dtc, vec.get_feature_names())
# viz.rf_viz(rfc, vec.get_feature_names())

# 模型保存
joblib.dump(pca, "./model/test_pca.m")
joblib.dump(dtc, "./model/test_dt.m")
joblib.dump(rfc, "./model/test_rf.m")
print("All model saved!")