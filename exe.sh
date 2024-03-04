#!/bin/bash

while true; do
    python3 G1.py 1 2
    if [ $? -ne 0 ]; then
        echo "G1.py failed, restarting..."
        continue
    fi

    python3 T2.py 3 0
    if [ $? -ne 0 ]; then
        echo "T2.py failed, restarting..."
        continue
    fi
    # break
done

