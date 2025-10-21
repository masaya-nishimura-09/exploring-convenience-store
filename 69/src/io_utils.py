# ファイル入出力ユーティリティ

import json
import datetime
import os
from color_utils import color_picker


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


# 地図を取得
def get_map(vertical: int) -> list:
    map = []
    root_dir = get_root_dir()
    with open(os.path.join(root_dir, "input/map.txt")) as map_file:
        for _ in range(vertical):
            map.append(list(map_file.readline().rstrip("\n")))
    return map


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
                    "rgb": color_picker(os.path.join(shopping_list_path, f)),
                }
            )
        else:
            shopping_list.append(
                {
                    "id": id,
                    "category": f.split("_")[0],
                    "name": f,
                    "rgb": color_picker(os.path.join(shopping_list_path, f)),
                }
            )
        id += 1

    return shopping_list


# qマップを取得
def get_q_map(item_amount: str, vertical: int) -> list:
    q_map = []
    for i in range(item_amount):
        item_q = []
        for j in range(4):
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
    if show_output:
        print(f"({x}, {y})")
    file.write(f"({x}, {y})\n")


# 進捗とステップ数を表示
def show_progress_steps(status):
    if status.show_output:
        print(f"Position: ({status.position.x}, {status.position.y}, {status.position.d})")
        print(f"Progress: {status.shopping_cart.progress}, Steps: {status.position.steps}")


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
        print(f"Map: ")
        for i in range(status.position.vertical):
            for j in range(status.position.horizontal):
                print(status.store_map[i][j], end="")
            print()
        print()

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
        for j in range(4):
            root_dir = get_root_dir()
            with open(os.path.join(root_dir, f"input/q/{i}/q{j}.txt"), "w") as f:
                for k in range(status.position.vertical):
                    line = " ".join(
                        f"{status.q_map[i][j][k][l]:.3f}" for l in range(status.position.horizontal)
                    )
                    f.write(line + "\n")
