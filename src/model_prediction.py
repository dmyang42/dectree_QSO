# -*- coding: utf-8 -*-

# 
# prediction of unknown sources in s82 variable source catalog
# author: topol @ USTC
# last modified: 2019/3/25
#
from data_util import std_data, get_feature, load_data
from sklearn.externals import joblib
import pandas as pd

rfc = joblib.load('./model/test_rf.m')
unknown_data, unknown_label = load_data('./train/other_sample_data4')
feature = get_feature('./train/raw/test_sample_data_1')
X_unknown, Y_unknown, vec_unknown = std_data(unknown_data, unknown_label, feature)
Y_predict = rfc.predict(X_unknown)
print(pd.value_counts(Y_predict))