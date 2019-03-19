# 
# i-band filter script:
# since for dr7, most sources with i band < 19.0 have spectroscopic observation
# that is to say, nQSO in s82 var catalog with i band < 19.0 are quite likely to be real not Quasar
# author: topol @ USTC
# last modified: 2019/3/19
#

from data_organize import read_ID_file

def if_quasar(MiQSO):
    if -0.001 < MiQSO + 9.9 < 0.001:
        return 0
    else:
        return 1

ID, r, ri, label = [], [], [], []
additional_quasar_ID = read_ID_file('./additional_confirmed_quasar')
with open('./data/stripe82candidateVar_v1.1.dat') as f:
    lines = f.readlines()
    # sources = []
    ID = []
    for line in lines[1:]:
        line = line.split()
        # source = {}
        i_band = float(line[4]) - float(line[7])
        quasar = if_quasar(float(line[16]))
        if i_band > 19.00 and quasar == 0 and line[0] not in additional_quasar_ID:
            # source['ID'] = line[0]
            # source['i'] = float(line[4]) - float(line[7])
            # sources.append(source)
            print(line[0])