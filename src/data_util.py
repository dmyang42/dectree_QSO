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

def load_data(filename):
    # 导入单个数据块数据,保存为矩阵格式输出
    # label代表是否是QSO
    try:
        with open(filename) as f:
            lines = f.readlines()
            data, label = [], []
            feature = lines[0].split()
            feature.remove('MiQSO')
            for line in lines[1:]:
                line = line.split()
                line = line[1:]
                try:
                    line = list(map(eval, line))
                except NameError:
                    print("inf in " + filename)
                else:
                    label.append(line.pop(7))
                    sample = line
                    data.append(sample)
            label = norm_label(label)
        return data, label
    except FileNotFoundError:
        print("Missing part: " + filename)
        return [], []
    
def merge_data(index_list):
    merged_data, merged_label = [], []
    for i in index_list:
        filename = "./train/test_sample_data_" + str(i)
        data, label = load_data(filename)
        merged_data = merged_data + data
        merged_label = merged_label + label
    return merged_data, merged_label

def main():
    data, label = merge_data(1,20)
    print(len(data))
    print(len(label))

if __name__ == "__main__":
    main()