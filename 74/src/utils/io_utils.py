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
    output_file_path = os.path.join(root_dir, f"output/tmp_data/{date_str}.txt")

    with open(output_file_path, "w") as file:
        file.write(f"{version} output data\n\n")
        file.write("Passing Points:\n")

    return output_file_path


# 座標を出力ファイルに書き込み
def write_position_to_file(file, x, y):
    file.write(f"({x}, {y})\n")


# 最終結果を出力
def write_results(
    status, output_file_path, shopping_list_str, cart_str, items_purchased_str
):
    with open(output_file_path, "a") as file:
        file.write(f"\nEpsilon: {status.epsilon}\n\n")
        file.write(f"{shopping_list_str}\n")
        file.write(f"{cart_str}\n")
        file.write(f"{items_purchased_str}\n")
        file.write(f"Initial money: {status.wallet.initial}¥\n\n")
        file.write(f"Cash balance: {status.wallet.balance}¥\n\n")
        file.write(
            f"Is shopping successful?: {status.shopping_cart.is_shopping_successful}\n\n"
        )
        file.write(f"Progress: {status.shopping_cart.progress}\n\n")
        file.write(f"Steps: {status.position.steps}\n\n")
        file.write(f"Map: \n")
        for i in range(status.position.vertical):
            for j in range(status.position.horizontal):
                file.write(f"{status.store_map[i][j]}")
            file.write("\n")


# 画像処理結果をCSVに書き込み
def write_image_processing_result(correct_name, correct_symbol, item_name, item_symbol):
    root_dir = get_root_dir()
    with open(os.path.join(root_dir, "output/image_processing_result.csv"), "a") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([correct_name, correct_symbol, item_name, item_symbol])
