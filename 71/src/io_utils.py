# ファイル入出力ユーティリティ

import datetime
import json
import time
import os
import shutil


# プロジェクトのルートディレクトリのパスを取得
def get_root_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 設定ファイルを読み込み
def load_config() -> dict:
    root_dir = get_root_dir()
    config_path = os.path.join(root_dir, "config.json")
    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)
    return config


# 出力用ファイルを作成
def create_output_file(version: str) -> str:
    # 現在の日付・時間を取得
    now = datetime.datetime.now()
    date = datetime.date.today()
    time = now.strftime("%H-%M-%S-%f")

    # 出力用ファイルを作成
    root_dir = get_root_dir()
    output_file_path = os.path.join(root_dir, f"output/tmp_data/{date}_{time}.txt")
    with open(output_file_path, "w") as file:
        file.write(f"{version} output data\n\n")
        file.write("Passing Points:\n")

    return output_file_path


# 買い物リスト（写真のパス）を取得
def get_shopping_list() -> list:
    root_dir = get_root_dir()
    images_path = os.path.join(root_dir, "images")
    shopping_list = []
    id = 0
    for category in os.listdir(images_path):
        category_path = os.path.join(images_path, category)
        for item in os.listdir(category_path):
            shopping_list.append(
                {
                    "id": id,
                    "category": category,
                    "name": item.split(".")[0],
                    "path": os.path.join(category_path, item),
                }
            )
            id += 1

    return shopping_list
