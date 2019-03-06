#!/usr/local/bin/python2
# -*- coding: utf-8 -*-
import multiprocessing
# We must import this explicitly, it is not imported by the top-level
# multiprocessing module.
import multiprocessing.pool
from run_javelin import javelin_fit
import time

#
# 注: 采用了multiprocessing提供的多进程库
# 但是需要重新继承一个子类,使得进程是non-daemon的
# 参考: stackoverflow.com/questions/6974695/python-process-pool-non-daemonic
#

# stripe82-var-catalog中信息需要的为need_list对应列数
# 为ID, ug, gr, ri, iz, gAmpl, rAmpl, iAmpl
need_list = [0, 5, 6, 7, 8, 10, 12, 14, 16]
output_file = open("./train/test_sample_data", "w")

# 下面是改写multiprocessing库中的Pool
# 使其变为non-daemon
class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

def thread_javelin(line):
    line = line.split() 
    ID = line[0]
    # 如果某个ID没有光变曲线数据的错误处理
    tau, sigma = javelin_fit(ID)

    output = []
    for need in need_list:
        # print >> output_file, ("%-20s" %line[need]), 
        output.append(line[need])
    output = output + [tau[0], tau[1], \
        tau[2], tau[3], tau[4], sigma[0], \
        sigma[1], sigma[2], sigma[3], sigma[4]]
    # print >> output_file, ("%-20.3f%-20.3f%-20.3f%-20.3f\
    #     %-20.3f%-20.3f%-20.3f%-20.3f%-20.3f%-20.3f" %(tau[0], tau[1], \
    #     tau[2], tau[3], tau[4], sigma[0], \
    #     sigma[1], sigma[2], sigma[3], sigma[4]))
    return output

def write_data(train_data_set):
    for data in train_data_set:
        for feature in data:
            print >> output_file, "%-20.3f" %(float(feature)),
        print >> output_file 

# 多进程 - 8
# start = time.clock()
start = time.time()
pool = MyPool(8)

train_data_set = []
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
    
    # 下面是多进程处理上面的for循环
outputs = pool.map(thread_javelin, lines[1:])

# print(outputs)
write_data(outputs)
pool.close()
pool.join()

# end = time.clock()
end = time.time()
print "Total time:", end - start