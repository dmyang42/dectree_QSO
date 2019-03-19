#!/bin/zsh

#
# re-run crashed block recorded in 'missing_part'
# author: topol @ USTC
# last modified: 2019/3/19
#

for line in `cat missing_part`
do
    start_point=`expr $line \* 100`
    end_point=`expr $line \* 100 + 100`
    python gen_data.py $start_point $end_point $line > ./log/gen${line}.log
    # echo $start_point
    # echo $end_point
done
