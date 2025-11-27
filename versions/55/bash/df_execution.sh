#!/bin/bash

df_file=55

for k in $(seq 0 2); do
    cp maps/map$k.txt input/map.txt
    cp starting_positions/s$k.txt input/starting_position.txt

    for l in $(seq 0 10); do
        epsilon=$((l * 10))
        cp epsilons/e$epsilon.txt input/epsilon.txt
        for j in $(seq 0 3); do
            for i in $(seq 1000); do
                ./df$df_file; sleep 1; done
            mv output/* data/map$k/e$epsilon/$j
            rm -r ./input/q
            cp -r ./memo/q input
        done
    done
done