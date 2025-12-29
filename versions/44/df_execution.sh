#!/bin/bash

for i in $(seq 1000); do ./df$1; sleep 1; done
