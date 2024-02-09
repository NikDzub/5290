#!/bin/bash

while true; do
    python3 a1.py 3 3 # a1.py {number of browsers open to search} {number of comments for video}
    if [ $? -ne 0 ]; then
        echo "a1.py failed, restarting..."
        continue
    fi

    python3 a2.py 
    if [ $? -ne 0 ]; then
        echo "a2.py failed, restarting..."
        continue
    fi
    # break
done