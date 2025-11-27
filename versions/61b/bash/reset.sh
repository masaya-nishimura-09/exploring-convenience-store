#!/bin/bash

rm -r ./input/q
cp -r ./fresh_stock/q input

rm -rf ./output/tmp_data/*

rm -r ./output/data
cp -r ./fresh_stock/data output/