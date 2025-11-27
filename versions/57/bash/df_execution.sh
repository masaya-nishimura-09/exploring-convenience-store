#!/bin/bash

df_file=57

for k in $(seq 0 2); do
    cp maps/map$k.txt input/map.txt
    cp starting_positions/s$k.txt input/starting_position.txt

    for l in $(seq 0 10); do
        cp epsilons/$l.txt input/epsilon.txt
        for j in $(seq 0 3); do
            for i in $(seq 1000); do
                ./df$df_file; sleep 1; done
            mv output/* data/map$k/$l/$j
            rm -r ./input/q
            cp -r ./memo/q input
        done
    done
done