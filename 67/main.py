import datetime
import random
import colorgram
import os
from operator import itemgetter
import json

VERTICAL = 20
HORIZONTAL = 50
color_cache = {}


class Status:
    def __init__(
        self,
        x,
        y,
        initial_money,
        shopping_list,
        cart,
        epsilon,
        q,
        map,
        item_amount,
        show_output,
    ):
        self.x = x
        self.y = y
        self.d = 0
        self.steps = 0
        self.px = x
        self.py = y
        self.pd = 0
        self.progress = 0
        self.initial_money = initial_money
        self.cash_balance = initial_money
        self.is_shopping_successful = True
        self.shopping_list = shopping_list
        self.cart = cart
        self.items_purchased = []
        self.epsilon = epsilon
        self.q = q
        self.map = map
        self.item_amount = item_amount
        self.show_output = show_output


# 会計をし、最安値の商品を購入
def checkout(status):
    cart = [
        item
        for item in status.cart
        if item is not None
        and item["name"] != "atm.jpg"
        and item["name"] != "cashier_register.jpg"
    ]

    # カートの中身を価格順にソート
    sorted_cart = sorted(cart, key=itemgetter("price"))

    # 購入したカテゴリリスト
    category_done = []

    # 所持金と相談しながら購入
    for item in sorted_cart:
        if item["category"] not in category_done:
            if item["price"] <= status.cash_balance:
                status.items_purchased.append(
                    {"name": item["name"], "price": item["price"]}
                )
                status.cash_balance = status.cash_balance - item["price"]
                category_done.append(item["category"])
            else:
                status.is_shopping_successful = False
                break

    return status


# ランダムな価格を生成
def random_price():
    price = random.randint(100, 10000)
    return price


# 2つのリストが同じか判別(順番も重複も無視)
def are_same_list(a, b):
    if set(a) == set(b):
        return True
    else:
        return False


# 画像の色を取得しリスト化
def color_picker(path):
    if path in color_cache:
        return color_cache[path]
    colors = colorgram.extract(path, 100)
    rgb_list = []
    for color in colors:
        rgb = color.rgb
        rgb_list.append(f"({rgb.r}, {rgb.g}, {rgb.b})")
    color_cache[path] = rgb_list
    return rgb_list


# 商品をカゴに入れる
def pick_item(status, item_code):
    item_rgb = color_picker(f"./input/item_images/{item_code}.jpg")
    item_id = 0
    item_name = ""
    item_category = ""

    price = 0
    if item_code == "$" or item_code == "-":
        price = 0
    else:
        price = random_price()

    # 見つけた商品のid、名前、カテゴリを取得
    for item in status.shopping_list:
        if are_same_list(item["rgb"], item_rgb):
            item_id = item["id"]
            item_name = item["name"]
            item_category = item["category"]
            break

    # カゴに見つけた商品を入れる
    for i in range(status.item_amount):
        if status.cart[i] == None:
            status.cart[i] = {
                "category": item_category,
                "symbol": item_code,
                "name": item_name,
                "price": price,
            }
            break

    return item_id


# 商品をかごに入れるべきか判別
def item_checker(status, item_code):
    # 対象の商品、atm、レジの色を取得
    item_rgb = color_picker(f"./input/item_images/{item_code}.jpg")

    atm_rgb = []
    for item in status.shopping_list:
        if item["name"] == "atm.jpg":
            atm_rgb = item["rgb"]
            break

    cashier_rgb = []
    for item in status.shopping_list:
        if item["name"] == "cashier_register.jpg":
            cashier_rgb = item["rgb"]
            break

    # まだ何も見つけてない　かつ　見つけたものがatmでない時
    if status.progress == 0 and not are_same_list(item_rgb, atm_rgb):
        return False

    # atmを見つけた後　かつ　見つけたものがatmの時
    if status.progress > 0 and are_same_list(item_rgb, atm_rgb):
        return False

    # レジ以外に見つけてないものがある　かつ　見つけたものがレジの時
    if status.progress < status.item_amount - 1 and are_same_list(
        item_rgb, cashier_rgb
    ):
        return False

    # 見つけた商品が買い物リストにある　かつ　まだカゴに入れてない時
    for s in status.shopping_list:
        if are_same_list(item_rgb, s["rgb"]):
            item_name = s["name"]
            if any(c is not None and item_name == c["name"] for c in status.cart):
                return False
            return True

    return False


# 商品をすでにカゴに入れたか判別
def item_picked_checker(item, cart):
    for c in cart:
        if c is not None:
            if c["name"] == item:
                return True
    return False


# Qマップを比較し、次の方向を決める
def q_comparison(status, next_direction):
    direction = next_direction
    value = 0

    # 買い物リストからatmとレジのidを取得
    atm_index = 0
    for item in status.shopping_list:
        if item["name"] == "atm.jpg":
            atm_index = item["id"]
            break

    cashier_register_index = 0
    for item in status.shopping_list:
        if item["name"] == "cashier_register.jpg":
            cashier_register_index = item["id"]
            break

    # まだatmを探している時
    if status.progress == 0:
        for i in range(4):
            if value < status.q[atm_index][i][status.x][status.y]:
                value = status.q[atm_index][i][status.x][status.y]
                direction = i

    # レジを探している時
    elif status.progress == status.item_amount - 1:
        for i in range(4):
            if value < status.q[cashier_register_index][i][status.x][status.y]:
                value = status.q[cashier_register_index][i][status.x][status.y]
                direction = i

    # 商品を探している時
    else:
        for i in range(status.item_amount):
            if i != atm_index and i != cashier_register_index:
                is_item_picked = item_picked_checker(
                    status.shopping_list[i]["name"], status.cart
                )
                if not is_item_picked:
                    for j in range(4):
                        if value < status.q[i][j][status.x][status.y]:
                            value = status.q[i][j][status.x][status.y]
                            direction = j
    if value == 0:
        direction = next_direction

    return direction


def is_random_walk(epsilon):
    return random.random() < epsilon


def walk(status, file):
    next_direction = random.randint(0, 3)
    random_walk = is_random_walk(status.epsilon)
    next_x = 0
    next_y = 0

    if random_walk == False:
        next_direction = q_comparison(status, next_direction)

    if next_direction == 0:
        next_x = status.x - 1
        next_y = status.y
    elif next_direction == 1:
        next_x = status.x
        next_y = status.y + 1
    elif next_direction == 2:
        next_x = status.x + 1
        next_y = status.y
    else:
        next_x = status.x
        next_y = status.y - 1

    # 次の場所がマップの範囲内の時
    if next_x >= 0 and next_y >= 0 and next_x < VERTICAL and next_y < HORIZONTAL:

        # Qマップを全て更新する
        for i in range(status.item_amount):
            if (
                status.q[i][next_direction][status.x][status.y]
                > status.q[i][status.pd][status.px][status.py]
            ):
                status.q[i][status.pd][status.px][status.py] = (
                    status.q[i][next_direction][status.x][status.y] * 0.9
                )

        # 次の場所が未通過か通過済みのとき
        if status.map[next_x][next_y] == " " or status.map[next_x][next_y] == "*":
            status.map[next_x][next_y] = "*"
            status.px = status.x
            status.py = status.y
            status.x = next_x
            status.y = next_y
            status.pd = next_direction
            status.steps = status.steps + 1

            if status.show_output:
                print(f"({status.x}, {status.y})")
            file.write(f"({status.x}, {status.y})\n")
            return status

        # 次の場所がスタート地点のとき
        elif status.map[next_x][next_y] == "1":
            return status

        # 次の場所に商品がある時
        else:
            should_pick = item_checker(status, status.map[next_x][next_y])

            if should_pick:

                # カートに商品を入れ、idを取得
                item_id = pick_item(status, status.map[next_x][next_y])

                # マップと進捗を更新
                status.progress = status.progress + 1
                status.q[item_id][next_direction][status.x][status.y] = 1000
            return status
    else:
        return status


# 設定ファイルからパラメータを取得
version = ""
item_amount = 0
prefer_lower_price_items = False
epsilon = 0
starting_x = 0
starting_y = 0
show_output = False

with open("./input/config.json", "r", encoding="utf-8") as file:
    data = json.load(file)

    # コードのバージョンを取得
    version = data["version"]

    # 商品（買い物リストの写真）の個数
    item_amount = data["item_amount"]

    # 最終的な商品の選択方法
    if data["prefer_lower_price_items"] == True:
        prefer_lower_price_items = True

    # εを取得
    epsilon = float(data["epsilon"])

    # スタート地点を取得
    starting_x = int(data["starting_x"])
    starting_y = int(data["starting_y"])

    # 出力をターミナルに表示するかどうか
    show_output = data["show_output"]

# 現在の日付・時間を取得
now = datetime.datetime.now()
date = datetime.date.today()
time = now.strftime("%H-%M-%S-%f")

# 出力用ファイルを作成
output_file_name = f"./output/tmp_data/{date}_{time}.txt"
with open(output_file_name, "w") as file:
    file.write(f"{version} output data\n\n")
    file.write("Passing Points:\n")

# 買い物リスト（写真のパス）を取得
shopping_list_path = "./input/shopping_list"
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

# 地図を取得
map = []
with open("./input/map.txt") as map_file:
    for _ in range(VERTICAL):
        map.append(list(map_file.readline().rstrip("\n")))

# Qマップを取得
q = []
for i in range(item_amount):
    item_q = []
    for j in range(4):
        current_q = []
        with open(f"./input/q/{i}/q{j}.txt") as f:
            for _ in range(VERTICAL):
                current_q.append([float(v) for v in f.readline().split()])
        item_q.append(current_q)
    q.append(item_q)


# カートの初期化
cart = [None] * item_amount

# 最初の所持金をランダムに決定
initial_money = random.randint(0, 100000)

# 状態の初期化
status = Status(
    starting_x,
    starting_y,
    initial_money,
    shopping_list,
    cart,
    epsilon,
    q,
    map,
    item_amount,
    show_output,
)

# 歩く(実験開始)
with open(output_file_name, "a") as file:
    keep_going = True
    while keep_going:
        status = walk(status, file)
        if status.show_output:
            print(f"Progress: {status.progress}, Steps: {status.steps}")
        if status.progress == item_amount:
            keep_going = False
status = checkout(status)

# 出力用に買い物リストのを文字列に変換
shopping_list_text = "Shopping List: "
for i in shopping_list:
    shopping_list_text += f"{i['name']},  "

# 出力用にカートの中身を文字列に変換(取得した順)
cart_text = "Visit order:\n"
order = 1
for i in status.cart:
    if i is not None:
        cart_text += f"{order}, {{ Symbol: {i['symbol']}, Name: {i['name']}, Price: {i['price']}¥ }}\n"
        order += 1

# 出力用に購入した商品を文字列に変換
items_purchased_text = "Items purchased: "
for i in status.items_purchased:
    items_purchased_text += f"{i['name']}: {i['price']}¥ -> "

# ターミナルに出力
if status.show_output:
    print(f"\nOutput file name: {date}_{time}.txt")
    print(f"Epsilon: {epsilon}")
    print(shopping_list_text)
    print(cart_text)
    print(items_purchased_text)
    print(f"Initial money: {status.initial_money}")
    print(f"Cash balance: {status.cash_balance}")
    print(f"Is shopping successful?: {status.is_shopping_successful}")
    print(f"Progress: {status.progress}")
    print(f"Steps: {status.steps}")
    print(f"Map: ")
    for i in range(VERTICAL):
        for j in range(HORIZONTAL):
            print(status.map[i][j], end="")
    print()
    print()

# ファイルに出力
with open(output_file_name, "a") as file:
    file.write(f"\nEpsilon: {epsilon}\n\n")
    file.write(f"{shopping_list_text}\n\n")
    file.write(f"{cart_text}\n\n")
    file.write(f"{items_purchased_text}\n\n")
    file.write(f"Initial money: {status.initial_money}\n\n")
    file.write(f"Cash balance: {status.cash_balance}\n\n")
    file.write(f"Is shopping successful?: {status.is_shopping_successful}\n\n")
    file.write(f"Progress: {status.progress}\n\n")
    file.write(f"Steps: {status.steps}\n\n")
    file.write(f"Map: \n")
    for i in range(VERTICAL):
        for j in range(HORIZONTAL):
            file.write(f"{status.map[i][j]}")
        file.write("\n")

# Qマップを保存
for i in range(item_amount):
    for j in range(4):
        with open(f"./input/q/{i}/q{j}.txt", "w") as f:
            for k in range(VERTICAL):
                line = " ".join(
                    f"{status.q[i][j][k][l]:.3f}" for l in range(HORIZONTAL)
                )
                f.write(line + "\n")
