#!/bin/bash

# 仮想環境をセットアップ
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install colorgram.py

# 買い物リストの個数を取得し、config.json を更新
ITEM_AMOUNT=$(ls -1 ./input/shopping_list | wc -l)
python3 -c "import json; f='./config.json'; data=json.load(open(f)); data['item_amount']=${ITEM_AMOUNT}; json.dump(data, open(f,'w'), indent=2)"

# 設定ファイルからバージョンを取得
VERSION=$(python3 -c "import json; data=json.load(open('./config.json')); print(data['version'])")

# qマップを初期化する関数
setup_q_maps() {
    rm -rf "input/q"
    mkdir -p input/q
    for i in $(seq 0 $((ITEM_AMOUNT - 1))); do
        mkdir -p input/q/$i
        cp -r input/fresh_q/* input/q/$i
    done  
}

# qマップをリセット
setup_q_maps

# 出力フォルダをリセット
rm -rf output

# 必要なフォルダを作成
mkdir -p output/data
mkdir -p output/tmp_data
mkdir -p output/data/0
mkdir -p output/data/1
mkdir -p output/data/2
mkdir -p output/data/3

# 4セット実行
for j in $(seq 0 3); do
    for i in $(seq 1000); do
        python3 main.py; sleep 1; done
    mv output/tmp_data/* output/data/$j
    setup_q_maps
done

# 統計情報をまとめる
touch stats.csv
python3 graph.py

# 現在の日付を取得
CURRENT_DATE=$(date +"%Y-%m-%d")

# 出力ファイルを圧縮
zip -r ${VERSION}_output_${CURRENT_DATE}.zip output