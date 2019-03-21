from sklearn.tree import _tree
from data_util import load_data, rnd_sampling

def load_data_set(mode, seed):
    # 抽样生成训练集、测试集
    # mode 0 - nqso是s82 std star的
    # mode 1 - nqso是做了iband filter并附加了dr7 quasar catalog
    # mode 2 - nqso仅做了iband filter
    qso_file = './train/QSO_sample_data' + str(mode)
    nqso_file = './train/nQSO_sample_data' + str(mode)
    QSO_data, QSO_label = load_data(qso_file)
    print("total QSO: ", len(QSO_label))
    nQSO_data, nQSO_label = load_data(nqso_file)
    print("total nQSO: ", len(nQSO_label))

    # 生成random sampling的数据集
    # 5500 / 800 为 训练集 / 测试集
    rnd_train_QSO_data, rnd_train_QSO_label, rnd_test_QSO_data, rnd_test_QSO_label \
        = rnd_sampling(QSO_data, QSO_label, 5600, 800, seed)
    rnd_train_nQSO_data, rnd_train_nQSO_label, rnd_test_nQSO_data, rnd_test_nQSO_label \
        = rnd_sampling(nQSO_data, nQSO_label, 5600, 800, seed)

    train_data = rnd_train_QSO_data + rnd_train_nQSO_data
    train_label = rnd_train_QSO_label + rnd_train_nQSO_label
    test_data = rnd_test_QSO_data + rnd_test_nQSO_data
    test_label = rnd_test_QSO_label + rnd_test_nQSO_label
    
    return train_data, train_label, test_data, test_label

def tree_to_code(tree, feature_names):
    # turn tree to python function
    # ref: https://stackoverflow.com/questions/20224526/how-to-extract-the-decision-rules-from-scikit-learn-decision-tree/22261053
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print("{}if {} <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print("{}else:  # if {} > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            print("{}return {}".format(indent, tree_.value[node]))

    recurse(0, 1)