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
    shopping_list_path = os.path.join(root_dir, "input/shopping_list")
    shopping_list = []
    id = 0
    for f in os.listdir(shopping_list_path):
        if f == "atm.jpg" or f == "cashier_register.jpg":
            shopping_list.append(
                {
                    "id": id,
                    "category": f.split(".")[0],
                    "name": f,
                    "path": os.path.join(shopping_list_path, f),
                }
            )
        else:
            shopping_list.append(
                {
                    "id": id,
                    "category": f.split("_")[0],
                    "name": f,
                    "path": os.path.join(shopping_list_path, f),
                }
            )
        id += 1

    return shopping_list


# qマップを取得
def get_q_map(item_amount: int, vertical: int) -> list:
    q_map = []
    for i in range(item_amount):
        item_q = []
        for j in range(8):
            current_q = []
            root_dir = get_root_dir()
            with open(os.path.join(root_dir, f"input/q/{i}/q{j}.txt")) as f:
                for _ in range(vertical):
                    current_q.append([float(v) for v in f.readline().split()])
            item_q.append(current_q)
        q_map.append(item_q)
    return q_map


# 座標を出力ファイルに書き込み+ターミナルに表示
def write_position_to_file(show_output, file, x, y):
    file.write(f"({x}, {y})\n")


def clear_terminal():
    # ターミナルの高さを取得
    terminal_height = shutil.get_terminal_size().lines
    # 高さ分の改行を出力
    print("\n" * terminal_height)
    

# ターミナルにマップと進捗を表示
def display_map(status, x, y):
    if status.show_output:
        # 画面クリア
        print("\033[H\033[J", end='')

        print("-" * 50)
        print()
        print(f"Map:")
        print("\n".join(status.store_map))
        print(f"\nProgress: {status.shopping_cart.progress}/{status.shopping_cart.item_amount}\n")
        print(f"Steps: {status.position.steps}\n")
        print(f"Position: ({x}, {y})")


# 最終結果を出力
def output_results(status, output_file_path):
    # 出力用に買い物リストのを文字列に変換
    shopping_list_text = "Shopping List:\n"
    for i in status.shopping_list:
        shopping_list_text += f"- {i['name']}\n"

    # 出力用にカートの中身を文字列に変換(取得した順)
    cart_text = "Visit order:\n"
    order = 1
    for i in status.shopping_cart.cart:
        if i is not None:
            cart_text += f"{order}, {{ Symbol: {i['symbol']}, Name: {i['name']}, Price: {i['price']}¥ }}\n"
            order += 1

    # 出力用に購入した商品を文字列に変換
    items_purchased_text = "Items purchased:\n"
    for i in status.shopping_cart.items_purchased:
        items_purchased_text += f"{{{i['name']}: {i['price']}¥}}\n"

    # ターミナルに出力
    if status.show_output:
        print(f"\nOutput file path: {output_file_path}\n")
        print(f"Epsilon: {status.epsilon}\n")
        print(shopping_list_text)
        print(cart_text)
        print(items_purchased_text)
        print(f"Initial money: {status.wallet.initial}¥\n")
        print(f"Cash balance: {status.wallet.balance}¥\n")
        print(f"Is shopping successful?: {status.shopping_cart.is_shopping_successful}\n")
        print(f"Progress: {status.shopping_cart.progress}\n")
        print(f"Steps: {status.position.steps}\n")
        clear_terminal()

    # ファイルに出力
    with open(output_file_path, "a") as file:
        file.write(f"\nEpsilon: {status.epsilon}\n\n")
        file.write(f"{shopping_list_text}\n")
        file.write(f"{cart_text}\n")
        file.write(f"{items_purchased_text}\n")
        file.write(f"Initial money: {status.wallet.initial}¥\n\n")
        file.write(f"Cash balance: {status.wallet.balance}¥\n\n")
        file.write(f"Is shopping successful?: {status.shopping_cart.is_shopping_successful}\n\n")
        file.write(f"Progress: {status.shopping_cart.progress}\n\n")
        file.write(f"Steps: {status.position.steps}\n\n")
        file.write(f"Map: \n")
        for i in range(status.position.vertical):
            for j in range(status.position.horizontal):
                file.write(f"{status.store_map[i][j]}")
            file.write("\n")


# 更新したqマップを保存
def save_q_map(status, item_amount):
    for i in range(item_amount):
        for j in range(8):
            root_dir = get_root_dir()
            with open(os.path.join(root_dir, f"input/q/{i}/q{j}.txt"), "w") as f:
                for k in range(status.position.vertical):
                    line = " ".join(
                        f"{status.q_map[i][j][k][l]:.3f}" for l in range(status.position.horizontal)
                    )
                    f.write(line + "\n")
