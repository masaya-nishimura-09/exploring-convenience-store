#!/bin/bash

for j in $(seq 0 3); do
    for i in $(seq 1000); do
        python3 main.py; sleep 1; done
    mv output/* data/$j
    rm -r ./input/q
    cp -r ./memo/q input
done
