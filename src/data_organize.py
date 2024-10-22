# -*- coding: utf-8 -*-

# 
# This is the script to organize test_sample_data_* file in ./train/
# Running this script will output two files including quasar and non-quasar respectively
# Two modes are available:
# mode 0 - 使用s82 std star catalog作为nQSO训练集(存在bias)
# mode 1 - 使用s82 var catalog中不确定是否为qso加上iband小于19等的条件作为nQSO训练集
# author: topol @ USTC
# last modified: 2019/3/28
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
    remove_ID = read_ID_file('./data/i_fainter_than_19')
    return remove_ID

def additional_QSO():
    # dr7 quasar catalog中更多被认证的qso
    # sb function
    # use sb astroML method
    additional_QSO_ID = read_ID_file('./data/additional_confirmed_quasar')
    return additional_QSO_ID

def confirmed_star():
    # s82 standard stars catalog
    # sb function
    # use sb astroML method
    confirmed_star_ID = read_ID_file('./data/additional_confirmed_star')
    return confirmed_star_ID

def dr14_spec_confirmed_quasar():
    # spectroscopic confirmed quasar in sdss dr14
    confirmed_quasar_ID = read_ID_file('./data/ID_spec_QSO')
    return confirmed_quasar_ID

def dr14_spec_confirmed_star():
    # spectroscopic confirmed star in sdss dr14
    confirmed_star_ID = read_ID_file('./data/ID_spec_star')
    return confirmed_star_ID

def dr14_pho_star():
    # photometric confirmed star in sdss dr14
    pho_star_ID = read_ID_file('./data/ID_pho_star')
    return pho_star_ID

def dr14_pho_galaxy():
    # photometric confirmed star in sdss dr14
    pho_galaxy_ID = read_ID_file('./data/ID_pho_galaxy')
    return pho_galaxy_ID

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

def load_data_mode_0(line, additional_QSO_ID, confirmed_star_ID, 
                        outfile1, outfile2, outfile3, 
                        quasar_num, nquasar_num, other_num):
    # 基本上作废了
    # use s82 standard star catalog to establish nQSO_file
    if int(float(line[0])) in additional_QSO_ID:
        line[8] = -23.33
    if norm_label(float(line[8])):
        print_line(line, outfile1)
        quasar_num = quasar_num + 1
    elif int(float(line[0])) in confirmed_star_ID:
        print_line(line, outfile2)
        nquasar_num = nquasar_num + 1
    else:
        print_line(line, outfile3)
        other_num = other_num + 1
    return quasar_num, nquasar_num, other_num

def load_data_mode_1(line, remove_ID, additional_QSO_ID, 
                        outfile1, outfile2, outfile3,
                        quasar_num, nquasar_num, other_num):
    # 基本上作废了
    # use i-band < 19.00 & not sure if quasar in 
    # s82 var catalog to establish nQSO_file
    if int(float(line[0])) in remove_ID:
        print_line(line, outfile3)
        other_num = other_num + 1
        return quasar_num, nquasar_num, other_num
    else:
        if int(float(line[0])) in additional_QSO_ID:
            line[8] = -23.33
        if norm_label(float(line[8])):
            print_line(line, outfile1)
            quasar_num = quasar_num + 1
        else:
            print_line(line, outfile2)
            nquasar_num = nquasar_num + 1    
    return quasar_num, nquasar_num, other_num

def load_data_mode_2(line, dr14_pho_star_ID, dr14_confirmed_quasar_ID, dr14_pho_galaxy_ID, 
                outfile1, outfile2, outfile3, quasar_num, nquasar_num, other_num):
    # match with dr14
    if int(float(line[0])) in dr14_confirmed_quasar_ID:
        line[8] = -23.33
        print_line(line, outfile1)
        quasar_num = quasar_num + 1
    elif int(float(line[0])) not in dr14_pho_galaxy_ID:
        if int(float(line[0])) in dr14_pho_star_ID:
            line[8] = -9.9
            print_line(line, outfile2)
            nquasar_num = nquasar_num + 1
        else:
            print_line(line, outfile3)
            other_num = other_num + 1
    return quasar_num, nquasar_num, other_num

def load_data_mode_3(line, dr14_confirmed_quasar_ID, dr14_pho_galaxy_ID, i_fainter_than_19, 
                outfile1, outfile2, outfile3, quasar_num, nquasar_num, other_num):
    # 我奔溃叻
    # i band < 19 , 然后分类
    # QSO用光谱证认, nQSO就是剩下的点源(去掉了星系)
    if int(float(line[0])) not in i_fainter_than_19:
        if int(float(line[0])) in dr14_confirmed_quasar_ID:
            line[8] = -23.33
            print_line(line, outfile1)
            quasar_num = quasar_num + 1
        else:
            line[8] = -9.9
            print_line(line, outfile2)
            nquasar_num = nquasar_num + 1
    elif int(float(line[0])) not in dr14_pho_galaxy_ID:
        print_line(line, outfile3)
        other_num = other_num + 1
    return quasar_num, nquasar_num, other_num

def load_data_mode_4(line, dr14_confirmed_quasar_ID, dr14_confirmed_star_ID, dr14_pho_galaxy_ID,
                    outfile1, outfile2, outfile3, quasar_num, nquasar_num, other_num):
    # 真不想写了
    # 光谱认证的QSO和star
    # 最干净的数据集
    if int(float(line[0])) in dr14_confirmed_quasar_ID:
        line[8] = -23.33
        print_line(line, outfile1)
        quasar_num = quasar_num + 1
    elif int(float(line[0])) in dr14_confirmed_star_ID:
        line[8] = -9.9
        print_line(line, outfile2)
        nquasar_num = nquasar_num + 1
    elif int(float(line[0])) not in dr14_pho_galaxy_ID:
        print_line(line, outfile3)
        other_num = other_num + 1
    return quasar_num, nquasar_num, other_num        

def load_data(infile, outfile1, outfile2, outfile3, mode):
    # 导入单个数据块数据, 将QSO和非QSO分开保存
    # outfile1是QSO文件
    # outfile2是非QSO文件
    # outfile3是余下的源
    remove_ID = i_band_filter() # list of nqso that has a >19.0 i band luminosity
    additional_QSO_ID = additional_QSO() # list of nqso that has later confirmed as qso
    confirmed_star_ID = confirmed_star() # list of nqso that has later confirmed as star
    dr14_pho_star_ID = dr14_pho_star()
    dr14_confirmed_quasar_ID = dr14_spec_confirmed_quasar()
    dr14_confirmed_star_ID = dr14_spec_confirmed_star()
    dr14_pho_galaxy_ID = dr14_pho_galaxy()
    quasar_num, nquasar_num, other_num = 0, 0, 0
    try:
        with open(infile) as f:
            lines = f.readlines()
            data, label = [], []
            feature = lines[0].split()
            for line in lines[1:]:
                line = line.split()

                if mode is 0: 
                    # use s82 standard star catalog to establish nQSO_file
                    quasar_num, nquasar_num, other_num = \
                        load_data_mode_0(line, additional_QSO_ID, confirmed_star_ID,
                                            outfile1, outfile2, outfile3, 
                                            quasar_num, nquasar_num, other_num)
                elif mode is 1: 
                    # use i-band < 19.00 & not sure if quasar in 
                    # s82 var catalog to establish nQSO_file
                    quasar_num, nquasar_num, other_num = \
                        load_data_mode_1(line, remove_ID, additional_QSO_ID,
                                            outfile1, outfile2, outfile3,
                                            quasar_num, nquasar_num, other_num)
                elif mode is 2: 
                    # match with dr14
                    quasar_num, nquasar_num, other_num = \
                        load_data_mode_2(line, dr14_pho_star_ID, dr14_confirmed_quasar_ID, dr14_pho_galaxy_ID,
                                    outfile1, outfile2, outfile3, quasar_num, nquasar_num, other_num)
                elif mode is 3:
                    # all sources i < 19.0
                    quasar_num, nquasar_num, other_num = \
                        load_data_mode_3(line, dr14_confirmed_quasar_ID, dr14_pho_galaxy_ID, remove_ID, 
                            outfile1, outfile2, outfile3, quasar_num, nquasar_num, other_num)
                elif mode is 4:
                    # all sources are spec confirmed
                    quasar_num, nquasar_num, other_num = \
                        load_data_mode_4(line, dr14_confirmed_quasar_ID, dr14_confirmed_star_ID, dr14_pho_galaxy_ID, 
                            outfile1, outfile2, outfile3, quasar_num, nquasar_num, other_num)
        return quasar_num, nquasar_num, other_num
    except FileNotFoundError:
        # 存在部分块不存在的情况
        print("Missing part: " + infile)
        return 0, 0, 0

def batch_load_data(index_list, outfile1, outfile2, outfile3, mode):
    # 加载多个数据块的文件到两类输出文件
    merged_data, merged_label = [], []
    quasar_total, nquasar_total, other_total = 0, 0, 0
    for i in index_list:
        filename = "./train/raw/test_sample_data_" + str(i)
        quasar_num, nquasar_num, other_num = load_data(filename, outfile1, outfile2, outfile3, mode)
        quasar_total = quasar_total + quasar_num
        nquasar_total = nquasar_total + nquasar_num
        other_total = other_total + other_num
    return quasar_total, nquasar_total, other_total

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

    QSO_file = open("./train/QSO_sample_data" + str(mode), "w+")
    nQSO_file = open("./train/nQSO_sample_data" + str(mode), "w+")
    other_file = open("./train/other_sample_data" + str(mode), "w+")
    feature = get_feature("./train/raw/test_sample_data_1")
    print_line(feature, QSO_file)
    print_line(feature, nQSO_file)
    print_line(feature, other_file)
    index_list = range(0,675) # traverse all test_sample_data_* files
    q, nq, oth= batch_load_data(index_list, QSO_file, nQSO_file, other_file, mode)
    print("total quasar: ", q)
    print("total nquasar: ", nq)
    print("others: ", oth)

if __name__ == "__main__":
    main()
