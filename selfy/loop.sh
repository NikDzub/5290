#!/bin/bash

while true; do

    # python3 run_once.py 3
    # if [ $? -ne 0 ]; then
    #     echo "run_once.py failed, restarting..."
    #     continue
    # fi

    python3 selfie6.py 3
    if [ $? -ne 0 ]; then
        echo "selfie6.py failed, restarting..."
        continue
    fi

    python3 M3.py 3 
    if [ $? -ne 0 ]; then
        echo "M3.py failed, restarting..."
        continue
    fi
    # break
done

