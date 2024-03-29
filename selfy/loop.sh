#!/bin/bash

while true; do
    python3 selfie5.py 3 
    if [ $? -ne 0 ]; then
        echo "failed, restarting..."
        continue
    fi
    # break
done

