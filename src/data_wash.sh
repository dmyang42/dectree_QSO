#!/bin/zsh
for i in `ls ./data/light_curve/` ;
do
    # echo $i
    python2 wash.py $i
done