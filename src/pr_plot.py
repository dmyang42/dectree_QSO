# -*- coding: utf-8 -*-

# 
# plot precision-recall curve
# author: topol @ USTC
# last modified: 2019/3/26
#
import matplotlib.pyplot as plt 
import numpy as np
from scipy.interpolate import spline

def read_score(filename, n1, n2):
    # n1是对于一个比例跑了多少个不同的随机数
    # n2是共有多少个测试集比例
    with open(filename) as f:
        lines = f.readlines()
        precisions, recalls, err_precisions, err_recalls = [], [], [], []
        for i in range(n2):
            precision, recall = [], []
            for line in lines[i*n1:(i+1)*n1]:
                line = line.split()
                precision.append(float(line[0]))
                recall.append(float(line[1]))
            precisions.append(sum(precision)/len(precision))
            recalls.append(sum(recall)/len(recall))
            err_precisions.append(np.std(precision)/np.sqrt(len(precision)))
            err_recalls.append(np.std(recall)/np.sqrt(len(recall)))
    return recalls, precisions, err_recalls, err_precisions

recall_1, precision_1, err_recall_1, err_precision_1 = read_score('./result/score_RF_imbalance_1_1.0', 50, 30)
recall_2_3, precision_2_3, err_recall_2_3, err_precision_2_3 = read_score('./result/score_RF_imbalance_2_3.0', 20, 30)
recall_2_6, precision_2_6, err_recall_2_6, err_precision_2_6 = read_score('./result/score_RF_imbalance_2_6.0', 20, 30)
recall_2_9, precision_2_9, err_recall_2_9, err_precision_2_9 = read_score('./result/score_RF_imbalance_2_9.0', 20, 30)
recall_2_12, precision_2_12, err_recall_2_12, err_precision_2_12 = read_score('./result/score_RF_imbalance_2_12.0', 20, 30)
# recall_3_3, precision_3_3 = read_score('./result/score_RF_imbalance_3_3')
# recall_3_6, precision_3_6 = read_score('./result/score_RF_imbalance_3_6')
# recall_3_10, precision_3_10 = read_score('./result/score_RF_imbalance_3_10')

plt.xlabel("testing set ratio (nQSO/QSO)")
plt.ylabel("qso precision")
test_size = [i / 2 for i in range(1,31,1)]
# interpolate_size = [i / 20 for i in range(10,301,1)]
# precision_1_smooth = spline(test_size, precision_1, interpolate_size)
# precision_2_3_smooth = spline(test_size, precision_2_3, interpolate_size)
# precision_2_6_smooth = spline(test_size, precision_2_6, interpolate_size)
# precision_2_9_smooth = spline(test_size, precision_2_9, interpolate_size)
# precision_2_12_smooth = spline(test_size, precision_2_12, interpolate_size)

plt.xlim(0, 16)

plt.scatter(test_size, precision_1, s=6, label="1:1 precision")
plt.scatter(test_size, recall_1, s=6, label="1:1 recall")
plt.errorbar(test_size, precision_1, yerr=err_precision_1, elinewidth=1, capsize=1)
plt.errorbar(test_size, recall_1, yerr=err_recall_1, elinewidth=1, capsize=1, alpha=0.6)

plt.scatter(test_size, precision_2_3, s=6, label="3:1 precision")
plt.scatter(test_size, recall_2_3, s=6, label="3:1 recall")
plt.errorbar(test_size, precision_2_3, yerr=err_precision_2_3, elinewidth=1,capsize=1)
plt.errorbar(test_size, recall_2_3, yerr=err_recall_2_3, elinewidth=1, capsize=1, alpha=0.6)

plt.scatter(test_size, precision_2_6, s=6, label="6:1 precision")
plt.scatter(test_size, recall_2_6, s=6, label="6:1 recall")
plt.errorbar(test_size, precision_2_6, yerr=err_precision_2_6, elinewidth=1,capsize=1)
plt.errorbar(test_size, recall_2_6, yerr=err_recall_2_6, elinewidth=1, capsize=1, alpha=0.6)

plt.scatter(test_size, precision_2_9, s=6, label="9:1 precision")
plt.scatter(test_size, recall_2_9, s=6, label="9:1 recall")
plt.errorbar(test_size, precision_2_9, yerr=err_precision_2_9, elinewidth=1,capsize=1)
plt.errorbar(test_size, recall_2_9, yerr=err_recall_2_9, elinewidth=1, capsize=1, alpha=0.6)

plt.scatter(test_size, precision_2_12, s=6, label="12:1 precision")
plt.scatter(test_size, recall_2_12, s=6, label="12:1 recall")
plt.errorbar(test_size, precision_2_12, yerr=err_precision_2_12, elinewidth=1,capsize=1)
plt.errorbar(test_size, recall_2_12, yerr=err_recall_2_12, elinewidth=1, capsize=1, alpha=0.6)

plt.legend()
plt.show()    