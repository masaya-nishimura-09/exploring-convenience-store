import os
import csv
import re
import os
import csv
from utils.config_utils import *
from utils.shopping_utils import get_shopping_list_str, get_cart_str, get_items_purchased_str
from utils.utils import get_date


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


# 最終的な結果をtxtファイルに書き込み
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


# 歩数の最小値、最大値、平均値を返す
def get_steps_data():
    sets = get_sets()
    root_dir = get_root_dir()
    runs_per_set = get_runs_per_set()
    data_directory = os.path.join(root_dir, "output/data")

    min_steps = float('inf') # 全結果の中の最小値（非常に大きい初期値）（全セット含む）
    max_steps = 0 # 全結果の中の最大値（全セット含む）
    average_steps = 0 # 全結果の平均値（全セット含む）
    sum_steps = 0 # 全結果の合計（全セット含む）
    total_count = 0  # 実際に読み込んだステップ数
    
    for num_set in range(0, sets):
        current_num_set_path = os.path.join(data_directory, f"{num_set}")

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
    return min_steps, max_steps, average_steps


def write_results_csv():    
    root_dir = get_root_dir()
    version = get_project_version()
    sets = get_sets()
    runs_per_set = get_runs_per_set()
    date_str = get_date()

    with open(os.path.join(root_dir, "output/stats.csv"), "w", newline="", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Version", "Date", "Runs_per_set", "Sets", "Min", "Max", "Average"])
        min_steps, max_steps, average_steps = get_steps_data()
   
        # 結果をcsvファイルに書き込み
        csv_writer.writerow([version, date_str, runs_per_set, sets, min_steps, max_steps, f"{average_steps:.2f}"])
