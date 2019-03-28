# 
# run RF for imbalance data set
# and do SMOTE to compensate this imbalance
# author: topol @ USTC
# last modified: 2019/3/26
#
from model_util import imbalance_data_set
from data_util import get_feature, std_data
from imblearn.over_sampling import SMOTE
from model_train import random_forest
from model_test import test_RF
import pandas as pd

train_data, train_label, test_data, test_label = imbalance_data_set(3, 3)
feature = get_feature('./train/raw/test_sample_data_1')
X, Y, vec = std_data(train_data, train_label, feature)
Y = Y.reshape(len(Y))
print("Original training set: ")
print(pd.value_counts(Y))

smo = SMOTE(random_state=3)
X_smo, Y_smo = smo.fit_sample(X, Y)
print("SMOTE training set: ")
print(pd.value_counts(Y_smo))

rfc = random_forest(X_smo, Y_smo)
X_test, Y_test, vec_test = std_data(test_data, test_label, feature)
test_RF(X_test, Y_test, rfc)

# smo = SMOTE(ratio={0:20000, 1:10000}, random_state=42)
# X_smo, Y_smo = smo.fit_sample(X, Y)
# rfc = random_forest(X_smo, Y_smo)
# test_RF(X_test, Y_test, rfc)
