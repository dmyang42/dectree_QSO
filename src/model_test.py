# -*- coding: utf-8 -*-

# 
# model test module
# author: topol @ USTC
# last modified: 2019/3/21
#
from data_util import get_feature
from sklearn.externals import joblib
from data_util import std_data
from sklearn.metrics import classification_report, confusion_matrix  

def calculate_precision(TP, FP):
    # precision = TP / (TP + FP)
    # TP: True Positive
    # FP: False Positive
    return TP / (TP + FP)

def calculate_recall(TP, FN):
    # recall = TP / (TP + FN)
    # TP: True Positive
    # FN: False Negative
    return TP / (TP + FN)

def test_DT(X, Y, dtc):
    # decision tree test
    Y_pred_dtc = dtc.predict(X)
    print("DTC Test Result: ")
    print("*******************************************")
    target_names = ['Not QSO', 'QSO']
    matrix = confusion_matrix(Y, Y_pred_dtc)
    print(matrix)
    qso_precision = calculate_precision(matrix[0][0], matrix[1][0])
    qso_recall = calculate_recall(matrix[0][0], matrix[0][1])
    nqso_precision = calculate_precision(matrix[1][1], matrix[0][1])
    nqso_recall = calculate_precision(matrix[1][1], matrix[1][0])
    print(classification_report(Y, Y_pred_dtc, target_names=target_names, digits=6))
    print("total score: ", dtc.score(X, Y))
    print("*******************************************\n")
    return qso_precision, qso_recall, nqso_precision, nqso_recall, dtc.score(X, Y)

def test_RF(X, Y, rfc):
    # random forest test
    Y_pred_rfc = rfc.predict(X)
    print("RFC Test Result(" + str(rfc.n_estimators) + "): ")
    print("*******************************************")
    target_names = ['Not QSO', 'QSO']
    matrix = confusion_matrix(Y, Y_pred_rfc)
    print(matrix)
    qso_precision = calculate_precision(matrix[0][0], matrix[1][0])
    qso_recall = calculate_recall(matrix[0][0], matrix[0][1])
    nqso_precision = calculate_precision(matrix[1][1], matrix[0][1])
    nqso_recall = calculate_precision(matrix[1][1], matrix[1][0])
    print(classification_report(Y, Y_pred_rfc, target_names=target_names, digits=6))
    print("total score: ", rfc.score(X, Y))
    print("*******************************************\n")
    return qso_precision, qso_recall, nqso_precision, nqso_recall, rfc.score(X, Y)

def test_AB(X, Y, abc):
    # decision tree test
    Y_pred_abc = abc.predict(X)
    print("ABC Test Result: ")
    print("*******************************************")
    target_names = ['Not QSO', 'QSO']
    matrix = confusion_matrix(Y, Y_pred_abc)
    print(matrix)
    qso_precision = calculate_precision(matrix[0][0], matrix[1][0])
    qso_recall = calculate_recall(matrix[0][0], matrix[0][1])
    nqso_precision = calculate_precision(matrix[1][1], matrix[0][1])
    nqso_recall = calculate_precision(matrix[1][1], matrix[1][0])
    print(classification_report(Y, Y_pred_abc, target_names=target_names, digits=6))
    print("total score: ", abc.score(X, Y))
    print("*******************************************\n")
    return qso_precision, qso_recall, nqso_precision, nqso_recall, abc.score(X, Y)

def test_GB(X, Y, gbc):
    # decision tree test
    Y_pred_gbc = gbc.predict(X)
    print("GBC Test Result: ")
    print("*******************************************")
    target_names = ['Not QSO', 'QSO']
    matrix = confusion_matrix(Y, Y_pred_gbc)
    print(matrix)
    qso_precision = calculate_precision(matrix[0][0], matrix[1][0])
    qso_recall = calculate_recall(matrix[0][0], matrix[0][1])
    nqso_precision = calculate_precision(matrix[1][1], matrix[0][1])
    nqso_recall = calculate_precision(matrix[1][1], matrix[1][0])
    print(classification_report(Y, Y_pred_gbc, target_names=target_names, digits=6))
    print("total score: ", gbc.score(X, Y))
    print("*******************************************\n")
    return qso_precision, qso_recall, nqso_precision, nqso_recall, gbc.score(X, Y)

def main():
    # ignore this part!

    test_index_list = range(0, 20)
    test_data, test_label = merge_data(test_index_list)
    best_rfc = joblib.load('./model/best_rf.m')
    # trained_grid = joblib.load('./model/test_grid.m')
    trained_pca = joblib.load('./model/test_pca.m')
    new_data = trained_pca.transform(test_data)

    # feature = get_feature('./train/test_sample_data_1')
    feature = list(map(str, range(trained_pca.n_components_)))
    X, Y, vec = std_data(new_data, test_label, feature)

    Y_best_rfc = best_rfc.predict(X)
    print("Best RFC Test Result(" + str(best_rfc.n_estimators) + "): ")
    print("*******************************************")
    target_names = ['Not QSO', 'QSO']
    print(confusion_matrix(Y, Y_best_rfc))  
    print(classification_report(Y, Y_best_rfc, target_names=target_names))
    print("total score: ", best_rfc.score(X, Y))

if __name__ == "__main__":
    main()