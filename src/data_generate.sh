#!/bin/zsh
for (( integer=382; integer <= 675; integer++))
do
    start_point=`expr $integer \* 100`
    end_point=`expr $integer \* 100 + 100`
    python data_generate.py $start_point $end_point $integer > ./log/gen${integer}.log
done
