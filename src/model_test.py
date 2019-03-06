from data_util import merge_data
from sklearn.externals import joblib
from data_util import std_data
from sklearn.metrics import classification_report, confusion_matrix  

test_index_list = range(1, 10)
test_data, test_label = merge_data(test_index_list)
trained_dtc = joblib.load('./model/test_dt.m')
trained_rfc = joblib.load('./model/test_rf.m')
trained_pca = joblib.load('./model/test_pca.m')
new_data = trained_pca.transform(test_data)

feature = list(map(str, range(trained_pca.n_components_)))
X, Y, vec = std_data(new_data, test_label, feature)
Y_pred_dtc = trained_dtc.predict(X)
print("DTC Test Result: ")
print("*******************************************")
print(confusion_matrix(Y, Y_pred_dtc))  
print(classification_report(Y, Y_pred_dtc))
print("*******************************************\n")

Y_pred_rfc = trained_rfc.predict(X)
print("RFC Test Result(" + str(trained_rfc.n_estimators) + "): ")
print("*******************************************")
print(confusion_matrix(Y, Y_pred_rfc))  
print(classification_report(Y, Y_pred_rfc))