# 
# model train module
# author: topol @ USTC
# last modified: 2019/3/19
#
from sklearn.decomposition import PCA 
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree

def PCA(data):
    # PCA预处理 - 数据降维
    # PCA模型需要保存, 在测试集和实际使用时都要使用
    # pca = PCA(n_components='mle', svd_solver='full')
    pca = PCA()
    new_data = pca.fit_transform(data)
    print("PCA training finished! - with " + str(pca.n_components_) + " features")
    return pca, new_data

def DT(X, Y):
    # 决策树训练, 也要保存下来测试使用
    dtc = tree.DecisionTreeClassifier(criterion="gini", max_depth=6, min_samples_split=2, \
        min_samples_leaf=1, max_leaf_nodes=28)
    dtc = dtc.fit(X, Y)
    print("Decision Tree training finished!")
    return dtc

def RF(X, Y):
    # 随机森林训练
    rfc = RandomForestClassifier(n_estimators=200, oob_score=True, criterion="gini", \
        max_features="log2")
    rfc.fit(X, Y)
    print("Random Forest training finished!")
    print("Random Forest oob_score: " + str(rfc.oob_score_))
    return rfc