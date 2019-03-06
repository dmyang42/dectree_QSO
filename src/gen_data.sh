#!/bin/zsh
for (( integer=382; interger <= 675; integer++))
do
    start_point=`expr $integer \* 100`
    end_point=`expr $integer \* 100 + 100`
    python gen_data.py $start_point $end_point $integer > ./log/gen${integer}.log
done
