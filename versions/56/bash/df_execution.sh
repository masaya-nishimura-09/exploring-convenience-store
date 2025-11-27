#!/bin/bash

for k in $(seq 0 2); do
    cp maps/map$k.txt input/map.txt
    cp starting_positions/s$k.txt input/starting_position.txt

    for l in $(seq 0 10); do
        epsilon=$((l * 10))
        cp epsilons/e$epsilon.txt input/epsilon.txt
        for j in $(seq 0 3); do
            for i in $(seq 1000); do
                python3 main.py; sleep 1; done
            mv output/* data/map$k/e$epsilon/$j
            rm -r ./input/q
            cp -r ./memo/q input
        done
    done
done

# cp maps/map1.txt input/map.txt
# cp starting_positions/s1.txt input/starting_position.txt

# for l in $(seq 0 10); do
#     epsilon=$((l * 10))
#     cp epsilons/e$epsilon.txt input/epsilon.txt
#     for i in $(seq 1000); do
#         python3 main.py; done
#     mv output/* data/map1/e$epsilon/0
#     rm -r ./input/q
#     cp -r ./memo/q input
# done