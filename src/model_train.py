# 
# model train module
# author: topol @ USTC
# last modified: 2019/3/21
#
from sklearn.decomposition import PCA 
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

def do_PCA(data):
    # PCA预处理 - 数据降维
    # PCA模型需要保存, 在测试集和实际使用时都要使用
    pca = PCA(n_components='mle', svd_solver='full')
    # pca = PCA()
    new_data = pca.fit_transform(data)
    print("PCA training finished! - with " + str(pca.n_components_) + " features")
    return pca, new_data

def decision_tree(X, Y):
    # 决策树训练, 也要保存下来测试使用
    dtc = DecisionTreeClassifier(criterion="gini", max_depth=6, min_samples_split=2, \
        min_samples_leaf=1, max_leaf_nodes=28)
    dtc = dtc.fit(X, Y)
    print("Decision Tree training finished!")
    return dtc

def random_forest(X, Y):
    # 随机森林训练
    rfc = RandomForestClassifier(n_estimators=200, oob_score=True, criterion="gini", \
        max_features="log2")
    rfc.fit(X, Y)
    print("Random Forest training finished!")
    print("Random Forest oob_score: " + str(rfc.oob_score_))
    return rfc

def adaptive_boost(X, Y):
    # AdaBoost训练
    abc = AdaBoostClassifier(DecisionTreeClassifier(max_depth=2, min_samples_split=20, min_samples_leaf=5),
                            algorithm="SAMME",
                            n_estimators=200, learning_rate=0.8)
    abc.fit(X, Y)
    print("AdaBoost training finished!")
    return abc

def gradient_boost(X, Y):
    # GBDT训练
    gbc = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60)
    gbc.fit(X, Y)
    print("GBDT training finished!")
    return gbc

def main():
    return 0
    
if __name__ == "__main__":
    main()