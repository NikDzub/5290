#!/bin/bash

while true; do
    python3 P1.py 3 2
    if [ $? -ne 0 ]; then
        echo "P1.py failed, restarting..."
        continue
    fi

    python3 P2.py 2
    if [ $? -ne 0 ]; then
        echo "P2.py failed, restarting..."
        continue
    fi
    # break
done