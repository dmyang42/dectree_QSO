# 
# This is the script to organize test_sample_data_* file in ./train/
# Running this script will output two files including quasar and non-quasar respectively
# Two modes are available:
# mode 0 - 使用s82 std star catalog作为nQSO训练集(存在bias)
# mode 1 - 使用s82 var catalog中不确定是否为qso加上iband小于19等的条件作为nQSO训练集
# author: topol @ USTC
# last modified: 2019/3/19
#
import sys
def print_line(list, outfile):
    # 格式化输出
    for item in list:
        print("%-20s" %item, end='', file=outfile)
    print(file=outfile)

def read_ID_file(filename):
    # 读取一个ID文件
    ID = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            ID.append(int(line[0]))
    return ID

def i_band_filter():
    # 去除i > 19.00的非QSO源
    # 大概有一万多个
    remove_ID = read_ID_file('./i_filter')
    return remove_ID

def additional_QSO():
    # dr7 quasar catalog中更多被认证的qso
    additional_QSO_ID = read_ID_file('./data/additional_confirmed_quasar')
    return additional_QSO_ID

def confirmed_star():
    # s82 standard stars catalog
    confirmed_star_ID = read_ID_file('./data/additional_confirmed_star')
    return confirmed_star_ID

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

def load_data(infile, outfile1, outfile2, mode):
    # 导入单个数据块数据, 将QSO和非QSO分开保存
    # outfile1是QSO文件
    # outfile2是非QSO文件
    remove_ID = i_band_filter() # list of nqso that has a >19.0 i band luminosity
    additional_QSO_ID = additional_QSO() # list of nqso that has later confirmed as qso
    confirmed_star_ID = confirmed_star() # list of nqso that has later confirmed as star
    try:
        with open(infile) as f:
            lines = f.readlines()
            data, label = [], []
            feature = lines[0].split()
            for line in lines[1:]:
                line = line.split()
                if mode is 1: # use s82 standard star catalog to establish nQSO_file
                    if int(float(line[0])) in additional_QSO_ID:
                        line[8] = 23.33
                    if norm_label(float(line[8])):
                        print_line(line, outfile1)
                    if int(float(line[0])) in confirmed_star_ID:
                        print_line(line, outfile2)
                elif mode is 0: # use i-band < 19.00 & not sure if quasar in s82 var catalog to establish nQSO_file
                    if int(float(line[0])) not in remove_ID:
                        if int(float(line[0])) in additional_QSO_ID:
                            line[8] = 23.33
                        if norm_label(float(line[8])):
                            print_line(line, outfile1)
                        else:
                            print_line(line, outfile2)
    except FileNotFoundError:
        # 存在部分块不存在的情况
        print("Missing part: " + infile)

def batch_load_data(index_list, outfile1, outfile2, mode):
    # 加载多个数据块的文件到两类输出文件
    merged_data, merged_label = [], []
    for i in index_list:
        filename = "./train/test_sample_data_" + str(i)
        load_data(filename, outfile1, outfile2, mode)

def get_feature(filename):
    # return feature list in certain catalog file
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
    # mode 0 - 使用s82 std star catalog作为nQSO训练集(存在bias)
    # mode 1 - 使用s82 var catalog中不确定是否为qso加上iband小于19等的条件作为nQSO训练集
    mode = int(sys.argv[1])

    QSO_file = open("./train/QSO_sample_data", "w+")
    nQSO_file = open("./train/nQSO_sample_data", "w+")
    feature = get_feature("./train/test_sample_data_1")
    print_line(feature, QSO_file)
    print_line(feature, nQSO_file)
    index_list = range(0,675) # traverse all test_sample_data_* files
    batch_load_data(index_list, QSO_file, nQSO_file, mode)

if __name__ == "__main__":
    main()
