def print_line(list, outfile):
    for item in list:
        print("%-20s" %item, end='', file=outfile)
    print(file=outfile)

def i_band_filter():
    # 去除i > 19.00的非QSO源
    # 大概有一万多个
    remove_ID = []
    with open('./i_filter') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            remove_ID.append(int(line[0]))
    return remove_ID

def norm_label(label):
    # 输入一个未处理的label列表
    # 返回处理后(0,1)的label列表
    # 0 -- 不是QSO
    # 1 -- 是QSO
    if -0.001 < label + 9.9 < 0.001:
        label = 0
    else:
        label = 1
    return label

def load_data(infile, outfile1, outfile2):
    # 导入单个数据块数据,将QSO和非QSO分开保存
    # outfile1是QSO文件
    # outfile2是非QSO文件
    remove_ID = i_band_filter()
    try:
        with open(infile) as f:
            lines = f.readlines()
            data, label = [], []
            feature = lines[0].split()
            for line in lines[1:]:
                line = line.split()
                if int(float(line[0])) not in remove_ID:
                    if norm_label(float(line[8])):
                        print_line(line, outfile1)
                    else:
                        print_line(line, outfile2)
    except FileNotFoundError:
        # 存在部分块不存在的情况
        print("Missing part: " + infile)

def batch_load_data(index_list, outfile1, outfile2):
    # 合并多个数据块
    merged_data, merged_label = [], []
    for i in index_list:
        filename = "./train/test_sample_data_" + str(i)
        load_data(filename, outfile1, outfile2)

def get_feature(filename):
    try:
        with open(filename) as f:
            lines = f.readlines()
            feature = lines[0].split()
        return feature
    except FileNotFoundError:
        # 存在部分块不存在的情况
        print("Missing part: " + filename)
        return []

def main():
    QSO_file = open("./train/QSO_sample_data", "w+")
    nQSO_file = open("./train/nQSO_sample_data", "w+")
    feature = get_feature("./train/test_sample_data_1")
    print_line(feature, QSO_file)
    print_line(feature, nQSO_file)
    index_list = range(0,675)
    batch_load_data(index_list, QSO_file, nQSO_file)

if __name__ == "__main__":
    main()
