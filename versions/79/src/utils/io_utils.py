# ファイル入出力ユーティリティ

import datetime
import json
import os
import csv


# プロジェクトのルートディレクトリのパスを取得
def get_root_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# 現在の日時を文字列で返す
def get_date_str():
    now = datetime.datetime.now()
    date = datetime.date.today()
    time = now.strftime("%H-%M-%S-%f")
    return f"{date}_{time}"


# 設定ファイルを読み込み
def load_config() -> dict:
    root_dir = get_root_dir()
    config_path = os.path.join(root_dir, "config.json")
    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)
    return config


# 出力用ファイルを作成
def create_output_file(version: str) -> str:
    date_str = get_date_str()
    root_dir = get_root_dir()
    output_file_path = os.path.join(root_dir, f"output/{date_str}.txt")

    with open(output_file_path, "w") as file:
        file.write(f"{date_str}\n\n")

    return output_file_path


def write_results(
    status, output_file_path
):
    with open(output_file_path, "a") as file:
        file.write(f"Map: \n")
        for i in range(status.position.vertical):
            for j in range(status.position.horizontal):
                file.write(f"{status.store_map[0][i][j]}")
            file.write("\n")
