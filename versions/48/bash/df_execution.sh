#!/bin/bash

cp maps/map$2.txt input/map.txt

cp starting_positions/s$2.txt input/starting_position.txt

cp epsilons/e$3.txt input/epsilon.txt

for i in $(seq 1000); do ./df$1; sleep 1; done