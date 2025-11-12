import datetime
import os
import csv
from config_utils import *
from shopping_utils import *


# 現在の日時を文字列で返す
def get_date():
    now = datetime.datetime.now()
    date = datetime.date.today()
    time = now.strftime("%H-%M-%S-%f")
    return date + "_" + time


# データ出力用ファイルを作成
def create_output_file():
    date = get_date()
    output_file_path = os.path.join(get_root_dir(), f"output/tmp_data/{date}.txt")
    with open(output_file_path, "w") as file:
        file.write(f"{get_project_version()} output data\n\n")
        file.write("Passing Points:\n")

    return output_file_path


# 座標を出力ファイルに書き込み
def write_position_to_file(file, x, y):
    file.write(f"({x}, {y})\n")


# 最終的な結果を書き込み
def write_results(status, output_file_path):
    shopping_list_str = get_shopping_list_str(status.shopping_list)
    cart_str = get_cart_str(status.shopping_cart.cart)
    items_purchased_str = get_items_purchased_str(status.shopping_cart.items_purchased)

    # ファイルに出力
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
    with open(
        os.path.join(get_root_dir(), "output/image_processing_result.csv"), "a"
    ) as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([correct_name, correct_symbol, item_name, item_symbol])
