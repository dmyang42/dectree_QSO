#!/bin/zsh
# 
# do multiple sampling
# to calculate the precision of final result
# 通过大量抽样, 确定平均分数的精确值
# author: topol @ USTC
# last modified: 2019/3/19
#
data_mode=$1
feature_mode=$2
for (( integer=1; integer <= 100; integer++))
do
    echo "running "$integer
    python dectree.py --data-mode=${data_mode} --feature-mode=${feature_mode} --random-seed=${integer} > /dev/null
done
