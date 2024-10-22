# -*- coding: utf-8 -*-

# 
# util used in model fitting
# primary jobs are:
# 1) load different mode data set
# 2) print feature importances of specific clf
# 3) turn clf into python function code
# author: topol @ USTC
# last modified: 2019/3/30
#
from sklearn.tree import _tree
from data_util import load_data, rnd_sampling
import numpy as np

def load_data_set(mode, feature_mode, seed=3):
    # 抽样生成训练集、测试集
    # mode 0 - nqso是s82 std star的
    # mode 1 - nqso是做了iband filter并附加了dr7 quasar catalog
    qso_file = './train/QSO_sample_data' + str(mode)
    nqso_file = './train/nQSO_sample_data' + str(mode)
    QSO_data, QSO_label, _ = load_data(qso_file, feature_mode)
    print("total QSO: ", len(QSO_label))
    nQSO_data, nQSO_label, _ = load_data(nqso_file, feature_mode)
    print("total nQSO: ", len(nQSO_label))

    min_size = min(len(QSO_label), len(nQSO_label))
    train_size = int(min_size * 5 / 6 - 1)
    test_size = int(min_size / 6 - 1)
    print("Training Set Size: ", train_size)
    print("Testing Set Size: ", test_size)
    print()

    # 生成random sampling的数据集
    # 训练集 / 测试集 = 5 : 1
    rnd_train_QSO_data, rnd_train_QSO_label, rnd_test_QSO_data, rnd_test_QSO_label \
        = rnd_sampling(QSO_data, QSO_label, train_size, test_size, seed)
    rnd_train_nQSO_data, rnd_train_nQSO_label, rnd_test_nQSO_data, rnd_test_nQSO_label \
        = rnd_sampling(nQSO_data, nQSO_label, train_size, test_size, seed)

    train_data = rnd_train_QSO_data + rnd_train_nQSO_data
    train_label = rnd_train_QSO_label + rnd_train_nQSO_label
    test_data = rnd_test_QSO_data + rnd_test_nQSO_data
    test_label = rnd_test_QSO_label + rnd_test_nQSO_label
    
    return train_data, train_label, test_data, test_label

def imbalance_data_set(mode, train_ratio, test_ratio, seed):
    # return imbalance train and test data set
    QSO_data, QSO_label, _ = load_data(filename='./train/QSO_sample_data3', mode='all')
    nQSO_data, nQSO_label, _ = load_data(filename='./train/nQSO_sample_data3', mode='all')
    rnd_train_QSO_data, rnd_train_QSO_label, rnd_test_QSO_data, rnd_test_QSO_label \
            = rnd_sampling(QSO_data, QSO_label, 1600, 400, seed)
    rnd_train_nQSO_data, rnd_train_nQSO_label, rnd_test_nQSO_data, rnd_test_nQSO_label \
            = rnd_sampling(nQSO_data, nQSO_label, int(1600*train_ratio), int(400*test_ratio), seed)
    train_data = rnd_train_QSO_data + rnd_train_nQSO_data
    train_label = rnd_train_QSO_label + rnd_train_nQSO_label
    test_data = rnd_test_QSO_data + rnd_test_nQSO_data
    test_label = rnd_test_QSO_label + rnd_test_nQSO_label
    return train_data, train_label, test_data, test_label

def print_feature_importance(clf, feature):
    # 打印分类器clf的feature_importances_
    # ref: https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    for f in range(len(feature)):
        print("%2d) %-*s %f" % (f + 1, 30, feature[indices[f]], importances[indices[f]]))


def tree_to_code(tree, feature_names):
    # turn tree to python function
    # ref: https://stackoverflow.com/questions/20224526/how-to-extract-the-decision-rules-from-scikit-learn-decision-tree/22261053
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print("{}if {} <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print("{}else:  # if {} > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            print("{}return {}".format(indent, tree_.value[node]))

    recurse(0, 1)