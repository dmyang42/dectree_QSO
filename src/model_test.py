# 
# model test module
# author: topol @ USTC
# last modified: 2019/3/19
#
from data_util import get_feature
from sklearn.externals import joblib
from data_util import std_data
from sklearn.metrics import classification_report, confusion_matrix  

def test_DT(X, Y, dtc):
    # decision tree test
    Y_pred_dtc = dtc.predict(X)
    print("DTC Test Result: ")
    print("*******************************************")
    target_names = ['Quasar', 'Not QSO']
    print(confusion_matrix(Y, Y_pred_dtc))  
    print(classification_report(Y, Y_pred_dtc, target_names=target_names, digits=4))
    print("total score: ", dtc.score(X, Y))
    print("*******************************************\n")
    return dtc.score(X, Y)

def test_RF(X, Y, rfc):
    # random forest test
    Y_pred_rfc = rfc.predict(X)
    print("RFC Test Result(" + str(rfc.n_estimators) + "): ")
    print("*******************************************")
    target_names = ['Quasar', 'Not QSO']
    print(confusion_matrix(Y, Y_pred_rfc))  
    print(classification_report(Y, Y_pred_rfc, target_names=target_names, digits=4))
    print("total score: ", rfc.score(X, Y))
    print("*******************************************\n")
    return rfc.score(X, Y)
    
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
    target_names = ['Quasar', 'Not QSO']
    print(confusion_matrix(Y, Y_best_rfc))  
    print(classification_report(Y, Y_best_rfc, target_names=target_names))
    print("total score: ", best_rfc.score(X, Y))

if __name__ == "__main__":
    main()