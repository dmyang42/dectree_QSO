#!/bin/zsh

#
# this is a stupid method to prevent data_generate.py from crashing
# by checking log file we know which block crashed
# author: topol @ USTC
# last modified: 2019/3/19
#

for (( integer=0; integer <= 675; integer++))
do
    start_point=`expr $integer \* 100`
    end_point=`expr $integer \* 100 + 100`
    python data_generate.py $start_point $end_point $integer > ./log/gen${integer}.log
done
