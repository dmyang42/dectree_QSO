#!/bin/zsh
# 
# imbalance problem
# 做三件事情:
# 1 - 训练集1:1, 测试集各种比例下的结果(绘制PR曲线)
# 2 - 训练集比例变化(用更多0类), 测试集各种比例下结果
# 3 - 训练集同上, 并做SMOTE, 测试集各种比例下结果 
# author: topol @ USTC
# last modified: 2019/3/30
#
task_type=$1
train_ratio=$2
if [ ${task_type} -eq 1 ]
then
    for (( integer=1; integer <= 40; integer++))
    do
        echo "running: "$integer
        test_ratio=$(($integer*0.5))
        for (( rnd=1; rnd <= 50; rnd++))
        do
            echo "random seed: "$rnd
            python model_imbalance.py --task-type=1 --train-ratio=1 --test-ratio=${test_ratio} --if-SMOTE=0 --random-seed=$rnd > /dev/null
        done
    done
elif [ ${task_type} -eq 2 ]
then
    for (( integer=1; integer <= 40; integer++))
    do
        echo "running: "$integer
        test_ratio=$(($integer*0.5))
        for (( rnd=1; rnd <= 50; rnd++))
        do
            echo "random seed: "$rnd
            python model_imbalance.py --task-type=2 --train-ratio=${train_ratio} --test-ratio=${test_ratio} --if-SMOTE=0 --random-seed=$rnd > /dev/null
        done
    done
elif [ ${task_type} -eq 3 ]
then
    for (( integer=1; integer <= 40; integer++))
    do
        echo "running: "$integer
        test_ratio=$(($integer*0.5))
        for (( rnd=1; rnd <= 50; rnd++))
        do
            echo "random seed: "$rnd
            python model_imbalance.py --task-type=3 --train-ratio=${train_ratio} --test-ratio=${test_ratio} --if-SMOTE=0 --random-seed=42 > /dev/null
        done
    done
else
    echo "No such task type!"
fi