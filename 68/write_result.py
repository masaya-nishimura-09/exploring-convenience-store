import datetime
import json
import re
import os
import csv


def write_csv(directory, version, date_str, csv_writer, runs_per_set, sets):
    # 結果の初期化
    min_steps = float('inf') # 全結果の中の最小値（非常に大きい初期値）（全セット含む）
    max_steps = 0 # 全結果の中の最大値（全セット含む）
    average_steps = 0 # 全結果の平均値（全セット含む）
    sum_steps = 0 # 全結果の合計（全セット含む）

    total_count = 0  # 実際に読み込んだステップ数

    for num_set in range(0, sets):
        current_num_set_path = os.path.join(directory, f"{num_set}")

        for output_file_name in sorted(os.listdir(current_num_set_path)):
            if output_file_name.endswith(".txt"):
                file_path = os.path.join(current_num_set_path, output_file_name)
                with open(file_path, "r", encoding="utf-8") as file:
                    for line in file:
                        match = re.search(r"Steps: (\d+)", line)
                        if match:
                            step = int(match.group(1))
                            # 最小値・最大値・合計を更新
                            min_steps = min(min_steps, step)
                            max_steps = max(max_steps, step)
                            sum_steps += step
                            total_count += 1
                            break

    # 実際に読み込んだ数と期待値を比較
    expected_count = runs_per_set * sets
    if total_count != expected_count:
        raise ValueError(
            f"読み込んだステップ数が期待値と異なります: {total_count} != {expected_count}"
        )

    # 平均値を計算
    average_steps = sum_steps / (runs_per_set * sets)

    # 結果をcsvファイルに書き込み
    csv_writer.writerow([version, date_str, runs_per_set, sets, min_steps, max_steps, f"{average_steps:.2f}"])

# 設定ファイルを読み込む
with open("./config.json", "r", encoding="utf-8") as file:
    data = json.load(file)

    # コードのバージョンを取得
    version = data["version"]

    # 1セットあたりの実行回数を取得
    runs_per_set = data["runs_per_set"]

    # セット数を取得
    sets = data["sets"]

with open("./output/stats.csv", "w", newline="", encoding="utf-8") as f:
    # 現在の日付・時間を取得
    now = datetime.datetime.now()
    date = datetime.date.today()
    time = now.strftime("%H-%M-%S-%f")
    date_str = f"{date}_{time}"

    # CSVのヘッダーを作成
    csv_writer = csv.writer(f)
    csv_writer.writerow(["Version", "Date", "Runs_per_set", "Sets" "Min", "Max", "Average"])

    directory = f"./output/data"
    write_csv(directory, version, date_str, csv_writer, runs_per_set, sets)
