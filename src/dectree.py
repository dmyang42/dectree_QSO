from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.metrics import make_scorer, accuracy_score
from sklearn.decomposition import PCA 
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.externals import joblib
from data_util import merge_data, std_data, get_feature
import subprocess
import visualize as viz

# 数据块合并
index_list = range(10,670)
data, label = merge_data(index_list)
print([label.count('0'), label.count('1')])

# PCA预处理 - 数据降维
# PCA模型需要保存, 在测试集和实际使用时都要使用
pca = PCA(n_components='mle', svd_solver='full')
pca = PCA()
new_data = pca.fit_transform(data)
print("PCA training finished! - with " + str(pca.n_components_) + " features")

new_data = data
# feature = get_feature('./train/test_sample_data_1')
feature = list(map(str, range(pca.n_components_)))
X, Y, vec = std_data(new_data, label, feature)

# 决策树训练, 也要保存下来测试使用
dtc = tree.DecisionTreeClassifier(criterion="gini", max_depth=6, min_samples_split=2, \
    min_samples_leaf=1, max_leaf_nodes=28)
dtc = dtc.fit(X, Y)
print("Decision Tree training finished!")

# 随机森林训练
rfc = RandomForestClassifier(n_estimators=200, oob_score=True, criterion="gini", \
    min_samples_split=2, min_samples_leaf=1, max_features="log2")
rfc = RandomForestClassifier(n_estimators=400, oob_score=True, criterion="gini")
rfc.fit(X, Y)
print("Random Forest training finished!")
print("Random Forest oob_score: " + str(rfc.oob_score_))

# dtc = tree.DecisionTreeClassifier(criterion="gini", max_depth=6, min_samples_split=2, \
#     min_samples_leaf=1, max_leaf_nodes=28)
# parameters = {'max_depth': range(2, 20)}
# kfold = KFold(n_splits=10)
# scoring_fnc = make_scorer(accuracy_score)
# grid = GridSearchCV(dtc, parameters, scoring_fnc, cv=kfold)
# grid = grid.fit(X, Y)
# clf = grid.best_estimator_
# for key in parameters.keys():
#     print('%s: %d'%(key, clf.get_params()[key]))

# viz.dt_viz(dtc, vec.get_feature_names())
# viz.rf_viz(rfc, vec.get_feature_names())

# 模型保存
joblib.dump(pca, "./model/test_pca.m")
joblib.dump(dtc, "./model/test_dt.m")
# joblib.dump(rfc, "./model/test_rf.m")
# joblib.dump(grid, "./model/test_grid.m")
print("All model saved!")