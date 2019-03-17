#!/bin/zsh
for (( integer=1; integer <= 101; integer++))
do
    echo "running "$integer
    python dectree.py $integer > /dev/null
done
