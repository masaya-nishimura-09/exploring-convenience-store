#!/bin/bash

# 設定ファイルからバージョンを取得
version=$(python3 -c "import json; data=json.load(open('./config.json')); print(data['version'])")

# 出力フォルダをリセット
rm -rf output
mkdir -p output

python3 src/main.py; 

# 設定ファイルを output フォルダにコピー
cp config.json output/

# 現在の日付を取得
current_date=$(date +"%Y-%m-%d")
current_time=$(date +"%H-%M-%S")

# 出力ファイルを圧縮
zip -r ${version}_output_${current_date}_${current_time}.zip output
