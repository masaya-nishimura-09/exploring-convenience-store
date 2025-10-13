#!/bin/bash

for k in $(seq 0 2); do
    cp maps/map$k.txt input/map.txt
    cp starting_positions/s$k.txt input/starting_position.txt

    for j in $(seq 0 3); do
        for i in $(seq 1000); do
            python3 main.py; sleep 1; done
        mv output/* data/map$k/$j
        rm -r ./input/q
        cp -r ./memo/q input
    done
done