from model_test import test_DT, test_RF, test_AB, test_GB
from model_util import tree_to_code, load_data_set
from data_util import std_data, get_feature
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np

def print_best_score(gsearch, param_test):
     # 输出best score
    print("Best score: %0.3f" % gsearch.best_score_)
    print("Best parameters set:")
    # 输出最佳的分类器到底使用了怎样的参数
    best_parameters = gsearch.best_estimator_.get_params()
    for param_name in sorted(param_test.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))


def dtc_parameter(param, range, X, Y):
    # do grid search to search the best 'param' in 'range' of dtc
    # 'param' and 'range' should be lists
    param_test = dict(zip(param, range))
    dtc = DecisionTreeClassifier(criterion="gini", max_depth=6, min_samples_split=4, \
        min_samples_leaf=1, max_leaf_nodes=16)
    gsearch = GridSearchCV(estimator=dtc, param_grid = param_test, scoring='roc_auc', cv=5)
    gsearch.fit(X,Y)
    # gsearch.grid_scores_, gsearch.best_params_, gsearch.best_score_
    print_best_score(gsearch, param_test)

def rfc_parameter(param, range, X, Y):
    # do grid search to search the best 'param' in 'range' of rfc
    # 'param' and 'range' should be lists
    param_test = dict(zip(param, range))
    rfc = RandomForestClassifier(n_estimators=1000, oob_score=True, criterion="gini", \
        max_features="log2", class_weight={0:1,1:6})
    gsearch = GridSearchCV(estimator=rfc, param_grid = param_test, scoring='roc_auc', cv=5)
    gsearch.fit(X,Y)
    # gsearch.grid_scores_, gsearch.best_params_, gsearch.best_score_
    print_best_score(gsearch, param_test)

def abc_parameter(param, range, X, Y):
    # do grid search to search the best 'param' in 'range' of abc
    # 'param' and 'range' should be lists
    param_test = dict(zip(param, range))
    abc = AdaBoostClassifier(DecisionTreeClassifier(max_depth=6, min_samples_split=10, min_samples_leaf=2),
                            algorithm="SAMME",
                            n_estimators=60, learning_rate=0.7)
    gsearch = GridSearchCV(estimator=abc, param_grid = param_test, scoring='roc_auc', cv=5)
    gsearch.fit(X,Y)
    # gsearch.grid_scores_, gsearch.best_params_, gsearch.best_score_
    print_best_score(gsearch, param_test)

def gbc_parameter(param, range, X, Y):
    # do grid search to search the best 'param' in 'range' of gbc
    # 'param' and 'range' should be lists
    param_test = dict(zip(param, range))
    gbc = GradientBoostingClassifier(learning_rate=0.6, n_estimators=65)
    gsearch = GridSearchCV(estimator=gbc, param_grid = param_test, scoring='roc_auc', cv=5)
    gsearch.fit(X,Y)
    # gsearch.grid_scores_, gsearch.best_params_, gsearch.best_score_
    print_best_score(gsearch, param_test)

# 1 - load data
train_data, train_label, test_data, test_label = load_data_set(2, 7000, 1200, 42)
feature = get_feature('./train/raw/test_sample_data_1')
X, Y, vec = std_data(train_data, train_label, feature)
Y = Y.reshape(len(Y))

# 2 - do gricSearchCV

# for dtc
# param = ["max_depth", "min_samples_split", "min_samples_leaf", "max_leaf_nodes"]
# param_range = [range(3,15,1), range(2,10,1), range(1,3,1), range(10,50,2)]
# dtc_parameter(param, param_range, X, Y)

# for abc
# param = ['n_estimators', 'learning_rate']
# param_range = [range(50,70,4), [0.1 * i for i in range(5,10,1)]]
# abc_parameter(param, param_range, X, Y)

# for gbc
param = ['n_estimators', 'learning_rate']
param_range = [range(40,80,5), [0.1 * i for i in range(5,10,1)]]
abc_parameter(param, param_range, X, Y)