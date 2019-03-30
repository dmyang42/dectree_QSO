# -*- coding: utf-8 -*-

# 
# prediction of unlabeled sources in s82 variable source catalog
# author: topol @ USTC
# last modified: 2019/3/30
#
from data_util import std_data, get_feature, load_data
from sklearn.externals import joblib
import pandas as pd

rfc = joblib.load('./model/rf_4_all.m')
unlabeled_data, unlabeled_label, unlabeled_ID = load_data(filename='./train/other_sample_data4', mode='all')
feature = get_feature()
X_unlabeled, Y_unlabeled, vec_unlabeled = std_data(unlabeled_data, unlabeled_label, feature)
Y_predict = rfc.predict(X_unlabeled)

out_file = open('./result/mode_4_predict', "w+")
for i in zip(unlabeled_ID, Y_predict):
    print(int(float(i[0])), i[1], file=out_file)

print(pd.value_counts(Y_predict))