# -*- coding: utf-8 -*-

# 
# util used in model fitting
# primary job is to load QSO_sample_data & nQSO_sample_data and to do random sampling
# author: topol @ USTC
# last modified: 2019/3/19
#
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
import random
from MyError import *

def get_feature(mode='all'):
    if mode == 'all':
        filename = './train/raw/test_sample_data_1'
        try:
            with open(filename) as f:
                lines = f.readlines()
                feature = lines[0].split()
                feature.remove('ID')
                feature.remove('MiQSO') # MiQSO相当于label, 从feature中移除
            return feature
        except FileNotFoundError:
            # 存在部分块不存在的情况
            print("Missing part: " + filename)
            return []
    elif mode == 'color':
        return ['ug', 'gr', 'ri', 'iz']
    elif mode == 'variability':
        return ['gAmpl', 'rAmpl', 'iAmpl', 'tau_u', 'tau_g', 'tau_r', 'tau_i', \
            'tau_z', 'sigma_u ', ' sigma_g ', ' sigma_r ', ' sigma_i ', ' sigma_z']
    else:
        raise InputError('No such feature mode!')

def norm_label(label):
    # 输入一个未处理的label列表
    # 返回处理后(0,1)的label列表
    # 0 -- 不是QSO
    # 1 -- 是QSO
    label_list = label
    for i in range(len(label_list)):
        if -0.001 < label_list[i] + 9.9 < 0.001:
            label_list[i] = str(0)
        else:
            label_list[i] = str(1)
    return label_list

def all_feature(_line):
    # 全部feature都使用
    return _line

def color_feature(_line):
    # 仅使用颜色feature
    _sub_line = _line[0:4]
    return _sub_line

def variability_feature(_line):
    # 仅使用光变feature
    _sub_line = _line[4:]
    return _sub_line

def load_data(filename, mode):
    # 导入单个数据块数据,保存为矩阵格式输出
    # label代表是否是QSO
    try:
        with open(filename) as f:
            lines = f.readlines()
            data, label, ID = [], [], []
            feature = lines[0].split()
            feature.remove('MiQSO') # MiQSO相当于label, 从feature中移除
            for line in lines[1:]:
                line = line.split()
                _id = line[0]
                line = line[1:]
                try:
                    line = list(map(eval, line))
                except NameError:
                    # 存在部分数据为inf
                    # 主要是JAVELIN拟合出的tau或sigma
                    # 这里的处理是直接扔掉该源
                    print("Infinity!")
                except SyntaxError:
                    print("EOF line!")
                else:
                    ID.append(_id)
                    label.append(line.pop(7)) # MiQSO对应的为7,pop掉
                    # now line features are:
                    # ug / gr / ri / iz / gAmpl / rAmpl / iAmpl / 
                    # tau_u / tau_g / tau_r / tau_i / tau_z / 
                    # sigma_u / sigma_g / sigma_r / sigma_i / sigma_z
                    # 0-3 are color
                    # 4-16 are variability
                    if mode == 'all':
                        sample = all_feature(line)
                    elif mode == 'color':
                        sample = color_feature(line)
                    elif mode == 'variability':
                        sample = variability_feature(line)
                    else:
                        raise InputError('No such feature mode!')
                    data.append(sample)
            label = norm_label(label)
        return data, label, ID
    except FileNotFoundError:
        # 存在部分块不存在的情况
        print("Missing part: " + filename)
        return [], []

def rnd_sampling(data, label, train_size, test_size, seed):
    # 随机抽样产生训练集和测试集
    random.seed(seed)
    rnd_train_data, rnd_train_label = [], []
    rnd_test_data, rnd_test_label = [], []
    if train_size + test_size < len(label):
        rnd_index = random.sample([i for i in range(len(label))], train_size + test_size)
        rnd_train_index = rnd_index[:train_size]
        rnd_test_index = rnd_index[train_size+1:]
        for index in rnd_train_index:
            rnd_train_data.append(data[index])
            rnd_train_label.append(label[index])
        for index in rnd_test_index:
            rnd_test_data.append(data[index])
            rnd_test_label.append(label[index])
        return rnd_train_data, rnd_train_label, \
            rnd_test_data, rnd_test_label
    else:
        print("Random sampling size too large!")
        return [], [], [], []

# def merge_data(index_list):
#     # 合并多个数据块
#     merged_data, merged_label = [], []
#     for i in index_list:
#         filename = "./train/test_sample_data_" + str(i)
#         data, label = load_data(filename)
#         merged_data = merged_data + data
#         merged_label = merged_label + label
#     return merged_data, merged_label

def std_data(data, label, feature):
    # 标准化数据格式, data_list为存放字典的列表
    # 每一个字典表示一个数据, 或者说一个源
    # 此处feature为之前各个feature的线性组合
    data_list = []
    for i in range(len(data)):
        unit_dict = {}
        for j in range(len(feature)):
            unit_dict[feature[j]] = data[i][j]
        data_list.append(unit_dict)
    vec = DictVectorizer()

    X = vec.fit_transform(data_list).toarray()
    lb = preprocessing.LabelBinarizer()
    Y = lb.fit_transform(label)
    return X, Y, vec

def main():
    data, label = merge_data(1,20)
    print(len(data))
    print(len(label))

if __name__ == "__main__":
    main()