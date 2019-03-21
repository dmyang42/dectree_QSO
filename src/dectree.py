# 
# the 'main' script
# using command 'python dectree.py 3' to run
# 3 represents a random seed
# author: topol @ USTC
# last modified: 2019/3/21
#
from model_train import do_PCA, decision_tree, random_forest, adaptive_boost, gradient_boost
from model_test import test_DT, test_RF, test_AB, test_GB
from model_util import tree_to_code, load_data_set
from sklearn.externals import joblib
from data_util import std_data, get_feature
import sys
# import subprocess
import model_visualize as viz

seed = int(sys.argv[1])
# 抽样生成训练集、测试集
mode = 0
train_data, train_label, test_data, test_label = load_data_set(mode, seed)

# 1 - PCA预处理 - 数据降维
# pca, new_data = do_PCA(train_data)
new_data = train_data

# 2 - 数据格式标准化
feature = get_feature('./train/test_sample_data_1')
# feature = list(map(str, range(pca.n_components_)))
X, Y, vec = std_data(new_data, train_label, feature)

# 3 - 决策树训练
dtc = decision_tree(X, Y)

# 4 - 随机森林训练
rfc = random_forest(X, Y)

# 5 - AdaBoost训练
abc = adaptive_boost(X, Y)

# 6- GBDT训练
gbc = gradient_boost(X, Y)

# viz.dt_viz(dtc, vec.get_feature_names())
# viz.rf_viz(rfc, vec.get_feature_names())

# 6 - 模型测试
# new_data = pca.transform(test_data)
new_data = test_data
X, Y, vec = std_data(new_data, test_label, feature)
qso_precision_DT, qso_recall_DT, nqso_precision_DT, nqso_recall_DT, score_DT = test_DT(X, Y, dtc)
qso_precision_RF, qso_recall_RF, nqso_precision_RF, nqso_recall_RF, score_RF = test_RF(X, Y, rfc)
qso_precision_AB, qso_recall_AB, nqso_precision_AB, nqso_recall_AB, score_AB = test_AB(X, Y, abc)
qso_precision_GB, qso_recall_GB, nqso_precision_GB, nqso_recall_GB, score_GB = test_GB(X, Y, gbc)

f1 = open("score_DT_0", "a+")
f2 = open("score_RF_0", "a+")
f3 = open("score_AB_0", "a+")
f4 = open("score_GB_0", "a+")
print(qso_precision_DT, qso_recall_DT, nqso_precision_DT, nqso_recall_DT, score_DT, file=f1)
print(qso_precision_RF, qso_recall_RF, nqso_precision_RF, nqso_recall_RF, score_RF, file=f2)
print(qso_precision_AB, qso_recall_AB, nqso_precision_AB, nqso_recall_AB, score_AB, file=f3)
print(qso_precision_GB, qso_recall_GB, nqso_precision_GB, nqso_recall_GB, score_GB, file=f4)

# trun tree model to python function
# ! - dtc only
# tree_to_code(dtc, feature)

# 7 - 模型保存
# joblib.dump(pca, "./model/test_pca.m")
# joblib.dump(dtc, "./model/test_dt.m")
# joblib.dump(rfc, "./model/test_rf.m")
# joblib.dump(abc, "./model/test_ab.m")
# joblib.dump(gbc, "./model/test_gbc.m")
# print("All model saved!")

