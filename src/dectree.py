# -*- coding: utf-8 -*-

# 
# the 'main' script
# using command 'python dectree.py 1 3' to run
# 1 represents data sets mode
# 3 represents a random seed
# author: topol @ USTC
# last modified: 2019/3/30
#
from model_train import do_PCA, decision_tree, random_forest, adaptive_boost, gradient_boost
from model_test import test_DT, test_RF, test_AB, test_GB
from model_util import tree_to_code, load_data_set, print_feature_importance
from sklearn.externals import joblib
from data_util import std_data, get_feature, load_data
import sys
import numpy as np
# import subprocess
import model_visualize as viz
import argparse

# 参数输入
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--data-mode', type=int, default=3)
parser.add_argument('--feature-mode', type=str, default='all')
parser.add_argument('--random-seed', type=int, default=3)
args = parser.parse_args()

mode = args.data_mode
feature_mode = args.feature_mode
seed = args.random_seed

# 抽样生成训练集、测试集
# mode 0 - nqso是s82 std star的(作废!)
# mode 1 - nqso是做了iband filter并附加了dr7 quasar catalog(作废!)
# mode 2 - 我们自己乱搞的(作废!)
# mode 3 - 所有源i_band < 19.0
# mode 4 - 光谱认证(clean)
train_data, train_label, test_data, test_label = load_data_set(mode, feature_mode, seed)

# 1 - PCA预处理 - 数据降维(作废!)
# pca, new_data = do_PCA(train_data)
new_data = train_data

# 2 - 数据格式标准化
feature = get_feature(feature_mode)
# feature = list(map(str, range(pca.n_components_)))
X, Y, vec = std_data(new_data, train_label, feature)
Y = Y.reshape(len(Y))

# 3 - 决策树训练
dtc = decision_tree(X, Y)
# print_feature_importance(dtc, vec.get_feature_names())

# 4 - 随机森林训练
rfc = random_forest(X, Y)
# print_feature_importance(rfc, vec.get_feature_names())

# 5 - AdaBoost训练
# abc = adaptive_boost(X, Y)
# print_feature_importance(abc, vec.get_feature_names())

# 6- GBDT训练
# gbc = gradient_boost(X, Y)
# print_feature_importance(gbc, vec.get_feature_names())

# viz.dt_viz(dtc, vec.get_feature_names())
# viz.rf_viz(rfc, vec.get_feature_names())

# 6 - 模型测试
# new_data = pca.transform(test_data)
new_data = test_data
X, Y, vec = std_data(new_data, test_label, feature)
qso_precision_DT, qso_recall_DT, nqso_precision_DT, nqso_recall_DT, score_DT = test_DT(X, Y, dtc)
qso_precision_RF, qso_recall_RF, nqso_precision_RF, nqso_recall_RF, score_RF = test_RF(X, Y, rfc)
# qso_precision_AB, qso_recall_AB, nqso_precision_AB, nqso_recall_AB, score_AB = test_AB(X, Y, abc)
# qso_precision_GB, qso_recall_GB, nqso_precision_GB, nqso_recall_GB, score_GB = test_GB(X, Y, gbc)

# f1 = open("./result/score_DT_"+str(mode)+"_"+feature_mode, "a+")
# f2 = open("./result/score_RF_"+str(mode)+"_"+feature_mode, "a+")
# f3 = open("./result/score_AB_"+str(mode)+"_"+feature_mode, "a+")
# f4 = open("./result/score_GB_"+str(mode)+"_"+feature_mode, "a+")
# print(qso_precision_DT, qso_recall_DT, nqso_precision_DT, nqso_recall_DT, score_DT, file=f1)
# print(qso_precision_RF, qso_recall_RF, nqso_precision_RF, nqso_recall_RF, score_RF, file=f2)
# print(qso_precision_AB, qso_recall_AB, nqso_precision_AB, nqso_recall_AB, score_AB, file=f3)
# print(qso_precision_GB, qso_recall_GB, nqso_precision_GB, nqso_recall_GB, score_GB, file=f4)

# trun tree model to python function
# ! - dtc only
# tree_to_code(dtc, feature)

# 7 - 模型保存
# joblib.dump(pca, "./model/test_pca.m")
joblib.dump(dtc, "./model/dt_"+str(mode)+"_"+feature_mode+".m")
joblib.dump(rfc, "./model/rf_"+str(mode)+"_"+feature_mode+".m")
# joblib.dump(abc, "./model/ab_"+str(mode)+"_"+feature_mode+".m")
# joblib.dump(gbc, "./model/gbc_"+str(mode)+"_"+feature_mode+".m")
print("All model saved!")

