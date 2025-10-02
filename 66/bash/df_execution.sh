#!/bin/bash

for j in $(seq 0 3); do
    for i in $(seq 1000); do
        python3 main.py; sleep 1; done
    mv output/tmp_data/* output/data/$j
    rm -r ./input/shopping_list
    cp -r ./fresh_stock/shopping_list input
done
