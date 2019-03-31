# -*- coding: utf-8 -*-

# 
# run RF for imbalance data set
# and do SMOTE to compensate this imbalance
# author: topol @ USTC
# last modified: 2019/3/30
#
from model_util import imbalance_data_set
from data_util import get_feature, std_data
from imblearn.over_sampling import SMOTE
from model_train import random_forest
from model_test import test_RF
import pandas as pd
import sys
import argparse
from MyError import *

def if_SMOTE(X, Y, flag=True, bias={0:1,1:1}):
    if flag is 1:
        # doing SMOTE
        smo = SMOTE(random_state=3)
        X_smo, Y_smo = smo.fit_sample(X, Y)
        print("SMOTE training set: ")
        print(pd.value_counts(Y_smo))
    elif flag is 0:
        # without doing SMOTE
        X_smo, Y_smo = X, Y

    class_weight = bias
    return X, Y, class_weight

# 参数输入
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--train-ratio', type=float, default=1)
parser.add_argument('--test-ratio', type=float, default=1)
parser.add_argument('--class-bias', type=float, default=1)
parser.add_argument('--random-seed', type=int, default=3)
parser.add_argument('--if-SMOTE', type=int, default=0)
parser.add_argument('--task-type', type=int, default=1) # three task type in total
# 1 - 训练集1:1, 测试集各种比例下的结果(绘制PR曲线)
# 2 - 训练集比例变化(用更多0类), 测试集各种比例下结果
# 3 - 训练集同上, 并做SMOTE, 测试集各种比例下结果 

args = parser.parse_args()

_seed = args.random_seed
_train_ratio = args.train_ratio
_test_ratio = args.test_ratio
_bias = args.class_bias
_flag = args.if_SMOTE
_task_type = args.task_type

train_data, train_label, test_data, test_label = imbalance_data_set(3, _train_ratio, _test_ratio, _seed)
feature = get_feature()
X, Y, vec = std_data(train_data, train_label, feature)
Y = Y.reshape(len(Y))
print("Original training set: ")
print(pd.value_counts(Y))

if _flag is 1:
    X_smo, Y_smo, class_weight = if_SMOTE(X, Y, flag=_flag, bias={0:1,1:_bias})
elif _flag is 0:
    X_smo, Y_smo, class_weight = if_SMOTE(X, Y, flag=_flag)
else:
    raise InputError('Input Flas Illegal!')

rfc = random_forest(X_smo, Y_smo, bias=True, _class_weight=class_weight)
X_test, Y_test, vec_test = std_data(test_data, test_label, feature)
_, _, qso_precision_RF, qso_recall_RF, _ = test_RF(X_test, Y_test, rfc)

f = open("./result/score_RF_imbalance_"+str(_task_type)+'_'+str(_train_ratio), "a+")
print(qso_precision_RF, qso_recall_RF, file=f)

# smo = SMOTE(ratio={0:20000, 1:10000}, random_state=42)
# X_smo, Y_smo = smo.fit_sample(X, Y)
# rfc = random_forest(X_smo, Y_smo)
# test_RF(X_test, Y_test, rfc)
