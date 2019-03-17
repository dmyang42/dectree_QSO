from data_util import merge_data
def if_quasar(MiQSO):
    if -0.001 < MiQSO + 9.9 < 0.001:
        return 0
    else:
        return 1

ID, r, ri, label = [], [], [], []
with open('./data/stripe82candidateVar_v1.1.dat') as f:
    lines = f.readlines()
    # sources = []
    ID = []
    for line in lines[1:]:
        line = line.split()
        # source = {}
        i_band = float(line[4]) - float(line[7])
        quasar = if_quasar(float(line[16]))
        if i_band > 19.00 and quasar == 0:
            # source['ID'] = line[0]
            # source['i'] = float(line[4]) - float(line[7])
            # sources.append(source)
            print(line[0])