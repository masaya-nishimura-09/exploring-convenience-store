#!/bin/bash

for k in $(seq 0 2); do
    cp maps/map$k.txt input/map.txt
    cp starting_positions/s$k.txt input/starting_position.txt

    cp epsilons/e80.txt input/epsilon.txt
    for j in $(seq 0 3); do
        for i in $(seq 1000); do
            ./df51; sleep 1; done
        mv output/* data/map$k/e80/$j
        rm -r ./input/q
        cp -r ./memo/q input
    done

    cp epsilons/e50.txt input/epsilon.txt
    for j in $(seq 0 3); do
        for i in $(seq 1000); do
            ./df51; sleep 1; done
        mv output/* data/map$k/e50/$j
        rm -r ./input/q
        cp -r ./memo/q input
    done

    cp epsilons/e20.txt input/epsilon.txt
    for j in $(seq 0 3); do
        for i in $(seq 1000); do
            ./df51; sleep 1; done
        mv output/* data/map$k/e20/$j
        rm -r ./input/q
        cp -r ./memo/q input
    done
done