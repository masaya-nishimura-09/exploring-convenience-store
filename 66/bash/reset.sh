#!/bin/bash

rm -r ./input/shopping_list
cp -r ./fresh_stock/shopping_list input

rm -rf ./output/tmp_data/*

rm -r ./output/data
cp -r ./fresh_stock/data output/
