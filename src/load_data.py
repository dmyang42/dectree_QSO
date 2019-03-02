def load_data(filename, need_list):
    feature_list = []
    data_list = []
    data_unit = []
    with open(filename) as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            line = line.split()
            need = []
            for t in need_list:
                need.append(line[t])
            if i == 0:
               feature_list = need
            else:
                if -0.001 < float(need[len(need)-1]) + 9.9 < 0.001:
                    need[len(need)-1] = str(0)
                else:
                    need[len(need)-1] = str(1)
                data_unit = need
                data_list.append(data_unit)
            i = i + 1
    return feature_list, data_list