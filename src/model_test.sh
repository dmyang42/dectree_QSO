#!/bin/zsh
# 
# do multiple sampling
# to calculate the precision of final result
# 通过大量抽样, 确定平均分数的精确值
# author: topol @ USTC
# last modified: 2019/3/19
#
mode=$1
for (( integer=1; integer <= 100; integer++))
do
    echo "running "$integer
    python dectree.py $mode $integer > /dev/null
done
