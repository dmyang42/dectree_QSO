# -*- coding: utf-8 -*-

# 
# author: topol @ USTC
# last modified: 2019/3/23
#

from data_organize import read_ID_file
import matplotlib.pyplot as plt

def if_quasar(MiQSO):
    if -0.001 < MiQSO + 9.9 < 0.001:
        return 0
    else:
        return 1

additional_quasar_ID = read_ID_file('./data/additional_confirmed_quasar')
with open('./data/stripe82candidateVar_v1.1.dat') as f:
    lines = f.readlines()
    i_bands = []
    zs = []
    for line in lines[1:]:
        line = line.split()
        i_band = float(line[4]) - float(line[7])
        z = float(line[15])
        quasar = if_quasar(float(line[16]))
        if quasar is 1:
            i_bands.append(i_band)
            zs.append(z)
# plt.hist(zs, bins=10, normed=1, edgecolor='black', range=(0, 4))
plt.hist(i_bands, bins=10, normed=1, edgecolor='black', range=(18, 20.2))
# plt.scatter(zs, i_bands, s=1)
plt.show()