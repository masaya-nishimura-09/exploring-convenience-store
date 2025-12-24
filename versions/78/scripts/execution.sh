#!/bin/bash

# 実行環境を有効化
source venv/bin/activate

# 1セットあたりの実行回数
runs_per_set=$(python3 -c "import json; data=json.load(open('./config.json')); print(data['runs_per_set'])")

# セット数（平均を取る回数）
sets=$(python3 -c "import json; data=json.load(open('./config.json')); print(data['sets'])")

# 買い物リストの個数を取得し、config.json を更新
item_amount=$(ls -1 ./input/shopping_list | wc -l)
python3 -c "import json; f='./config.json'; data=json.load(open(f)); data['item_amount']=${item_amount}; json.dump(data, open(f,'w'), indent=2)"

# 設定ファイルからバージョンを取得
version=$(python3 -c "import json; data=json.load(open('./config.json')); print(data['version'])")

# qマップを初期化する関数
setup_q_maps() {
    rm -rf "input/q"
    mkdir -p input/q
    for i in $(seq 0 $((item_amount - 1))); do
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
touch output/stats.csv
mkdir -p output/graphs
for i in $(seq 0 $((sets - 1))); do
    mkdir -p output/data/$i
done  
touch output/image_processing_result.csv
echo "correct_name,correct_symbol,item_name,item_symbol" > output/image_processing_result.csv

# 複数セット実行
for j in $(seq 0 $((sets - 1))); do
    for i in $(seq 1 $runs_per_set); do
        python3 src/main.py; 
    done
    mv output/tmp_data/* output/data/$j
    setup_q_maps
done

# csvに書き込み
python3 write_results_csv.py

# グラフを作成
python3 create_graphs.py

# 設定ファイルを output フォルダにコピー
cp config.json output/

# 現在の日付を取得
current_date=$(date +"%Y-%m-%d")
current_time=$(date +"%H-%M-%S")

# 出力ファイルを圧縮
zip -r ${version}_output_${current_date}_${current_time}.zip output
