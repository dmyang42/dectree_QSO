# 
# calculate average score
# author: topol @ USTC
# last modified: 2019/3/27
#
import numpy as np
import sys

model = sys.argv[1]
filename = './score_' + model + '_0' 
with open(filename) as f:
    lines = f.readlines()
    qso_p, qso_r, nqso_p, nqso_r, score = [], [], [], [], []
    for line in lines:
        line = line.split()
        qso_p.append(float(line[0]))
        qso_r.append(float(line[1]))
        nqso_p.append(float(line[2]))
        nqso_r.append(float(line[3]))
        score.append(float(line[4]))

print(sum(score)/len(score), np.std(score)/np.sqrt(len(score)))
print(sum(qso_p)/len(qso_p), np.std(qso_p)/np.sqrt(len(qso_p)))
print(sum(qso_r)/len(qso_r), np.std(qso_r)/np.sqrt(len(qso_r)))
print(sum(nqso_p)/len(nqso_p), np.std(nqso_p)/np.sqrt(len(nqso_p)))
print(sum(nqso_r)/len(nqso_r), np.std(nqso_r)/np.sqrt(len(nqso_r)))