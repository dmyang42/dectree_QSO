from model_train import PCA, DT, RF
from model_test import test_DT, test_RF
from sklearn.externals import joblib
from data_util import load_data, std_data, get_feature, rnd_sampling
import sys
# import subprocess
# import data_visualize as viz

seed = int(sys.argv[1])
# 抽样生成训练集、测试集
QSO_data, QSO_label = load_data('./train/QSO_sample_data')
print("total QSO: ", len(QSO_label))
nQSO_data, nQSO_label = load_data('./train/nQSO_sample_data')
print("total nQSO: ", len(nQSO_label))

rnd_train_QSO_data, rnd_train_QSO_label, rnd_test_QSO_data, rnd_test_QSO_label \
    = rnd_sampling(QSO_data, QSO_label, 5000, 800, seed)
rnd_train_nQSO_data, rnd_train_nQSO_label, rnd_test_nQSO_data, rnd_test_nQSO_label \
    = rnd_sampling(nQSO_data, nQSO_label, 5000, 800, seed)

train_data = rnd_train_QSO_data + rnd_train_nQSO_data
train_label = rnd_train_QSO_label + rnd_train_nQSO_label
test_data = rnd_test_QSO_data + rnd_test_nQSO_data
test_label = rnd_test_QSO_label + rnd_test_nQSO_label

# 1 - PCA预处理 - 数据降维
# 出了点问题，暂时没有做PCA
# pca, new_data = PCA(train_data)
new_data = train_data

# 2 - 数据格式标准化
feature = get_feature('./train/test_sample_data_1')
# feature = list(map(str, range(pca.n_components_)))
X, Y, vec = std_data(new_data, train_label, feature)

# 3 - 决策树训练
dtc = DT(X, Y)

# 4 - 随机森林训练
rfc = RF(X, Y)

# viz.dt_viz(dtc, vec.get_feature_names())
# viz.rf_viz(rfc, vec.get_feature_names())

# 5 - 模型测试
# new_data = pca.transform(test_data)
new_data = test_data
X, Y, vec = std_data(new_data, test_label, feature)
score_DT = test_DT(X, Y, dtc)
score_RF = test_RF(X, Y, rfc)

f1 = open("score_DT", "a+")
f2 = open("score_RF", "a+")
print(score_DT, file=f1)
print(score_RF, file=f2)

# 6 - 模型保存
# joblib.dump(pca, "./model/test_pca.m")
# joblib.dump(dtc, "./model/test_dt.m")
# joblib.dump(rfc, "./model/test_rf.m")
# print("All model saved!")

