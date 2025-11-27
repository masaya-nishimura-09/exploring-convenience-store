#!/bin/bash

mkdir -p output/data
mkdir -p output/tmp_data
mkdir -p output/data/0
mkdir -p output/data/1
mkdir -p output/data/2
mkdir -p output/data/3

for j in $(seq 0 3); do
    for i in $(seq 100); do
        python3 main.py; done
    mv output/tmp_data/* output/data/$j
    rm -r ./input/q
    cp -r ./fresh_stock/q input
done
