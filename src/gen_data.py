# -*- coding: utf-8 -*-
import time
from run_javelin import javelin_fit
from multiprocessing.dummy import Pool as ThreadPool

# 多线程 - 8
# start = time.clock()
start = time.time()
pool = ThreadPool(8)

def thread_javelin(line):
    line = line.split() 
    ID = line[0]
    # 如果某个ID没有光变曲线数据的错误处理
    tau, sigma = javelin_fit(ID)
    for need in need_list:
        print >> output_file, ("%-20s" %line[need]), 
    print >> output_file, ("%-20.3f%-20.3f%-20.3f%-20.3f\
        %-20.3f%-20.3f%-20.3f%-20.3f%-20.3f%-20.3f" %(tau[0], tau[1], \
        tau[2], tau[3], tau[4], sigma[0], \
        sigma[1], sigma[2], sigma[3], sigma[4]))

# stripe82-var-catalog中信息需要的为need_list对应列数
# 为ID, ug, gr, ri, iz, gAmpl, rAmpl, iAmpl
need_list = [0, 5, 6, 7, 8, 10, 12, 14, 16]
output_file = open("./train/test_sample_data", "w")
with open('./data/test') as f:
    # ! -- error处理要写
    # 根据need_list打印ID及需要的特征
    lines = f.readlines()
    feature_list = lines[0].split()
    need_feature = []
    for need in need_list:
        need_feature.append(feature_list[need])

    # 这里硬编码加入JAVELIN拟合得到的特征
    need_feature.append("tau_u")
    need_feature.append("tau_g")
    need_feature.append("tau_r")
    need_feature.append("tau_i")
    need_feature.append("tau_z")
    need_feature.append("sigma_u")
    need_feature.append("sigma_g")
    need_feature.append("sigma_r")
    need_feature.append("sigma_i")
    need_feature.append("sigma_z")
    
    for feature in need_feature:
        print >> output_file, ("%-20s" %feature),
    print >> output_file

    # 遍历所有的源，输出一个训练集格式数据文件
    # 单线程
    # for line in lines[1:]:
    #     line = line.split() 
    #     ID = line[0]
    #     # 如果某个ID没有光变曲线数据的错误处理
    #     tau, sigma = javelin_fit(ID)
    #     for need in need_list:
    #         print >> output_file, ("%-20s" %line[need]), 
    #     print >> output_file, ("%-20.3f%-20.3f%-20.3f%-20.3f\
    #         %-20.3f%-20.3f%-20.3f%-20.3f%-20.3f%-20.3f" %(tau[0], tau[1], \
    #         tau[2], tau[3], tau[4], sigma[0], \
    #         sigma[1], sigma[2], sigma[3], sigma[4]))
    
    # 下面是多线程处理上面的for循环
    pool.map(thread_javelin, lines[1:])

pool.close()
pool.join()

# end = time.clock()
end = time.time()
print "Total time:", end - start